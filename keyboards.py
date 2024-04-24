from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu_ikb() -> InlineKeyboardMarkup:
    return (InlineKeyboardBuilder()
            .button(text='My groups', callback_data='groups')
            .button(text='Create group', callback_data='create_group')
            .adjust(2)
            .as_markup())


def get_create_group_ikb() -> InlineKeyboardMarkup:
    return (InlineKeyboardBuilder()
            .button(text='Confirm', callback_data='confirm_create_group')
            .button(text='Main menu', callback_data='to_main_menu')
            .adjust(2)
            .as_markup())


def get_members_ikb(user_id, members: list[int]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for m in members:
        builder.button(text=f"{m}", callback_data=f'member_choose_{m}_{user_id}')
    return (builder
            .button(text='Main menu', callback_data='to_main_menu')
            .adjust(1)
            .as_markup())


def get_edit_member_ikb(user_id, admin_id) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().button(text='Edit member', callback_data='member_edit')
    if user_id == admin_id:
        builder.button(text='Edit group', callback_data='group_edit')
    return (builder
            .button(text='Main menu', callback_data='to_main_menu')
            .adjust(1)
            .as_markup())
