import asyncio
import logging

from src.bot import bot, dp
from src.handlers.products import products_router
from src.handlers.users import users_router

logging.basicConfig(level=logging.INFO)

dp.include_router(users_router)
dp.include_router(products_router)


async def main() -> None:
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
