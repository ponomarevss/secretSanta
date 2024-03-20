from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from admin import DB_URL
from model.entities import Base, User, Group

engine = create_engine(url=DB_URL)
Base.metadata.create_all(engine)


if __name__ == '__main__':
    # u1 = User(user_id=101)
    # u2 = UserTable(user_id=102)
    #
    # g1 = GroupTable(group_id=901)
    # g2 = GroupTable(group_id=902)

    # u1.groups = [g1, g2]

    with Session(engine) as session:
        # session.merge(u1)

        stmt = select(User).where(User.user_id == 101)
        user = session.scalar(stmt)

        # session.commit()

        print(user)
