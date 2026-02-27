from aiogram import F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputMediaPhoto, Message

from src.api.file_storage.files import FilesApi
from src.api.shop_backend.carts import CartsApi
from src.api.shop_backend.users import UsersApi
from src.callbacks.cart import CartCallback
from src.kb import cart_kb
from src.schemas.carts import CartStateData
from src.states import CartState
from src.utils.files import file_bytes_to_photo

carts_router = Router(name='Carts')


@carts_router.message(F.text == 'Корзина 🛒')
async def show_cart(message: Message, state: FSMContext) -> None:
    user = await UsersApi.get(message.from_user.id)
    user_cart = await CartsApi.get_active(user_id=user.id)
    if user_cart is None:
        await message.answer(text='Корзина пуста!')
    else:
        items = [
            {
                'title': item.product.title,
                'price': item.product.price,
                'brand': item.product.brand,
                'image_path': item.product.image_path,
                'quantity': item.quantity,
                'product_id': item.product_id,
            }
            for item in user_cart.items
        ]
        await state.set_state(CartState.items)
        await state.update_data(items=items, current_index=0, user_id=user_cart.user_id)
        image_bytes = await FilesApi.get(user_cart.items[0].product.image_path)
        image = await file_bytes_to_photo(image_bytes, title=user_cart.items[0].product.title)
        await message.answer_photo(
            photo=image,
            caption=(
                f'{user_cart.items[0].product.brand} {user_cart.items[0].product.title}\n'
                f'Количество: {user_cart.items[0].quantity}\n'
                f'Цена за штуку: {user_cart.items[0].product.price}\n'
                f'Всего: {user_cart.items[0].product.price * user_cart.items[0].quantity}\n\n'
                f'Страница 1 из {len(user_cart.items)}'
            ),
            reply_markup=cart_kb,
        )


@carts_router.callback_query(CartCallback.filter(F.action == 'next'))
async def next_item(callback: CallbackQuery, state: FSMContext) -> None:
    cart_data = CartStateData.model_validate(await state.get_data())
    if (cart_data.current_index + 1) >= len(cart_data.items):
        await callback.answer(text='Товары закончились!', show_alert=True)
    else:
        await callback.answer()
        current_index = cart_data.current_index + 1
        await state.update_data(current_index=current_index)
        item = cart_data.items[current_index]
        image_bytes = await FilesApi.get(item.image_path)
        image = await file_bytes_to_photo(image_bytes, title=item.title)
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=image,
                caption=(
                    f'{item.brand} {item.title}\n'
                    f'Количество: {item.quantity}\n'
                    f'Цена за штуку: {item.price}\n'
                    f'Всего: {item.price * item.quantity}\n\n'
                    f'Страница {current_index + 1} из {len(cart_data.items)}'
                ),
            ),
            reply_markup=cart_kb,
        )


@carts_router.callback_query(CartCallback.filter(F.action == 'prev'))
async def prev_item(callback: CallbackQuery, state: FSMContext) -> None:
    cart_data = CartStateData.model_validate(await state.get_data())
    if (cart_data.current_index - 1) < 0:
        await callback.answer(text='Вы на первой странице', show_alert=True)
    else:
        await callback.answer()
        current_index = cart_data.current_index - 1
        await state.update_data(current_index=current_index)
        item = cart_data.items[current_index]
        image_bytes = await FilesApi.get(item.image_path)
        image = await file_bytes_to_photo(image_bytes, title=item.title)
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=image,
                caption=(
                    f'{item.brand} {item.title}\n'
                    f'Количество: {item.quantity}\n'
                    f'Цена за штуку: {item.price}\n'
                    f'Всего: {item.price * item.quantity}\n\n'
                    f'Страница {current_index + 1} из {len(cart_data.items)}'
                ),
            ),
            reply_markup=cart_kb,
        )


@carts_router.callback_query(CartCallback.filter(F.action == 'delete'))
async def delete_item(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.answer(text='Товар удалён из корзины', show_alert=True)
    cart_data = CartStateData.model_validate(await state.get_data())
    product_id = cart_data.items[cart_data.current_index].product_id
    await CartsApi.delete_from_cart(user_id=cart_data.user_id, product_id=product_id)

    user_cart = await CartsApi.get_active(user_id=cart_data.user_id)
    if not user_cart.items:
        await callback.message.delete()
        await CartsApi.delete_cart(user_id=cart_data.user_id)
    else:
        items = [
            {
                'title': item.product.title,
                'price': item.product.price,
                'brand': item.product.brand,
                'image_path': item.product.image_path,
                'quantity': item.quantity,
                'product_id': item.product_id,
            }
            for item in user_cart.items
        ]
        await state.update_data(items=items, current_index=0, user_id=user_cart.user_id)
        image_bytes = await FilesApi.get(user_cart.items[0].product.image_path)
        image = await file_bytes_to_photo(image_bytes, title=user_cart.items[0].product.title)
        await callback.message.edit_media(
            media=InputMediaPhoto(
                media=image,
                caption=(
                    f'{user_cart.items[0].product.brand} {user_cart.items[0].product.title}\n'
                    f'Количество: {user_cart.items[0].quantity}\n'
                    f'Цена за штуку: {user_cart.items[0].product.price}\n'
                    f'Всего: {user_cart.items[0].product.price * user_cart.items[0].quantity}\n\n'
                    f'Страница 1 из {len(user_cart.items)}'
                ),
            ),
            reply_markup=cart_kb,
        )
