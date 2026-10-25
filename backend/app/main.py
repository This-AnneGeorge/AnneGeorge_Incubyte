import os
import secrets
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import jwt
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from pydantic import (
    BaseModel,
    EmailStr,
    Field as PydanticField,
    field_validator,
)
from pwdlib import PasswordHash
from sqlalchemy import update
from sqlmodel import Field, Session, SQLModel, select

from app.database import make_engine


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    role: str = Field(default="user")


class Vehicle(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    make: str
    model: str
    category: str
    price: Decimal = Field(
        default=Decimal("0.00"),
        max_digits=12,
        decimal_places=2,
    )
    quantity: int = Field(default=0, ge=0)


class RegistrationRequest(BaseModel):
    email: EmailStr
    password: str = PydanticField(min_length=8)


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    role: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str


class VehicleCreate(BaseModel):
    make: str = PydanticField(min_length=1)
    model: str = PydanticField(min_length=1)
    category: str = PydanticField(min_length=1)
    price: Decimal = PydanticField(
        gt=0,
        max_digits=12,
        decimal_places=2,
    )
    quantity: int = PydanticField(ge=0)

    @field_validator("make", "model", "category")
    @classmethod
    def strip_and_validate_text(cls, value: str) -> str:
        cleaned = value.strip()
        if not cleaned:
            raise ValueError("must not be blank")
        return cleaned


class RestockRequest(BaseModel):
    amount: int = PydanticField(gt=0)


class VehicleResponse(BaseModel):
    id: int
    make: str
    model: str
    category: str
    price: Decimal
    quantity: int


password_hasher = PasswordHash.recommended()
bearer_scheme = HTTPBearer(auto_error=False)


def create_app(database_url: str | None = None) -> FastAPI:
    engine = make_engine(database_url)
    SQLModel.metadata.create_all(engine)

    configured_secret = os.getenv("JWT_SECRET_KEY")
    if os.getenv("APP_ENV") == "production" and not configured_secret:
        raise RuntimeError("JWT_SECRET_KEY is required in production")

    secret_key = configured_secret or secrets.token_urlsafe(32)
    app = FastAPI(title="Car Dealership Inventory API")

    origins = [
        origin.strip().rstrip("/")
        for origin in os.getenv(
            "CORS_ORIGINS",
            "http://localhost:5173",
        ).split(",")
        if origin.strip()
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["Authorization", "Content-Type"],
    )

    def get_current_user(
        credentials: HTTPAuthorizationCredentials | None = Depends(
            bearer_scheme
        ),
    ) -> User:
        unauthorized = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing authentication token",
            headers={"WWW-Authenticate": "Bearer"},
        )

        if credentials is None:
            raise unauthorized

        try:
            payload = jwt.decode(
                credentials.credentials,
                secret_key,
                algorithms=["HS256"],
            )
            user_id = int(payload["sub"])
        except (InvalidTokenError, KeyError, TypeError, ValueError):
            raise unauthorized

        with Session(engine) as session:
            user = session.get(User, user_id)

        if user is None:
            raise unauthorized

        return user

    def require_admin(
        current_user: User = Depends(get_current_user),
    ) -> User:
        if current_user.role != "admin":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Admin access required",
            )
        return current_user

    @app.post(
        "/api/auth/register",
        response_model=UserResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def register(request: RegistrationRequest):
        email = str(request.email).strip().lower()

        with Session(engine) as session:
            existing_user = session.exec(
                select(User).where(User.email == email)
            ).first()

            if existing_user is not None:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Email is already registered",
                )

            user = User(
                email=email,
                password_hash=password_hasher.hash(request.password),
            )
            session.add(user)
            session.commit()
            session.refresh(user)
            return user

    @app.post("/api/auth/login", response_model=TokenResponse)
    def login(request: LoginRequest):
        email = str(request.email).strip().lower()

        with Session(engine) as session:
            user = session.exec(
                select(User).where(User.email == email)
            ).first()

            if user is None or not password_hasher.verify(
                request.password, user.password_hash
            ):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            expires_at = datetime.now(timezone.utc) + timedelta(minutes=60)
            token = jwt.encode(
                {"sub": str(user.id), "exp": expires_at},
                secret_key,
                algorithm="HS256",
            )
            return TokenResponse(access_token=token, token_type="bearer")

    @app.get("/api/auth/me", response_model=UserResponse)
    def get_my_profile(
        current_user: User = Depends(get_current_user),
    ):
        return current_user

    @app.post(
        "/api/vehicles",
        response_model=VehicleResponse,
        status_code=status.HTTP_201_CREATED,
    )
    def add_vehicle(
        request: VehicleCreate,
        current_user: User = Depends(get_current_user),
    ):
        with Session(engine) as session:
            vehicle = Vehicle(**request.model_dump())
            session.add(vehicle)
            session.commit()
            session.refresh(vehicle)
            return vehicle

    @app.get("/api/vehicles", response_model=list[VehicleResponse])
    def list_vehicles(current_user: User = Depends(get_current_user)):
        with Session(engine) as session:
            return session.exec(select(Vehicle)).all()

    @app.get("/api/vehicles/search", response_model=list[VehicleResponse])
    def search_vehicles(
        make: str | None = None,
        model: str | None = None,
        category: str | None = None,
        min_price: Decimal | None = Query(default=None, ge=0),
        max_price: Decimal | None = Query(default=None, ge=0),
        current_user: User = Depends(get_current_user),
    ):
        if (
            min_price is not None
            and max_price is not None
            and min_price > max_price
        ):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="min_price cannot exceed max_price",
            )

        statement = select(Vehicle)

        if make:
            statement = statement.where(Vehicle.make.ilike(f"%{make.strip()}%"))
        if model:
            statement = statement.where(
                Vehicle.model.ilike(f"%{model.strip()}%")
            )
        if category:
            statement = statement.where(
                Vehicle.category.ilike(f"%{category.strip()}%")
            )
        if min_price is not None:
            statement = statement.where(Vehicle.price >= min_price)
        if max_price is not None:
            statement = statement.where(Vehicle.price <= max_price)

        with Session(engine) as session:
            return session.exec(statement).all()

    @app.put("/api/vehicles/{vehicle_id}", response_model=VehicleResponse)
    def update_vehicle(
        vehicle_id: int,
        request: VehicleCreate,
        current_user: User = Depends(get_current_user),
    ):
        with Session(engine) as session:
            vehicle = session.get(Vehicle, vehicle_id)

            if vehicle is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vehicle not found",
                )

            for field_name, value in request.model_dump().items():
                setattr(vehicle, field_name, value)

            session.add(vehicle)
            session.commit()
            session.refresh(vehicle)
            return vehicle

    @app.delete(
        "/api/vehicles/{vehicle_id}",
        status_code=status.HTTP_204_NO_CONTENT,
    )
    def delete_vehicle(
        vehicle_id: int,
        admin: User = Depends(require_admin),
    ):
        with Session(engine) as session:
            vehicle = session.get(Vehicle, vehicle_id)

            if vehicle is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vehicle not found",
                )

            session.delete(vehicle)
            session.commit()

    @app.post(
        "/api/vehicles/{vehicle_id}/purchase",
        response_model=VehicleResponse,
    )
    def purchase_vehicle(
        vehicle_id: int,
        current_user: User = Depends(get_current_user),
    ):
        with Session(engine) as session:
            result = session.execute(
                update(Vehicle)
                .where(
                    Vehicle.id == vehicle_id,
                    Vehicle.quantity > 0,
                )
                .values(quantity=Vehicle.quantity - 1)
            )

            if result.rowcount != 1:
                vehicle = session.get(Vehicle, vehicle_id)

                if vehicle is None:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="Vehicle not found",
                    )

                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Vehicle is out of stock",
                )

            session.commit()
            return session.get(Vehicle, vehicle_id)

    @app.post(
        "/api/vehicles/{vehicle_id}/restock",
        response_model=VehicleResponse,
    )
    def restock_vehicle(
        vehicle_id: int,
        request: RestockRequest,
        admin: User = Depends(require_admin),
    ):
        with Session(engine) as session:
            result = session.execute(
                update(Vehicle)
                .where(Vehicle.id == vehicle_id)
                .values(quantity=Vehicle.quantity + request.amount)
            )

            if result.rowcount != 1:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Vehicle not found",
                )

            session.commit()
            return session.get(Vehicle, vehicle_id)

    return app


app = create_app()