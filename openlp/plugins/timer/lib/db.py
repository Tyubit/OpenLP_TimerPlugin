"""
The :mod:`db` module provides the database and schema that is the backend for the Timer plugin.
"""
from sqlalchemy.orm import declarative_base,sessionmaker
from sqlalchemy import Column, types
from sqlalchemy.types import Integer, Unicode, UnicodeText ,Boolean,Time


from openlp.core.db.helpers import init_db
from openlp.core.common.i18n import get_locale_key, get_natural_key

Base = declarative_base()


class TimerSlide(Base):
    """
    TimerSlide model
    """

    __tablename__ = 'timer_slide'

    id = Column(Integer, primary_key=True)
    title = Column(types.Unicode(255), nullable=False)
    text = Column(types.Unicode(255))
    timer_duration = Column(Integer)
    timer_use_timer = Column(Boolean)
    timer_use_specific_time = Column(Boolean)
    theme_name = Column(Unicode(128))

    # By default sort the timers by its title considering language specific characters.
    def __lt__(self, other):
        return get_natural_key(self.title) < get_natural_key(other.title)

    def __eq__(self, other):
        return get_natural_key(self.title) == get_natural_key(other.title)

    def __hash__(self):
        """
        Return the hash for a timer slide.
        """
        return self.id


def init_schema(url):
    """
    Setup the timer database connection and initialise the database schema

    :param url:  The database to setup
    """
    session, metadata = init_db(url, base=Base)
    metadata.create_all(bind=metadata.bind, checkfirst=True)
    return session