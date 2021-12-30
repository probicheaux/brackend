from abc import ABC
from sqlalchemy.orm import Session
from brackend.db.models import (
    EngineGetter,
    Tournament,
)


class TournamentRepository(ABC):
    engine = EngineGetter.get_or_create_engine()

    @classmethod
    def search_by_name(cls, name, count=20):
        with Session(cls.engine) as session:
            search = "%{}%".format(name)
            results = session.query(Tournament)\
                .filter(Tournament.name.like(search))\
                .limit(count)\
                .all()
            return results


