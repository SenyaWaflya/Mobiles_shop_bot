from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.api.products import ProductsApi
from src.callbacks.brand import BrandCallback
from src.callbacks.product import ProductCallback
from src.kb import brands_kb, product_kb, products_kb

products_router = Router(name='products')


@products_router.message(F.text == 'Каталог 🔍')
async def brands_catalog(message: Message) -> None:
    await message.answer(text='Выберите фирму устройства', reply_markup=await brands_kb())


@products_router.callback_query(BrandCallback.filter(F.action == 'open'))
async def open_brands(callback: CallbackQuery, callback_data: BrandCallback) -> None:
    await callback.answer()
    await callback.message.edit_text(text='Выберите модель', reply_markup=await products_kb(callback_data.title))


@products_router.callback_query(BrandCallback.filter(F.action == 'back'))
async def close_brands(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_text(text='Выберите фирму устройства', reply_markup=await brands_kb())


@products_router.callback_query(ProductCallback.filter(F.action == 'open'))
async def open_product(callback: CallbackQuery, callback_data: ProductCallback, state: FSMContext) -> None:
    await callback.answer()
    product = await ProductsApi.get(callback_data.id)
    await state.update_data(brand=product['brand'], product_id=product['id'])
    await callback.message.edit_text(
        text=f'Фирма: {product["brand"]}\nМодель: {product["title"]}\nЦена: {product["price"]}',
        reply_markup=product_kb,
    )


@products_router.callback_query(ProductCallback.filter(F.action == 'back'))
async def close_product(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    brand = data['brand']
    await callback.message.edit_text(text='Выберите модель', reply_markup=await products_kb(brand))
