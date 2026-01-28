from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from src.kb import main_kb

users_router = Router(name='users')


@users_router.message(CommandStart())
async def start_msg(message: Message) -> None:
    await message.answer(text=f'Привет, <b>{message.from_user.first_name}</b>', reply_markup=main_kb)
