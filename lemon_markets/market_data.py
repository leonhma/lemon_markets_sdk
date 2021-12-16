"""Module for accessing market data."""

from datetime import datetime
from typing import Union

from pandas import DataFrame

from lemon_markets.account import Account
from lemon_markets.helpers.api_client import _ApiClient
from lemon_markets.helpers.time_helper import parse_datetime
from lemon_markets.instrument import Instrument
from lemon_markets.trading_venue import TradingVenue


class OHLC(_ApiClient):
    """
    Class to access OHLC data.

    Parameters
    ----------
    account : Account
        The account object containing your credentials

    """

    def __init__(self, account: Account):
        super().__init__(account=account)

    def get_data(
            self, instrument: Instrument, x1: str, venue: TradingVenue = None,
            sorting: str = None, date_from: datetime = None,
            date_to: datetime = None, decimals: bool = None, as_df: bool = True) -> Union[dict, DataFrame, None]:
        """
        Get OHLC data on the specified instrument.

        Parameters
        ----------
        instrument : Instrument
            The instrument to get data on
        x1 : str
            The granularity of the data. Either `M1`, `H1` or `D1`
        venue : TradingVenue, optional
            The trading venue
        sorting : str, optional
            By default, the data is not ordered. Choose between `asc` (oldest to newest)
            or `desc` (newest to oldest).
        date_from : int | str, optional
            Limit the data to after this point in time. A timestamp or date in iso-string format.
        date_to : int | str, optional
            Limit the data to before this point in time. A timestamp or date in iso-string format.
        decimals : bool, optional
            Numbers format. Default is true.
        as_df : bool, optional
            Return the data as a pandas dataframe, `True` by default.

        Returns
        -------
        Union[dict, pandas.DataFrame, None]
            Either the raw json data (as a dict, in UTC timezone) or a pandas dataframe (timezone adjusted and -aware).
            If the response is empty (no data is available), `None` is returned.

        """
        endpoint = f'ohlc/{x1}/'
        params = {'isin': instrument.isin}
        if venue is not None:
            params['mic'] = venue.mic
        if sorting is not None:
            params['sorting'] = sorting
        if date_from is not None:
            params['from'] = date_from
        if date_to is not None:
            params['to'] = date_to
        if decimals is not None:
            params['decimals'] = decimals
        results = self._request(endpoint=endpoint, params=params)['results']       # TODO make it _request_paged

        if len(results) == 0:
            return None

        if not as_df:
            return results

        df = DataFrame(results)
        df['t'] = df['t'].apply(lambda t: parse_datetime(t))
        df.set_index('t', inplace=True)
        if sorting == 'desc':
            df.sort_index(ascending=False, inplace=True)
        else:
            df.sort_index(ascending=True, inplace=True)

        return df
