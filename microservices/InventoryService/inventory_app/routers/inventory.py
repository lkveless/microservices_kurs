from fastapi import APIRouter, Depends, HTTPException
from ..models import models, schemas
from ..db.database import AsyncSessionLocal, engine
from ..db import crud
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@router.get('/', response_model=list[schemas.Inventory])
async def get_products(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    db_products = await crud.read_products(db, skip, limit)
    return db_products


@router.get('/{product_id}', response_model=schemas.Inventory)
async def get_product_by_id(product_id: str, db: AsyncSession = Depends(get_db)):
    db_product = await crud.read_product_by_id(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Продукт с таким id не найден")
    return db_product


@router.post('/', response_model=schemas.Inventory)
async def add_product(product: schemas.InventoryCreate, db: AsyncSession = Depends(get_db)):
    db_product = await crud.read_product_by_name(db, product.product_name)
    if db_product:
        raise HTTPException(status_code=400, detail=f"{product.product_name.title()} уже существует")
    return await crud.create_product(db, product)


@router.put('/{product_id}', response_model=schemas.Inventory)
async def change_product(product_id: str, product: schemas.InventoryUpdate, db: AsyncSession = Depends(get_db)):
    db_product = await crud.update_product(db, product_id, product)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Продукт с таким id не найден")
    return db_product


@router.delete('/{product_id}')
async def remove_product(product_id: str, db: AsyncSession = Depends(get_db)):
    db_product = await crud.delete_product(db, product_id)
    if db_product is None:
        raise HTTPException(status_code=404, detail="Продукт с таким id не найден")
    return db_product
