# Processes events from OpenF1 query api
from datetime import datetime, timedelta
from decimal import Decimal
from pathlib import Path
import os

import asyncio
import json
import requests
import s3fs
from sqlalchemy_helpers.aio import AsyncDatabaseManager
from polars import DataFrame
from typing import Any
from loguru import logger
from typer import Typer

from storage import Storage
from app.api.circuit.models import Circuit
from app.api.country.models import Country
from app.api.turn.models import Turn
from app.api.meeting.models import Meeting
from app.api.session.models import Session
from app.api.team.models import Team
from app.api.driver.models import Driver
from app.api.event.models import Event
from app.api.event_role.models import EventRole
from app.api.location.models import Location


app = Typer()


@app.command()
def process_overtakes(session_key: int) -> None:
    """
    Outputs overtakes as events for a given session
    Note: session_key must match a race session
    """

    # Read drivers, position, location, multiviewer map data from storage instead of querying

    # Get all drivers for a session by number
    driver_data = _query_endpoint(
        base_url=_get_openf1_base_url(),
        endpoint="drivers",
        query_string=f"session_key={session_key}"
    )
    driver_numbers = list(map(lambda driver : driver["driver_number"], driver_data))

    for driver_number in driver_numbers:

        logger.info(f"Starting iteration for driver '{driver_number}'")

        position_data = _query_endpoint(
            base_url=_get_openf1_base_url(),
            endpoint="position",
            query_string=f"session_key={session_key}&driver_number={driver_number}"
        )

        # Ensure that position changes are sorted by date
        position_data.sort(key=lambda position : _to_datetime(position["date"]))

        all_overtakes = []

        # For each position change, check if driver is not currently in pit
        for idx, position in enumerate(position_data):
            position_date = _to_datetime(position["date"])

            logger.info(f"Driver: {driver_number}, Position: {position["position"]}")

            if idx == 0:
                # No prev positions to compare, therefore no overtakes
                continue

            # Get prev position change
            prev_position = position_data[idx - 1]

            # If prev position was higher, then categorize as driver overtaking another driver
            # Since driver x overtaking driver y and driver y being overtaken by driver x are equivalent, we only process the former
            if position["position"] < prev_position["position"]:
                logger.info(f"Overtaking")

                all_drivers_ahead_position_data_prev = _query_endpoint(
                    base_url=_get_openf1_base_url(),
                    endpoint="position",
                    query_string=f"session_key={session_key}&date<{_to_timestring(position_date)}&position<{prev_position["position"]}"
                )
                all_drivers_behind_position_data_curr = _query_endpoint(
                    base_url=_get_openf1_base_url(),
                    endpoint="position",
                    query_string=f"session_key={session_key}&date>={_to_timestring(position_date)}&position>{position["position"]}"
                )

                # Filter for driver numbers that were previously ahead of the current driver but are now behind
                all_driver_numbers_ahead_prev = list(map(lambda position : position["driver_number"], all_drivers_ahead_position_data_prev))
                all_driver_numbers_behind_curr = list(map(lambda position : position["driver_number"], all_drivers_behind_position_data_curr))

                all_overtaken_driver_numbers = list(set(all_driver_numbers_ahead_prev) & set(all_driver_numbers_behind_curr))
                
                # Get position data for overtaken drivers
                all_overtaken_drivers_position_data_curr = list(filter(lambda position : position["driver_number"] in all_overtaken_driver_numbers, all_drivers_behind_position_data_curr))

                # Get num_overtakes position changes from overtaken drivers closest to the time of the position change from the overtaking driver
                # - this prevents previous overtakes for the same positions from being processed again
                all_overtaken_drivers_position_data_curr.sort(key=lambda position : abs(_to_datetime(position["date"]) - position_date))
                num_overtakes = abs(position["position"] - prev_position["position"])
                overtaken_drivers_position_data_curr = all_overtaken_drivers_position_data_curr[0:num_overtakes]

                for overtaken_position in overtaken_drivers_position_data_curr:
                    estimated_location =_get_estimated_overtake_location(session_key=session_key, overtaking_driver_number=driver_number, overtaken_driver_number=overtaken_position["driver_number"], date=position_date)
                    all_overtakes.append((position_data, overtaken_position, estimated_location))

        for overtake in all_overtakes:
            _insert_overtake_event(session_key=session_key, overtake=overtake)


