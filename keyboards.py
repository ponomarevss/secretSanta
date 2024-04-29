from typing import Any, Dict

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


def get_groups_ikb(groups: list[Dict[str, Any]]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for g in groups:
        text = f"{g['s_name']}" if (g['s_name'] is not None) else f"{g['group_id']}"
        builder.button(text=text, callback_data=f"group_choose_{g['auto_id']}")
    return (builder
            .button(text='Main menu', callback_data='to_main_menu')
            .adjust(1)
            .as_markup())

# def get_members_ikb(user_id, members: list[int]) -> InlineKeyboardMarkup:
#     builder = InlineKeyboardBuilder()
#     for m in members:
#         builder.button(text=f"{m}", callback_data=f'member_choose_{m}_{user_id}')
#     return (builder
#             .button(text='Main menu', callback_data='to_main_menu')
#             .adjust(1)
#             .as_markup())


def get_edit_ikb(is_admin: bool) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder().button(text='Edit member', callback_data='member_edit')
    if is_admin:
        builder.button(text='Edit group', callback_data='group_edit')
    return (builder.button(text='Main menu', callback_data='to_main_menu')
            .adjust(1)
            .as_markup())


def get_edit_member_ikb() -> InlineKeyboardMarkup:
    return (InlineKeyboardBuilder()
            .button(text='Edit member', callback_data='member_edit')
            .button(text='Main menu', callback_data='to_main_menu')
            .adjust(1)
            .as_markup())
