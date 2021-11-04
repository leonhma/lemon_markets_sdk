"""Module for listing trading venues and their opening/closing times."""

from dataclasses import dataclass
from datetime import datetime, time, timedelta

from lemon_markets.account import Account
from lemon_markets.helpers.api_client import _ApiClient
from lemon_markets.helpers.time_helper import parse_datetime


class TradingVenues(_ApiClient):
    """
    Available trading venues.

    Attributes
    ----------
    trading_venues : list[TradingVenue]
        A list of all Trading venues.

    Parameters
    ----------
    account : Account
        Your auth data

    """

    trading_venues = None
    _account = None

    def __init__(self, account: Account):       # noqa
        _account = account
        super().__init__(account=_account)
        self.get_venues()

    def get_venues(self):
        """Load the list of trading venues."""
        data = self._request(endpoint='venues/')
        data_rows = data['results']
        self.trading_venues = [TradingVenue._from_response(
            self._account, data) for data in data_rows]


@dataclass()
class TradingVenue(_ApiClient):
    """
    A trading venue.

    Attributes
    ----------
    name : str
        The name of the venue.
    title : str
        The title of the venue.
    mic : str
        The mic identifier of the venue.
    opening_days : list[str]
        The days in the next month the venue has opened.
        Dates in the format `yyyy-mm-dd`.
    opening_time : datetime.time
        The timezone- and DST-adjusted time the venue opens.
    closing_time : datetime.time
        The timezone- and DST-adjusted time the venue closes.
    currency : str
        Only available if this venue is the property of an instrument,
        `None` otherwise. The currency the instrument is traded in with this venue.
    tradable : bool
        Only available if this venue is the property of an instrument,
        `None` otherwise. Whether the instrument is tradable.

    """

    name: str = None
    title: str = None
    mic: str = None
    opening_days: list = None
    opening_time: time = None
    closing_time: time = None
    currency: str = None
    tradable: bool = None
    _account: Account = None

    @classmethod
    def _from_response(cls, account, data: dict, currency: str = None, tradable: bool = None):
        return cls(
            _account=account,
            name=data['name'],
            title=data['title'],
            mic=data['mic'],
            opening_days=data['opening_days'],
            opening_time=parse_datetime(
                '2000-01-01T'+data['opening_hours']['start'],
                data['opening_hours']['timezone']
            ).time(),
            closing_time=parse_datetime(
                '2000-01-01T'+data['opening_hours']['end'],
                data['opening_hours']['timezone']
            ).time(),
            currency=currency,
            tradable=tradable
        )

    def __post_init__(self):            # noqa
        super().__init__(self._account)

    @property
    def is_open(self) -> bool:
        """
        Check if the venue is open.

        Returns
        -------
        bool
            `True` if the venue is currently open, `False` otherwise.

        """
        return self._request(f'venues?mic={self.mic}')['results'][0]['is_open']

    @property
    def time_until_close(self) -> timedelta:
        """
        Get time until the next 'close-event' of the venue.

        Returns
        -------
        timedelta
            The time until close.

        """
        data = self._request(f'venues?mic={self.mic}')['results'][0]
        for date in data['opening_days']:
            local_close = parse_datetime(
                date+'T'+data['opening_hours']['end'],
                data['opening_hours']['timezone']
                )
            local_now = datetime.now().astimezone()
            if local_now > local_close:
                continue
            return local_close - local_now

    @property
    def time_until_open(self) -> timedelta:
        """
        Get time until the next 'open-event' of the venue.

        Returns
        -------
        timedelta
            The time until open.

        """
        data = self._request(f'venues?mic={self.mic}')['results'][0]
        for date in data['opening_days']:
            local_open = parse_datetime(
                date+'T'+data['opening_hours']['start'],
                data['opening_hours']['timezone']
                )
            local_now = datetime.now().astimezone()
            if local_now > local_open:
                continue
            return local_open - local_now
