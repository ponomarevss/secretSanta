from sqlalchemy import select, Engine
from sqlalchemy.orm import Session

from model.entities import User, Group, Member


class Presenter:
    def __init__(self, engine: Engine):
        self.engine = engine

    def provide_user(self, user_id, s_username) -> User:
        user = self.fetch_user(user_id)
        if user is None:
            user = User(user_id=user_id, s_username=s_username)
            self.save_user(user)
        return user

    def save_user(self, user: User):
        with Session(self.engine) as session:
            session.merge(user)
            session.commit()

    def fetch_user(self, user_id: int) -> User:
        stmt = select(User).where(User.user_id == user_id)
        return Session(self.engine).scalar(stmt)

    def save_group(self, group: Group):
        with Session(self.engine) as session:
            session.merge(group)
            session.commit()

    def fetch_group(self, group_id: str) -> Group:
        stmt = select(Group).where(Group.group_id == group_id)
        return Session(self.engine).scalar(stmt)

    def save_member(self, member: Member):
        with Session(self.engine) as session:
            session.merge(member)
            session.commit()

    def fetch_member(self, member_id: str) -> Member:
        stmt = select(Member).where(Member.member_id == member_id)
        return Session(self.engine).scalar(stmt)
