import dramatiq
from dramatiq.brokers.redis import RedisBroker
from firebase_admin.auth import create_user, get_user
from sqlalchemy import select
from sqlalchemy.orm import Session

from brackend.db.models import EngineGetter, NotFoundException, Tournament, User
from brackend.util import BrackendException

redis_broker = RedisBroker(host="redis")
dramatiq.set_broker(redis_broker)

def save_new_tournament(name, firebase_id):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        session.expire_on_commit = False
        new_tourny = Tournament(name=name)
        user = get_user_by_uid(firebase_id)
        if user is None:
            raise BrackendException("Somehow a nonexistent user is trying to save a tournament")
        new_tourny.users.append(user)
        session.add(new_tourny)
        session.commit()
        return new_tourny

def save_new_user(username, firebase_id):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        session.expire_on_commit = False
        new_user = User(firebase_id=firebase_id, username=username)
        session.add(new_user)
        session.commit()
        return new_user

def get_user_ids():
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        users = session.query(User).all()
        return [u.id for u in users]


def get_tournament_ids():
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        users = session.query(Tournament).all()
        return [u.id for u in users]


def get_tournament_by_id(t_id):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        tournament = session\
            .query(Tournament)\
            .filter(Tournament.id == t_id)\
            .one_or_none()
        return tournament

def get_tournaments_by_uid(uid):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        tournaments = session\
            .query(Tournament)\
            .join(Tournament.users)\
            .where(User.firebase_id == uid)\
            .all()
        return tournaments

def get_user_by_uid(uid):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        user = session\
            .query(User)\
            .filter(User.firebase_id == uid)\
            .one_or_none()
        return user
