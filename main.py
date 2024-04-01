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

    # u1 = User(user_id=101)
    # g1 = Group(group_id=901)
    # m1 = Member(member_id=301)

    # u1.members = [m1]
    # g1.members.append(m1)

    # with Session(engine) as session:
        # session.merge(u1)
        # session.merge(g1)
        # session.merge(m1)
        # session.commit()
        # stmt = select(Member).where(Member.member_id == 301)
        # member = session.scalar(stmt)
        # stmt = select(User).where(User.user_id == 101)
        # user = session.scalar(stmt)
        # stmt = select(Group).where(Group.group_id == 901)
        # gr = session.scalar(stmt)
        # print(member)
        # for m in gr.members:
        #     print(m)

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
