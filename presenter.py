import uuid
from typing import Dict, Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from model.entities import User, Group, Member


def user_to_dict(user) -> Dict[str, Any]:
    return dict(user_id=user.user_id,
                s_username=user.s_username,
                members=[m.member_id for m in user.members])


def member_to_dict(member) -> Dict[str, Any]:
    return dict(member_id=member.member_id,
                s_nickname=member.s_nickname,
                s_wishes=member.s_wishes,
                s_address=member.s_address,
                recipient_id=member.recipient_id,
                user_id=member.user_id,
                group_id=member.group_id)


def group_to_dict(group) -> Dict[str, Any]:
    return dict(group_id=group.group_id,
                s_name=group.s_name,
                s_description=group.s_description,
                admin_id=group.admin_id,
                members=[m.member_id for m in group.members])


class Presenter:
    def __init__(self, session: Session):
        self.session = session

    def start_main_menu_update(self, user_id, s_username) -> Dict[str, Any]:
        user = self.fetch_user(user_id)
        if user is None:
            user = User(user_id=user_id, s_username=s_username)
            self.save_user(user)
        return user_to_dict(user)

    def return_main_menu_update(self, user_id) -> Dict[str, Any]:
        user = self.fetch_user(user_id)
        return user_to_dict(user)

    def create_group_update(self, user_id) -> Dict[str, Any]:
        user = self.fetch_user(user_id)
        group = Group(group_id=f'g:{user.user_id}:{str(uuid.uuid4().hex)}', admin_id=user.user_id)
        member = Member(member_id=f'm:{user.user_id}:{str(uuid.uuid4().hex)}')
        user.members.append(member)
        group.members.append(member)
        self.save_user(user)
        self.save_group(group)
        member = self.fetch_member(member.member_id)
        return dict(user=user_to_dict(user), member=member_to_dict(member), group=group_to_dict(group))

    def choose_member_update(self, member_id) -> Dict[str, Any]:
        member = self.fetch_member(member_id)
        return dict(member=member_to_dict(member), group=group_to_dict(member.group))

    def save_user(self, user: User):
        self.session.merge(user)
        self.session.commit()

    def fetch_user(self, user_id: int) -> User:
        stmt = select(User).where(User.user_id == user_id)
        return self.session.scalar(stmt)

    def save_group(self, group: Group):
        self.session.merge(group)
        self.session.commit()

    def fetch_group(self, group_id: str) -> Group:
        stmt = select(Group).where(Group.group_id == group_id)
        return self.session.scalar(stmt)

    def save_member(self, member: Member):
        self.session.merge(member)
        self.session.commit()

    def fetch_member(self, member_id: str) -> Member:
        stmt = select(Member).where(Member.member_id == member_id)
        return self.session.scalar(stmt)
