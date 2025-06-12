# Processes events from OpenF1 query api
import os
import datetime
import pathlib

import json
import polars
import typing
import loguru
import requests
import typer

app = typer.Typer()


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
        endpoint='drivers',
        query_string=f'session_key={session_key}'
    )
    driver_numbers = list(map(lambda driver : driver['driver_number'], driver_data))

    dates = _get_session_dates(session_key)
    start_date = dates[0]

    for driver_number in [14]:

        loguru.logger.info(f"Starting iteration for driver '{driver_number}'")

        position_data = _query_endpoint(
            base_url=_get_openf1_base_url(),
            endpoint='position',
            query_string=f'session_key={session_key}&driver_number={driver_number}'
        )

        # Ensure that position changes are sorted by date
        position_data.sort(key=_get_date_attr)

        # For each position change, check if driver is not currently in pit
        for idx, position in enumerate(position_data):
            position_date = _to_datetime(position['date'])

            loguru.logger.info(f"Driver: {driver_number}, Position: {position['position']}")

            if idx == 0:
                # No prev positions to compare, therefore no overtakes
                continue

            # Get prev position change
            prev_position = position_data[idx - 1]

            # If prev position was higher, then categorize as driver overtaking another driver
            if position['position'] < prev_position['position']:
                loguru.logger.info(f"Overtaking")

                all_drivers_ahead_position_data_prev = _query_endpoint(
                    base_url=_get_openf1_base_url(),
                    endpoint='position',
                    query_string=f'session_key={session_key}&date<{_to_timestring(position_date)}&position<{prev_position['position']}'
                )
                all_drivers_behind_position_data_curr = _query_endpoint(
                    base_url=_get_openf1_base_url(),
                    endpoint='position',
                    query_string=f'session_key={session_key}&date>={_to_timestring(position_date)}&position>{position['position']}'
                )

                # Filter for driver numbers that were previously ahead of the current driver but are now behind
                all_driver_numbers_ahead_prev = list(map(lambda position : position['driver_number'], all_drivers_ahead_position_data_prev))
                all_driver_numbers_behind_curr = list(map(lambda position : position['driver_number'], all_drivers_behind_position_data_curr))

                all_overtaken_driver_numbers = list(set(all_driver_numbers_ahead_prev) & set(all_driver_numbers_behind_curr))
                
                # Get position data for overtaken drivers
                all_overtaken_drivers_position_data_curr = list(filter(lambda position : position['driver_number'] in all_overtaken_driver_numbers, all_drivers_behind_position_data_curr))

                # Get num_overtakes position changes from overtaken drivers closest to the time of the position change from the overtaking driver
                # - this prevents previous overtakes for the same positions from being processed again
                all_overtaken_drivers_position_data_curr.sort(key=lambda position : abs(_to_datetime(position['date']) - position_date))
                num_overtakes = abs(position['position'] - prev_position['position'])
                overtaken_drivers_position_data_curr = all_overtaken_drivers_position_data_curr[0:num_overtakes]

                print(overtaken_drivers_position_data_curr)
                for overtaken_position in overtaken_drivers_position_data_curr:
                    print(_get_overtake_location(session_key=session_key, overtaking_driver_number=driver_number, overtaken_driver_number=overtaken_position['driver_number'], date=position_date, start_date=start_date))

                # TODO: create event response - if position_date is > end_date, assume overtake is due to penalty

            else:
                loguru.logger.info(f"Overtaken")

                # Categorize as driver being overtaken by another driver
                all_drivers_behind_position_data_prev = _query_endpoint(
                    base_url=_get_openf1_base_url(),
                    endpoint='position',
                    query_string=f'session_key={session_key}&date<{_to_timestring(position_date)}&position>{prev_position['position']}'
                )
                all_drivers_ahead_position_data_curr = _query_endpoint(
                    base_url=_get_openf1_base_url(),
                    endpoint='position',
                    query_string=f'session_key={session_key}&date>={_to_timestring(position_date)}&position<{position['position']}'
                )

                # Filter for driver numbers that were previously behind the current driver but are now ahead
                all_driver_numbers_behind_prev = list(map(lambda position : position['driver_number'], all_drivers_behind_position_data_prev))
                all_driver_numbers_ahead_curr = list(map(lambda position : position['driver_number'], all_drivers_ahead_position_data_curr))

                all_overtaking_driver_numbers = list(set(all_driver_numbers_behind_prev) & set(all_driver_numbers_ahead_curr))

                # Get position data for overtaking drivers
                all_overtaking_drivers_position_data_curr = list(filter(lambda position : position['driver_number'] in all_overtaking_driver_numbers, all_drivers_ahead_position_data_curr))

                # Get num_overtakes position changes from overtaken drivers closest to the time of the position change from the overtaking driver
                # - this prevents previous overtakes for the same positions from being processed again
                all_overtaking_drivers_position_data_curr.sort(key=lambda position : abs(_to_datetime(position['date']) - position_date))
                num_overtakes = abs(position['position'] - prev_position['position'])
                overtaking_drivers_position_data_curr = all_overtaking_drivers_position_data_curr[0:num_overtakes]

                print(overtaking_drivers_position_data_curr)
                for overtaking_position in overtaking_drivers_position_data_curr:
                    print(_get_overtake_location(session_key=session_key, overtaking_driver_number=overtaking_position['driver_number'], overtaken_driver_number=driver_number, date=_to_datetime(overtaking_position['date']), start_date=start_date))


