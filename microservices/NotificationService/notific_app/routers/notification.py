from datetime import datetime
from fastapi import APIRouter
from ..db.database import database
from aiokafka import AIOKafkaConsumer
import json
import asyncio

router = APIRouter()
loop = asyncio.get_event_loop()
consumer = AIOKafkaConsumer(
        "order_topic",
        bootstrap_servers="kafka:9092",
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        enable_auto_commit=True,
        group_id="notification_service_group",
        loop=loop
    )


# Прием сообщения из kafka
async def consume_from_kafka():
    await consumer.start()

    try:
        async for message in consumer:
            kafka_message = message.value
            order_id = kafka_message.get('order_id')
            order_date = kafka_message.get('order_date')
            message_type = kafka_message.get('message_type')
            total_cost = kafka_message.get('total_cost')
            products = kafka_message.get('products')

            notification_data = {
                "message_type": message_type,
                "order_info": {
                    "order_id": order_id,
                    "order_date": order_date,
                    "total_cost": total_cost,
                    "products": products
                },
                "date": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            }
            await database.notifications.insert_one(notification_data)
    finally:
        await consumer.stop()


@router.on_event("startup")
async def startup_event():
    loop.create_task(consume_from_kafka())


@router.on_event("shutdown")
async def shutdown_event():
    await consumer.stop()


@router.get("/")
async def get_notifications():
    notifications = await database.notifications.find({}).to_list(length=None)
    return [{**notification, "_id": str(notification["_id"])} for notification in notifications]
