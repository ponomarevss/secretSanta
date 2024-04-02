from aiogram.fsm.state import StatesGroup, State


class GroupStates(StatesGroup):
    name = State()
    description = State()


class MemberStates(StatesGroup):
    nickname = State()
    wishes = State()
    address = State()
