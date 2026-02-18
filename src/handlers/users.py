from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import InputMediaPhoto, Message

from src.api.file_storage.files import FilesApi
from src.api.shop_backend.carts import CartsApi
from src.api.shop_backend.users import UsersApi
from src.kb import main_kb
from src.schemas.users import UserDto
from src.utils.files import file_bytes_to_photo

users_router = Router(name='users')


@users_router.message(CommandStart())
async def start(message: Message) -> None:
    user_dto = UserDto(tg_id=str(message.from_user.id), username=message.from_user.username)
    await UsersApi.add(user_dto)
    await message.answer(text=f'Привет, <b>{message.from_user.first_name}</b>', reply_markup=main_kb)


@users_router.message(F.text == 'Профиль 🧑‍💻')
async def show_profile(message: Message) -> None:
    user = await UsersApi.get(message.from_user.id)
    await message.answer(text=(f'Имя пользователя: {user.username}\nTelegram ID: {user.tg_id}'))


@users_router.message(F.text == 'Контакты ℹ️')
async def show_contacts(message: Message) -> None:
    await message.answer(
        text=('По вопросам писать:\nTelegram : @golychh\nEmail: fathat2013.ag@gmail.com\nТелефон: +7(977)108-82-48')
    )


@users_router.message(F.text == 'Корзина 🛒')
async def show_cart(message: Message) -> None:
    user = await UsersApi.get(message.from_user.id)
    user_cart = await CartsApi.get_active(user_id=user.id)
    if user_cart is None:
        await message.answer(text='Корзина пуста!')
    else:
        items = user_cart.items
        media = []

        caption_text = '<b>🛒 Ваша корзина:</b>\n\n'
        total_price = 0
        for i, cart_item in enumerate(items, start=1):
            price = cart_item.product.price
            quantity = cart_item.quantity
            total_price += price * quantity

            caption_text += f'{i}. <b>{cart_item.product.title}</b>\n   Кол-во: {quantity}\n   Цена: {price} ₽\n\n'

        caption_text += f'<b>Итого: {total_price} ₽</b>'

        for index, item in enumerate(items):
            item_image_bytes = await FilesApi.get(item.product.image_path)
            item_image = await file_bytes_to_photo(file_bytes=item_image_bytes, title=item.product.title)
            if index == 0:
                media.append(InputMediaPhoto(media=item_image, caption=caption_text))
            else:
                media.append(InputMediaPhoto(media=item_image))
        await message.answer_media_group(media=media)
