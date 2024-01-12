from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+asyncpg://postgres:postgres@postgres-product:5432/products"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL
)
AsyncSessionLocal = async_sessionmaker(engine, autocommit=False, autoflush=False, class_=AsyncSession)

Base = declarative_base()
