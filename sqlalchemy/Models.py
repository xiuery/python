
from BaseModel import BaseModel
from sqlalchemy import Column
from sqlalchemy.types import CHAR, Integer, String, DATE, SMALLINT


class User(BaseModel):
    __tablename__ = 'x_admin_user'

    id = Column(Integer, primary_key=True)
    username = Column(String(128))


if __name__ == '__main__':
    from DBSession import DBSession

    db_session = DBSession()
    users = db_session.query(User).all()

    print(users)

