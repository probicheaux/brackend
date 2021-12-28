import dramatiq
from dramatiq.brokers.redis import RedisBroker
from firebase_admin.auth import create_user, get_user
from flask_restful import current_app
from sqlalchemy import select
from sqlalchemy.orm import Session

from brackend.db.models import (
    EngineGetter,
    NotFoundException,
    Tournament,
    User,
    UserRole,
    UserTournament,
)
from brackend.util import BrackendException

redis_broker = RedisBroker(host="redis")
dramatiq.set_broker(redis_broker)


def save_new_tournament(name, firebase_id):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        session.expire_on_commit = False
        new_tourney = Tournament(name=name)
        user = get_user_by_uid(firebase_id)
        session.add(user)
        if user is None:
            raise BrackendException("Somehow a nonexistent user is trying to save a tournament")
        session.add(new_tourney)
        session.flush()
        assert new_tourney.id is not None
        new_user_tournament = UserTournament(
            user_id=user.id, tournament_id=new_tourney.id, role=UserRole.organizer
        )
        session.add(new_user_tournament)
        session.commit()
        current_app.logger.info("Users: %s", new_tourney.users)
        current_app.logger.info("Tournaments: %s", user.tournaments)
        return new_tourney


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
        tournament = session.query(Tournament).filter(Tournament.id == t_id).one_or_none()
        return tournament


def get_tournaments_by_uid(uid):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        tournaments = (
            session.query(Tournament)
            .join(Tournament.user_tournaments)
            .join(UserTournament.user)
            .where(User.firebase_id == uid)
            .all()
        )
        return tournaments


def get_user_by_uid(uid):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        user = session.query(User).filter(User.firebase_id == uid).one_or_none()
        return user
