from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from src.callbacks.brand import BrandCallback
from src.callbacks.product import ProductCallback
from src.kb import catalog_kb, main_kb, product_kb, products_kb

users_router = Router(name='users')


@users_router.message(CommandStart())
async def start_msg(message: Message) -> None:
    await message.answer(text=f'Привет, <b>{message.from_user.first_name}</b>', reply_markup=main_kb)


@users_router.message(F.text == 'Каталог 🔍')
async def brands_catalog(message: Message) -> None:
    await message.answer(text='Выберите фирму устройства', reply_markup=catalog_kb)


@users_router.callback_query(BrandCallback.filter())
async def products_catalog(callback: CallbackQuery, callback_data: BrandCallback) -> None:
    await callback.answer()

    if callback_data.action == 'open':
        await callback.message.edit_text(text='Выберите модель', reply_markup=await products_kb(callback_data.name))
    elif callback_data.action == 'back':
        await callback.message.edit_text(text='Выберите фирму устройства', reply_markup=catalog_kb)


@users_router.callback_query(ProductCallback.filter())
async def product_info(callback: CallbackQuery, callback_data: ProductCallback) -> None:
    await callback.answer()

    if callback_data.action == 'open':
        await callback.message.edit_text(
            text=f'Фирма: {callback_data.brand}\nМодель: {callback_data.title}', reply_markup=product_kb
        )
    elif callback_data.action == 'back':
        await callback.message.edit_text(text='Выберите модель', reply_markup=await products_kb(callback_data.brand))