async def _insert_overtake_event(session_key: int, overtake: Any):
    # HISTORICAL_DB_CONNECTION_STRING = os.getenv("HISTORICAL_DB_CONNECTION_STRING", "")
    HISTORICAL_DB_CONNECTION_STRING = "postgresql://root:W8CZyn5sJHDinR@query-db/root" # TODO: replace with environment variable
    PATH_TO_ALEMBIC_DIR = str(Path(__file__).parent.joinpath("migrations").absolute())

    db = AsyncDatabaseManager(HISTORICAL_DB_CONNECTION_STRING, PATH_TO_ALEMBIC_DIR)
    db_session = db.Session()

    # Position data for initiating driver, position data for overtaken driver and location
    initiator_position_data, participant_position_data, estimated_location = overtake

    session_content = _query_endpoint(
        base_url=_get_openf1_base_url(),
        endpoint="sessions",
        query_string=f"session_key={session_key}"
    )
    session_data = session_content[0]

    meeting_content = _query_endpoint(
        base_url=_get_openf1_base_url(),
        endpoint="meetings",
        query_string=f"meeting_key={db_session["meeting_key"]}"
    )
    meeting_data = meeting_content[0]

    # Add circuit
    curr_year = datetime.now().year
    circuit_data = _query_endpoint(
        base_url=_get_multiviewer_base_url(),
        endpoint=f"circuits/{meeting_data["circuit_key"]}/{curr_year}"
    )

    circuit_country_obj, _ = await Circuit.get_or_create(
        session=db_session,
        code=meeting_data["country_code"],
        name=meeting_data["country_name"]
    )

    circuit_obj, _ = await Circuit.get_or_create(
        session=db_session,
        year=meeting_data["year"],
        name=meeting_data["circuit_short_name"],
        location=meeting_data["location"],
        rotation=circuit_data["rotation"],
        country_id=circuit_country_obj.id
    )

    # Add turns for circuit
    circuit_turn_data = circuit_data["corners"]

    for turn in circuit_turn_data:
        await Turn.get_or_create(
            session=db_session,
            year=meeting_data["year"],
            number=turn["number"],
            angle=_to_decimal(turn["angle"]),
            length=_to_decimal(turn["length"]),
            x=_to_decimal(turn["trackPosition"]["x"]),
            y=_to_decimal(turn["trackPosition"]["y"]),
            circuit_id=circuit_obj.id
        )

    # Add meeting
    meeting_obj, _ = await Meeting.get_or_create(
        session=db_session,
        year=meeting_data["year"],
        name=meeting_data["meeting_name"],
        official_name=meeting_data["meeting_official_name"],
        start_date=_to_datetime(meeting_data["date_start"]),
        utc_offset=_to_timedelta(meeting_data["gmt_offset"]),
        circuit_id=circuit_obj.id
    )

    # Add session
    session_obj, _ = await Session.get_or_create(
        session=db_session,
        name=session_data["session_name"],
        type=session_data["session_type"],
        start_date=_to_datetime(session_data["date_start"]),
        end_date=_to_datetime(session_data["date_end"]),
        utc_offset=_to_timedelta(session_data["gmt_offset"]),
        meeting_id=meeting_obj.id
    )

    initiator_driver_content = _query_endpoint(
        base_url=_get_openf1_base_url(),
        endpoint="drivers",
        query_string=f"session_key={session_key}&driver_number={initiator_position_data["driver_number"]}"
    )
    initiator_driver_data = initiator_driver_content[0]

    participant_driver_content = _query_endpoint(
        base_url=_get_openf1_base_url(),
        endpoint="drivers",
        query_string=f"session_key={session_key}&driver_number={participant_position_data["driver_number"]}"
    )
    participant_driver_data = participant_driver_content[0]

    # Add team(s)
    initiator_team_obj, _ = await Team.get_or_create(
        session=db_session,
        name=initiator_driver_data["team_name"],
        color=initiator_driver_data["team_colour"]
    )
    participant_team_obj, _ = await Team.get_or_create(
        session=db_session,
        name=participant_driver_data["team_name"],
        color=participant_driver_data["team_colour"]
    )

    # Associate teams with meetings, sessions, and drivers
    initiator_team_obj.teams.append(meeting_obj)
    participant_team_obj.teams.append(meeting_obj)

    initiator_team_obj.teams.append(session_obj)
    participant_team_obj.teams.append(session_obj)

    initiator_team_obj.teams.append(initiator_driver_obj)
    participant_team_obj.teams.append(participant_driver_obj)

    # Add driver(s)
    initiator_driver_country_obj, _ = await Country.get_or_create(
        session=db_session,
        code=initiator_driver_data["country_code"]
    )
    participant_driver_country_obj, _ = await Country.get_or_create(
        session=db_session,
        code=participant_driver_data["country_code"]
    )

    initiator_driver_obj, _ = await Driver.get_or_create(
        session=db_session,
        number=initiator_driver_data["driver_number"],
        acronym=initiator_driver_data["name_acronym"],
        first_name=initiator_driver_data["first_name"],
        last_name=initiator_driver_data["last_name"],
        full_name=initiator_driver_data["full_name"],
        broadcast_name=initiator_driver_data["broadcast_name"],
        image_url=initiator_driver_data["headshot_url"],
        country_id=initiator_driver_country_obj.id,
        meeting_id=meeting_obj.id,
        session_id=session_obj.id,
        team_id=initiator_team_obj.id
    )
    participant_driver_obj, _ = await Driver.get_or_create(
        session=db_session,
        number=participant_driver_data["driver_number"],
        acronym=participant_driver_data["name_acronym"],
        first_name=participant_driver_data["first_name"],
        last_name=participant_driver_data["last_name"],
        full_name=participant_driver_data["full_name"],
        broadcast_name=participant_driver_data["broadcast_name"],
        image_url=participant_driver_data["headshot_url"],
        country_code=participant_driver_data["country_code"],
        country_id=participant_driver_country_obj.id,
        meeting_id=meeting_obj.id,
        session_id=session_obj.id,
        team_id=participant_team_obj.id
    )

    # Associate drivers with meetings and sessions
    initiator_driver_obj.teams.append(meeting_obj)
    participant_driver_obj.teams.append(meeting_obj)

    initiator_driver_obj.teams.append(session_obj)
    participant_driver_obj.teams.append(session_obj)

    # Add event
    event_obj, _ = await Event.get_or_create(
        session=db_session,
        date=_to_datetime(estimated_location["date"]),
        elapsed_time=_to_datetime(estimated_location["date"]) - _to_datetime(session_data["date_start"]),
        lap_number=_get_lap_number(session_key=session_key, date=_to_datetime(estimated_location["date"])),
        category="car-action", # TODO: make enum
        cause="overtake",
        session_id=session_obj.id
    ) 

    # Add location
    location_obj, _ = await Location.get_or_create(
        session=db_session,
        date=_to_datetime(estimated_location["date"]),
        x=estimated_location["x"],
        y=estimated_location["y"],
        z=estimated_location["z"],
        event_id=event_obj.id
    )

    # Associate events with drivers
    initiator_event_role_obj = await EventRole.get_or_create(
        driver_id=initiator_driver_obj.id,
        role="initiator"
    )
    participant_event_role_obj = await EventRole.get_or_create(
        driver_id=participant_driver_obj.id,
        role="participant"
    )
    event_obj.drivers.append(initiator_event_role_obj)
    event_obj.drivers.append(participant_event_role_obj)

    db_session.commit()
    db_session.close()


