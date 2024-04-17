from typing import Dict, Any, List

from sqlalchemy import select, func, and_, delete
from sqlalchemy.orm import Session

from model.entities import User, Group, Member, Link


def user_to_dict(user) -> Dict[str, Any]:
    return dict(user_id=user.user_id,
                s_username=user.s_username,
                # members=[m.member_id for m in user.members]
                )


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
                # members=[m.member_id for m in group.members]
                )


class Presenter:
    def __init__(self, session: Session):
        self.session = session

    def start_main_menu_update(self, user_id, s_username) -> Dict[str, Any]:
        user = self._provide_user(s_username, user_id)
        return dict(user=user_to_dict(user))

    def return_main_menu_update(self, user_id) -> Dict[str, Any]:
        user = self._fetch_user(user_id)
        return dict(user=user_to_dict(user))

    def create_group_update(self, user_id) -> Dict[str, Any]:
        user = self._fetch_user(user_id)
        group = Group(admin_id=user.user_id)
        member = Member()
        return self.append_member_update(user, group, member)

    def choose_member_update(self, member_id) -> Dict[str, Any]:
        member = self._fetch_member(member_id)
        return dict(member=member_to_dict(member), group=group_to_dict(member.group))

    def add_member_by_deeplink_update(self, args: str, user_id, s_username) -> Dict[str, Any]:
        args_list = args.split(';')
        if self._is_link_valid(link_id=int(args_list[0]), group_id=int(args_list[1])):
            user = self._provide_user(s_username, user_id)
            group = self._fetch_group(int(args_list[1]))
            member = Member()
            self._delete_link(link_id=int(args_list[0]), group_id=int(args_list[1]))
            return self.append_member_update(user, group, member)
        else:
            print("Invalid link")
            return dict()

    def append_member_update(self, user, group, member):
        user.members.append(member)
        group.members.append(member)
        self._save_user(user)
        self._save_group(group)
        member = self._fetch_member(member.member_id)
        group = self._fetch_group(member.group_id)
        return dict(user=user_to_dict(user), member=member_to_dict(member), group=group_to_dict(group))

    def create_link(self, group_id: str) -> str:
        group_id = int(group_id)
        stmt = select(func.max(Link.link_id)).where(Link.group_id == group_id)
        link_id = self.session.scalar(stmt)
        if link_id is not None:
            link_id += 1
        else:
            link_id = 1

        new_link = Link(link_id=link_id, group_id=group_id)
        self._save_link(new_link)
        return f"{link_id};{group_id}"

    def _is_link_valid(self, link_id: int, group_id: int) -> bool:
        stmt = select(Link).where(and_(Link.link_id == link_id, Link.group_id == group_id))
        if self.session.scalar(stmt) is None:
            return False
        return True

    def _provide_user(self, s_username, user_id):
        user = self._fetch_user(user_id)
        if user is None:
            user = User(user_id=user_id, s_username=s_username)
            self._save_user(user)
        return user

    def _save_user(self, user: User):
        self.session.merge(user)
        self.session.commit()

    def _fetch_user(self, user_id: int) -> User:
        stmt = select(User).where(User.user_id == user_id)
        return self.session.scalar(stmt)

    def _save_group(self, group: Group):
        self.session.merge(group)
        self.session.commit()

    def _fetch_group(self, group_id: int) -> Group:
        stmt = select(Group).where(Group.group_id == group_id)
        return self.session.scalar(stmt)

    def _save_member(self, member: Member):
        self.session.merge(member)
        self.session.commit()

    def _fetch_member(self, member_id: int) -> Member:
        stmt = select(Member).where(Member.member_id == member_id)
        return self.session.scalar(stmt)

    def _fetch_members_list(self, user_id: int) -> List[Member]:
        stmt = select(Member).where(Member.user_id == user_id)
        return list(self.session.scalars(stmt))

    def _save_link(self, link: Link):
        self.session.merge(link)
        self.session.commit()

    def _delete_link(self, link_id: int, group_id: int):
        stmt = delete(Link).where(and_(Link.link_id == link_id, Link.group_id == group_id))
        self.session.execute(stmt)
        self.session.commit()
