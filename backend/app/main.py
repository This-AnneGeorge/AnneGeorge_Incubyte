from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr, Field as PydanticField
from pwdlib import PasswordHash
from sqlmodel import Field, Session, SQLModel, create_engine, select


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(index=True, unique=True)
    password_hash: str
    role: str = Field(default="user")


class RegistrationRequest(BaseModel):
    email: EmailStr
    password: str = PydanticField(min_length=8)


class UserResponse(BaseModel):
    id: int
    email: str
    role: str


password_hasher = PasswordHash.recommended()


def create_app(database_url: str = "sqlite:///./dealership.db") -> FastAPI:
    engine = create_engine(
        database_url,
        connect_args={"check_same_thread": False},
    )
    SQLModel.metadata.create_all(engine)

    app = FastAPI(title="Car Dealership Inventory API")

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

    return app


app = create_app()