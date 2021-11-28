import dramatiq
from dramatiq.brokers.redis import RedisBroker
from sqlalchemy.orm import Session

from brackend.db.models import EngineGetter, Tournament, User

redis_broker = RedisBroker(host="redis")
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def save_new_user_email(username, password, email):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        new_user = User(username=username, password=password, email=email, verified=False)
        session.add(new_user)
        session.commit()


@dramatiq.actor
def save_new_tournament(name):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        new_tourny = Tournament(name=name)
        session.add(new_tourny)
        session.commit()


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
