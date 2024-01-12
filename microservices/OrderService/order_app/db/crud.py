from InventoryService.inventory_app.models import schemas as inventory_schemas
import httpx


async def read_product_info(product_id: str) -> inventory_schemas.Inventory | None:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://127.0.0.1:8000/inventory/{product_id}")
            response.raise_for_status()
            return inventory_schemas.Inventory(**response.json())
    except httpx.HTTPStatusError:
        return None


async def update_inventory(product_id: str, new_quantity: int) -> None:
    async with httpx.AsyncClient() as client:
        url = f"http://127.0.0.1:8000/inventory/{product_id}"
        payload = {"quantity_on_inventory": new_quantity}
        response = await client.put(url, json=payload)
        response.raise_for_status()
