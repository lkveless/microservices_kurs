from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models import models, schemas


async def read_products(db: AsyncSession, skip: int, limit: int):
    db_products = await db.execute(select(models.Inventory).offset(skip).limit(limit))
    return db_products.scalars().all()


async def read_product_by_name(db: AsyncSession, name: str):
    db_product = await db.execute(select(models.Inventory).where(models.Inventory.product_name == name))
    return db_product.scalar()


async def read_product_by_id(db: AsyncSession, product_id: str):
    db_product = await db.execute(select(models.Inventory).where(models.Inventory.product_id == product_id))
    return db_product.scalar()


async def create_product(db: AsyncSession, product: schemas.InventoryCreate) -> schemas.Inventory:
    new_product = models.Inventory(
        product_name=product.product_name,
        quantity_on_inventory=product.quantity_on_inventory,
        current_price=product.current_price
    )
    db.add(new_product)
    await db.commit()
    await db.refresh(new_product)
    return new_product


async def update_product(db: AsyncSession, product_id: str, product: schemas.InventoryUpdate) -> (schemas.Inventory |
                                                                                                  None):
    db_product = await read_product_by_id(db, product_id)

    if db_product is None:
        return db_product

    if product.product_name is not None:
        db_product.product_name = product.product_name
    if product.quantity_on_inventory is not None:
        db_product.quantity_on_inventory = product.quantity_on_inventory
    if product.current_price is not None:
        db_product.current_price = product.current_price

    await db.commit()
    await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: str):
    db_product = await read_product_by_id(db, product_id)
    if db_product is None:
        return db_product
    await db.delete(db_product)
    await db.commit()
    return {"message": f"Продукт ({db_product.product_name}) успешно удален"}
