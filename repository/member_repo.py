from typing import List

from sqlalchemy import select, func, and_
from sqlalchemy.orm import Session

from model.entities import Member


class MemberRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_member(self, member: Member):
        self.session.merge(member)
        self.session.commit()

    def new_member_id(self, user_id: int):
        stmt = select(func.max(Member.member_id)).where(Member.user_id == user_id)
        member_id = self.session.scalar(stmt)
        if member_id is not None:
            member_id += 1
        else:
            member_id = 1
        return member_id

    def get_member(self, member_id: int, user_id) -> Member:
        stmt = select(Member).where(and_(Member.member_id == member_id, Member.user_id == user_id))
        return self.session.scalar(stmt)

    def create_member(self, user_id: int, group_auto_id) -> Member:
        member_id = self.new_member_id(user_id)
        member = Member(member_id=member_id, user_id=user_id, group_auto_id=group_auto_id)
        self.save_member(member)
        return self.get_member(member_id=member_id, user_id=user_id)

    def get_members_list_by_user(self, user_id: int) -> List[Member]:
        stmt = select(Member).where(Member.user_id == user_id)
        return list(self.session.scalars(stmt))

    def get_members_list_by_group(self, group_auto_id: int) -> List[Member]:
        stmt = select(Member).where(Member.group_auto_id == group_auto_id)
        return list(self.session.scalars(stmt))