def _get_lap_number(session_key: int, date: datetime) -> int:
    """
    Gets the lap number for a race session at the given date (the current lap number of the leading driver)
    """

    # Get interval data for all drivers that have led before the given date
    interval_content = _query_endpoint(
        base_url=_get_openf1_base_url(),
        endpoint="intervals",
        query_string=f"session_key={session_key}&date<={_to_timestring(date)}&gap_to_leader=0"
    )

    # Find the most recent driver that has led
    most_recent_leader_interval = min(interval_content, key=lambda interval : abs(_to_datetime(interval["date"]) - date))
    most_recent_leader_number = most_recent_leader_interval["driver_number"]

    # Find the most recent completed lap
    lap_content = _query_endpoint(
        base_url=_get_openf1_base_url(),
        endpoint="laps",
        query_string=f"session_key={session_key}&date_start<={_to_timestring(date)}&driver_number={most_recent_leader_number}"
    )
    most_recent_leader_completed_lap = min(lap_content, key=lambda interval : abs(_to_datetime(interval["date_start"]) - date))

    assert date <= _to_datetime(most_recent_leader_completed_lap["date_start"]) + _to_timedelta(most_recent_leader_completed_lap["lap_duration"])

    return most_recent_leader_completed_lap["lap_number"]
    

def _get_estimated_overtake_location(session_key: int, overtaking_driver_number: int, overtaken_driver_number: int, date: datetime) -> dict[str, Any]:
    """
    Returns the estimated overtake location for an overtaking driver on an overtaken driver using the given date
    i.e. the location where the overtake is considered fully complete
    """
    logger.info(f"Processing driver {overtaking_driver_number} overtake on {overtaken_driver_number}")

    # TIME_INTERVAL_S should be around interval sampling rate (~5hz)
    TIME_INTERVAL_S ="5"
    delta = _to_timedelta(TIME_INTERVAL_S)

    estimated_overtake_date = _get_estimated_overtake_date(
        session_key=session_key,
        overtaking_driver_number=overtaking_driver_number,
        overtaken_driver_number=overtaken_driver_number,
        date=date
    )
    
    if estimated_overtake_date is None:
        return None
    
    estimated_overtake_location_data = _query_endpoint(
        base_url=_get_openf1_base_url(),
        endpoint="location",
        query_string=f"session_key={session_key}&driver_number={overtaking_driver_number}&date>={_to_timestring(estimated_overtake_date - delta)}&date<={_to_timestring(estimated_overtake_date + delta)}"
    )

    # Get closest location data to most likely overtake date
    return min(estimated_overtake_location_data, key=lambda location : abs(_to_datetime(location["date"]) - estimated_overtake_date))


