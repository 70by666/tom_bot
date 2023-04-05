import os

from dotenv import find_dotenv, load_dotenv
from sqlalchemy import BigInteger, Column, String, create_engine
from sqlalchemy.orm import declarative_base, scoped_session, sessionmaker

load_dotenv(find_dotenv())

# config
user = str(os.getenv('DATABASE_USER'))
password = str(os.getenv('DATABASE_PASSWORD'))
host = str(os.getenv('DATABASE_HOST'))
database = str(os.getenv('DATABASE_NAME'))

engine = create_engine('postgresql+psycopg2://{}:{}@{}/{}'.format(
    user,
    password,
    host,
    database,
))

session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()
Base.query = session.query_property()


class Numbers(Base):
    __tablename__ = 'numbers'
    
    id = Column(BigInteger, primary_key=True)
    last_name = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    patronymic = Column(String, nullable=False)
    number = Column(String, nullable=False)
    who_contributed_id = Column(BigInteger)
    who_contributed_name = Column(String)


Base.metadata.create_all(bind=engine)
