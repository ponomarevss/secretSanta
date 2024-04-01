from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_stateless_message_ikb() -> InlineKeyboardMarkup:
    return (InlineKeyboardBuilder().button(text=f'My groups', callback_data=f'groups')
            .button(text=f'Create group', callback_data=f'create_group')
            .adjust(1)
            .as_markup()
            )
