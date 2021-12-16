"""The entry point of all your scripts."""

from dataclasses import dataclass
from datetime import date, datetime
from lemon_markets.config import PAPER_TRADING_REST_URL, TRADING_REST_URL



class Account:
    """
    Represents an account's credentials.

    Attributes
    ----------
    access_token : str
        A currently valid access token
    access_token_type : str
        Type of the access token. Currently only `bearer`

    Raises
    ------
    Exception
        Raised because real-money trading is not available yet.
    LemonTokenException
        Raised if the server responded with an unknown
        authentication type.

    """

    _token: str

    created_at: datetime = None
    account_id: str = None
    firstname: str = None
    lastname: str = None
    email: str = None
    phone: str = None
    address: str = None
    billing_address: str = None
    billing_email: str = None
    billing_name: str = None
    billing_vat: str = None
    mode: str = None
    deposit_id: str = None
    client_id: str = None
    account_number: str = None
    iban_brokerage: str = None
    iban_origin: str = None
    bank_name_origin: str = None
    balance: float = None
    cash_to_invest: float = None
    cash_to_withdraw: float = None
    trading_plan: str = None
    data_plan: str = None
    tax_allowance: float = None
    tax_allowance_start: date = None
    tax_allowance_end: date = None

    _TRADING_REST_URL: str

    def __init__(self, token: str,
                 trading_type: str = 'paper'):
        # sourcery skip: remove-unreachable-code
        """
        Initialize with client_id and client_secret.

        Parameters
        ----------
        token : str
            A valid authentication key.
        trading_type : str, optional
            The type of trading to use, by default `paper`

        Raises
        ------
        Exception
            Raised because real-money trading is not available yet

        """
        self._token = token

        if trading_type.lower() == 'paper':
            self._TRADING_REST_URL = PAPER_TRADING_REST_URL
        elif trading_type.lower() == 'money':
            self._TRADING_REST_URL = TRADING_REST_URL

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

    def _authorize(self, props: dict = None) -> dict:
        """
        Return a dict with the authorization header and the data passed to `props`

        Parameters
        ----------
        props : dict, optional
            Additional properties to add to the dict, by default `None`

        Returns
        -------
        dict
            The authorization dict: {"Authorization": "Bearer " + self._access_token}

        """
        if not props:
            props = {}
        props['Authorization'] = f'Bearer {self.access_token}'

        return props
