from __future__ import annotations

from typing import List, Optional

from sqlalchemy import Column, BigInteger, Table, ForeignKey, String, DateTime
from sqlalchemy.orm import mapped_column, DeclarativeBase, relationship, Mapped


class Base(DeclarativeBase):
    pass


association_table = Table(
    "association_table",
    Base.metadata,
    Column("left_id", ForeignKey("t_user.user_id"), primary_key=True),
    Column("right_id", ForeignKey("t_group.group_id"), primary_key=True),
)


class User(Base):
    __tablename__ = "t_user"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    s_nickname: Mapped[Optional[str]] = mapped_column(String(30))
    s_wishes: Mapped[Optional[str]] = mapped_column(String(150))
    s_address: Mapped[Optional[str]] = mapped_column(String(150))
    santa_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    recipient_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    groups: Mapped[List[Group]] = relationship(secondary="association_table", back_populates="users")

    def __repr__(self) -> str:
        return (f"User("
                f"user_id={self.user_id}, "
                f"s_nickname={self.s_nickname}, "
                f"s_wishes={self.s_wishes}, "
                f"s_address={self.s_address}, "
                f"santa_id={self.santa_id}, "
                f"recipient_id={self.recipient_id}, "
                f"groups={[group.group_id for group in self.groups]}"
                f")")


class Group(Base):
    __tablename__ = 't_group'

    group_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    s_name: Mapped[Optional[str]] = mapped_column(String(30))
    s_description: Mapped[Optional[str]] = mapped_column(String(150))
    admin_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    users: Mapped[List[User]] = relationship(secondary='association_table', back_populates='groups')

    def __repr__(self) -> str:
        return (f"Group("
                f"group_id={self.group_id}, "
                f"s_name={self.s_name}, "
                f"s_description={self.s_description}, "
                f"admin_id={self.admin_id}, "
                f"users={[user.user_id for user in self.users]}"
                f")")


class Game(Base):
    __tablename__ = 't_game'

    game_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    group_id: Mapped[int] = mapped_column(BigInteger)
    dt_start: Mapped[Optional[DateTime]] = mapped_column(DateTime)
    dt_finish: Mapped[Optional[DateTime]] = mapped_column(DateTime)

    def __repr__(self) -> str:
        return (f"Game("
                f"game_id={self.game_id}, "
                f"group_id={self.group_id}, "
                f"dt_start={self.dt_start}, "
                f"dt_finish={self.dt_finish}"
                f")")


class Gift(Base):
    __tablename__ = 't_gift'

    gift_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    game_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    santa_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    recipient_id: Mapped[Optional[int]] = mapped_column(BigInteger)
    s_feedback: Mapped[Optional[str]] = mapped_column(String(150))
    i_rating: Mapped[Optional[int]] = mapped_column()

    def __repr__(self) -> str:
        return (f"Gift("
                f"gift_id={self.gift_id}, "
                f"game_id={self.game_id}, "
                f"santa_id={self.santa_id}, "
                f"recipient_id={self.recipient_id}, "
                f"s_feedback={self.s_feedback}, "
                f"i_rating={self.i_rating}"
                f")")
