from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.payload import decode_payload

from keyboards import get_main_menu_ikb, get_create_group_ikb, get_groups_ikb, get_edit_ikb
from new_presenter import NewPresenter

new_rt = Router()


@new_rt.message(CommandStart(deep_link=True))
async def deep_link_handler(
        message: Message, command: CommandObject, state: FSMContext, presenter: NewPresenter):
    args = decode_payload(command.args)
    data = await state.update_data(
        presenter.add_member_by_deeplink_update(args, message.from_user.id, message.from_user.username))
    text = data['text']
    await message.answer(text=text)


@new_rt.message(CommandStart())
async def command_start_message_handler(message: Message, state: FSMContext, presenter: NewPresenter):
    await state.clear()
    data = await state.update_data(presenter.start_main_menu_update(message.from_user.id, message.from_user.username))
    await message.answer(text=data['text'], reply_markup=get_main_menu_ikb())


@new_rt.callback_query(F.data.startswith("create_group"))
async def create_group_button_callback_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(
        text=f"{data['s_username']}\nCreate new group with you as a first member",
        reply_markup=get_create_group_ikb())


@new_rt.callback_query(F.data.startswith("confirm_create_group"))
async def confirm_create_group_button_callback(callback: CallbackQuery, state: FSMContext, presenter: NewPresenter):
    data = await state.get_data()
    data = await state.update_data(presenter.create_group_update(data['user_id']))
    await callback.message.edit_text(text=f"{data['text']}", reply_markup=get_edit_ikb(True))


@new_rt.callback_query(F.data.startswith("to_main_menu"))
async def to_main_menu_button_callback(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    await callback.message.edit_text(
        text=f"{data['s_username']}, you are in main menu again", reply_markup=get_main_menu_ikb())


@new_rt.callback_query(F.data.startswith("groups"))
async def groups_button_callback(callback: CallbackQuery, state: FSMContext, presenter: NewPresenter):
    data = await state.get_data()
    data = await state.update_data(presenter.return_groups_update(data['user_id']))
    text, groups = data['text'], data['groups']
    await callback.message.edit_text(text=text, reply_markup=get_groups_ikb(groups))


@new_rt.callback_query(F.data.startswith("group_choose"))
async def group_button_callback(callback: CallbackQuery, state: FSMContext, presenter: NewPresenter):
    data = await state.get_data()
    group_auto_id = callback.data.split('_')[2]
    data = await state.update_data(presenter.choose_group_update(data['user_id'], group_auto_id))
    text, is_admin = data['text'], data['is_admin']
    await callback.message.edit_text(text=text, reply_markup=get_edit_ikb(is_admin))


# @new_rt.callback_query(F.data.startswith('group_edit'))
# async def group_edit_callback(callback: CallbackQuery, state: FSMContext, presenter: Presenter):
#     #TODO временно используем эту кнопку для создания ссылки
#     data = await state.get_data()
#     link = await create_start_link(callback.bot, presenter.create_link(data['group']['group_id']), encode=True)
#     await callback.message.answer(link)


# @new_rt.message(GroupStates.name)
# async def group_states_name_message_handler(message: Message, state: FSMContext):
#     pass


# @new_rt.message(GroupStates.description)
# async def group_states_description_message_handler(message: Message, state: FSMContext):
#     pass


# @new_rt.message()
# async def stateless_message_handler(message: Message):
#     pass
