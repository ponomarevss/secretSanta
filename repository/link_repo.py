from sqlalchemy import select, func, and_, delete

from model.entities import Link


class LinkRepository:
    def __init__(self, session):
        self.session = session

    def save_link(self, link: Link):
        self.session.merge(link)
        self.session.commit()

    def new_link_id(self, group_auto_id: int):
        stmt = select(func.max(Link.link_id)).where(Link.auto_id == group_auto_id)
        link_id = self.session.scalar(stmt)
        if link_id is not None:
            link_id += 1
        else:
            link_id = 1
        return link_id

    def is_link_valid(self, link_id: int, group_id: int) -> bool:
        stmt = select(Link).where(and_(Link.link_id == link_id, Link.group_id == group_id))
        if self.session.scalar(stmt) is None:
            return False
        return True

    def delete_link(self, link_id: int, group_id: int):
        stmt = delete(Link).where(and_(Link.link_id == link_id, Link.group_id == group_id))
        self.session.execute(stmt)
        self.session.commit()
