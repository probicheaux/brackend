import dramatiq
from dramatiq.brokers.redis import RedisBroker
from flask_restful import current_app
from sqlalchemy.orm import Session

from brackend.db.models import (
    EngineGetter,
    Tournament,
    User,
    UserTournament,
)
from brackend.db.enums import UserRole
from brackend.util import BrackendException

redis_broker = RedisBroker(host="redis")
dramatiq.set_broker(redis_broker)


def save_new_tournament(data, firebase_id):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        session.expire_on_commit = False
        new_tourney = Tournament(
            name=data.get("name"),
            desription=data.get("description"),
            start_date=data.get("start_date"),
            end_date=data.get("end_date"),
        )
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
    """
    returns a list of all users in the database
    """
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        users = session.query(User).all()
        return [u.id for u in users]


def get_tournament_ids():
    """
    returns a list of all tournaments in the database
    """
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        users = session.query(Tournament).all()
        return [u.id for u in users]


def delete_tournament(tid, uid):
    """
    delete tournament from the database
    """
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        tournament = (
            session.query(Tournament)
            .join(Tournament.user_tournaments)
            .join(UserTournament.user)
            .where(Tournament.id == tid)
            .where(User.firebase_id == uid)
            .where(UserRole.organizer == UserTournament.role)
        ).one_or_none()
        assert tournament is not None
        session.delete(tournament)
        session.commit()
        return True


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
