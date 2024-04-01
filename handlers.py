from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from model.entities import User
from presenter import Presenter

# import presenter

rt = Router()


@rt.callback_query(F.data.startswith("groups"))
async def groups_button_callback_handler(callback: CallbackQuery, state: FSMContext):
    # await presenter.get_groups(state)
    data = await state.get_data()
    print(data['foo'])


@rt.callback_query(F.data.startswith("create_group"))
async def create_group_button_callback_handler(callback: CallbackQuery, state: FSMContext):
    pass


@rt.message(CommandStart())
async def command_start_message_handler(message: Message, presenter: Presenter):
    await stateless_message_handler(message, presenter)

# @rt.message(Command('save'))
# async def command_save_handler(message: Message, presenter: Presenter):
#     user = User(user_id=101)
#     presenter.save_user(user)
#     await message.answer('presenter.save_user(User(user_id=101))')
#
#
# @rt.message(Command('fetch'))
# async def command_fetch_handler(message: Message, presenter: Presenter):
#     user = presenter.fetch_user(101)
#     print(user)
#     await message.answer(user.__repr__())


@rt.message()
async def stateless_message_handler(message: Message, presenter: Presenter):
    user = presenter.provide_user(message.from_user.id, message.from_user.username)
    await message.answer(user.__repr__())
