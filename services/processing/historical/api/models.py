from datetime import datetime, timedelta
from decimal import Decimal
from typing import ClassVar, Literal

from pydantic import BaseModel

# Request models
class CircuitFilterParams(BaseModel):
    circuit_id: int | None = None
    year: int | None = None
    circuit_name: str | None = None
    circuit_location: str | None = None
    circuit_rotation: int | None = None
    country_id: str | None = None
    country_code: str | None = None
    country_name: str | None = None


class MeetingFilterParams(BaseModel):
    meeting_id: int | None = None
    year: int | None = None
    meeting_name: str | None = None
    meeting_official_name: str | None = None
    start_date: datetime | None = None
    utc_offset: timedelta | None = None


class SessionFilterParams(BaseModel):
    session_id: int | None = None
    year: int | None = None
    meeting_name: str | None = None
    session_name: str | None = None
    session_type: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    utc_offset: timedelta | None = None


class TeamFilterParams(BaseModel):
    team_id: int | None = None
    year: int | None = None
    team_name: str | None = None
    team_color: str | None = None


class DriverFilterParams(BaseModel):
    driver_id: int | None = None
    year: int | None = None
    driver_number: int | None = None
    driver_acronym: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    broadcast_name: str | None = None
    image_url: str | None = None
    country_id: int | None = None
    country_code: str | None = None


class EventFilterParams(BaseModel):
    event_id: int | None = None
    date: datetime | None = None
    elapsed_time: timedelta | None = None
    lap_number: int | None = None
    category: str | None = None
    cause: str | None = None


# Query parameters to database columns - this should mirror the respective classes in db_model
class CountryColumns(BaseModel):
    id: int | None = None
    code: int | None = None
    name: Decimal | None = None


class TurnColumns(BaseModel):
    number: int | None = None
    angle: Decimal | None = None
    length: Decimal | None = None
    x: Decimal | None = None
    y: Decimal | None = None


class CircuitColumns(BaseModel):
    id: int | None = None
    year: int | None = None
    name: str | None = None
    location: str | None = None
    rotation: int | None = None


class MeetingColumns(BaseModel):
    id: int | None = None
    year: int | None = None
    name: str | None = None
    official_name: str | None = None
    start_date: datetime | None = None
    utc_offset: timedelta | None = None


class SessionColumns(BaseModel):
    name: str | None = None
    type: str | None = None
    start_date: datetime | None = None
    end_date: datetime | None = None
    utc_offset: timedelta | None = None


class TeamColumns(BaseModel):
    id: int | None = None
    year: int | None = None
    name: str | None = None
    color: str | None = None


class DriverColumns(BaseModel):
    id: int | None = None
    year: int | None = None
    number: int | None = None
    acronym: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    full_name: str | None = None
    broadcast_name: str | None = None
    image_url: str | None = None


class EventColumns(BaseModel):
    id: int | None = None
    date: datetime | None = None
    elapsed_time: timedelta | None = None
    lap_number: int | None = None
    category: str | None = None
    cause: str | None = None


class LocationColumns(BaseModel):
    date: datetime | None = None
    x: Decimal | None = None
    y: Decimal | None = None


class PitColumns(BaseModel):
    date: datetime | None = None
    duration: Decimal | None = None


class RaceControlColumns(BaseModel):
    date: datetime | None = None
    message: str | None = None


# Maps column names in db models to respective names found in response models
class CircuitColumnNamesToResponseNames(BaseModel):
    id: ClassVar[str] = 'circuit_id'
    year: ClassVar[str] = 'year'
    name: ClassVar[str] = 'circuit_name'
    location: ClassVar[str] = 'circuit_location'
    rotation: ClassVar[str] = 'circuit_rotation'
    country_id: ClassVar[str] = 'country_id'


class TurnColumnNamesToResponseNames(BaseModel):
    number: ClassVar[str] = 'number'
    angle: ClassVar[str] = 'angle'
    length: ClassVar[str] = 'length'
    x: ClassVar[str] = 'x'
    y: ClassVar[str] = 'y'
    circuit_id: ClassVar[str] = 'circuit_id'


class CountryColumnNamesToResponseNames(BaseModel):
    id: ClassVar[str] = 'country_id'
    code: ClassVar[str] = 'country_code'
    name: ClassVar[str] = 'country_name'
    

# Response models
class TurnDataResponse(BaseModel):
    number: int
    angle: Decimal
    length: Decimal
    x: Decimal
    y: Decimal


class LocationDataResponse(BaseModel):
    date: datetime
    x: Decimal
    y: Decimal


class PitDataResponse(BaseModel):
    date: datetime
    duration: Decimal


class RaceControlDataResponse(BaseModel):
    date: datetime
    message: str


class EventDriverParticipationDataResponse(BaseModel):
    driver_id: int
    role: Literal['initiator'] | Literal['participant']


class EventDataResponse(BaseModel):
    date: datetime
    elapsed_time: timedelta
    lap_number: int | None
    category: str
    cause: str
    drivers: list[EventDriverParticipationDataResponse] | None
    details: LocationDataResponse | PitDataResponse | RaceControlDataResponse


class CircuitResponse(BaseModel):
    circuit_id: int
    year: int
    circuit_name: str
    circuit_location: str
    circuit_rotation: int
    turns: list[TurnDataResponse]
    country_id: int
    country_code: str
    country_name: str


class MeetingResponse(BaseModel):
    meeting_id: int
    circuit_id: int
    year: int
    meeting_name: str
    meeting_official_name: str
    start_date: datetime
    utc_offset: timedelta


class SessionResponse(BaseModel):
    session_id: int
    circuit_id: int
    meeting_id: int
    year: int
    session_name: str
    session_type: str
    start_date: datetime
    end_date: datetime
    utc_offset: timedelta


class TeamResponse(BaseModel):
    team_id: int
    year: int
    team_name: str
    team_color: str


class DriverResponse(BaseModel):
    driver_id: int
    team_id: int
    year: int
    driver_number: int
    driver_acronym: str
    last_name: str
    full_name: str
    broadcast_name: str
    image_url: str
    country_id: int
    country_code: str


class EventResponse(BaseModel):
    event_id: int
    circuit_id: int
    meeting_id: int
    session_id: int
    data: EventDataResponse