def _get_estimated_overtake_date(session_key: int, overtaking_driver_number: int, overtaken_driver_number: int, date: datetime) -> datetime | None:
    """
    Returns the estimated date of the overtake for an overtaking driver on an overtaken driver, None if the date cannot be estimated
    NOTE: this only works for unlapped cars i.e. their gap to leader is not "+1 LAP", "+2 LAPS", etc.
    """

    # TIME_INTERVAL_S should be relatively large (we know that positions are recorded per lap, therefore the overtake must have occurred on the previous lap)
    TIME_INTERVAL_S = "300"
    delta = _to_timedelta(TIME_INTERVAL_S)

    # Get interval data for all cars, sort by gap to leader and find the driver with next smallest gap to leader
    interval_data = _query_endpoint(
        base_url=_get_openf1_base_url(),
        endpoint="intervals",
        query_string=f"session_key={session_key}&date>={_to_timestring(date - delta)}&date<={_to_timestring(date)}"
    )
    overtaken_driver_interval_data = list(filter(lambda interval : interval["driver_number"] == overtaken_driver_number, interval_data))
    overtaken_driver_interval_data.sort(key=lambda interval : _to_datetime(interval["date"]))

    overtaking_driver_interval_data = list(filter(lambda interval : interval["driver_number"] == overtaking_driver_number, interval_data))
    overtaking_driver_interval_data.sort(key=lambda interval : _to_datetime(interval["date"]))

    for overtaking_driver_interval in overtaking_driver_interval_data:
        # Want gap to leader by pursuing driver to be initially larger, then smaller than some other driver
        intervals_before = list(filter(lambda interval : (_to_datetime(interval["date"]) < _to_datetime(overtaking_driver_interval["date"])), overtaken_driver_interval_data))
        intervals_after = list(filter(lambda interval : (_to_datetime(interval["date"]) >= _to_datetime(overtaking_driver_interval["date"])), overtaken_driver_interval_data))

        intervals_with_overtaking_driver_behind_before = list(filter(lambda interval : _to_timedelta(f"{interval["gap_to_leader"]}") is not None and _to_timedelta(f"{interval["gap_to_leader"]}") < _to_timedelta(f"{overtaking_driver_interval["gap_to_leader"]}"), intervals_before))
        intervals_with_overtaking_driver_ahead_after = list(filter(lambda interval : _to_timedelta(f"{interval["gap_to_leader"]}") is not None and _to_timedelta(f"{interval["gap_to_leader"]}") > _to_timedelta(f"{overtaking_driver_interval["gap_to_leader"]}"), intervals_after))

        driver_numbers_ahead_before = list(map(lambda interval : interval["driver_number"], intervals_with_overtaking_driver_behind_before))
        driver_numbers_behind_after = list(map(lambda interval : interval["driver_number"], intervals_with_overtaking_driver_ahead_after))

        overtaken_driver_numbers = list(set(driver_numbers_ahead_before) & set(driver_numbers_behind_after))

        if overtaken_driver_number in overtaken_driver_numbers:
            return _to_datetime(overtaking_driver_interval["date"])
        
    return None