def _get_overtake_location(session_key: int, overtaking_driver_number: int, overtaken_driver_number: int, date: datetime.datetime, start_date: datetime.datetime) -> dict[str, typing.Any]:
    """
    Returns the most likely overtake location for a pursuing driver using the given date
    i.e. the location where the overtake is considered fully complete
    """
    loguru.logger.info(f"Processing driver {overtaking_driver_number} overtake on {overtaken_driver_number}")

    # TIME_INTERVAL_S should match the interval in _get_driver_ahead and be reasonably close to interval sampling rate (~5hz)
    TIME_INTERVAL_S ='5'
    delta = _to_timedelta(TIME_INTERVAL_S)

    most_likely_overtake_date = None

    # Beginning from date, get interval data in batches, sort by descending order, and find interval data point having the overtaken driver ahead
    curr_date = date

    while most_likely_overtake_date is None and curr_date >= start_date:
        interval_data = _query_endpoint(
            base_url=_get_openf1_base_url(),
            endpoint='intervals',
            query_string=f'session_key={session_key}&driver_number={overtaking_driver_number}&date>={_to_timestring(curr_date - delta)}&date<={_to_timestring(curr_date)}'
        )

        interval_data.sort(key=lambda interval : abs(_to_datetime(interval['date']) - curr_date), reverse=True)

        for interval in interval_data:
            interval_driver_ahead = _get_driver_ahead(
                session_key=session_key,
                driver_number=overtaking_driver_number,
                date=_to_datetime(interval['date'])
            )
            loguru.logger.info(f"Curr driver ahead: {interval_driver_ahead}")

            if interval_driver_ahead == overtaken_driver_number or interval_driver_ahead == overtaking_driver_number:
                # Last data point where overtaken driver is still ahead - likely overtake
                most_likely_overtake_date = _to_datetime(interval['date'])
                break

        curr_date -= delta
    
    if most_likely_overtake_date is None:
        return None
    
    most_likely_overtake_location_data = _query_endpoint(
        base_url=_get_openf1_base_url(),
        endpoint='location',
        query_string=f'session_key={session_key}&driver_number={overtaking_driver_number}&date>={_to_timestring(most_likely_overtake_date - _to_timedelta('1'))}&date<={_to_timestring(most_likely_overtake_date + _to_timedelta('1'))}'
    )

    # Get closest location data to most likely overtake date
    return min(most_likely_overtake_location_data, key=lambda location : abs(_to_datetime(location['date']) - most_likely_overtake_date))


def _get_driver_ahead(session_key: int, driver_number: int, date: datetime.datetime) -> typing.Optional[int]:
    """
    Returns the driver number immediately ahead of the given driver number at the given date, otherwise None if the driver is leading
    """

    # TIME_INTERVAL_S should match the interval in _get_overtake_location and be reasonably close to interval sampling rate (~5hz)
    TIME_INTERVAL_S = '5'
    delta = _to_timedelta(TIME_INTERVAL_S)

    # Get interval data for all cars, sort by gap to leader and find the driver with next smallest gap to leader
    interval_data = _query_endpoint(
        base_url=_get_openf1_base_url(),
        endpoint='intervals',
        query_string=f'session_key={session_key}&date>={_to_timestring(date - delta)}&date<={_to_timestring(date)}'
    )

    most_recent_interval_data = []
    most_recent_interval_data_drivers = set() # Keeps track of driver numbers that have already been added to sorted_interval_data

    # Get the most recent interval data for each driver in descending order
    interval_data.sort(key=lambda interval : abs(_to_datetime(interval['date']) - date), reverse=True)

    for interval in interval_data:
        if not interval['driver_number'] in most_recent_interval_data_drivers and interval['gap_to_leader'] is not None:
            most_recent_interval_data.append(interval)
            most_recent_interval_data_drivers.add(interval['driver_number'])

    # Order interval data by gap to leader
    most_recent_interval_data.sort(key=lambda interval : (_to_timedelta(f'{interval['gap_to_leader']}') is not None, _to_timedelta(f'{interval['gap_to_leader']}')))

    # Get index of given driver's interval
    driver_idx = None

    for idx, interval in enumerate(most_recent_interval_data):
        if interval['driver_number'] == driver_number:
            driver_idx = idx

    if driver_idx == 0:
        # Driver is leading
        return driver_number
    
    if driver_idx is None:
        # Driver could not be found
        return None
    
    # Return the driver with the next smallest gap to leader
    return most_recent_interval_data[driver_idx - 1]['driver_number']


