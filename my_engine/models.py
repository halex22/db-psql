from typing import Annotated, Optional

from engine import engine
from sqlalchemy import Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

id = Annotated[int, mapped_column(Integer, primary_key=True, autoincrement=True)]
numeric = Annotated[float, mapped_column(Numeric(4, 1), nullable=False)]
stat = Annotated[int, mapped_column(Integer, nullable=False)]


class Base(DeclarativeBase):
    id: Mapped[id] 
    name: ...

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.name}'


class Pokemon(Base):
    __tablename__ = 'pokemon'
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    national_id: Mapped[int] = mapped_column(Integer(), nullable=False, name='National')
    height: Mapped[numeric]
    weight: Mapped[numeric]
    species: Mapped[str] = mapped_column(String(70), nullable=False)
    main_type: Mapped['Types'] = relationship('Types', back_populates='pokemon')
    second_type: Mapped[Optional['Types']] = relationship('Types', back_populates='pokemon')


class Types(Base):
    __tablename__ = 'pokemons_types'
    name: Mapped[str] = mapped_column(String(20), nullable=False)


class Ability(Base):
    __tablename__ = 'pokemons_abilities'
    name: Mapped[str] = mapped_column(String(50))


class BaseStats(Base):
    __tablename__ = 'stats'
    id: Mapped[id]
    hp: Mapped[stat]
    attack: Mapped[stat]
    defense: Mapped[stat]
    sp_atk: Mapped[stat]
    sp_def: Mapped[stat]
    speed: Mapped[stat]


if __name__ == '__main__':
    Base.metadata.create_all(engine)
