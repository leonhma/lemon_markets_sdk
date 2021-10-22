"""Module for accessing market data."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Union

from pandas import DataFrame as DataFrame
from pandas import to_datetime

from lemon_markets.account import Account
from lemon_markets.helpers.api_client import _ApiClient
from lemon_markets.helpers.time_helper import datetime_to_timestamp_seconds
from lemon_markets.instrument import Instrument
from lemon_markets.trading_venue import TradingVenue


@dataclass()
class OHLC(_ApiClient):
    """
    Class to access OHLC data.

    Parameters
    ----------
    account : Account
        The account object containing your credentials

    """

    def __init__(self, account: Account):       # noqa
        super().__init__(account=account)

    def get_data(
            self, instrument: Instrument, venue: TradingVenue, x1: str,
            ordering: str = None, date_from: datetime = None,
            date_until: datetime = None, as_df: bool = True) -> Union[dict, DataFrame, None]:
        """
        Get OHLC data on the specified instrument.

        Parameters
        ----------
        instrument : Instrument
            The instrument to get data on
        venue : TradingVenue
            The trading venue
        x1 : str
            The granularity of the data. Either `M1`, `H1` or `D1`
        ordering : str, optional
            By default, the data is not ordered. Choose between "date" (oldest to newest) or "-date" (newest to oldest).
        date_from : datetime, optional
            Limit the data to after this point in time
        date_until : datetime, optional
            Limit the data to before this point in time
        as_df : bool, optional
            Return the data as a pandas dataframe, by default True

        Returns
        -------
        Union[dict, pandas.DataFrame, None]
            Either the raw response json data (as dict) or a pandas dataframe.
            If the response is empty (no data available) None is returned.

        """
        endpoint = f"trading-venues/{venue.mic}/instruments/{instrument.isin}/data/ohlc/{x1}/"
        params = {}
        if ordering is not None:
            params['ordering'] = ordering
        if date_from is not None:
            params['date_from'] = int(datetime_to_timestamp_seconds(date_from))
        if date_until is not None:
            params['date_until'] = int(datetime_to_timestamp_seconds(date_until))
        results = self._request(endpoint=endpoint, params=params)['results']       # TODO make it _request_paged

        if len(results) == 0:
            return None

        if not as_df:
            return results
        from_tz = timezone.utc
        to_tz = datetime.now().astimezone().tzinfo
        df = DataFrame(results)
        df['t'] = to_datetime(df['t'], unit='s').dt.tz_localize(from_tz).dt.tz_convert(to_tz)
        df.set_index('t', inplace=True)
        if ordering == '-date':
            df.sort_index(ascending=False, inplace=True)
        else:
            df.sort_index(ascending=True, inplace=True)

        return df
