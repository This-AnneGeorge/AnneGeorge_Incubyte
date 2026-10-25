import os

from sqlalchemy.engine import Engine
from sqlmodel import create_engine


LOCAL_DATABASE_URL = "sqlite:///./dealership.db"


def make_engine(database_url: str | None = None) -> Engine:
    url = database_url or os.getenv("DATABASE_URL", LOCAL_DATABASE_URL)

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql+psycopg://", 1)
    elif url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)

    connect_args = (
        {"check_same_thread": False}
        if url.startswith("sqlite:")
        else {}
    )

    return create_engine(
        url,
        connect_args=connect_args,
        pool_pre_ping=True,
    )