from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DeclarativeBase = declarative_base()


def db_connect():
    return create_engine('mysql+mysqlconnector://ciel:123456@localhost/spider', echo=True)


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)  # 创建数据库


def get_session(engine):
    return sessionmaker(bind=engine)()


def init_sqlalchemy():
    engine = db_connect()
    create_table(engine)
    return get_session(engine)


class B5Model(DeclarativeBase):
    __tablename__ = "csgo_b5"
    id = Column(Integer, primary_key=True)  # 主键自增
    map = Column(String(10))
    steamId = Column(String(18))
    score = Column(String(10))
    time = Column(DateTime)
    kda = Column(String(10))
    result = Column(String(10))
    rws = Column(String(10))
    rating = Column(String(10))
    damage = Column(String(10))
    url = Column(String(100), unique=True)
    adr = Column(String(30))
    headshot = Column(String(10))
    awp = Column(String(2))
    firstKill = Column(String(2))

    def __init__(self, **items):
        super(B5Model, self).__init__(**items)
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])


class A5EModel(DeclarativeBase):
    __tablename__ = "csgo_5e"
    id = Column(Integer, primary_key=True)  # 主键自增
    map = Column(String(10))
    domain = Column(String(30))
    score = Column(String(10))
    time = Column(DateTime)
    kda = Column(String(10))
    result = Column(String(10))
    rws = Column(String(10))
    rating = Column(String(10))
    damage = Column(String(10))
    url = Column(String(100), unique=True)
    adr = Column(String(30))
    headshot = Column(String(10))
    awp = Column(String(2))
    firstKill = Column(String(2))

    def __init__(self, **items):
        super(A5EModel, self).__init__(**items)
        for key in items:
            if hasattr(self, key):
                setattr(self, key, items[key])
