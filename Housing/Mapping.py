from sqlalchemy import Column, create_engine
from sqlalchemy.types import Integer, String, TEXT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

MYSQL_SETTING = "mysql://test:test123@104.224.160.190:3306/housing?charset=utf8"

engine = create_engine(MYSQL_SETTING, pool_size=20, max_overflow=0)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

BaseModel = declarative_base()


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


class Registration(BaseModel):
    __tablename__ = 'hs_registration'

    id = Column(Integer, primary_key=True)
    pur_apply = Column(String(64))
    status = Column(String(64))
    type = Column(String(64))
    family_type = Column(String(64))
    divorce_time = Column(String(32))
    number = Column(String(32))
    area = Column(String(32))
    license = Column(String(32))

    person_type = Column(String(32))
    certificate_type = Column(String(32))
    username = Column(String(32))
    id_card = Column(String(32))
    is_join = Column(String(32))
    talent_type = Column(String(32))
    household_area = Column(String(64))
    social_type = Column(String(32))
    social_number = Column(String(32))
    company_name = Column(String(64))
    certificate_company_name = Column(String(64))
    stationed = Column(String(64))
    full_name_troops = Column(String(64))

    family_member = Column(TEXT)
    create_time = Column(Integer)
    update_time = Column(Integer)
    delete_time = Column(Integer)

    def to_dict(self):
        return {c.name: getattr(self, c.name, None) for c in self.__table__.columns}


if __name__ == '__main__':
    session = DBSession()
    result = session.query(Registration).all()
    print(result)
