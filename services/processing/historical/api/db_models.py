from sqlalchemy import Table, Column, ForeignKey, UniqueConstraint, ForeignKeyConstraint, DateTime, String, Numeric, Interval
from sqlalchemy.orm import Mapped, mapped_column, relationship
from db import Base


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


class Country(Base):
    __tablename__ = 'country'
    __table_args__ = (
        UniqueConstraint(
            columns=('year', 'name'),
            name='uq_circuit_year_and_name'
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(3), unique=True)
    name: Mapped[str | None] = mapped_column(unique=True) # Driver data only comes with country code

    circuits: Mapped[list['Circuit']] = relationship(
        back_populates='country', cascade='all, delete-orphan'
    )

    drivers: Mapped[list['Driver']] = relationship(
        back_populates='country', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Country(id={self.id!r}, code={self.code!r}, name={self.name!r}"


class Circuit(Base):
    __tablename__ = 'circuit'
    __table_args__ = (
        UniqueConstraint(
            columns=('year', 'name'),
            name='uq_circuit_year_and_name'
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int]
    name: Mapped[str]
    location: Mapped[str]
    rotation: Mapped[int]

    # Many-to-one rel with country as parent
    country_id: Mapped[int] = mapped_column(ForeignKey(column='country.id'))
    country: Mapped['Country'] = relationship(back_populates='circuits')
    
    meetings: Mapped[list['Meeting']] = relationship(
        back_populates='circuit', cascade='all, delete-orphan'
    )

    turns: Mapped[list['Turn']] = relationship(
        back_populates='circuit', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Circuit(id={self.id!r}, year={self.year!r}, name={self.name!r}, country_code={self.country_code}, country_name={self.country_name!r}, location={self.location!r}, rotation={self.rotation!r})"
    

class Turn(Base):
    __tablename__ = 'turn'

    number: Mapped[int] = mapped_column(primary_key=True)
    angle: Mapped[Numeric] = mapped_column(Numeric(precision=18, scale=15))
    length: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=15))
    x: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=15))
    y: Mapped[Numeric] = mapped_column(Numeric(precision=20, scale=15))

    # Many-to-one weak rel with circuit as owner
    circuit_id: Mapped[int] = mapped_column(ForeignKey(column='circuit.id'), primary_key=True)
    circuit: Mapped['Circuit'] = relationship(back_populates='turns')

    def __repr__(self) -> str:
        return f"Turn(year={self.year!r}, number={self.number!r}, angle={self.angle!r}, length={self.length}, x={self.x!r}, location={self.y!r}, circuit_id={self.circuit_id!r})"


class Meeting(Base):
    __tablename__ = 'meeting'
    __table_args__ = (
        UniqueConstraint(
            columns=('year', 'name'),
            name='uq_meeting_year_and_name'
        )
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

    sessions: Mapped[list['Session']] = relationship(
        back_populates='meeting', cascade='all, delete-orphan'
    )

    teams: Mapped[list['Team']] = relationship(
        secondary=meeting_team_participation_table, back_populates='meetings', cascade='all, delete-orphan'
    )

    drivers: Mapped[list['Driver']] = relationship(
        secondary=meeting_driver_participation_table, back_populates='meetings', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Meeting(id={self.id!r}, year={self.year!r}, name={self.name!r}, official_name={self.official_name!r}, start_date={self.start_date}, utc_offset={self.utc_offset!r}, circuit_id={self.circuit_id!r})"


class Session(Base):
    __tablename__ = 'session'

    name: Mapped[str] = mapped_column(primary_key=True)
    type: Mapped[str]
    start_date: Mapped[DateTime]
    end_date: Mapped[DateTime]
    utc_offset: Mapped[Interval]

    # Weak rel with meeting as parent
    meeting_id: Mapped[int] = mapped_column(ForeignKey(column='meeting.id'), primary_key=True)
    meeting: Mapped['Meeting'] = relationship(back_populates='sessions')

    events: Mapped[list['Event']] = relationship(
        back_populates='session', cascade='all, delete-orphan'
    )

    teams: Mapped[list['Team']] = relationship(
        secondary=session_team_participation_table, back_populates='sessions', cascade='all, delete-orphan'
    )

    drivers: Mapped[list['Driver']] = relationship(
        secondary=session_driver_participation_table, back_populates='sessions', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Session(name={self.name!r}, type={self.type!r}, start_date={self.start_date}, end_date={self.end_date}, utc_offset={self.utc_offset!r}, meeting_id={self.meeting_id!r}"


class Team(Base):
    __tablename__ = 'team'
    __table_args__ = (
        UniqueConstraint(
            columns=('year', 'name'),
            name='uq_team_year_and_name'
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int]
    name: Mapped[str]
    color: Mapped[str] = mapped_column(String(length=6))

    meetings: Mapped[list['Meeting']] = relationship(
        secondary=meeting_team_participation_table, back_populates='teams', cascade='all, delete-orphan'
    )

    sessions: Mapped[list['Session']] = relationship(
        secondary=meeting_team_participation_table, back_populates='teams', cascade='all, delete-orphan'
    )

    drivers: Mapped[list['Driver']] = relationship(
        secondary=team_driver_participation_table, back_populates='teams', cascade='all, delete-orphan'
    )

    def __repr__(self) -> str:
        return f"Team(id={self.id!r}, year={self.year!r}, name={self.name!r}, color={self.color!r}"


class Driver(Base):
    __tablename__ = 'driver'
    __table_args__ = (
        UniqueConstraint(
            columns=('year', 'number'),
            name='uq_driver_year_and_number'
        )
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    year: Mapped[int]
    number: Mapped[int]
    acronym: Mapped[str] = mapped_column(String(length=3))
    first_name: Mapped[str]
    last_name: Mapped[str]
    full_name: Mapped[str]
    broadcast_name: Mapped[str]
    image_url: Mapped[str]

    # Many-to-one rel with country as parent
    country_id: Mapped[int] = mapped_column(ForeignKey(column='country.id'))
    country: Mapped['Country'] = relationship(back_populates='drivers')

    meetings: Mapped[list['Meeting']] = relationship(
        secondary=meeting_team_participation_table, back_populates='drivers', cascade='all, delete-orphan'
    )

    sessions: Mapped[list['Session']] = relationship(
        secondary=meeting_team_participation_table, back_populates='drivers', cascade='all, delete-orphan'
    )

    teams: Mapped[list['Team']] = relationship(
        secondary=team_driver_participation_table, back_populates='drivers', cascade='all, delete-orphan'
    )

    events: Mapped[list['Event'] | None] = relationship(back_populates='driver', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"Driver(id={self.id!r}, year={self.year!r}, number={self.number!r}, acronym={self.acronym!r}, first_name={self.first_name!r}, last_name={self.last_name!r}, full_name={self.full_name!r}, broadcast_name={self.broadcast_name!r}, image_url={self.image_url!r}, country_code={self.country_code!r}"


class Event(Base):
    __tablename__ = 'event'
    __table_args__ = (
        ForeignKeyConstraint(
            columns=('meeting_id', 'session_name'),
            refcolumns=('session.meeting_id, session.name'),
            name='fk_event_meeting_id_and_session_name'
        )
    )
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[DateTime]
    elapsed_time: Mapped[Interval]
    lap_number: Mapped[int | None]
    category: Mapped[str]
    cause: Mapped[str]

    # Many-to-one rel with session as parent
    meeting_id: Mapped[int]
    session_name: Mapped[str]
    session: Mapped['Session'] = relationship(back_populates='events')

    # One-to-one rel with location
    location: Mapped['Location' | None] = relationship(back_populates='event', cascade='all, delete-orphan')

    # One-to-one rel with pit
    pit: Mapped['Pit' | None] = relationship(back_populates='event', cascade='all, delete-orphan')

    # One-to-one rel with race control
    race_control: Mapped['RaceControl' | None] = relationship(back_populates='event', cascade='all, delete-orphan')

    # Many-to-many rel with driver
    drivers: Mapped[list['Driver'] | None] = relationship(back_populates='event', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"Event(id={self.id!r}, date={self.date!r}, elapsed_time={self.elapsed_time!r}), lap_number={self.lap_number!r}, category={self.category!r}, cause={self.cause!r}, meeting_id={self.meeting_id!r}, session_name={self.session_name!r}"
    

class EventDriverParticipation(Base):
    __tablename__ = 'event_driver_participation'

    event_id: Mapped[int] = mapped_column(ForeignKey(column='event.id'), primary_key=True)
    driver_id: Mapped[int] = mapped_column(ForeignKey(column='driver.id'), primary_key=True)
    role: Mapped[str] # One of: 'initiator' or 'participant'

    event: Mapped['Event'] = relationship(back_populates='drivers', cascade='all, delete-orphan')
    driver: Mapped['Driver'] = relationship(back_populates='events', cascade='all, delete-orphan')


class Location(Base):
    __tablename__ = 'location'

    date: Mapped[DateTime] = mapped_column(primary_key=True)
    x: Mapped[int]
    y: Mapped[int]
    z: Mapped[int]
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey(column='event.id'), primary_key=True)
    event: Mapped['Event'] = relationship(back_populates='location', cascade='all, delete-orphan', single_parent=True)
    
    def __repr__(self) -> str:
        return f"Location(date={self.date!r}, x={self.x!r}, y={self.y!r}, z={self.z!r}"
    

class Pit(Base):
    __tablename__ = 'pit'

    date: Mapped[str] = mapped_column(primary_key=True)
    duration: Mapped[Numeric] = mapped_column(Numeric(precision=6, scale=1)) # Max pit duration should be in the hours
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey(column='event.id'), primary_key=True)
    event: Mapped['Event'] = relationship(back_populates='pit', cascade='all, delete-orphan', single_parent=True)
    
    def __repr__(self) -> str:
        return f"Pit(date={self.date!r}, duration={self.duration!r}"
    

class RaceControl(Base):
    __tablename__ = 'race_control'

    date: Mapped[str] = mapped_column(primary_key=True)
    message: Mapped[str]
    
    # One-to-one weak rel with event as owner
    event_id: Mapped[int] = mapped_column(ForeignKey(column='event.id'), primary_key=True)
    event: Mapped['Event'] = relationship(back_populates='race_control', cascade='all, delete-orphan', single_parent=True)
    
    def __repr__(self) -> str:
        return f"RaceControl(date={self.date!r}, message={self.message!r}"