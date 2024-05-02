from typing import Dict, Any

from sqlalchemy.orm import Session

from model.entities import Link, User
from repository.group_repo import GroupRepository
from repository.link_repo import LinkRepository
from repository.member_repo import MemberRepository
from repository.user_repo import UserRepository


class Presenter:
    def __init__(self, session: Session):
        self.session = session
        self.user_repo = UserRepository(session)
        self.group_repo = GroupRepository(session)
        self.member_repo = MemberRepository(session)
        self.link_repo = LinkRepository(session)

    def start_main_menu_update(self, user_id, s_username, data):
        self.user_repo.save_user(User(user_id=user_id, s_username=s_username))
        data['user_id'] = user_id
        data['s_username'] = s_username
        data['text'] = f"Hello, {s_username}!"

    def create_group_button_update(self, data):
        data['text'] = f"{data['s_username']}\nCreate new group with you as a first member"

    def confirm_create_group_update(self, data):
        user_id = data['user_id']
        group = self.group_repo.create_group(user_id)
        member = self.member_repo.create_member(user_id=user_id, group_auto_id=group.auto_id)
        data['text'] = f"{data['s_username']}\nGroup: {group.group_id}\nMember: {member.member_id}"

    def to_main_menu_update(self, data):
        data['text'] = f"{data['s_username']}, you are in main menu again"

    def groups_button_update(self, data):
        groups = self.group_repo.get_groups_for_user(data['user_id'])
        data['groups'] = [self._group_to_dict(g) for g in groups]
        data['text'] = f"{data['s_username']}, groups list:"

    def choose_group_update(self, group_auto_id, data):
        group = self.group_repo.get_group_by_auto_id(auto_id=group_auto_id)
        member = self.member_repo.get_member_by_user_and_group(user_id=data['user_id'], group_auto_id=group_auto_id)
        data['group'] = self._group_to_dict(group)
        data['member'] = self._member_to_dict(member)
        data['is_admin'] = data['user_id'] == group.admin_id
        data['text'] = f"{data['s_username']}, you are in\ngroup: {group.group_id}\nas member: {member.member_id}"

    def add_member_by_deeplink_update(self, args: str, user_id, s_username, data):
        data['user_id'] = user_id
        data['s_username'] = s_username
        self.user_repo.save_user(User(user_id=user_id, s_username=s_username))
        args_list = args.split(';')
        link_id, group_auto_id = int(args_list[0]), int(args_list[1])
        is_valid = self.link_repo.is_link_valid(link_id=link_id, group_auto_id=group_auto_id)
        is_user_not_in_group = self.member_repo.is_user_not_in_group(user_id=user_id, group_auto_id=group_auto_id)
        if not is_valid:
            data['text'] = "Invalid link"
        elif not is_user_not_in_group:
            data['text'] = "You are already in this group"
        else:
            group = self.group_repo.get_group_by_auto_id(group_auto_id)
            member = self.member_repo.provide_member(user_id=user_id, group_auto_id=group_auto_id)
            data['group'] = self._group_to_dict(group)
            data['member'] = self._member_to_dict(member)
            data['text'] = f"{s_username}, joined to\ngroup: {group.group_id}\nas member: {member.member_id}"
            self.link_repo.delete_link(link_id=link_id, group_id=group_auto_id)

    def create_link(self, data) -> str:
        group_auto_id = data['group']['auto_id']
        link_id = self.link_repo.new_link_id(group_auto_id)
        self.link_repo.save_link(Link(link_id=link_id, group_auto_id=group_auto_id))
        return f"{link_id};{group_auto_id}"

    def group_edit_update(self, data):
        data['text'] = (f"Edit group\n"
                        f"ID:{data['group']['auto_id']}\n"
                        f"Name: {data['group']['s_name']}\n"
                        f"Description: {data['group']['s_description']}")

    def _group_to_dict(self, group) -> Dict[str, Any]:
        return dict(auto_id=group.auto_id,
                    group_id=group.group_id,
                    s_name=group.s_name,
                    s_description=group.s_description,
                    admin_id=group.admin_id,
                    )

    def _groups_to_dict(self, groups: list[Any]) -> list[Dict[str, Any]]:
        return [self._group_to_dict(g) for g in groups]

    def _member_to_dict(self, member) -> Dict[str, Any]:
        return dict(member_id=member.member_id,
                    s_nickname=member.s_nickname,
                    s_wishes=member.s_wishes,
                    s_address=member.s_address,
                    recipient_id=member.recipient_id,
                    user_id=member.user_id,
                    group_auto_id=member.group_auto_id
                    )
