import time
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message

from new_presenter import NewPresenter
from presenter import Presenter


class PresenterMiddleware(BaseMiddleware):
    def __init__(self, presenter: NewPresenter):
    # def __init__(self, presenter: Presenter):
        super().__init__()
        self.presenter = presenter

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any],
    ) -> Any:
        with self.presenter.session:
            data["presenter"] = self.presenter
            return await handler(event, data)


class AntispamMiddleware(BaseMiddleware):
    def __init__(self, v_in_i_cooldown: int) -> None:
        self.f_timestamp = 0.0
        self.i_cooldown = v_in_i_cooldown

    async def __call__(
            self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        f_timestamp = time.time()
        if f_timestamp - self.f_timestamp > self.i_cooldown:
            self.f_timestamp = f_timestamp
            return await handler(event, data)
        else:
            return
