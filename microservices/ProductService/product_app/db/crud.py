from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import models, schemas


async def get_products(db: AsyncSession, skip: int, limit: int):
    db_products = await db.execute(select(models.Products).offset(skip).limit(limit))
    return db_products.scalars().all()


async def get_product_by_id(db: AsyncSession, product_id: str):
    db_product = await db.execute(select(models.Products).where(models.Products.product_id == product_id))
    return db_product.scalar()


async def create_product(db: AsyncSession, product: schemas.ProductCreate) -> schemas.Product:
    new_product = models.Products(name=product.name, weight=product.weight, description=product.description)
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


async def update_product(db: AsyncSession, product_id: str, product: schemas.ProductUpdate) -> schemas.Product | None:
    db_product = await get_product_by_id(db, product_id)
    if db_product is None:
        return db_product
    if product.name is not None:
        db_product.name = product.name
    if product.weight is not None:
        db_product.weight = product.weight
    if product.description is not None:
        db_product.description = product.description
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: str):
    db_product = await get_product_by_id(db, product_id)
    if db_product is None:
        return db_product
    await db.delete(db_product)
    await db.commit()
    return f"Продукт ({db_product.name}) успешно удален"
