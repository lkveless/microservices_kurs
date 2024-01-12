import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List
from OrderService.order_app.routers.order import get_all_orders
from ProductService.product_app.routers.products import read_products
from ProductService.product_app.db.database import AsyncSessionLocal


@strawberry.type
class Product:
    product_id: str
    name: str
    weight: float
    description: str
 

@strawberry.type
class OrderProduct:
    product_id: str
    product_name: str
    quantity: int
    cost: float


@strawberry.type
class OrderBase:
    order_date: str = None


@strawberry.type
class Order:
    order_id: str
    products: List[OrderProduct]
    total_cost: float


@strawberry.input
class ProductInput:
    product_id: str
    quantity: int


@strawberry.input
class CreateOrderInput(Order):
    products: List[ProductInput]


@strawberry.input
class CancelOrderInput:
    order_id: str


@strawberry.type
class Query:
    @strawberry.field(get_all_orders)
    async def get_orders(self) -> list[Order]:
        orders = await get_all_orders()
        return [
            Order(
                order_id=str(order['_id']),
                products=[
                    OrderProduct(product_id=product['product_id'],
                                 product_name=product['product_name'],
                                 quantity=product['quantity'],
                                 cost=float(product['cost']))
                    for product in order['products']
                ],
                total_cost=float(order['total_cost'])
            )
            for order in orders
        ]

    @strawberry.field(read_products)
    async def get_products(self) -> list[Product]:
        async with AsyncSessionLocal() as session:
            products = await read_products(skip=0, limit=100, db=session)
            return products


@strawberry.type
class Mutation:
    @strawberry.mutation
    async def create_order(self, order: CreateOrderInput) -> Order:
        pass

    @strawberry.mutation
    async def delete_order(self, order: CancelOrderInput) -> Order:
        pass


# Создание схемы
schema = strawberry.Schema(Query, Mutation)

graphql_app = GraphQLRouter(schema)
