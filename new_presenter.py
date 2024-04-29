from typing import Dict, Any

from sqlalchemy.orm import Session

from model.entities import Link
from repository.group_repo import GroupRepository
from repository.link_repo import LinkRepository
from repository.member_repo import MemberRepository
from repository.user_repo import UserRepository


# def member_to_dict(member) -> Dict[str, Any]:
#     return dict(member_id=member.member_id,
#                 s_nickname=member.s_nickname,
#                 s_wishes=member.s_wishes,
#                 s_address=member.s_address,
#                 recipient_id=member.recipient_id,
#                 user_id=member.user_id,
#                 group_auto_id=member.group_auto_id)


class NewPresenter:
    def __init__(self, session: Session):
        self.session = session
        self.user_repo = UserRepository(session)
        self.group_repo = GroupRepository(session)
        self.member_repo = MemberRepository(session)
        self.link_repo = LinkRepository(session)

    def start_main_menu_update(self, user_id, s_username) -> Dict[str, Any]:
        user = self.user_repo.provide_user(user_id=user_id, s_username=s_username)
        text = f"Hello, {user.s_username}!"
        return dict(user_id=user_id, s_username=s_username, text=text)

    def create_group_update(self, user_id) -> Dict[str, Any]:
        user = self.user_repo.get_user(user_id)
        group = self.group_repo.create_group(user_id)
        member = self.member_repo.create_member(user_id=user_id, group_auto_id=group.auto_id)
        text = f"{user.s_username}\nGroup: {group.group_id}\nMember: {member.member_id}"
        return dict(text=text)

    def return_groups_update(self, user_id: int) -> Dict[str, Any]:
        user = self.user_repo.get_user(user_id)
        groups = self.group_repo.get_groups_list(user_id)
        return dict(text=f"{user.s_username}, groups list:", groups=[self._group_to_dict(g) for g in groups])

    def choose_group_update(self, user_id, group_auto_id) -> Dict[str, Any]:
        user = self.user_repo.get_user(user_id)
        member = self.member_repo.get_member_by_user_and_group(user_id, group_auto_id)
        group = self.group_repo.get_group_by_auto_id(auto_id=group_auto_id)
        text = f"{user.s_username}, you are in\ngroup: {group.group_id}\nas member: {member.member_id}"
        is_admin = user_id == group.admin_id
        return dict(text=text, is_admin=is_admin)

#TODO from here
    def add_member_by_deeplink_update(self, args: str, user_id, s_username) -> Dict[str, Any]:
        user = self.user_repo.get_user(user_id)
        args_list = args.split(';')
        is_valid = self.link_repo.is_link_valid(link_id=int(args_list[0]), group_auto_id=int(args_list[1]))
        if is_valid and (user is None):
            user = self.user_repo.provide_user(s_username, user_id)
            group = self.group_repo.get_group_by_auto_id(int(args_list[1]))
            member = self.member_repo.provide_member(user_id=user_id, group_auto_id=int(args_list[1]))
            self.link_repo.delete_link(link_id=int(args_list[0]), group_id=int(args_list[1]))
            text = f"{user.s_username}, joined to\ngroup: {group.group_id}\nas member: {member.member_id}"
            return dict(text=text)
        else:
            return dict(text="Invalid link")

    def create_link(self, group_auto_id: str) -> str:
        group_auto_id = int(group_auto_id)
        link_id = self.link_repo.new_link_id(group_auto_id)

        new_link = Link(link_id=link_id, group_auto_id=group_auto_id)
        self.link_repo.save_link(new_link)
        return f"{link_id};{group_auto_id}"
#TODO to here
    def _group_to_dict(self, group) -> Dict[str, Any]:
        members = self.member_repo.get_members_for_group(group.auto_id)
        return dict(auto_id=group.auto_id,
                    group_id=group.group_id,
                    s_name=group.s_name,
                    s_description=group.s_description,
                    admin_id=group.admin_id,
                    members=[m.member_id for m in members]
                    )

    def _groups_to_dict(self, groups: list[Any]) -> list[Dict[str, Any]]:
        return [self._group_to_dict(g) for g in groups]
