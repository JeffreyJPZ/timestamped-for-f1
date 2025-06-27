from typing import List, Optional
from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint, DateTime, String, Numeric, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base


meeting_team_participation_table = Table(
    'meeting_team_participation',
    Base.metadata,
    Column('meeting_id', ForeignKey('meeting.id'), primary_key=True),
    Column('team_id', ForeignKey('team.id'), primary_key=True)
)


session_team_participation_table = Table(
    'session_team_participation',
    Base.metadata,
    Column('session_id', ForeignKey('session.id'), primary_key=True),
    Column('team_id', ForeignKey('team.id'), primary_key=True)
)


meeting_driver_participation_table = Table(
    'meeting_driver_participation',
    Base.metadata,
    Column('meeting_id', ForeignKey('meeting.id'), primary_key=True),
    Column('driver_id', ForeignKey('driver.id'), primary_key=True)
)


session_driver_participation_table = Table(
    'session_driver_participation',
    Base.metadata,
    Column('session_id', ForeignKey('session.id'), primary_key=True),
    Column('driver_id', ForeignKey('driver.id'), primary_key=True)
)


team_driver_participation_table = Table(
    'team_driver_participation',
    Base.metadata,
    Column('team_id', ForeignKey('team.id'), primary_key=True),
    Column('driver_id', ForeignKey('driver.id'), primary_key=True)
)


class Circuit(Base):
    __tablename__ = 'circuit'
    __table_args__ = (
        UniqueConstraint('year', 'name', name='uq_circuit_year_and_name')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int]
    name: Mapped[str]
    country_code: Mapped[str]
    country_name: Mapped[str]
    location: Mapped[str]
    rotation: Mapped[int]
    
    meetings: Mapped[List['Meeting']] = relationship(
        back_populates='circuit', cascade='all, delete-orphan'
    )

    turns: Mapped[List['Turn']] = relationship(
        back_populates='circuit', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Circuit(id={self.id!r}, year={self.year!r}, name={self.name!r}, country_code={self.country_code}, country_name={self.country_name!r}, location={self.location!r}, rotation={self.rotation!r})"
    

class Turn(Base):
    __tablename__ = 'turn'
    __table_args__ = (
        UniqueConstraint('circuit_id', 'number', name='uq_turn_circuit_id_and_number')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[int]
    angle: Mapped[Numeric] = mapped_column(Numeric(precision=18, scale=15))
    length: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=15))
    x: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=15))
    y: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=15))

    # Many-to-one weak rel with circuit as owner
    circuit_id: Mapped[int] = mapped_column(ForeignKey(column='circuit.id'), primary_key=True)
    circuit: Mapped['Circuit'] = relationship(back_populates='turns')

    def __repr__(self) -> str:
        return f"Turn(id={self.id!r}, number={self.number!r}, angle={self.angle!r}, length={self.length}, x={self.x!r}, location={self.y!r}, circuit_id={self.circuit_id!r})"


