from sqlalchemy import select, and_, func
from sqlalchemy.orm import Session

from model.entities import Group


class GroupRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_group(self, group: Group):
        self.session.merge(group)
        self.session.commit()

    def get_group(self, group_id: int, admin_id: int) -> Group:
        stmt = select(Group).where(and_(Group.group_id == group_id, Group.admin_id == admin_id))
        return self.session.scalar(stmt)

    def get_group_by_auto_id(self, auto_id: int) -> Group:
        stmt = select(Group).where(Group.auto_id == auto_id)
        return self.session.scalar(stmt)

    def new_group_id(self, admin_id: int):
        stmt = select(func.max(Group.group_id)).where(Group.admin_id == admin_id)
        group_id = self.session.scalar(stmt)
        if group_id is not None:
            group_id += 1
        else:
            group_id = 1
        return group_id

    def create_group(self, admin_id: int) -> Group:
        group_id = self.new_group_id(admin_id)
        group = Group(group_id=group_id, admin_id=admin_id)
        self.save_group(group)
        return self.get_group(group_id=group_id, admin_id=admin_id)
