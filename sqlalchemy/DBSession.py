from settings import MYSQL_SETTING
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(MYSQL_SETTING, pool_size=20, max_overflow=0)
DBSession = sessionmaker(bind=engine)



