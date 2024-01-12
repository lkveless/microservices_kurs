from fastapi import APIRouter, HTTPException
from ..models import schemas
from ..db.database import database
from ..db import crud
from aiokafka import AIOKafkaProducer
import json
from datetime import datetime
from bson.objectid import ObjectId

router = APIRouter()


# Отправка сообщения в Kafka
async def send_to_kafka(kafka_order_data):
    producer = AIOKafkaProducer(
        bootstrap_servers='kafka:9092',
        value_serializer=lambda m: json.dumps(m).encode('utf-8'),
    )
    try:
        await producer.start()
        await producer.send_and_wait('order_topic', value=kafka_order_data)  # Отправляем сообщение в тему Kafka
    finally:
        await producer.stop()


# Получение всех заказов
@router.get('/')
async def get_all_orders():
    orders = await database.orders.find({}).to_list(length=None)
    return [{**order, "_id": str(order["_id"])} for order in orders]


# Создание заказа
@router.post('/')
async def add_order(order: schemas.OrderCreate):
    order_products = []
    total_cost = 0.0

    for product in order.products:
        product_info = await crud.read_product_info(product.product_id)

        if not product_info:
            raise HTTPException(
                status_code=404,
                detail=f"Продукт с id {product.product_id} не найден"
            )

        available_quantity = product_info.quantity_on_inventory
        if product.quantity > available_quantity:  # Проверка есть ли на складе нужное кол-во товара
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточное количество товара '{product_info.product_name}' на складе"
            )

        total_cost += product_info.current_price * product.quantity

        # Данные о продуктах в заказе
        order_products.append({
            "product_id": product.product_id,
            "product_name": product_info.product_name,
            "quantity": product.quantity,
            "cost": product_info.current_price
        })

        # Обновление кол-ва товара на складе с учетом заказа
        await crud.update_inventory(product.product_id, available_quantity - product.quantity)

    new_order = {
        "order_date": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        "products": order_products,
        "total_cost": total_cost
    }

    await database.orders.insert_one(new_order)  # Сохранение заказа в MongoDB

    kafka_order_data = {
        "order_id": str(new_order["_id"]),
        "order_date": new_order["order_date"],
        "message_type": "Заказ создан",
        "total_cost": new_order["total_cost"],
        "products": new_order["products"]
    }

    await send_to_kafka(kafka_order_data)  # Отправка асинхронного сообщения о создании заказа в Kafka

    return kafka_order_data


# Отмена заказа
@router.delete("/{order_id}")
async def cancel_order(order_id: str):
    db_order = await database.orders.find_one({"_id": ObjectId(order_id)})

    if db_order is None:
        raise HTTPException(status_code=404, detail=f"Заказ с id {order_id} не найден")

    order = {**db_order, "_id": str(db_order["_id"])}  # Получение документа с id конвертированным в строку

    for product in order["products"]:
        product_info = await crud.read_product_info(product["product_id"])
        available_quantity = product_info.quantity_on_inventory

        # Обновление кол-ва товара на складе с учетом отмены заказа
        await crud.update_inventory(product["product_id"], available_quantity + product["quantity"])

    await database.orders.find_one_and_delete({"_id": db_order["_id"]})  # Удаление заказа из коллекции

    kafka_cancel_data = {
        "order_id": order_id,
        "order_date": order["order_date"],
        "products": order["products"],
        "total_cost": order["total_cost"],
        "message_type": "Заказ отменен"
    }

    await send_to_kafka(kafka_cancel_data)  # Отправка асинхронного сообщения об отмене заказа в Kafka

    return kafka_cancel_data


# Получение заказа по id
@router.get("/{order_id}")
async def get_order(order_id: str):
    order = await database.orders.find_one({"_id": ObjectId(order_id)})
    return {**order, "_id": str(order["_id"])}
