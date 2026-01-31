from httpx import AsyncClient

from src.schemas.products import Product
from src.settings import settings


class ProductsApi:
    @staticmethod
    async def get_all() -> list[Product]:
        async with AsyncClient() as client:
            resp = await client.get(f'{settings.SHOP_BACKEND_API_URL}/products/')
            products = [Product.model_validate(product) for product in resp.json()]
            return products

    @staticmethod
    async def get(product_id: int) -> Product:
        async with AsyncClient() as client:
            resp = await client.get(f'{settings.SHOP_BACKEND_API_URL}/products/{product_id}')
            product = Product.model_validate(resp.json())
            return product

    @staticmethod
    async def get_brands() -> list[str]:
        async with AsyncClient() as client:
            resp = await client.get(f'{settings.SHOP_BACKEND_API_URL}/products/brands')
            brands = resp.json()
            return brands
