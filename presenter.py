from typing import Dict, Any

from sqlalchemy.orm import Session

from model.entities import Link
from repository.group_repo import GroupRepository
from repository.link_repo import LinkRepository
from repository.member_repo import MemberRepository
from repository.user_repo import UserRepository


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
        self.user_repo = UserRepository(session)
        self.group_repo = GroupRepository(session)
        self.member_repo = MemberRepository(session)
        self.link_repo = LinkRepository(session)

    def start_main_menu_update(self, user_id, s_username) -> Dict[str, Any]:
        user = self.user_repo.provide_user(s_username, user_id)
        return dict(user=self._user_to_dict(user))

    def return_main_menu_update(self, user_id) -> Dict[str, Any]:
        user = self.user_repo.get_user(user_id)
        return dict(user=self._user_to_dict(user))

    def create_group_update(self, user_id) -> Dict[str, Any]:
        user = self.user_repo.get_user(user_id)
        group = self.group_repo.create_group(user_id)
        member = self.member_repo.create_member(user_id=user_id, group_auto_id=group.auto_id)
        return dict(user=self._user_to_dict(user), member=member_to_dict(member), group=self._group_to_dict(group))

    def choose_member_update(self, member_id, user_id) -> Dict[str, Any]:
        member = self.member_repo.get_member(member_id, user_id)
        group = self.group_repo.get_group_by_auto_id(auto_id=member.group_auto_id)
        return dict(member=member_to_dict(member), group=self._group_to_dict(group))

    def add_member_by_deeplink_update(self, args: str, user_id, s_username) -> Dict[str, Any]:
        args_list = args.split(';')
        if self.link_repo.is_link_valid(link_id=int(args_list[0]), group_id=int(args_list[1])):
            user = self.user_repo.provide_user(s_username, user_id)
            group = self.group_repo.get_group(int(args_list[1]), user_id)
            member = self.member_repo.create_member(user_id=user_id, group_auto_id=group.auto_id)
            self.link_repo.delete_link(link_id=int(args_list[0]), group_id=int(args_list[1]))
            return dict(user=self._user_to_dict(user), member=member_to_dict(member), group=self._group_to_dict(group))
        else:
            print("Invalid link")
            return dict()

    def create_link(self, group_id: str) -> str:
        group_id = int(group_id)
        link_id = self.link_repo.new_link_id(group_id)

        new_link = Link(link_id=link_id, group_id=group_id)
        self.link_repo.save_link(new_link)
        return f"{link_id};{group_id}"

    def _user_to_dict(self, user) -> Dict[str, Any]:
        members = self.member_repo.get_members_list_by_user(user.user_id)
        return dict(user_id=user.user_id,
                    s_username=user.s_username,
                    members=[m.member_id for m in members]
                    )

    def _group_to_dict(self, group) -> Dict[str, Any]:
        members = self.member_repo.get_members_list_by_group(group.auto_id)
        return dict(group_id=group.group_id,
                    s_name=group.s_name,
                    s_description=group.s_description,
                    admin_id=group.admin_id,
                    members=[m.member_id for m in members]
                    )
