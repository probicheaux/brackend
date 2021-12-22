import dramatiq
from dramatiq.brokers.redis import RedisBroker
from firebase_admin.auth import create_user, get_user
from sqlalchemy import select
from sqlalchemy.orm import Session

from brackend.db.models import EngineGetter, NotFoundException, Tournament, User
from brackend.tasks.auth import (
    AuthenticationError,
    check_password,
    encode_auth_token,
    generate_verification_email,
)
from brackend.util import BrackendException, send_email

redis_broker = RedisBroker(host="redis")
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def save_new_user_email(username, password, email_address):
    engine = EngineGetter.get_or_create_engine()
    user = create_user(email=email_address)
    with Session(engine) as session:
        new_user = User(
            username=username,
            password=password,
            email=email_address,
            firebase_id=user.uid,
            verified=False,
        )
        session.add(new_user)
        session.commit()

    verification_email = generate_verification_email(email_address)
    subject = "Verify your account for smus bracket"
    send_email(email_address, subject, verification_email)


def login_user(username, password):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine, future=True) as session:
        stmt = select(User).where(User.username == username).limit(2)
        users = session.execute(stmt).scalars().all()

        if not users:
            raise NotFoundException("Found no matching account")
        if len(users) != 1:
            raise BrackendException("Expected exactly one matching user")

        user = users[0]
        is_correct_pass = check_password(user.password, password)
        if not is_correct_pass:
            raise AuthenticationError("Password doesn't match")

        if not user.verified:
            firebase_user = get_user(user.firebase_id)
            if not firebase_user.email_verified:
                raise BrackendException("Must verify your email address")

            user.verified = True
            session.add(user)
            session.commit()

    return encode_auth_token(user.id)


@dramatiq.actor
def save_new_tournament(name):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        session.expire_on_commit = False
        new_tourny = Tournament(name=name)
        session.add(new_tourny)
        session.commit()
        return new_tourny


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


def get_tournament_by_id(id):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        tournament = session\
            .query(Tournament)\
            .filter(Tournament.id == id)\
            .one_or_none()
        return tournament