class Meeting(Base):
    __tablename__ = 'meeting'
    __table_args__ = (
        UniqueConstraint('year', 'name', name='uq_meeting_year_and_name')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int]
    name: Mapped[str]
    official_name: Mapped[str]
    start_date: Mapped[DateTime]
    utc_offset: Mapped[str] = mapped_column(Interval)

    # Many-to-one rel with circuit as parent
    circuit_id: Mapped[int] = mapped_column(ForeignKey(column='circuit.id'))
    circuit: Mapped['Circuit'] = relationship(back_populates='meetings')

    sessions: Mapped[List['Session']] = relationship(
        back_populates='meeting', cascade='all, delete-orphan'
    )

    teams: Mapped[List['Team']] = relationship(
        secondary=meeting_team_participation_table, back_populates='meetings', cascade='all, delete-orphan'
    )

    drivers: Mapped[List['Driver']] = relationship(
        secondary=meeting_driver_participation_table, back_populates='meetings', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Meeting(id={self.id!r}, year={self.year!r}, name={self.name!r}, official_name={self.official_name!r}, start_date={self.start_date}, utc_offset={self.utc_offset!r}, circuit_id={self.circuit_id!r})"


class Session(Base):
    __tablename__ = 'session'
    __table_args__ = (
        UniqueConstraint('meeting_id', 'name', name='uq_session_meeting_id_and_name')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    type: Mapped[str]
    start_date: Mapped[DateTime]
    end_date: Mapped[DateTime]
    utc_offset: Mapped[Interval]

    # Weak rel with meeting as parent
    meeting_id: Mapped[int] = mapped_column(ForeignKey(column='meeting.id'), primary_key=True)
    meeting: Mapped['Meeting'] = relationship(back_populates='sessions')

    events: Mapped[List['Event']] = relationship(
        back_populates='session', cascade='all, delete-orphan'
    )

    teams: Mapped[List['Team']] = relationship(
        secondary=session_team_participation_table, back_populates='sessions', cascade='all, delete-orphan'
    )

    drivers: Mapped[List['Driver']] = relationship(
        secondary=session_driver_participation_table, back_populates='sessions', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Session(id={self.id!r}, name={self.name!r}, type={self.type!r}, start_date={self.start_date}, end_date={self.end_date}, utc_offset={self.utc_offset!r}, meeting_id={self.meeting_id!r}"


class Team(Base):
    __tablename__ = 'team'
    __table_args__ = (
        UniqueConstraint('year', 'name', name='uq_team_year_and_name')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int]
    name: Mapped[str]
    color: Mapped[str] = mapped_column(String(length=6))

    meetings: Mapped[List['Meeting']] = relationship(
        secondary=meeting_team_participation_table, back_populates='teams', cascade='all, delete-orphan'
    )

    sessions: Mapped[List['Session']] = relationship(
        secondary=meeting_team_participation_table, back_populates='teams', cascade='all, delete-orphan'
    )

    drivers: Mapped[List['Driver']] = relationship(
        secondary=team_driver_participation_table, back_populates='teams', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Team(id={self.id!r}, year={self.year!r}, name={self.name!r}, color={self.color!r}"


class Driver(Base):
    __tablename__ = 'driver'
    __table_args__ = (
        UniqueConstraint('year', 'driver_number', name='uq_driver_year_and_driver_number')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int]
    driver_number: Mapped[int]
    acronym: Mapped[str] = mapped_column(String(length=3))
    first_name: Mapped[str]
    last_name: Mapped[str]
    full_name: Mapped[str]
    broadcast_name: Mapped[str]
    image_url: Mapped[str]
    country_code: Mapped[str]

    meetings: Mapped[List['Meeting']] = relationship(
        secondary=meeting_team_participation_table, back_populates='drivers', cascade='all, delete-orphan'
    )

    sessions: Mapped[List['Session']] = relationship(
        secondary=meeting_team_participation_table, back_populates='drivers', cascade='all, delete-orphan'
    )

    teams: Mapped[List['Team']] = relationship(
        secondary=team_driver_participation_table, back_populates='drivers', cascade='all, delete-orphan'
    )

    events: Mapped[Optional[List['Event']]] = relationship(back_populates='driver', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"Driver(id={self.id!r}, year={self.year!r}, driver_number={self.driver_number!r}, acronym={self.acronym!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, full_name={self.full_name!r}, broadcast_name={self.broadcast_name!r}, image_url={self.image_url!r}, country_code={self.country_code!r}"


class Event(Base):
    __tablename__ = 'event'
    __table_args__ = (
        UniqueConstraint('session_id', 'date', name='uq_event_session_id_and_date')
    )
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[DateTime]
    elapsed_time: Mapped[Interval]
    lap_number: Mapped[Optional[int]]
    category: Mapped[str]
    cause: Mapped[str]

    # Many-to-one rel with session as parent
    session_id: Mapped[int] = mapped_column(ForeignKey(column='session.id'))
    session: Mapped['Session'] = relationship(back_populates='events')

    # One-to-one rel with location
    location: Mapped[Optional['Location']] = relationship(back_populates='event', cascade='all, delete-orphan')

    # One-to-one rel with pit
    pit: Mapped[Optional['Pit']] = relationship(back_populates='event', cascade='all, delete-orphan')

    # One-to-one rel with race control
    race_control: Mapped[Optional['RaceControl']] = relationship(back_populates='event', cascade='all, delete-orphan')

    # Many-to-many rel with driver
    drivers: Mapped[Optional[List['Driver']]] = relationship(back_populates='event', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"Event(id={self.id!r}, date={self.date!r}, elapsed_time={self.elapsed_time!r})"
    

class EventDriverParticipation(Base):
    __tablename__ = 'event_driver_participation'

    event_id: Mapped[int] = mapped_column(ForeignKey(column='event.id'), primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey(column='driver.id'), primary_key=True)
    role: Mapped[str] # One of: 'initiator' or 'participant'

    event: Mapped['Event'] = relationship(back_populates='drivers', cascade='all, delete-orphan')
    driver: Mapped['Driver'] = relationship(back_populates='events', cascade='all, delete-orphan')


class Location(Base):
    __tablename__ = 'location'
    __table_args__ = (
        UniqueConstraint('event_id', name='uq_race_control_event_id')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[DateTime]
    x: Mapped[int]
    y: Mapped[int]
    z: Mapped[int]
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey(column='event.id'), primary_key=True)
    event: Mapped['Event'] = relationship(back_populates='location', cascade='all, delete-orphan', single_parent=True)
    
    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, date={self.date!r}, x={self.x!r}, y={self.y!r}, z={self.z!r}"
    

class Pit(Base):
    __tablename__ = 'pit'
    __table_args__ = (
        UniqueConstraint('event_id', name='uq_race_control_event_id')
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[str]
    pit_duration: Mapped[Numeric] = mapped_column(Numeric(precision=6, scale=1)) # Max pit duration should be in the hours
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey(column='event.id'), primary_key=True)
    event: Mapped['Event'] = relationship(back_populates='pit', cascade='all, delete-orphan', single_parent=True)
    
    def __repr__(self) -> str:
        return f"Pit(id={self.id!r}, date={self.date!r}, pit_duration={self.pit_duration!r}"
    

class RaceControl(Base):
    __tablename__ = 'race_control'
    __table_args__ = (
        UniqueConstraint('event_id', name='uq_race_control_event_id'),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[str]
    message: Mapped[str]
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey(column='event.id'), primary_key=True)
    event: Mapped['Event'] = relationship(back_populates='race_control', cascade='all, delete-orphan', single_parent=True)
    
    def __repr__(self) -> str:
        return f"RaceControl(id={self.id!r}, date={self.date!r}, message={self.message!r}"