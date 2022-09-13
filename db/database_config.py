from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

engine = create_engine(
    "postgresql+psycopg2://db_user:db_user123@127.0.0.1:5432/database",
    echo=False,
)


def get_session():
    return sessionmaker(engine)
