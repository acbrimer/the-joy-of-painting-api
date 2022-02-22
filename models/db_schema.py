from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, CHAR, Integer, Date, ForeignKey, Table, create_mock_engine
import os
from .base import Base

# Define dimension tables


class Episode(Base):
    """Episode - an episode of The Joy of Painting"""

    __tablename__ = 'episodes'

    id = Column(CHAR(6), primary_key=True)
    season = Column(Integer, nullable=False)
    episode = Column(Integer, nullable=False)
    title = Column(String(255), nullable=False)
    painting_title = Column(String(255), nullable=True)
    painting_index = Column(Integer, nullable=False)
    image_url = Column(String, nullable=True)
    youtube_url = Column(String, nullable=True)
    air_date = Column(Date, nullable=True)


class Color(Base):
    """Color - a color used by Bob Ross in a painting """
    __tablename__ = 'colors'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    hex = Column(String(7), nullable=False)


class Subject(Base):
    """Subject - lookup table for episode subjects"""
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


episode_subjects = Table('episode_subjects', Base.metadata,
                         Column('episode_id', ForeignKey(
                             'episodes.id'), primary_key=True),
                         Column('subject_id', ForeignKey(
                             'subjects.id'), primary_key=True),

                         )

painting_colors = Table('painting_colors', Base.metadata,
                        Column('episode_id', ForeignKey(
                            'episodes.id'), primary_key=True),
                        Column('color_id', ForeignKey('colors.id'), primary_key=True))


def dump(sql, *multiparams, **params):
    print(sql.compile(dialect=engine.dialect))


if __name__ == '__main__':
    DB_PROVIDER = os.environ.get('DB_PROVIDER', 'sqlite')
    engine = create_mock_engine(f'{DB_PROVIDER}://', dump)
    Base.metadata.create_all(engine, checkfirst=False)
