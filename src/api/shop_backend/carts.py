from httpx import AsyncClient, _status_codes

from src.schemas.carts import Cart, CartItem, CartItemDto
from src.settings import settings


class CartsApi:
    @staticmethod
    async def get_active(user_id: int) -> Cart | None:
        async with AsyncClient() as client:
            resp = await client.get(url=f'{settings.SHOP_BACKEND_API_URL}/carts/{user_id}')
            if resp.status_code == _status_codes.code.NOT_FOUND:
                return None
            cart = Cart.model_validate(resp.json())
            return cart

    @staticmethod
    async def add_to_cart(user_id: int, item_dto: CartItemDto) -> CartItem:
        async with AsyncClient() as client:
            item_dto = item_dto.model_dump()
            resp = await client.post(url=f'{settings.SHOP_BACKEND_API_URL}/carts/{user_id}', json=item_dto)
            resp.raise_for_status()
            cart_item = CartItem.model_validate(resp.json())
            return cart_item
