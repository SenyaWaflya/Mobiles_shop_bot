from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from src.api.file_storage.files import FilesApi
from src.api.shop_backend.products import ProductsApi
from src.callbacks.brand import BrandCallback
from src.callbacks.product import ProductCallback
from src.kb import brands_kb, product_kb, products_kb
from src.utils.files import file_bytes_to_photo, get_static_photo

products_router = Router(name='products')


@products_router.message(F.text == 'Каталог 🔍')
async def brands_catalog(message: Message) -> None:
    photo = await get_static_photo('catalog_icon.png')
    await message.answer_photo(photo=photo, caption='Выберите фирму устройства', reply_markup=await brands_kb())


@products_router.callback_query(BrandCallback.filter(F.action == 'open'))
async def open_brands(callback: CallbackQuery, callback_data: BrandCallback) -> None:
    await callback.answer()
    await callback.message.edit_caption(caption='Выберите модель', reply_markup=await products_kb(callback_data.title))


@products_router.callback_query(BrandCallback.filter(F.action == 'back'))
async def close_brands(callback: CallbackQuery) -> None:
    await callback.answer()
    await callback.message.edit_caption(caption='Выберите фирму устройства', reply_markup=await brands_kb())


@products_router.callback_query(ProductCallback.filter(F.action == 'open'))
async def open_product(callback: CallbackQuery, callback_data: ProductCallback, state: FSMContext) -> None:
    await callback.answer()
    product = await ProductsApi.get(callback_data.id)
    product_image_bytes = await FilesApi.get(product.image_path)
    product_image = await file_bytes_to_photo(file_bytes=product_image_bytes, title=product.title)
    await state.update_data(brand=product.brand, product_id=product.id)
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=product_image,
            caption=(
                f'Фирма: {product.brand}\n'
                f'Модель: {product.title}\n'
                f'Цена: {product.price}\n'
                f'Количество на складе: {product.quantity}'
            ),
        ),
        reply_markup=product_kb,
    )


@products_router.callback_query(ProductCallback.filter(F.action == 'back'))
async def close_product(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer()
    data = await state.get_data()
    brand = data['brand']
    await callback.message.edit_media(
        media=InputMediaPhoto(
            media=await get_static_photo('catalog_icon.png'),
            caption='Выберите модель',
        ),
        reply_markup=await products_kb(brand),
    )
