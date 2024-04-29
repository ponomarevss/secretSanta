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

    def get_member(self, member_id: int, user_id: int) -> Member:
        stmt = select(Member).where(and_(Member.member_id == member_id, Member.user_id == user_id))
        return self.session.scalar(stmt)

    def get_member_by_user_and_group(self, user_id: int, group_auto_id: int) -> Member:
        stmt = select(Member).where(and_(Member.user_id == user_id, Member.group_auto_id == group_auto_id))
        return self.session.scalar(stmt)

    def provide_member(self, user_id: int, group_auto_id: int) -> Member:
        member = self.get_member_by_user_and_group(user_id, group_auto_id)
        if member is None:
            member = self.create_member(user_id, group_auto_id)
        return member
    #TODO Где-то косяк с добавлением члена по ссылке. Потестить методы предоставления и создания члена

    def create_member(self, user_id: int, group_auto_id: int) -> Member:
        member_id = self.new_member_id(user_id)
        member = Member(member_id=member_id, user_id=user_id, group_auto_id=group_auto_id)
        self.save_member(member)
        return self.get_member(member_id=member_id, user_id=user_id)

    def get_members_for_user(self, user_id: int) -> list[Member]:
        stmt = select(Member).where(Member.user_id == user_id)
        return list(self.session.scalars(stmt))

    def get_members_for_group(self, group_auto_id: int) -> list[Member]:
        stmt = select(Member).where(Member.group_auto_id == group_auto_id)
        return list(self.session.scalars(stmt))
