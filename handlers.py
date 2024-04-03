from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from keyboards import get_main_menu_ikb, get_create_group_ikb, get_members_ikb, get_edit_member_ikb
from presenter import Presenter
from states import GroupStates

rt = Router()


@rt.message(CommandStart())
async def command_start_message_handler(message: Message, state: FSMContext, presenter: Presenter):
    await state.clear()
    data = await state.update_data(
        user=presenter.start_main_menu_update(message.from_user.id, message.from_user.username))
    await message.answer(text=str(data['user']['s_username']), reply_markup=get_main_menu_ikb())


@rt.callback_query(F.data.startswith("create_group"))
async def create_group_button_callback_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(
        text=f"{data['user']['s_username']}\n\n Create new group with you as a first member",
        reply_markup=get_create_group_ikb())


@rt.callback_query(F.data.startswith("confirm_create_group"))
async def confirm_create_group_button_callback(
        callback: CallbackQuery, state: FSMContext, presenter: Presenter):

    data = await state.get_data()
    data = await state.update_data(presenter.create_group_update(data['user']['user_id']))

    user, group, member = data['user'], data['group'], data['member']
    await callback.message.edit_text(
        text=f"{user['s_username']}\n{group['group_id']}\n{member['member_id']}",
        reply_markup=get_edit_member_ikb(user['user_id'], group['admin_id'])
    )


@rt.callback_query(F.data.startswith("to_main_menu"))
async def to_main_menu_button_callback_handler(callback: CallbackQuery, state: FSMContext, presenter: Presenter):
    data = await state.get_data()
    await state.clear()
    data = await state.update_data(user=presenter.return_main_menu_update(data['user']['user_id']))
    await callback.message.edit_text(text=data['user']['s_username'], reply_markup=get_main_menu_ikb())


@rt.callback_query(F.data.startswith("groups"))
async def groups_button_callback(callback: CallbackQuery, state: FSMContext, presenter: Presenter):
    data = await state.get_data()
    user = data['user']
    await callback.message.edit_text(text=f"{user['s_username']}",
                                     reply_markup=get_members_ikb(user['members']))


@rt.callback_query(F.data.startswith("member_m"))
async def member_button_callback(callback: CallbackQuery, state: FSMContext, presenter: Presenter):
    data = await state.update_data(presenter.choose_member_update(callback.data.split('_')[1]))
    user, group, member = data['user'], data['group'], data['member']
    await callback.message.edit_text(
        text=f"{user['s_username']}\n{group['group_id']}\n{member['member_id']}",
        reply_markup=get_edit_member_ikb(user['user_id'], group['admin_id'])
    )


@rt.message(GroupStates.name)
async def group_states_name_message_handler(message: Message, state: FSMContext):
    pass


@rt.message(GroupStates.description)
async def group_states_description_message_handler(message: Message, state: FSMContext):
    pass


@rt.message()
async def stateless_message_handler(message: Message):
    pass
