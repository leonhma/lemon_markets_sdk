"""The entry point of all your scripts."""

import json
import time

import requests

from lemon_markets.config import (DEFAULT_AUTH_API_URL,                 # noqa
                                  DEFAULT_MONEY_DATA_REST_API_URL,
                                  DEFAULT_MONEY_REST_API_URL,
                                  DEFAULT_PAPER_DATA_REST_API_URL)
from lemon_markets.exceptions import LemonTokenException


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

    _client_ID: str
    _client_secret: str

    _access_token: str
    _access_token_type: str
    _access_token_expires: int

    _DATA_API_URL: str

    def __init__(self, client_id: str, client_secret: str,
                 trading_type: str = 'paper'):
        # sourcery skip: remove-unreachable-code
        """
        Initialize with client_id and client_secret.

        Parameters
        ----------
        client_id : str
            The id of your client
        client_secret : str
            The secret of your client
        trading_type : str, optional
            The type of trading to use, by default `paper`

        Raises
        ------
        Exception
            Raised because real-money trading is not available yet
        LemonTokenException
            Raised if the server responds with an invalid token type

        """
        self._client_ID = client_id
        self._client_secret = client_secret

        if trading_type.lower() == 'paper':
            self._DATA_API_URL = DEFAULT_PAPER_DATA_REST_API_URL
        elif trading_type.lower() == 'money':
            raise Exception('Real money trading is not available yet!')
            self._DATA_API_URL = DEFAULT_MONEY_DATA_REST_API_URL

        self._request_access_token()

    def _request_access_token(self):
        data = {"client_id": self._client_ID,
                "client_secret": self._client_secret,
                "grant_type": "client_credentials"}
        response = requests.post(url=DEFAULT_AUTH_API_URL, data=data)
        response.raise_for_status()

        data = json.loads(response.content)

        self._access_token = data['access_token']
        self._access_token_type = data['token_type']
        if self._access_token_type not in ['bearer']:
            raise LemonTokenException('The access token is not of type bearer.')
        self._access_token_expires = int(
            time.time()) + data['expires_in'] - 60

    @property
    def access_token(self) -> str:
        """
        Temporary access token for the client.

        Returns
        -------
        str
            The access token

        """
        if time.time() > self._access_token_expires:
            self._request_access_token()

        return self._access_token

    @property
    def access_token_type(self) -> str:
        """
        Type of the access token.

        Returns
        -------
        str
            The type. Currently only `bearer`

        """
        if time.time() > self._access_token_expires:
            self._request_access_token()

        return self._access_token_type

    @property
    def _authorization(self) -> dict:
        """
        Temporary access token packaged in a dict like the client needs it for authorization.

        Returns
        -------
        dict
            The authorization dict (currently only of type `bearer`): {"Authorization": "Bearer " + self.access_token}

        """
        if self._access_token_type == 'bearer':
            token_string = 'Bearer ' + self.access_token
        else:
            raise LemonTokenException('The access token is not from type bearer.')

        return {'Authorization': token_string}
