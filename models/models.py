
from typing import Annotated, List, Optional

from sqlalchemy import (BigInteger, Boolean, Column, ForeignKey, Integer,
                        Numeric, String, Table, Text)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

id = Annotated[int, mapped_column(
    BigInteger, primary_key=True, autoincrement=True)]
sm_str = Annotated[str, mapped_column(String(20), nullable=False)]
numeric = Annotated[float, mapped_column(Numeric(4, 1), nullable=False)]
numeric_null = Annotated[float, mapped_column(Numeric(4, 1))]
stat = Annotated[int, mapped_column(Integer, nullable=False)]
type_fk = Annotated[BigInteger, mapped_column(ForeignKey('types.id'))]
ability_fk = Annotated[BigInteger, mapped_column(ForeignKey('abilities.id'))]


class Base(DeclarativeBase):
    id: Mapped[id]
    name: ...

    def __str__(self) -> str:
        return f'{self.__class__.__name__}: {self.name}'


breeding_egg_group = Table(
    'breeding_egg_group', Base.metadata,
    Column('breeding_id', BigInteger, ForeignKey(
        'breeding.id'), primary_key=True),
    Column('egg_group_id', BigInteger, ForeignKey(
        'egg_group.id'), primary_key=True)
)

types_poke_group = Table(
    'types_poke_group', Base.metadata,
    Column('id', BigInteger, primary_key=True, index=True, autoincrement=True),
    Column('type_id', BigInteger, ForeignKey('types.id'), primary_key=True, index=True),
    Column('pokemon_id', BigInteger, ForeignKey('pokemons.id'), primary_key=True, index=True)
)


abilities_poke_group = Table(
    'abilities_poke_group', Base.metadata,
    Column('id', BigInteger, primary_key=True, index=True, autoincrement=True),
    Column('ability_id', BigInteger, ForeignKey('abilities.id'), primary_key=True, index=True),
    Column('pokemon_id', BigInteger, ForeignKey('pokemons.id'), primary_key=True, index=True)
)


class Types(Base):
    __tablename__ = 'types'
    name: Mapped[str] = mapped_column(String(20), nullable=False)
    pokemons: Mapped[List['Pokemons']] = relationship(
        'Types', back_populates='types', secondary=types_poke_group)


class Ability(Base):
    __tablename__ = 'abilities'
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    pokemons: Mapped[List['Pokemons']] = relationship(
        'Ability', secondary=abilities_poke_group, back_populates='abilities'
    )
    pokemons_hidden: Mapped[List['Pokemons']] = relationship(
        'Pokemons', foreign_keys='pokemons.hidden_ability_id', back_populates='hidden_ability')


class Pokemons(Base):
    __tablename__ = 'pokemons'
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    national_id: Mapped[int] = mapped_column(
        Integer(), nullable=False, name='National')
    height: Mapped[numeric]
    weight: Mapped[numeric]
    species: Mapped[str] = mapped_column(String(70), nullable=False)
    abilities: Mapped[List['Ability']] = relationship(
        'Pokemons', secondary=abilities_poke_group, back_populates='pokemons'
    )
    hidden_ability_id: Mapped[Optional[ability_fk]]
    hidden_ability: Mapped['Ability'] = relationship(
        'abilities', back_populates='pokemons')
    stats: Mapped['BaseStats'] = relationship(
        'stats', back_populates='pokemons')
    training: Mapped['Training'] = relationship(
        'training', back_populates='pokemons')


class BaseStats(Base):
    __tablename__ = 'base_stats'
    pokemon_id: Mapped[BigInteger] = mapped_column(ForeignKey('pokemons.id'))
    pokemon: Mapped['Pokemons'] = relationship(
        'Pokemons', foreign_keys='pokemons.id', back_populates='stats')
    hp: Mapped[stat]
    attack: Mapped[stat]
    defense: Mapped[stat]
    sp_atk: Mapped[stat]
    sp_def: Mapped[stat]
    speed: Mapped[stat]


class Training(Base):
    __tablename__ = 'training_stats'
    pokemon_id: Mapped[BigInteger] = mapped_column(ForeignKey('pokemons.id'))
    pokemon: Mapped['Pokemons'] = relationship(
        'Pokemons', foreign_keys='pokemons.id', back_populates='stats')
    base_exp: Mapped[Integer] = mapped_column(Integer, nullable=False)
    cath_rate: Mapped[numeric]
    friend_cat_id: Mapped[BigInteger] = mapped_column(
        ForeignKey('friendship_category.id'))
    friend_cat: Mapped['CategoryFriendship'] = relationship(
        'friendship_category', back_populates='pokemons.training')
    growth_rate_id: Mapped[BigInteger] = mapped_column(
        ForeignKey('growth_rate_category.id'))
    growth_rate: Mapped['GrowthRate'] = relationship(
        'growth_rate_category', back_populates='pokemons.training')


class CategoryFriendship(Base):
    __tablename__ = 'friendship_categories'
    name: Mapped[sm_str]


class GrowthRate(Base):
    __tablename__ = 'growth_rate_categories'
    name: Mapped[sm_str]


class PokemonGame(Base):
    __tablename__ = 'pokemon_games'
    name: Mapped[sm_str]


class PokedexEntry(Base):
    __tablename__ = 'pokedex_entries'
    pokemon_id: Mapped[BigInteger] = mapped_column(ForeignKey('pokemons.id'))
    pokemon_game_id: Mapped[BigInteger] = mapped_column(
        ForeignKey('pokemon_game.id'))
    description: Mapped[str] = mapped_column(Text, nullable=False)


class Breeding(Base):
    __tablename__ = 'breeding_stats'
    pokemon_id: Mapped[BigInteger] = mapped_column(ForeignKey('pokemons.id'))
    egg_groups: Mapped[List['EggGroup']] = relationship(
        'EggGroup', back_populates='breeding', secondary=breeding_egg_group)
    genderless: Mapped[bool] = mapped_column(Boolean, default=False)
    male: Mapped[Optional[numeric_null]]
    female: Mapped[Optional[numeric_null]]


class EggGroup(Base):
    __tablename__ = 'egg_groups'
    name: Mapped[sm_str]
    breeding: Mapped[List['Breeding']] = relationship(
        'Breeding', secondary=breeding_egg_group, back_populates='egg_group')
    

# class PokemonType(Base):

