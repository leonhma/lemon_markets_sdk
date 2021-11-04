"""Module for working with instruments."""

from dataclasses import dataclass
from enum import Enum
from typing import List

from lemon_markets.account import Account
from lemon_markets.helpers.api_client import _ApiClient
from lemon_markets.trading_venue import TradingVenue


class InstrumentType(Enum):
    """
    Class for different instrument types.

    Attributes
    ----------
    STOCK
        Instrument of type stock
    BOND
        Of type bond
    FUND
        Of type fund
    WARRANT
        Of type warrant

    """

    STOCK = 'stock'
    BOND = 'bond'
    FUND = 'fund'
    WARRANT = 'warrant'


@dataclass()
class Instrument:
    """
    Represents an instrument.

    Attributes
    ----------
    isin : str
        The isin identifier of the instrument
    wkn : str
        The wkn identifier
    name : str
        The name of the instrument (company name + identifier when the company has multiple instruments)
    title : str
        The title of the instrument (company name)
    symbol : str
        The short symbol the instrument
    currency : str
        Abbreviation of the reported currency
    tradable : str
        Whether the instrument can be traded
    trading_venues : List[TradingVenue]
        Places where this instrument is traded

    Raises
    ------
    ValueError
        Raised if instrument type is not known

    """

    isin: str = None
    wkn: str = None
    name: str = None
    title: str = None
    type: str = None
    symbol: str = None
    trading_venues: List[TradingVenue] = None

    @classmethod
    def _from_response(cls, account: Account, data: dict):
        try:
            type_ = InstrumentType(data['type'])
        except (ValueError, KeyError):
            raise ValueError(f'Unexpected instrument type: {data["type"]}')
        venues = []
        api_client = _ApiClient(account)
        for res in data['venues']:
            vdata = api_client._request(f'venues?mic={res["mic"]}')['results'][0]
            venues.append(TradingVenue._from_response(account, vdata, res['currency'], res['tradable']))
        return cls(
            isin=data['isin'],
            wkn=data['wkn'],
            name=data['name'],
            title=data['title'],
            type=type_,
            symbol=data['symbol'],
            trading_venues=venues
        )


class Instruments(_ApiClient):
    """
    Class for searching instruments.

    Parameters
    ----------
    account: Account
        The account object

    """

    def __init__(self, account: Account):       # noqa
        super().__init__(account=account)

    def list_instruments(self, *args, **kwargs) -> List[Instrument]:
        """
        List all instruments with matching criteria.

        Note
        ----
        Don't call this method with no parameters given. It will fetch all
        available stocks, bonds, calls, etc. and take a very long time to return.

        Parameters
        ----------
        tradable : bool, optional
            Search for tradable instruments.
        search : str, optional
            A search term
        currency : str, optional
            A specific currency
        type : str, optional
            A type (`stock`, `bond`, `fund` or `warrant`)

        Returns
        -------
        List[Instrument]
            List of instruments matching your query

        """
        assert not args, 'Please supply the arguments with a keyword i.e. `tradable=True` instead of a positional `True`.'
        result_pages = self._request_paged('instruments/', params=kwargs)
        return [Instrument._from_response(self._account, res) for res in result_pages]
