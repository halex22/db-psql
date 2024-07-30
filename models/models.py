
from typing import Annotated, List, Optional

from sqlalchemy import BigInteger, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

id = Annotated[int, mapped_column(
    BigInteger, primary_key=True, autoincrement=True)]
numeric = Annotated[float, mapped_column(Numeric(4, 1), nullable=False)]
stat = Annotated[int, mapped_column(Integer, nullable=False)]
# _type = Annotated['Types',  relationship('Types', back_populates='pokemons')]
type_fk = Annotated[BigInteger, mapped_column(ForeignKey('Types.id'))]
# _ability = Annotated[Optional['Ability'], relationship('Ability', back_populates='pokemons')]
ability_fk = Annotated[BigInteger, mapped_column(ForeignKey('Ability.id'))]
_type = Annotated['Types', 'Mapped[Types]']
_ability = Annotated['Ability', 'Mapped[Ability]']


class Base(DeclarativeBase):
    id: Mapped[id]
    name: ...

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.name}'


class Types(Base):
    __tablename__ = 'types'
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    pokemons: Mapped[List['Pokemons']] = relationship(
        'Pokemons', foreign_keys='Pokemons.main_type_id', back_populates='main_type')
    pokemons_second: Mapped[List['Pokemons']] = relationship(
        'Pokemons', foreign_keys='Pokemons.second_type_id', back_populates='second_type')


class Ability(Base):
    __tablename__ = 'abilities'
    name: Mapped[str] = mapped_column(String(50))
    pokemons: Mapped[List['Pokemons']] = relationship(
        'Pokemons', foreign_keys='Pokemons.ability_id', back_populates='ability')


class Pokemons(Base):
    __tablename__ = 'pokemons'
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    national_id: Mapped[int] = mapped_column(
        Integer(), nullable=False, name='National')
    height: Mapped[numeric]
    weight: Mapped[numeric]
    species: Mapped[str] = mapped_column(String(70), nullable=False)
    main_type_id: Mapped[type_fk]
    main_type: Mapped[_type] = relationship('Types', back_populates='pokemons')
    second_type_id: Mapped[type_fk]
    second_type: Mapped[_type] = relationship('Types', back_populates='pokemons')
    ability_id: Mapped[ability_fk]
    ability: Mapped[_ability] = relationship('Ability', back_populates='pokemons')
    hidden_ability_id: Mapped[Optional[ability_fk]]
    hidden_ability: Mapped[_ability] = relationship('Ability', back_populates='pokemons')


class BaseStats(Base):
    __tablename__ = 'stats'
    hp: Mapped[stat]
    attack: Mapped[stat]
    defense: Mapped[stat]
    sp_atk: Mapped[stat]
    sp_def: Mapped[stat]
    speed: Mapped[stat]
