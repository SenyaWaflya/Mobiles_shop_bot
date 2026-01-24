from aiogram.filters.callback_data import CallbackData


class BrandCallback(CallbackData, prefix='brand'):
    name: str
    action: str
