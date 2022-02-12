from lemon_markets.client import Client
from .helpers.api_client import _ApiClient
from .helpers.time_helper import parse_datetime
from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class Account(_ApiClient):
    # TODO docstring
    """
    Represents an account's personal data.

    Parameters
    ----------
    client : Client
        The client to use.

    Attributes
    ----------
    created_at : datetime.datetime
    account_id : str
    firstname : str
    lastname : str
    email : str
    phone : str
    address : str
    billing_address : str
    billing_email : str
    billing_name : str
    billing_vat : str
    mode : str
    deposit_id : str
    client_id : str
    account_number : int
    iban_brokerage : str
    iban_origin : str
    bank_name_origin : str
    balance : float
    cash_to_invest : float
    cash_to_withdraw : float
    trading_plan : str
    data_plan : str
    tax_allowance : float
    tax_allowance_start : datetime.date
    tax_allowance_end : datetime.date

    """
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
    account_number: int = None
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

    def __init__(self, client: Client) -> None:
        super().__init__(client)

        res = self._request('account')['results']

        for property in ['account_id', 'firstname', 'lastname', 'email', 'phone', 'address', 'billing_address', 'billing_email', 'billing_name', 'billing_vat', 'mode', 'deposit_id', 'client_id', 'iban_brokerage', 'iban_origin', 'bank_name_origin', 'trading_plan', 'data_plan']:
            self[property] = res[property]
        
        for property in ['balance', 'cash_to_invest', 'cash_to_withdraw', 'tax_allowance']:
            self[property] = float(res[property])
        
        for property in ['tax_allowance_start', 'tax_allowance_end']:
            self[property] = date.fromisoformat(res[property])

        self.created_at = parse_datetime(res['created_at'])
