from aiogram.filters.callback_data import CallbackData


class ProductCallback(CallbackData, prefix='product'):
    id: int
    brand: str
    title: str
    action: str
