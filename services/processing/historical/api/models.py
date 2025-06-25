from typing import List, Optional
from sqlalchemy import ForeignKey, DateTime, String, Numeric, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .db import Base


class Meeting(Base):
    __tablename__ = 'meeting'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int]
    name: Mapped[str]
    official_name: Mapped[str]
    start_date: Mapped[DateTime]
    utc_offset: Mapped[str] = mapped_column(Interval)

    # Many-to-one rel with circuit as parent
    circuit_id: Mapped[int] = mapped_column(ForeignKey(column='circuit.id'))
    circuit: Mapped['Circuit'] = relationship(back_populates="meetings")

    sessions: Mapped[List['Session']] = relationship(
        back_populates='meeting', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Meeting(id={self.id!r}, year={self.year!r}, name={self.name!r}, official_name={self.official_name!r}, start_date={self.start_date}, utc_offset={self.utc_offset!r}, circuit_id={self.circuit_id!r})"
    

class Circuit(Base):
    __tablename__ = 'circuit'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
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
        return f"Circuit(id={self.id!r}, name={self.name!r}, country_key={self.country_key!r}, country_code={self.country_code}, country_name={self.country_name!r}, location={self.location!r})"
    

class Turn(Base):
    __tablename__ = 'turn'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    number: Mapped[int]
    angle: Mapped[Numeric] = mapped_column(Numeric(precision=18, scale=15))
    length: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=15))
    x: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=15))
    y: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=15))

    # Weak rel with circuit as owner
    circuit_id: Mapped[int] = mapped_column(ForeignKey(column='circuit.id'), primary_key=True)
    circuit: Mapped['Circuit'] = relationship(back_populates="turns")

    def __repr__(self) -> str:
        return f"Turn(id={self.id!r}, number={self.number!r}, angle={self.angle!r}, length={self.length}, x={self.x!r}, location={self.y!r}, circuit_id={self.circuit_id!r})"


