from aiogram.filters.callback_data import CallbackData


class CartCallback(CallbackData, prefix='cart'):
    product_id: int
    quantity: int
    action: str
