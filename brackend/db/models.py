"""Module that defines/creates/holds ORMs for the database."""
import enum
from datetime import datetime

from brackend.util import DOCKER_POSTGRES_URL, BrackendException
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, create_engine
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class MatchProgress(enum.Enum):
    not_started = enum.auto()
    in_progress = enum.auto()
    completed = enum.auto()


class UserRole(enum.Enum):
    player = enum.auto()
    spectator = enum.auto()
    organizer = enum.auto()


class NotFoundException(BrackendException):
    pass


class User(Base):
    """User table."""

    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    verified = Column(Boolean, default=False)
    tournaments = relationship("Tournament", secondary="user_tournaments", back_populates="users")
    firebase_id = Column(String(255), nullable=False)
    admin = Column(Boolean, default=False)

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"


class Tournament(Base):
    """Tournament table."""

    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    date = Column(DateTime, default=datetime.now)
    users = relationship("User", secondary="user_tournaments", backref="tournaments")
    brackets = relationship("Bracket", backref="tournaments")

    def __repr__(self):
        return f"Tournament(id={self.id}, name={self.name})"


class UserTournament(Base):
    """Join table to keep track of which tournaments a user has and vice versa."""

    __tablename__ = "user_tournaments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))
    role = Column(ENUM(UserRole), nullable=False)


class Bracket(Base):
    """Table representing a bracket."""

    __tablename__ = "brackets"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    tournament = Column(Integer, ForeignKey("tournaments.id"))
    rounds = relationship("Round", backref="brackets")


class Round(Base):
    __tablename__ = "rounds"
    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(255), nullable=False)
    bracket = Column(Integer, ForeignKey("tournaments.id"))
    matches = relationship("Match", backref="rounds")


class Match(Base):
    __tablename__ = "matches"
    id = Column(Integer, primary_key=True)
    round = Column(Integer, ForeignKey("rounds.id"))
    round_position = Column(Integer)
    progress = Column(Enum(MatchProgress), nullable=False)
    players = relationship("User", secondary="match_users", backref="matches")


class MatchUsers(Base):
    __tablename__ = "match_users"
    id = Column(Integer, primary_key=True)
    match = Column(Integer, ForeignKey("matches.id"))
    user = Column(Integer, ForeignKey("users.id"))
    score = Column(Integer)


class EngineGetter:
    """Thing to get the engine."""

    _engine = None

    @classmethod
    def get_or_create_engine(cls):
        """Get a sql connection engine or return the extant one."""
        if cls._engine is None:
            cls._engine = create_engine(DOCKER_POSTGRES_URL, echo=True, future=True)
        return cls._engine


def clear_models():
    engine = EngineGetter.get_or_create_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
