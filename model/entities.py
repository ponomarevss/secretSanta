from __future__ import annotations

from typing import List

from sqlalchemy import BigInteger, ForeignKey, String
from sqlalchemy.orm import mapped_column, DeclarativeBase, relationship, Mapped


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "t_user"

    user_id = mapped_column(BigInteger, primary_key=True)
    members: Mapped[List[Member]] = relationship(back_populates='user')

    def __repr__(self) -> str:
        return (f"User("
                f"user_id={self.user_id}, "
                f"members={[m.member_id for m in self.members]}"
                f")")


class Group(Base):
    __tablename__ = 't_group'

    group_id = mapped_column(BigInteger, primary_key=True)
    s_name = mapped_column(String(30))
    s_description = mapped_column(String(150))
    admin_id = mapped_column(BigInteger, ForeignKey('t_user.user_id'))
    members: Mapped[List[Member]] = relationship(back_populates='group')

    def __repr__(self) -> str:
        return (f"Group("
                f"group_id={self.group_id}, "
                f"s_name={self.s_name}, "
                f"s_description={self.s_description}, "
                f"admin_id={self.admin_id}, "
                f"members={[m.member_id for m in self.members]}"
                f")")


class Member(Base):
    __tablename__ = "t_member"

    member_id = mapped_column(BigInteger, primary_key=True)
    s_nickname = mapped_column(String(30))
    s_wishes = mapped_column(String(150))
    s_address = mapped_column(String(150))
    recipient_id = mapped_column(BigInteger, ForeignKey("t_member.member_id"))
    santas: Mapped[List[Member]] = relationship('Member')
    user_id = mapped_column(BigInteger, ForeignKey('t_user.user_id'))
    user: Mapped[User] = relationship('User', back_populates='members')
    group_id = mapped_column(BigInteger, ForeignKey('t_group.group_id'))
    group: Mapped[Group] = relationship(back_populates='members')

    def __repr__(self) -> str:
        return (f"Member("
                f"member_id={self.member_id}, "
                f"s_nickname={self.s_nickname}, "
                f"s_wishes={self.s_wishes}, "
                f"s_address={self.s_address}, "
                f"recipient_id={self.recipient_id}, "
                f"santas={[s.member_id for s in self.santas]}, "
                f"user_id={self.user_id}, "
                f"group_id={self.group_id}"
                f")")


# class Game(Base):
#     __tablename__ = 't_game'
#
#     game_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     group_id: Mapped[int] = mapped_column(BigInteger)
#     dt_start: Mapped[Optional[DateTime]] = mapped_column(DateTime)
#     dt_finish: Mapped[Optional[DateTime]] = mapped_column(DateTime)
#
#     def __repr__(self) -> str:
#         return (f"Game("
#                 f"game_id={self.game_id}, "
#                 f"group_id={self.group_id}, "
#                 f"dt_start={self.dt_start}, "
#                 f"dt_finish={self.dt_finish}"
#                 f")")


# class Gift(Base):
#     __tablename__ = 't_gift'
#
#     gift_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
#     game_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     santa_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     recipient_id: Mapped[Optional[int]] = mapped_column(BigInteger)
#     s_feedback: Mapped[Optional[str]] = mapped_column(String(150))
#     i_rating: Mapped[Optional[int]] = mapped_column()
#
#     def __repr__(self) -> str:
#         return (f"Gift("
#                 f"gift_id={self.gift_id}, "
#                 f"game_id={self.game_id}, "
#                 f"santa_id={self.santa_id}, "
#                 f"recipient_id={self.recipient_id}, "
#                 f"s_feedback={self.s_feedback}, "
#                 f"i_rating={self.i_rating}"
#                 f")")
