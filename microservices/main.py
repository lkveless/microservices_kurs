from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from ProductService.product_app.routers.products import router as product_router
from OrderService.order_app.routers.order import router as order_router
from InventoryService.inventory_app.routers.inventory import router as inventory_router
from NotificationService.notific_app.routers.notification import router as notification_router
from Graphql.graph import graphql_app

tags_metadata = [
    {
        "name": "ProductService",
        "description": "Operations with products.",
    },
    {
        "name": "OrderService",
        "description": "Create, cancel and read orders.",
    },
    {
        "name": "InventoryService",
        "description": "Operations with products of inventory.",
    },
    {
        "name": "NotificationService",
        "description": "Read all notifications.",
    },
    {
        "name": "GraphQL",
        "description": "ProductService with OrderService"
    }
]

app = FastAPI(openapi_tags=tags_metadata,
              title="Microservices",
              description="Some FastAPI services. For more details about GraphQL, "
                          "visit [GraphQL Service](http://127.0.0.1:8000/graphql)"
              )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"error": "Неверный формат данных"}
    )


# Обработчик глобальных исключений, который ловит все необработанные исключения
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Ошибка сервера"}
    )


app.include_router(product_router, prefix='/product', tags=["ProductService"])
app.include_router(order_router, prefix='/order', tags=["OrderService"])
app.include_router(inventory_router, prefix='/inventory', tags=["InventoryService"])
app.include_router(notification_router, prefix="/notification", tags=["NotificationService"])
app.include_router(graphql_app, prefix='/graphql', tags=["GraphQL"], include_in_schema=False)
