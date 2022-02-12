from .config import _PAPER_TRADING_REST_URL, _TRADING_REST_URL
from .helpers.api_client import _ApiClient
from enum import Enum


class TradingType(Enum):
    PAPER = 'paper'
    MONEY = 'money'


class Client:
    """Class representing the base client for API access.
    It stores your auth token and should be the starting point of your program.

    Parameters
    ----------
    token : str
        A valid authentication key.
    trading_type : TradingType, default: TradingType.PAPER
        The type of trading to use.

    Attributes
    ----------
    access_token : str
        The auth token.

    """
    # TODO see if the default parameter field gets properly highlighted, else use :class:
    _token: str
    _TRADING_REST_URL: str

    def __init__(self, token: str,
                 trading_type: TradingType = TRADING_TYPE_PAPER):
        self._token = token

        if trading_type == 'paper':
            self._TRADING_REST_URL = _PAPER_TRADING_REST_URL
        elif trading_type == 'money':
            self._TRADING_REST_URL = _TRADING_REST_URL


    @property
    def access_token(self) -> str:
        """
        Temporary access token for the client.

        Returns
        -------
        str
            The access token

        """
        # TODO check token for validity

        return self._token

    def _auth_header(self, props: dict = None) -> dict:
        """
        Return a dict with the authorization header and the data passed to `props`

        Parameters
        ----------
        props : dict, optional
            Additional properties to add to the dict, by default `None`.
            An already existent Authorization header will be replaced.

        Returns
        -------
        dict
            The authorization dict: {...props, "Authorization": "Bearer " + self.access_token}

        """
        if not props:
            props = {}
        props['Authorization'] = f'Bearer {self.access_token}'

        return props