@app.command()
def collect_circuit(circuit_key: int) -> None:
    """
    Gathers all data for a circuit using the Multiviewer API, and uploads data to remote storage
    """
    curr_year = datetime.now().year
    circuit_data = _query_endpoint(
        base_url=_get_multiviewer_base_url(),
        endpoint=f"circuits/{circuit_key}/{curr_year}"
    )

    df = DataFrame(data=circuit_data)
    
    Storage.write(
        destination=".parquet",
        filesystem=s3fs.S3FileSystem(),
        dataframe=df,
        format="parquet"
    )


@app.command()
def collect_session(session_key: int) -> None:
    """
    Gathers all data from a session using the OpenF1 API, and uploads data to remote storage
    """
    collections = [
        "car_data",
        "drivers",
        "intervals",
        "laps",
        "location",
        "pit",
        "position",
        "race_control",
        "stints",
        "team_radio",
        "weather"
    ]
    dates = _get_session_dates(session_key)
    start_date, end_date = dates

    for collection in collections:
        df = _collect_collection(session_key=session_key, collection=collection, start_date=start_date, end_date=end_date)
        Storage.write(
            destination=".parquet",
            filesystem=s3fs.S3FileSystem(),
            dataframe=df,
            format="parquet"
        )


def _collect_collection(
        session_key: int,
        collection: str,
        start_date: datetime,
        end_date: datetime
    ) -> DataFrame:
    """
    Return data from OpenF1 API from start_time until end_time as a DataFrame
    """

    # Interval for date filter in queries
    TIME_INTERVAL_S = "10"
    delta = _to_timedelta(TIME_INTERVAL_S)

    curr_start = start_date
    curr_end = start_date + delta
    df = None

    while curr_start < end_date:
        logger.info(f"Starting iteration for collection '{collection}' with start date '{curr_start} and end date '{curr_end}'")

        collection_batch = _query_endpoint(
            base_url=_get_openf1_base_url(),
            endpoint=collection,
            query_string=f"session_key={session_key}&date>={_to_timestring(curr_start)}&date<={_to_timestring(curr_end)}")

        if isinstance(df, DataFrame):
            temp_df = DataFrame(data=collection_batch)

            # Prefer vstack since we are appending many dataframes and not performing queries
            df = df.vstack(temp_df)
        else:
            df = DataFrame(data=collection_batch)
            
        curr_start += delta
        curr_end += delta
    
    df = df.rechunk()

    return df


def _get_session_dates(session_key: int) -> tuple[datetime, datetime]:
    """
    Returns the dates for a session in the order (start, end)
    """

    session_content = _query_endpoint(
        base_url=_get_openf1_base_url(),
        endpoint="sessions",
        query_string=f"session_key={session_key}"
    )

    if len(session_content) == 0:
        # Session does not exist
        raise ValueError(f"Session with session key ${session_key} could not be found.")
    
    session = session_content[0]
    if "date_start" not in session or "date_end" not in session:
        # Improper schema
        raise ValueError(f"Start and end dates for session with session key ${session_key} could not be found.")
    
    return _to_datetime(session["date_start"]), _to_datetime(session["date_end"])


def _query_endpoint(base_url: str, endpoint: str, query_string: str | None = None) -> list[dict[str, Any]] | dict[str, Any]:
    """
    Returns a Python object from a JSON endpoint
    """
    # Take query params as a string to allow for inequalities needed for OpenF1 API
    url = f"{_join_url(base_url, endpoint)}"

    if query_string is not None:
        url += f"?{query_string}"

    # Need User-Agent header to avoid being blocked by Multiviewer API
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1"
    }

    response = requests.get(url=url, headers=headers)

    return json.loads(response.content)


