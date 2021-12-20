"""Module that defines/creates/holds ORMs for the database."""
from brackend.util import BrackendException
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


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

    def __repr__(self):
        return f"User(id={self.id}, username={self.username})"


class Tournament(Base):
    """Tournament table."""

    __tablename__ = "tournaments"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    users = relationship("User", secondary="user_tournaments", back_populates="tournaments")

    def __repr__(self):
        return f"Tournament(id={self.id}, name={self.name})"


class UserTournament(Base):
    """Join table to keep track of which tournaments a user has and vice versa."""

    __tablename__ = "user_tournaments"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    tournament_id = Column(Integer, ForeignKey("tournaments.id"))


class EngineGetter:
    """Thing to get the engine."""

    _engine = None

    @classmethod
    def get_or_create_engine(cls):
        """Get a sql connection engine or return the extant one."""
        if cls._engine is None:
            cls._engine = create_engine(
                "postgresql://postgres:postgres@db/brackend", echo=True, future=True
            )
        return cls._engine


def clear_models():
    engine = EngineGetter.get_or_create_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_models()
