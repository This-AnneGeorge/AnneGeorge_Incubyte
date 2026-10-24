import os
import secrets
from datetime import datetime, timedelta, timezone
from decimal import Decimal

import jwt
from fastapi import Depends, FastAPI, HTTPException, Query, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import InvalidTokenError
from pydantic import BaseModel, EmailStr, Field as PydanticField
from pwdlib import PasswordHash
from sqlalchemy import update
from sqlmodel import Field, Session, SQLModel, create_engine, select


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


class VehicleResponse(BaseModel):
    id: int
    make: str
    model: str
    category: str
    price: Decimal
    quantity: int


password_hasher = PasswordHash.recommended()
bearer_scheme = HTTPBearer(auto_error=False)


def create_app(database_url: str = "sqlite:///./dealership.db") -> FastAPI:
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)

    secret_key = os.getenv("JWT_SECRET_KEY") or secrets.token_urlsafe(32)
    app = FastAPI(title="Car Dealership Inventory API")

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

    return app


app = create_app()