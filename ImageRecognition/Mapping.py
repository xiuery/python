from sqlalchemy import Column, create_engine
from sqlalchemy.types import Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

MYSQL_SETTING = "mysql://root:root@192.168.200.228:3306/housing?charset=utf8"

engine = create_engine(MYSQL_SETTING, pool_size=20, max_overflow=0)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

BaseModel = declarative_base()


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


class Price(BaseModel):
    __tablename__ = 'hs_price'

    id = Column(Integer, primary_key=True)
    house = Column(String(16))
    building = Column(String(16))
    room = Column(String(16))
    inner_area = Column(String(16))
    pool_area = Column(String(16))
    planning = Column(String(16))
    quotation = Column(String(16))

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}
