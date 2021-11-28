import dramatiq
import yagmail
from dramatiq.brokers.redis import RedisBroker
from sqlalchemy import select
from sqlalchemy.orm import Session

from brackend.db.models import EngineGetter, NotFoundException, Tournament, User
from brackend.tasks.auth import (
    AuthenticationError,
    check_password,
    create_user_firebase,
    encode_auth_token,
    generate_verification_email,
)
from brackend.util import BrackendException, send_email

redis_broker = RedisBroker(host="redis")
dramatiq.set_broker(redis_broker)


@dramatiq.actor
def save_new_user_email(username, password, email_address):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        new_user = User(
            username=username, password=password, email=email_address, verified=False
        )
        session.add(new_user)
        session.commit()

    create_user_firebase(email_address)
    verification_email = generate_verification_email(email_address)
    subject = "Verify your account for smus bracket"
    send_email(email_address, subject, verification_email)


def login_user(username, password):
    engine = EngineGetter.get_or_create_engine()
    with Session(engine) as session:
        stmt = select(User).where(User.username == username).limit(2)
        users = session.query()session.execute(stmt).all()

    if not users:
        raise NotFoundException("Found no matching account")
    if len(users) != 1:
        raise BrackendException("Expected exactly one matching user")

    user = users[0]

    is_correct_pass = check_password(user.password, password)
    if not is_correct_pass:
        raise AuthenticationError("Password doesn't match")

    return encode_auth_token(user.id)


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