def _get_date_attr(data: dict[str, typing.Any]) -> datetime.datetime:
    """
    Returns the 'date' attribute as a datetime
    """
    return _to_datetime(data['date'])


@app.command()
def collect_circuit(circuit_key: int) -> None:
    """
    Gathers all data for a circuit using the Multiviewer API, and uploads data to remote storage
    """
    curr_year = datetime.datetime.now().year
    circuit_data = _query_endpoint(
        base_url=_get_multiviewer_base_url(),
        endpoint=f'circuits/{circuit_key}/{curr_year}'
    )

    with open(pathlib.Path.cwd() / f'{circuit_key}-{curr_year}.json', 'w') as file:
        json.dump(obj=circuit_data, fp=file)


@app.command()
def collect_session(session_key: int) -> None:
    """
    Gathers all data from a session using the OpenF1 API, and uploads data to remote storage
    """
    collections = [
        'car_data',
        # 'drivers',
        # 'intervals',
        # 'laps',
        # 'location',
        # 'pit',
        # 'position',
        # 'race_control',
        # 'stints',
        # 'team_radio',
        # 'weather'
    ]
    dates = _get_session_dates(session_key)
    start_date = dates[0]
    end_date = dates[1]

    for collection in collections:
        df = _collect_collection(session_key=session_key, collection=collection, start_date=start_date, end_date=end_date)
        _write_to_storage(dataframe=df, url=pathlib.Path.cwd() / f'{session_key}-{collection}.parquet')


def _collect_collection(
        session_key: int,
        collection: str,
        start_date: datetime,
        end_date: datetime
    ) -> polars.DataFrame:
    """
    Return data from OpenF1 API from start_time until end_time as a DataFrame
    """

    # Interval for date filter in queries
    TIME_INTERVAL_S = '10'
    delta = _to_timedelta(TIME_INTERVAL_S)

    curr_start = start_date
    curr_end = start_date + delta
    df = None

    while curr_start < end_date:
        loguru.logger.info(f"Starting iteration for collection '{collection}' with start date '{curr_start}' and end date '{curr_end}'")

        collection_batch = _query_endpoint(
            base_url=_get_openf1_base_url(),
            endpoint=collection,
            query_string=f'session_key={session_key}&date>={_to_timestring(curr_start)}&date<={_to_timestring(curr_end)}')

        if isinstance(df, polars.DataFrame):
            temp_df = polars.DataFrame(data=collection_batch)

            # Prefer vstack since we are appending many dataframes and not performing queries
            df = df.vstack(temp_df)
        else:
            df = polars.DataFrame(data=collection_batch)
            
        curr_start += delta
        curr_end += delta
    
    df = df.rechunk()

    return df


def _write_to_storage(dataframe: polars.DataFrame, url: str) -> None:
    """
    Writes the given dataframe with collection data to the given url
    """

    dataframe.write_parquet(url)


def _get_session_dates(session_key: int) -> tuple[datetime.datetime]:
    """
    Returns the dates for a session in the order (start, end)
    """

    session_content = _query_endpoint(
        base_url=_get_openf1_base_url(),
        endpoint='sessions',
        query_string=f'session_key={session_key}'
    )

    if len(session_content) == 0:
        # Session does not exist
        raise ValueError(f"Session with session key ${session_key} could not be found.")
    
    session = session_content[0]
    if 'date_start' not in session or 'date_end' not in session:
        # Improper schema
        raise ValueError(f"Start and end dates for session with session key ${session_key} could not be found.")
    
    return (
        _to_datetime(session['date_start']),
        _to_datetime(session['date_end'])
    )


def _query_endpoint(base_url: str, endpoint: str, query_string: typing.Optional[str] = None) -> list[dict[str, typing.Any]] | dict[str, typing.Any]:
    """
    Returns a Python object from a JSON endpoint
    """
    # Take query params as a string to allow for inequalities needed for OpenF1 API
    url = f'{_join_url(base_url, endpoint)}'

    if query_string is not None:
        url += f'?{query_string}'

    # Need User-Agent header to avoid being blocked by Multiviewer API
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1'
    }

    response = requests.get(url=url, headers=headers)

    return json.loads(response.content)


