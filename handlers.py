from aiogram import Router, F
from aiogram.filters import CommandStart, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.deep_linking import create_start_link
from aiogram.utils.payload import decode_payload

from keyboards import get_main_menu_ikb, get_create_group_ikb, get_groups_ikb, get_edit_ikb, get_edit_group_ikb
from presenter import Presenter
from states import GroupStates, MemberStates

rt = Router()


@rt.message(CommandStart(deep_link=True))
async def deep_link_handler(message: Message, command: CommandObject, state: FSMContext, presenter: Presenter):
    args = decode_payload(command.args)
    await state.clear()
    data = await state.get_data()
    presenter.add_member_by_deeplink_update(args=args,
                                            user_id=message.from_user.id,
                                            s_username=message.from_user.username,
                                            data=data)
    data = await state.update_data(data)
    await message.answer(text=data['text'])


@rt.message(CommandStart())
async def command_start_message_handler(message: Message, state: FSMContext, presenter: Presenter):
    await state.clear()
    data = await state.get_data()
    presenter.start_main_menu_update(user_id=message.from_user.id, s_username=message.from_user.username, data=data)
    await state.update_data(data)
    await message.answer(text=data['text'], reply_markup=get_main_menu_ikb())


@rt.callback_query(F.data.startswith("create_group"))
async def create_group_button_callback_handler(callback: CallbackQuery, state: FSMContext, presenter: Presenter):
    data = await state.get_data()
    presenter.create_group_button_update(data=data)
    await state.update_data(data)
    await callback.message.edit_text(text=data['text'], reply_markup=get_create_group_ikb())


@rt.callback_query(F.data.startswith("confirm_create_group"))
async def confirm_create_group_button_callback(callback: CallbackQuery, state: FSMContext, presenter: Presenter):
    data = await state.get_data()
    presenter.confirm_create_group_update(data=data)
    await state.update_data(data)
    await state.set_state(GroupStates.name)
    await callback.message.edit_text(text=data['text'])


@rt.message(GroupStates.name)
async def set_group_name_message_handler(message: Message, state: FSMContext, presenter: Presenter):
    data = await state.get_data()
    presenter.group_name_set_update(message.text, data)
    await state.update_data(data)
    await state.set_state(GroupStates.description)
    await message.answer(text=data['text'])


@rt.message(GroupStates.description)
async def set_group_description_message_handler(message: Message, state: FSMContext, presenter: Presenter):
    data = await state.get_data()
    presenter.group_description_set_update(message.text, data)
    await state.update_data(data)
    await message.answer(text=data['text'])
    presenter.member_edit_invitation_update(data)
    await message.answer(data['text'])
    await state.set_state(MemberStates.nickname)


@rt.message(MemberStates.nickname)
async def set_member_nickname_message_handler(message: Message, state: FSMContext, presenter: Presenter):
    data = await state.get_data()
    presenter.member_nickname_set_update(message.text, data)
    await state.update_data(data)
    await state.set_state(MemberStates.wishes)
    await message.answer(text=data['text'])


@rt.message(MemberStates.wishes)
async def set_member_wishes_message_handler(message: Message, state: FSMContext, presenter: Presenter):
    data = await state.get_data()
    presenter.member_wishes_set_update(message.text, data)
    await state.update_data(data)
    await state.set_state(MemberStates.address)
    await message.answer(text=data['text'])


@rt.message(MemberStates.address)
async def set_member_address_message_handler(message: Message, state: FSMContext, presenter: Presenter):
    data = await state.get_data()
    presenter.member_address_set_update(message.text, data)
    await message.answer(text=data['text'])
    presenter.group_create_update(data)
    presenter.member_create_update(data)
    await message.answer(text=data['text'], reply_markup=get_edit_ikb(True))
    await state.update_data(data)
    await state.set_state(None)


@rt.callback_query(F.data.startswith("to_main_menu"))
async def to_main_menu_button_callback(callback: CallbackQuery, state: FSMContext, presenter: Presenter):
    data = await state.get_data()
    presenter.to_main_menu_update(data=data)
    await state.update_data(data)
    await callback.message.edit_text(text=data['text'], reply_markup=get_main_menu_ikb())


@rt.callback_query(F.data.startswith("groups"))
async def groups_button_callback(callback: CallbackQuery, state: FSMContext, presenter: Presenter):
    data = await state.get_data()
    presenter.groups_button_update(data)
    await state.update_data(data)
    await callback.message.edit_text(text=data['text'], reply_markup=get_groups_ikb(data['groups']))


@rt.callback_query(F.data.startswith("group_choose"))
async def group_button_callback(callback: CallbackQuery, state: FSMContext, presenter: Presenter):
    group_auto_id = callback.data.split('_')[2]
    data = await state.get_data()
    presenter.choose_group_update(group_auto_id=group_auto_id, data=data)
    await state.update_data(data)
    text, is_admin = data['text'], data['is_admin']
    await callback.message.edit_text(text=text, reply_markup=get_edit_ikb(is_admin))


@rt.callback_query(F.data.startswith('group_edit'))
async def group_edit_callback(callback: CallbackQuery, state: FSMContext, presenter: Presenter):
    data = await state.get_data()
    presenter.group_edit_update(data)
    await state.update_data(data)
    await callback.message.edit_text(data['text'], reply_markup=get_edit_group_ikb())


@rt.callback_query(F.data.startswith('add_member'))
async def add_member_callback(callback: CallbackQuery, state: FSMContext, presenter: Presenter):
    data = await state.get_data()
    link = await create_start_link(callback.bot, presenter.create_link(data), encode=True)
    await callback.message.answer(link)

# @new_rt.message(GroupStates.name)
# async def group_states_name_message_handler(message: Message, state: FSMContext):
#     pass


# @new_rt.message(GroupStates.description)
# async def group_states_description_message_handler(message: Message, state: FSMContext):
#     pass


# @new_rt.message()
# async def stateless_message_handler(message: Message):
#     pass