class Session(Base):
    __tablename__ = 'session'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int]
    name: Mapped[str]
    type: Mapped[str]
    start_date: Mapped[DateTime]
    end_date: Mapped[DateTime]
    utc_offset: Mapped[Interval]

    # Many-to-one rel with meeting as parent
    meeting_id: Mapped[int] = mapped_column(ForeignKey(column='meeting.id'))
    meeting: Mapped['Meeting'] = relationship(back_populates='sessions')

    events: Mapped[List['Event']] = relationship(
        back_populates='session', cascade='all, delete-orphan'
    )

    locations: Mapped[List['Location']] = relationship(
        back_populates='session', cascade='all, delete-orphan'
    )

    pits: Mapped[List['Pit']] = relationship(
        back_populates='session', cascade='all, delete-orphan'
    )

    race_controls: Mapped[List['RaceControl']] = relationship(
        back_populates='session', cascade='all, delete-orphan'
    )

    drivers: Mapped[List['Driver']] = relationship(
        back_populates='session', cascade='all, delete-orphan'
    )

    teams: Mapped[List['Team']] = relationship(
        back_populates='session', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Session(id={self.id!r}, year={self.year!r}, name={self.name!r}, type={self.type!r}, start_date={self.start_date}, end_date={self.end_date}, utc_offset={self.utc_offset!r}, meeting_id={self.meeting_id!r}"


class Team(Base):
    __tablename__ = 'team'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    color: Mapped[str] = mapped_column(String(length=6))

    # Many-to-one rel with session as parent
    session_id: Mapped[int] = mapped_column(ForeignKey(column='session.id'))
    session: Mapped['Session'] = relationship(back_populates='teams')

    drivers: Mapped[List['Driver']] = relationship(
        back_populates='team', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Team(id={self.id!r}, name={self.name!r}, color={self.color!r}, session_id={self.session_id!r}"


class Event(Base):
    __tablename__ = 'event'

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
    location_id: Mapped[Optional[int]] = mapped_column(ForeignKey(column='location.id'))
    location: Mapped[Optional['Location']] = relationship(back_populates='event', cascade='all')

    # One-to-one rel with pit
    pit_id: Mapped[Optional[int]] = mapped_column(ForeignKey(column='pit.id'))
    pit: Mapped[Optional['Pit']] = relationship(back_populates='event', cascade='all')

    # One-to-one rel with race control
    race_control_id: Mapped[Optional[int]] = mapped_column(ForeignKey(column='race_control.id'))
    race_control: Mapped[Optional['RaceControl']] = relationship(back_populates='event', cascade='all-orphan')

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


class Driver(Base):
    __tablename__ = 'driver'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    driver_number: Mapped[int]
    acronym: Mapped[str] = mapped_column(String(length=3))
    first_name: Mapped[str]
    last_name: Mapped[str]
    full_name: Mapped[str]
    broadcast_name: Mapped[str]
    image_url: Mapped[str]
    country_code: Mapped[str]

    # Many-to-one rel with session as parent
    session_id: Mapped[int] = mapped_column(ForeignKey(column='session.id'))
    session: Mapped['Session'] = relationship(back_populates='drivers')

    # Many-to-one rel with team as parent
    team_id: Mapped[int] = mapped_column(ForeignKey(column='team.id'))
    team: Mapped['Location'] = relationship(back_populates='drivers')

    # Many-to-many rel with event
    events: Mapped[Optional[List['Event']]] = relationship(back_populates='driver', cascade='all, delete-orphan')

    locations: Mapped[List['Location']] = relationship(
        back_populates='driver', cascade='all, delete-orphan'
    )

    pits: Mapped[List['Pit']] = relationship(
        back_populates='driver', cascade='all, delete-orphan'
    )

    race_controls: Mapped[List['RaceControl']] = relationship(
        back_populates='driver', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Driver(id={self.id!r}, driver_number={self.driver_number!r}, acronym={self.acronym!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, full_name={self.full_name!r}, broadcast_name={self.broadcast_name!r}, headshot_url={self.headshot_url!r}, country_code={self.country_code!r}"


class Location(Base):
    __tablename__ = 'location'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[DateTime]
    x: Mapped[int]
    y: Mapped[int]
    z: Mapped[int]

    # Many-to-one rel with session as parent
    session_id: Mapped[int] = mapped_column(ForeignKey(column='session.id'))
    session: Mapped['Session'] = relationship(back_populates='locations')

    # Many-to-one rel with driver as parent
    driver_id: Mapped[int] = mapped_column(ForeignKey(column='driver.id'))
    driver: Mapped['Driver'] = relationship(back_populates='locations')
    
    # One-to-one rel with event
    event: Mapped[Optional['Event']] = relationship(back_populates='location', cascade='all')
    
    def __repr__(self) -> str:
        return f"Location(id={self.id!r}, date={self.date!r}, x={self.x!r}, y={self.y!r}, z={self.z!r}, session_id={self.session_id!r}, driver_id={self.driver_id!r}"
    

class Pit(Base):
    __tablename__ = 'pit'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[str]
    pit_duration: Mapped[Numeric] = mapped_column(Numeric(precision=6, scale=1)) # Max pit duration should be in the hours

    # Many-to-one rel with session as parent
    session_id: Mapped[int] = mapped_column(ForeignKey(column='session.id'))
    session: Mapped['Session'] = relationship(back_populates='pits')

    # Many-to-one rel with driver as parent
    driver_id: Mapped[int] = mapped_column(ForeignKey(column='driver.id'))
    driver: Mapped['Driver'] = relationship(back_populates='pits')
    
    # One-to-one rel with event
    event: Mapped[Optional['Event']] = relationship(back_populates='pit', cascade='all')
    
    def __repr__(self) -> str:
        return f"Pit(id={self.id!r}, date={self.date!r}, pit_duration={self.pit_duration!r}, session_id={self.session_id!r}, driver_id={self.driver_id!r}"
    

class RaceControl(Base):
    __tablename__ = 'race_control'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[str]
    message: Mapped[str]

    # Many-to-one rel with session as parent
    session_id: Mapped[int] = mapped_column(ForeignKey(column='session.id'))
    session: Mapped['Session'] = relationship(back_populates='race_controls')

    # Many-to-one rel with driver as parent
    driver_id: Mapped[int] = mapped_column(ForeignKey(column='driver.id'))
    driver: Mapped['Driver'] = relationship(back_populates='race_controls')
    
    # One-to-one rel with event
    event: Mapped[Optional['Event']] = relationship(back_populates='race_control', cascade='all')
    
    def __repr__(self) -> str:
        return f"RaceControl(id={self.id!r}, date={self.date!r}, message={self.message!r}"

