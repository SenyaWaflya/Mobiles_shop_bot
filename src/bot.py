from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from src.settings import settings

bot = Bot(
    token=settings.TOKEN,
    default=DefaultBotProperties(link_preview_is_disabled=True, parse_mode='HTML'),
)
dp = Dispatcher()