def _get_openf1_base_url() -> str:
    """
    Base address for the running OpenF1 service
    """

    # ADDRESS = os.getenv("OPENF1_ADDRESS", "0.0.0.0:8000")
    ADDRESS = "0.0.0.0:8000" # TODO: replace with environment variable

    return f"http://{ADDRESS}/v1"


def _get_multiviewer_base_url() -> str:
    """
    Base address for the Multiviewer service
    """

    return f"http://api.multiviewer.app/api/v1"


def _join_url(*args) -> str:
    """
    Credit to OpenF1 https://github.com/br-g/openf1/blob/9e497783662594093da3ae290226692315c2d8d2/src/openf1/util/misc.py#L11-L15
    Join URL parts with a forward slash
    """
    if any(len(e) == 0 or e is None for e in args):
        raise ValueError(f"Invalid URL components: {args}")
    return "/".join([e.strip("/") for e in args])


def _to_decimal(x: str | float | Decimal) -> Decimal | None:
    if isinstance(x, str) or isinstance(x, float):
        try:
            return Decimal(value=f"{x}")
        except Exception as exc:
            logger.debug(f"Failed to parse decimal '{x}'",
                          exc_info=exc)
            return None
    elif isinstance(x, Decimal):
        return None
    
    return None
    

def _to_timedelta(x: str | datetime) -> datetime | None:
    """
    Credit to FastF1 for inspiration https://github.com/theOehrly/Fast-F1/blob/317bacf8c61038d7e8d0f48165330167702b349f/fastf1/utils.py#L120-L175

    Fast timedelta object creation from a time string

    Permissible string formats:

        For example: "13:24:46.320215" with:

            - optional hours and minutes
            - optional microseconds and milliseconds with
              arbitrary precision (1 to 6 digits)

        Examples of valid formats:

            - "24.3564" (seconds + milli/microseconds)
            - "36:54" (minutes + seconds)
            - "8:45:46" (hours, minutes, seconds)

    Args:
        x: timestamp
    """
    # this is faster than using pd.timedelta on a string
    if isinstance(x, str) and len(x):
        try:
            hours, minutes = 0, 0
            if len(hms := x.split(":")) == 3:
                hours, minutes, seconds = hms
            elif len(hms) == 2:
                minutes, seconds = hms
            else:
                seconds = hms[0]

            if "." in seconds:
                seconds, msus = seconds.split(".")
                if len(msus) < 6:
                    msus = msus + "0" * (6 - len(msus))
                elif len(msus) > 6:
                    msus = msus[0:6]
            else:
                msus = 0

            return timedelta(
                hours=int(hours), minutes=int(minutes),
                seconds=int(seconds), microseconds=int(msus)
            )

        except Exception as exc:
            logger.debug(f"Failed to parse timedelta string '{x}'",
                          exc_info=exc)
            return None

    elif isinstance(x, datetime):
        return x

    else:
        return None


def _to_datetime(x: str | datetime) -> datetime | None:
    """
    Credit to FastF1 for inspiration https://github.com/theOehrly/Fast-F1/blob/317bacf8c61038d7e8d0f48165330167702b349f/fastf1/utils.py#L178-L227

    Fast datetime object creation from a date string.

    Permissible string formats:

        "2020-12-13T13:27:15+00:00" with:

            - with optional UTC offset

    Args:
        x: timestamp
    """
    if isinstance(x, str):
        try:
            if "." in x:
                return datetime.strptime(
                    x,
                    "%Y-%m-%dT%H:%M:%S.%f%z" # Have to use "%z" instead of "%:z" as recommended in the docs since it has not been implemented for strptime yet
                )
            return datetime.strptime(
                    x,
                    "%Y-%m-%dT%H:%M:%S%z"
                )
        
        except Exception as exc:
            logger.debug(f"Failed to parse datetime string '{x}'",
                          exc_info=exc)
            return None

    elif isinstance(x, datetime):
        return x

    else:
        return None


def _to_timestring(x: str | datetime) \
        -> str | None:
    """
    Converts a datetime object into its string representation
    """
    if isinstance(x, datetime):
        try:
            return x.strftime(
                "%Y-%m-%dT%H:%M:%S.%f%:z"
            )

        except Exception as exc:
            logger.debug(f"Failed to convert datetime to string '{x}'",
                          exc_info=exc)
            return None

    elif isinstance(x, str):
        return x

    else:
        return None
    

if __name__ == "__main__":
    app()
