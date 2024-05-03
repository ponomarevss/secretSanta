from typing import Dict, Any

from sqlalchemy.orm import Session

from model.entities import Link, User, Group, Member
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
        data['text'] = (f"{data['s_username']}\n"
                        f"Create new group with you as a first member.")

    def confirm_create_group_update(self, data):
        admin_id = data['user_id']
        group_id = self.group_repo.new_group_id(admin_id)
        data['group'] = self._group_to_dict(Group(group_id=group_id, admin_id=admin_id))
        data['text'] = "Set name for new group."

    def group_name_set_update(self, s_name, data):
        data['group']['s_name'] = s_name
        data['text'] = (f"Group name: {s_name}\n"
                        f"Set group description.")

    def group_description_set_update(self, s_description, data):
        data['group']['s_description'] = s_description
        data['text'] = (f"Group: {data['group']['s_name']}\n"
                        f"description: {s_description}\n")

    def member_edit_invitation_update(self, data):
        data['text'] = f"Set your nickname in this group.\n"

    def member_nickname_set_update(self, s_nickname, data):
        user_id = data['user_id']
        member_id = self.member_repo.new_member_id(user_id)
        data['member'] = self._member_to_dict(Member(user_id=user_id, member_id=member_id))
        data['member']['s_nickname'] = s_nickname
        data['text'] = f"Now write your wishes."

    def member_wishes_set_update(self, s_wishes, data):
        data['member']['s_wishes'] = s_wishes
        data['text'] = f"Where you'd like to catch your presents?"

    def member_address_set_update(self, s_address, data):
        data['member']['s_address'] = s_address
        data['text'] = (f"Your nickname: {data['member']['s_nickname']}\n"
                        f"wishes: {data['member']['s_wishes']}\n"
                        f"address: {data['member']['s_address']}\n")

    def group_create_update(self, data):
        group_dict = data['group']
        group = self.group_repo.create_group(Group(group_id=group_dict['group_id'],
                                                   s_name=group_dict['s_name'],
                                                   s_description=group_dict['s_description'],
                                                   admin_id=group_dict['admin_id']))
        data['group']['auto_id'] = group.auto_id
        data['text'] = f"You are in group '{data['group']['s_name']}' as '{data['member']['s_nickname']}'\n"

    def member_create_update(self, data):
        member_dict = data['member']
        data['member']['group_auto_id'] = data['group']['auto_id']
        member = self.member_repo.create_member(Member(member_id=member_dict['member_id'],
                                                       s_nickname=member_dict['s_nickname'],
                                                       s_wishes=member_dict['s_wishes'],
                                                       s_address=member_dict['s_address'],
                                                       user_id=member_dict['user_id'],
                                                       group_auto_id=member_dict['group_auto_id']))
        data['member']['auto_id'] = member.auto_id

    def to_main_menu_update(self, data):
        data['text'] = f"{data['s_username']}, you are in main menu again"

    def groups_button_update(self, data):
        groups = self.group_repo.get_groups_for_user(data['user_id'])
        data['groups'] = [self._group_to_dict(g) for g in groups]
        data['text'] = f"{data['s_username']}, groups list:"

    def choose_group_update(self, group_auto_id, data):
        group = self.group_repo.get_group_by_auto_id(auto_id=group_auto_id)
        member = self.member_repo.get_member_by_user_and_group(user_id=data['user_id'], group_auto_id=group_auto_id)
        members = self.member_repo.get_members_for_group(group_auto_id=group_auto_id)
        data['group'] = self._group_to_dict(group)
        data['members'] = [self._member_to_dict(m) for m in members]
        data['member'] = self._member_to_dict(member)
        data['is_admin'] = data['user_id'] == group.admin_id
        data['text'] = (f"You are in group '{group.s_name}' as '{member.s_nickname}'\n"
                        f"members list:\n")
        for m in members:
            data['text'] += f"{m.s_nickname}\n"

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
