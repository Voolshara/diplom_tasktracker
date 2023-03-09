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
    __tablename__ = 'Task'
    id = sa.Column(sa.Integer, primary_key=True)
    taskName = sa.Column(sa.String(), unique=True)
    phone = sa.Column(sa.String())
    email = sa.Column(sa.String())
    nickName = sa.Column(sa.String())
    name = sa.Column(sa.String())
    addInfo = sa.Column(sa.String())
    phone_text = sa.Column(sa.String())
    status = sa.Column(sa.Boolean())

def check_task(task_name: str) -> bool:
    with create_session() as session:
        db_response = session.query(Task).filter(Task.taskName == task_name).one_or_none()
        return db_response is None
    
def get_all_running_tasks() -> list:
    with create_session() as session:
        db_response = session.query(Task).filter(Task.status == True).all()
        if len(db_response) == 0:
            return []
        out_data = [[
            el.id, el.taskName, el.phone, el.email, el.nickName, el.name, el.addInfo, el.phone_text, el.status
            ] for el in db_response]
        out_data.sort(key=lambda x: x[0])
        return out_data
    
def get_all_close_tasks() -> list:
    with create_session() as session:
        db_response = session.query(Task).filter(Task.status == False).all()
        if len(db_response) == 0:
            return []
        out_data = [[
            el.id, el.taskName, el.phone, el.email, el.nickName, el.name, el.addInfo, el.phone_text, el.status
            ] for el in db_response]
        out_data.sort(key=lambda x: x[0])
        return out_data
    
def new_task(task_name: str) -> str:
    with create_session() as session:
        session.add(
            Task(
                taskName = task_name,
                phone = "",
                email = "",
                nickName = "",
                name = "",
                addInfo = "",
                phone_text = "",
                status = True,
            )
        )

def get_now_phone(task_id: int) -> list:
    with create_session() as session:
        db_response = session.query(Task).filter(Task.id == task_id).one_or_none()
        return [db_response.phone, db_response.phone_text] if db_response is not None else ["", ""]

def set_data(form_data: dict) -> None:
    with create_session() as session:
        session.query(Task).filter(
            Task.id == int(form_data['task'])
            ).update({
                Task.phone: form_data['phone'],
                Task.email: form_data['email'],
                Task.nickName: form_data['Nickname'],
                Task.name: form_data['name'],
                Task.addInfo: form_data['addinfo'],
                Task.phone_text: form_data['phone_text'],
            })
        
def change_status(task_id: int) -> None:
    with create_session() as session:
        session.query(Task).filter(
            Task.id == task_id
            ).update({
                Task.status: False
            })

def create_all_tables():
    Base.metadata.create_all(engine)

