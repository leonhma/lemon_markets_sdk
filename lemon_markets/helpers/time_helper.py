"""Various helper functions for dealing with time."""
from datetime import datetime
from time import time
from typing import Union

from dateutil.parser import parse
from pytz import timezone


def timestamp_seconds_to_datetime(ts: Union[int, float]) -> datetime:
    """
    Convert unix timestamp to datetime object.

    Parameters
    ----------
    ts : Union[int, float]
        The timestamp to convert

    Returns
    -------
    datetime
        The corresponding datetime object

    """
    return datetime.fromtimestamp(ts).astimezone()


def datetime_to_timestamp_seconds(dt: datetime) -> float:
    """
    Convert datetime to unix timestamp.

    Parameters
    ----------
    dt : datetime
        The datetime object

    Returns
    -------
    float
        The unix timestamp

    """
    return int(dt.timestamp())


def timestamp_milliseconds_to_datetime(ts: Union[int, float]) -> datetime:
    """
    Convert posix milliseconds timestamp to datetime object.

    Parameters
    ----------
    ts : Union[int, float]
        The timestamp in milliseconds to convert

    Returns
    -------
    datetime
        The corresponding datetime object

    """
    return datetime.fromtimestamp(ts / 1000).astimezone()


def datetime_to_timestamp_milliseconds(dt: datetime) -> float:
    """
    Convert datetime to posix milliseconds timestamp.

    Parameters
    ----------
    dt : datetime
        The datetime object

    Returns
    -------
    float
        The posix milliseconds timestamp

    """
    return int(dt.timestamp() * 1000)


def current_time() -> datetime:
    """Return timezone-aware current time as datetime."""
    return datetime.now().astimezone()


def time(year: int = datetime.now().year,
         month: int = datetime.now().month,
         day: int = datetime.now().day,
         hour: int = datetime.now().hour,
         minute: int = datetime.now().minute,
         second: int = datetime.now().second) -> datetime:
    """Return the current datetime in local timezone."""
    return datetime(year=year,
                    month=month,
                    day=day,
                    hour=hour,
                    minute=minute,
                    second=second).astimezone()


def parse_datetime(datestring: str, tzfallback: str = 'UTC') -> datetime:
    """
    Parse the timezone-aware datetime from a string.

    Parameters
    ----------
    datestring : str
        The string to parse.
    tzfallback : str, optional
        The timezone to use if none is present in the datestring, by default `UTC`.

    Returns
    -------
    datetime
        The timezone-aware datetime parsed from the string.

    """
    time = parse(datestring)
    if not time.tzinfo:
        time = timezone(tzfallback).localize(time)
    return time.astimezone()


def timestamp() -> int:
    """Return the current timestamp in seconds. Not meant to be used as timezone-aware."""
    return int(time().timestamp())
