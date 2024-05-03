from sqlalchemy import select, and_, func, update
from sqlalchemy.orm import Session

from model.entities import Group, Member


class GroupRepository:
    def __init__(self, session: Session):
        self.session = session

    def save_group(self, group: Group):
        self.session.merge(group)
        self.session.commit()

    def new_group_id(self, admin_id: int) -> int:
        stmt = select(func.max(Group.group_id)).where(Group.admin_id == admin_id)
        group_id = self.session.scalar(stmt)
        if group_id is not None:
            group_id += 1
        else:
            group_id = 1
        return group_id

    def create_group(self, group) -> Group:
        self.save_group(group)
        return self.get_group(group_id=group.group_id, admin_id=group.admin_id)

    # def create_group(self, admin_id: int) -> Group:
    #     group_id = self.new_group_id(admin_id)
    #     group = Group(group_id=group_id, admin_id=admin_id)
    #     self.save_group(group)
    #     return self.get_group(group_id=group_id, admin_id=admin_id)

    def get_group(self, group_id: int, admin_id: int) -> Group:
        stmt = select(Group).where(and_(Group.group_id == group_id, Group.admin_id == admin_id))
        return self.session.scalar(stmt)

    def get_group_by_auto_id(self, auto_id: int) -> Group:
        stmt = select(Group).where(Group.auto_id == auto_id)
        return self.session.scalar(stmt)

    def get_groups_for_user(self, user_id: int):
        groups_id_stmt = select(Member.group_auto_id).where(Member.user_id == user_id)
        stmt = select(Group).where(Group.auto_id.in_(groups_id_stmt)).order_by(Group.group_id)
        return self.session.scalars(stmt)

    def update_group(self, group):
        auto_id: int = group.auto_id
        stmt = (update(Group).where(Group.auto_id == auto_id)
                .values(s_name=group.s_name, s_description=group.s_description))
        self.session.execute(stmt)
        self.session.commit()
