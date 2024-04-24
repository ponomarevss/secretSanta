from typing import Dict, Any, List

from sqlalchemy import select, func, and_, delete
from sqlalchemy.orm import Session

from model.entities import User, Group, Member, Link


def member_to_dict(member) -> Dict[str, Any]:
    return dict(member_id=member.member_id,
                s_nickname=member.s_nickname,
                s_wishes=member.s_wishes,
                s_address=member.s_address,
                recipient_id=member.recipient_id,
                user_id=member.user_id,
                group_id=member.group_auto_id)


class Presenter:
    def __init__(self, session: Session):
        self.session = session

    def start_main_menu_update(self, user_id, s_username) -> Dict[str, Any]:
        user = self._provide_user(s_username, user_id)
        return dict(user=self._user_to_dict(user))

    def return_main_menu_update(self, user_id) -> Dict[str, Any]:
        user = self._get_user(user_id)
        return dict(user=self._user_to_dict(user))

    def create_group_update(self, user_id) -> Dict[str, Any]:
        user = self._get_user(user_id)
        group = self._create_group(user_id)
        member = self._create_member(user_id=user_id, group_auto_id=group.auto_id)
        self._save_member(member)
        return dict(user=self._user_to_dict(user), member=member_to_dict(member), group=self._group_to_dict(group))

    def choose_member_update(self, member_id, user_id) -> Dict[str, Any]:
        member = self._get_member(member_id, user_id)
        group = self._get_group_by_auto_id(auto_id=member.group_auto_id)
        return dict(member=member_to_dict(member), group=self._group_to_dict(group))

    def add_member_by_deeplink_update(self, args: str, user_id, s_username) -> Dict[str, Any]:
        args_list = args.split(';')
        if self._is_link_valid(link_id=int(args_list[0]), group_id=int(args_list[1])):
            user = self._provide_user(s_username, user_id)
            group = self._get_group(int(args_list[1]), user_id)
            member = self._create_member(user_id=user_id, group_auto_id=group.auto_id)
            self._delete_link(link_id=int(args_list[0]), group_id=int(args_list[1]))
            return dict(user=self._user_to_dict(user), member=member_to_dict(member), group=self._group_to_dict(group))
        else:
            print("Invalid link")
            return dict()

    def create_link(self, group_id: str) -> str:
        group_id = int(group_id)
        link_id = self._new_link_id(group_id)

        new_link = Link(link_id=link_id, group_id=group_id)
        self._save_link(new_link)
        return f"{link_id};{group_id}"

    """
    private methods
    """

    def _provide_user(self, s_username, user_id):
        user = self._get_user(user_id)
        if user is None:
            user = User(user_id=user_id, s_username=s_username)
            self._save_user(user)
        return user

    def _save_user(self, user: User):
        self.session.merge(user)
        self.session.commit()

    def _get_user(self, user_id: int) -> User:
        stmt = select(User).where(User.user_id == user_id)
        return self.session.scalar(stmt)

    def _user_to_dict(self, user) -> Dict[str, Any]:
        members = self._get_members_list(user.user_id)
        return dict(user_id=user.user_id,
                    s_username=user.s_username,
                    members=[m.member_id for m in members]
                    )

    def _save_group(self, group: Group):
        self.session.merge(group)
        self.session.commit()

    def _get_group(self, group_id: int, admin_id: int) -> Group:
        stmt = select(Group).where(and_(Group.group_id == group_id, Group.admin_id == admin_id))
        return self.session.scalar(stmt)

    def _get_group_by_auto_id(self, auto_id: int) -> Group:
        stmt = select(Group).where(Group.auto_id == auto_id)
        return self.session.scalar(stmt)

    def _new_group_id(self, admin_id: int):
        stmt = select(func.max(Group.group_id)).where(Group.admin_id == admin_id)
        group_id = self.session.scalar(stmt)
        if group_id is not None:
            group_id += 1
        else:
            group_id = 1
        return group_id

    def _create_group(self, admin_id: int) -> Group:
        group_id = self._new_group_id(admin_id)
        group = Group(group_id=group_id, admin_id=admin_id)
        self._save_group(group)
        return self._get_group(group_id=group_id, admin_id=admin_id)

    def _group_to_dict(self, group) -> Dict[str, Any]:
        members = self._get_members_list(group.auto_id)
        return dict(group_id=group.group_id,
                    s_name=group.s_name,
                    s_description=group.s_description,
                    admin_id=group.admin_id,
                    members=[m.member_id for m in members]
                    )

    def _save_member(self, member: Member):
        self.session.merge(member)
        self.session.commit()

    def _new_member_id(self, user_id: int):
        stmt = select(func.max(Member.member_id)).where(Member.user_id == user_id)
        member_id = self.session.scalar(stmt)
        if member_id is not None:
            member_id += 1
        else:
            member_id = 1
        return member_id

    def _get_member(self, member_id: int, user_id) -> Member:
        stmt = select(Member).where(and_(Member.member_id == member_id, Member.user_id == user_id))
        return self.session.scalar(stmt)

    def _create_member(self, user_id: int, group_auto_id) -> Member:
        member_id = self._new_member_id(user_id)
        member = Member(member_id=member_id, user_id=user_id, group_auto_id=group_auto_id)
        self._save_member(member)
        return self._get_member(member_id=member_id, user_id=user_id)

    def _get_members_list(self, parent_id: int) -> List[Member]:
        stmt = select(Member).where(Member.user_id == parent_id)
        return list(self.session.scalars(stmt))

    def _save_link(self, link: Link):
        self.session.merge(link)
        self.session.commit()

    def _new_link_id(self, group_auto_id: int):
        stmt = select(func.max(Link.link_id)).where(Link.auto_id == group_auto_id)
        link_id = self.session.scalar(stmt)
        if link_id is not None:
            link_id += 1
        else:
            link_id = 1
        return link_id

    def _is_link_valid(self, link_id: int, group_id: int) -> bool:
        stmt = select(Link).where(and_(Link.link_id == link_id, Link.group_id == group_id))
        if self.session.scalar(stmt) is None:
            return False
        return True

    def _delete_link(self, link_id: int, group_id: int):
        stmt = delete(Link).where(and_(Link.link_id == link_id, Link.group_id == group_id))
        self.session.execute(stmt)
        self.session.commit()
