from httpx import AsyncClient

from src.settings import settings


class ProductsApi:
    @staticmethod
    async def get_products() -> list[dict]:
        async with AsyncClient() as client:
            resp = await client.get(f'{settings.API_URL}/products/')
            return resp.json()
