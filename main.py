import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy import create_engine

from admin import DB_URL, API_TOKEN, CACHE_URL
from handlers import rt
from middlewares import PresenterMiddleware
from model.entities import Base
from presenter import Presenter


async def start():
    engine = create_engine(url=DB_URL)
    Base.metadata.create_all(engine)
    presenter = Presenter(engine)

    bot = Bot(API_TOKEN)
    storage = RedisStorage.from_url(url=CACHE_URL, connection_kwargs={"decode_responses": True})

    dp = Dispatcher(storage=storage)
    dp.update.middleware.register(PresenterMiddleware(presenter=presenter))
    dp.include_router(router=rt)

    try:
        await dp.start_polling(bot)
    except Exception as _ex:
        print(f"There is an exception - {_ex}")
    finally:
        await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
