import asyncio
import logging
import sys

from aiogram.fsm.storage.redis import RedisStorage
from sqlalchemy import create_engine, select
from aiogram import Bot, Dispatcher
from sqlalchemy.orm import Session

from admin import DB_URL, API_TOKEN, CACHE_URL
from handlers import rt
from model.entities import Base, User, Group, Member


async def start():
    engine = create_engine(url=DB_URL)
    Base.metadata.create_all(engine)

    u1 = User(user_id=101)
    u2 = User(user_id=102)
    g1 = Group(group_id=901)
    g2 = Group(group_id=902)
    u1.groups = [g1, g2]
    u2.groups = [g1]
    m1 = Member(member_id=301)
    m2 = Member(member_id=302)
    g1.members = [m1, m2]

    with Session(engine) as session:
        stmt = select(Group).where(Group.group_id == 901)
        gr = session.scalar(stmt)
        print(gr)
        for m in gr.members:
            print(m)

    # bot = Bot(API_TOKEN)
    # storage = RedisStorage.from_url(url=CACHE_URL, connection_kwargs={"decode_responses": True})
    #
    # dp = Dispatcher(storage=storage)
    # dp.include_router(router=rt)
    #
    # try:
    #     await dp.start_polling(bot)
    # except Exception as _ex:
    #     print(f"There is an exception - {_ex}")
    # finally:
    #     await bot.session.close()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
