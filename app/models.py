from datetime import datetime
from typing import List
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import DeclarativeBase

from sqlalchemy import Column
from sqlalchemy import Table
from sqlalchemy import ForeignKey
from sqlalchemy import Integer



class Base(DeclarativeBase):
    pass



class Game(Base):
    __tablename__ = 'games'

    id: Mapped[int] = mapped_column(primary_key=True)
    appid: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column()
    release_date: Mapped[datetime] = mapped_column()
    required_age: Mapped[int] = mapped_column()
    price: Mapped[float] = mapped_column()
    dlc_count: Mapped[int] = mapped_column()
    about_the_game: Mapped[str] = mapped_column()
    windows: Mapped[bool] = mapped_column() 
    mac: Mapped[bool] = mapped_column()
    linux: Mapped[bool] = mapped_column()
    positive: Mapped[int] = mapped_column()
    negative: Mapped[int] = mapped_column()
    score_rank: Mapped[int] = mapped_column()
    developers: Mapped[str] = mapped_column()
    publishers: Mapped[str] = mapped_column()

    supported_languages: Mapped[List['SupportedLanguages']] = relationship(back_populates='games', secondary='games_supported_languages')
    categories: Mapped[List['Categories']] = relationship(back_populates='games', secondary='games_categories')
    genres: Mapped[List['Genres']] = relationship(back_populates='games', secondary='games_genres')
    tags: Mapped[List['Tags']] = relationship(back_populates='games', secondary='games_tags')



class SupportedLanguages(Base):
    __tablename__ = 'supported_languages'

    id: Mapped[int] = mapped_column(primary_key=True)
    supported_language: Mapped[str] = mapped_column(nullable=True)

    games: Mapped[List[Game]] = relationship(back_populates='supported_languages', secondary='games_supported_languages')



class Categories(Base):
    __tablename__ = 'categories'

    id: Mapped[int] = mapped_column(primary_key=True)
    category: Mapped[str] = mapped_column(nullable=True)

    games: Mapped[List[Game]] = relationship(back_populates='categories', secondary='games_categories')



class Genres(Base):
    __tablename__ = 'genres'

    id: Mapped[int] = mapped_column(primary_key=True)
    genre: Mapped[str] = mapped_column(nullable=True)

    games: Mapped[List[Game]] = relationship(back_populates='genres', secondary='games_genres')



class Tags(Base):
    __tablename__ = 'tags'

    id: Mapped[int] = mapped_column(primary_key=True)
    tag: Mapped[str] = mapped_column(nullable=True)

    games: Mapped[List[Game]] = relationship(back_populates='tags', secondary='games_tags')



games_supported_languages = Table(
    'games_supported_languages',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('supported_language_id', Integer, ForeignKey('supported_languages.id'))
)



games_categories = Table(
    'games_categories',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('category_id', Integer, ForeignKey('categories.id'))
)



games_genres = Table(
    'games_genres',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('genre_id', Integer, ForeignKey('genres.id'))
)



games_tags = Table(
    'games_tags',
    Base.metadata,
    Column('game_id', Integer, ForeignKey('games.id')),
    Column('tag_id', Integer, ForeignKey('tags.id'))
)
