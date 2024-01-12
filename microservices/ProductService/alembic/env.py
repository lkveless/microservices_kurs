import asyncio
from alembic import context
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

target_metadata = Base.metadata


def do_run_migrations(connection):
    context.configure(
        compare_type=True,
        dialect_opts={"paramstyle": "named"},
        connection=connection,
        target_metadata=target_metadata,
        include_schemas=True,
        version_table_schema=target_metadata.schema,
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = create_async_engine("postgresql+asyncpg://postgres:postgres@postgres-product:5432/products",
                                      future=True)

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)


asyncio.run(run_migrations_online())

