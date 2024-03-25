from typing import Any, Dict

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


# def get_stateless_message_text(user_id, username) -> Dict[str, Any]:
    # найти юзера
    # если есть фразу с возвращением, короткая сводка о группах
    # если нет внести в бд

    # избавить презентер от Message and FSMContext



    # этот хэндлер принимает не чаще чем раз в пять секунд


    # return f'Welcome, {username}' # подумать что возвращать


def get_stateless_message_ikb() -> InlineKeyboardMarkup:
    return (InlineKeyboardBuilder().button(text=f'My groups', callback_data=f'groups')
            .button(text=f'Create group', callback_data=f'create_group')
            .as_markup()
            )


async def get_groups(state: FSMContext):
    pass
