import os
from contextlib import contextmanager

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func

from dotenv import load_dotenv
import phonenumbers


load_dotenv()
engine = sa.create_engine(
    'postgresql://{}:{}@{}:{}/{}'.format(
        os.getenv('PG_USER'),
        os.getenv('PG_PASSWORD'),
        os.getenv('PG_HOST'),
        os.getenv('PG_PORT'),
        os.getenv('PG_DB_NAME'),
    )
)

Session = sessionmaker(bind=engine)
Base = declarative_base()

@contextmanager
def create_session(**kwargs):
    new_session = Session(**kwargs)
    try:
        yield new_session
        new_session.commit()
    except Exception:
        new_session.rollback()
        raise
    finally:
        new_session.close()


class Task(Base):
    __tablename__ = 'City'
    id = sa.Column(sa.Integer, primary_key=True)
    taskName = sa.Column(sa.String())
    phone = sa.Column(sa.String())
    email = sa.Column(sa.String())
    nickName = sa.Column(sa.String())
    name = sa.Column(sa.String())
    addInfo = sa.Column(sa.String())
    phone_text = sa.Column(sa.String())
    status = sa.Column(sa.Boolean())


def new_task(task_name: str) -> str:
    pass


def create_all_tables():
    Base.metadata.create_all(engine)

