import asyncio
import uuid

from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import get_stateless_message_ikb
from presenter import Presenter
from states import GroupStates

rt = Router()


@rt.message(CommandStart())
async def command_start_message_handler(message: Message, state: FSMContext, presenter: Presenter):
    await state.clear()
    await stateless_message_handler(message, presenter)


@rt.callback_query(F.data.startswith("groups"))
async def groups_button_callback_handler(callback: CallbackQuery, state: FSMContext):
    pass


@rt.callback_query(F.data.startswith("create_group"))
async def create_group_button_callback_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(text=callback.message.text, reply_markup=None)

    new_group = {'admin_id': callback.message.from_user.id, 'group_id': str(uuid.uuid4())}
    new_member = {'member_id': f'{callback.message.from_user.id}:{str(uuid.uuid4())}'}

    await state.update_data(new_group=new_group, new_member=new_member)

    await callback.message.answer(text=str(new_group))
    await callback.message.answer(text=str(new_member))
    await asyncio.sleep(1)
    await callback.message.answer(text='Set new group name')

    await state.set_state(GroupStates.name)


@rt.message(GroupStates.name)
async def group_states_name_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    new_group = data['new_group']
    new_group['s_name'] = message.text
    await state.update_data(new_group=new_group)

    await message.answer(text=str(new_group))
    await asyncio.sleep(1)
    await message.answer(text='Set new group description')

    await state.set_state(GroupStates.description)


@rt.message(GroupStates.description)
async def group_states_description_message_handler(message: Message, state: FSMContext):
    data = await state.get_data()

    new_group = data['new_group']
    new_group['s_description'] = message.text

    await state.update_data(new_group=new_group)

    await message.answer(text=str(new_group))

    await state.set_state(None)


@rt.message()
async def stateless_message_handler(message: Message, presenter: Presenter):
    user = presenter.provide_user(message.from_user.id, message.from_user.username)
    await message.answer(text=user.__repr__(), reply_markup=get_stateless_message_ikb())
