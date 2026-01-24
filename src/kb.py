from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardBuilder,
)

from src.api.catalog import ProductsApi
from src.callbacks.brand import BrandCallback
from src.callbacks.product import ProductCallback

catalog = KeyboardButton(text='Каталог 🔍')
profile = KeyboardButton(text='Профиль 🧑‍💻')
cart = KeyboardButton(text='Корзина 🛒')
contacts = KeyboardButton(text='Контакты ℹ️')
main_kb = ReplyKeyboardBuilder([[catalog], [profile, cart], [contacts]]).as_markup(resize_keyboard=True)

apple = InlineKeyboardButton(text='Apple 🍎', callback_data=BrandCallback(name='Apple', action='open').pack())
xiaomi = InlineKeyboardButton(text='Xiaomi 📱', callback_data=BrandCallback(name='Xiaomi', action='open').pack())
catalog_kb = InlineKeyboardBuilder([[apple, xiaomi]]).as_markup(resize_keyboard=True)

to_cart = InlineKeyboardButton(text='Добавить в корзину 🛒', callback_data='to_cart')
back = InlineKeyboardButton(
    text='Назад ⏪', callback_data=ProductCallback(id=-1, brand='all', title='all', action='back').pack()
)
product_kb = InlineKeyboardBuilder([[to_cart, back]]).as_markup(resize_keyboard=True)


async def products_kb(brand: str) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    products = await ProductsApi.get_products()
    for product in products:
        if product['brand'] == brand:
            builder.button(
                text=product['title'],
                callback_data=ProductCallback(
                    id=product['id'], brand=product['brand'], title=product['title'], action='open'
                ),
            )
    builder.row(InlineKeyboardButton(text='Назад ⏪', callback_data=BrandCallback(name='all', action='back').pack()))
    return builder.as_markup()
