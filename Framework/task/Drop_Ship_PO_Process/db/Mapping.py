from sqlalchemy import Column, create_engine
from sqlalchemy.types import CHAR, Integer, String, DATE, SMALLINT
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from settings import MYSQL_SETTING

engine = create_engine(MYSQL_SETTING, pool_size=20, max_overflow=0)
# 创建DBSession类型:
DBSession = sessionmaker(bind=engine)

BaseModel = declarative_base()


def init_db():
    BaseModel.metadata.create_all(engine)


def drop_db():
    BaseModel.metadata.drop_all(engine)


class VendorInfo(BaseModel):
    __tablename__ = 'dsp_vendor_info'

    id = Column(Integer, primary_key=True)
    vendor = Column(Integer)
    vendor_name = Column(String(128))
    bu = Column(String(16))
    url = Column(String(128))
    browser = Column(String(16))
    username = Column(String(64))
    password = Column(String(32))
    ip_address = Column(String(32))


class Config(BaseModel):
    __tablename__ = 'dsp_config'

    id = Column(Integer, primary_key=True)
    app_id = Column(Integer, primary_key=True)
    key_name = Column(CHAR(60))
    key_value = Column(CHAR(200))
    key_type = Column(CHAR(60))
    remark = Column(CHAR(200))
    status = Column(SMALLINT)
    create_time = Column(Integer)
    update_time = Column(Integer)
    delete_time = Column(Integer)
