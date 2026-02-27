from pydantic import BaseModel

from src.schemas.products import Product
from src.schemas.users import UserResponse


class CartItem(BaseModel):
    cart_id: int
    product_id: int
    quantity: int
    id: int
    product: Product


class Cart(BaseModel):
    id: int
    user_id: int
    status: str
    user: UserResponse
    items: list[CartItem]


class CartItemDto(BaseModel):
    product_id: int
    quantity: int


class CartItemState(BaseModel):
    title: str
    price: int
    brand: str
    image_path: str
    quantity: int
    product_id: int


class CartStateData(BaseModel):
    items: list[CartItemState]
    current_index: int
    user_id: int