def _get_openf1_base_url() -> str:
    """
    Base address for the running OpenF1 service
    """

    # ADDRESS = os.getenv('OPENF1_ADDRESS', '0.0.0.0:8000')
    ADDRESS = '0.0.0.0:8000' # TODO: replace with environment variable

    return f'http://{ADDRESS}/v1'


def _get_multiviewer_base_url() -> str:
    """
    Base address for the Multiviewer service
    """

    return f'http://api.multiviewer.app/api/v1'


def _join_url(*args) -> str:
    """
    Credit to OpenF1 https://github.com/br-g/openf1/blob/9e497783662594093da3ae290226692315c2d8d2/src/openf1/util/misc.py#L11-L15
    Join URL parts with a forward slash
    """
    if any(len(e) == 0 or e is None for e in args):
        raise ValueError(f"Invalid URL components: {args}")
    return "/".join([e.strip("/") for e in args])


def _to_timedelta(x: typing.Union[str, datetime.timedelta]) \
        -> typing.Optional[datetime.timedelta]:
    """
    Credit to FastF1 for inspiration https://github.com/theOehrly/Fast-F1/blob/317bacf8c61038d7e8d0f48165330167702b349f/fastf1/utils.py#L120-L175

    Fast timedelta object creation from a time string

    Permissible string formats:

        For example: `13:24:46.320215` with:

            - optional hours and minutes
            - optional microseconds and milliseconds with
              arbitrary precision (1 to 6 digits)

        Examples of valid formats:

            - `24.3564` (seconds + milli/microseconds)
            - `36:54` (minutes + seconds)
            - `8:45:46` (hours, minutes, seconds)

    Args:
        x: timestamp
    """
    # this is faster than using pd.timedelta on a string
    if isinstance(x, str) and len(x):
        try:
            hours, minutes = 0, 0
            if len(hms := x.split(':')) == 3:
                hours, minutes, seconds = hms
            elif len(hms) == 2:
                minutes, seconds = hms
            else:
                seconds = hms[0]

            if '.' in seconds:
                seconds, msus = seconds.split('.')
                if len(msus) < 6:
                    msus = msus + '0' * (6 - len(msus))
                elif len(msus) > 6:
                    msus = msus[0:6]
            else:
                msus = 0

            return datetime.timedelta(
                hours=int(hours), minutes=int(minutes),
                seconds=int(seconds), microseconds=int(msus)
            )

        except Exception as exc:
            loguru.logger.debug(f"Failed to parse timedelta string '{x}'",
                          exc_info=exc)
            return None

    elif isinstance(x, datetime.timedelta):
        return x

    else:
        return None


def _to_datetime(x: typing.Union[str, datetime.datetime]) \
        -> typing.Optional[datetime.datetime]:
    """
    Credit to FastF1 for inspiration https://github.com/theOehrly/Fast-F1/blob/317bacf8c61038d7e8d0f48165330167702b349f/fastf1/utils.py#L178-L227

    Fast datetime object creation from a date string.

    Permissible string formats:

        '2020-12-13T13:27:15+00:00' with:

            - with optional UTC offset

    Args:
        x: timestamp
    """
    if isinstance(x, str):
        try:
            if '.' in x:
                return datetime.datetime.strptime(
                    x,
                    '%Y-%m-%dT%H:%M:%S.%f%z' # Have to use '%z' instead of '%:z' as recommended in the docs since it has not been implemented for strptime yet
                )
            return datetime.datetime.strptime(
                    x,
                    '%Y-%m-%dT%H:%M:%S%z'
                )
        
        except Exception as exc:
            loguru.logger.debug(f"Failed to parse datetime string '{x}'",
                          exc_info=exc)
            return None

    elif isinstance(x, datetime.datetime):
        return x

    else:
        return None


def _to_timestring(x: typing.Union[str, datetime.datetime]) \
        -> typing.Optional[str]:
    """
    Converts a datetime object into its string representation
    """
    if isinstance(x, datetime.datetime):
        try:
            return x.strftime(
                '%Y-%m-%dT%H:%M:%S.%f%:z'
            )

        except Exception as exc:
            loguru.logger.debug(f"Failed to convert datetime to string '{x}'",
                          exc_info=exc)
            return None

    elif isinstance(x, str):
        return x

    else:
        return None
    

if __name__ == "__main__":
    app()
