from sqlalchemy import select
from sqlalchemy.orm import Session

from model.entities import User


class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def provide_user(self, s_username, user_id):
        user = self.get_user(user_id)
        if user is None:
            user = User(user_id=user_id, s_username=s_username)
            self.save_user(user)
        return user

    def save_user(self, user: User):
        self.session.merge(user)
        self.session.commit()

    def get_user(self, user_id: int) -> User:
        stmt = select(User).where(User.user_id == user_id)
        return self.session.scalar(stmt)
