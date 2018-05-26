from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# MYSQL_SETTING = 'mysql://root:root@192.168.200.227:3306/apps?charset=utf8'
MYSQL_SETTING = 'mysql://root:root@192.168.200.227:3306/apps?charset=utf8'


engine = create_engine(MYSQL_SETTING, pool_size=20, max_overflow=0)
DBSession = sessionmaker(bind=engine)



