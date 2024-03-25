from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import presenter

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
async def command_start_message_handler(message: Message):
    await stateless_message_handler()


@rt.message()
async def stateless_message_handler(message: Message):
    # найти юзера
    # если есть фразу с возвращением, короткая сводка о группах
    # если нет внести в бд

    # избавить презентер от Message and FSMContext

    # text = presenter.get_stateless_message_text(message.from_user.id, message.from_user.username)
    ikb = presenter.get_stateless_message_ikb()
    # await message.answer(text=text, reply_markup=ikb)
