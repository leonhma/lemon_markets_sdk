"""Module for managing spaces."""

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import List

from lemon_markets.account import Account
from lemon_markets.helpers.api_client import _ApiClient
from lemon_markets.helpers.time_helper import parse_datetime, timestamp


class SpaceType(Enum):
    """
    Class for different space types.

    Attributes
    ----------
    AUTO
        Automatic order execution
    MANUAL
        Manual order execution

    """
    AUTO = 'auto'
    MANUAL = 'manual'


@dataclass
class Space(_ApiClient):
    """
    Class representing a space.

    Attributes
    ----------
    cache_seconds : int
        The number of seconds after which the cache is invalidated. Defaults to 10 seconds.
    id : str
        The id of the space
    name : str
        The name of the space
    description : str
        The description of the space
    type : SpaceType
        The type of the space
    linked : str
        The linked spaces
    created_at : datetime
        The date and time the space was created
    risk_limit : float
        The risk limit of the space
    buying_power : float
        The buying power of the space
    earnings : float
        The earnings of the space
    backfire : float
        The backfire of the space


    Raises
    ------
    ValueError
        If the space type is invalid

    """  # TODO figure out what `linked` is
    # static properties of the space
    id: str
    created_at: datetime

    _latest_update: int = 0
    _cache: dict = None
    _account: Account = None
    _deleted = False

    cache_seconds: int = 10

    name = property(lambda self: self._get_space_cache()['name'])
    description = property(lambda self: self._get_space_cache()['description'])
    type = property(lambda self: self._get_space_cache()['type'])
    linked = property(lambda self: self._get_space_cache()['linked'])

    risk_limit = property(lambda self: self._get_space_cache()['risk_limit'])
    buying_power = property(lambda self: self._get_space_cache()['buying_power'])
    earnings = property(lambda self: self._get_space_cache()['earnings'])
    backfire = property(lambda self: self._get_space_cache()['backfire'])

    @classmethod
    def _from_response(cls, account: Account, data: dict):
        return cls(
            created_at=parse_datetime(data['created_at']),
            id=data['id'],
            _account=account
        )

    def __post_init__(self):
        super().__init__(account=self._account)

    def _update_space_cache(self):
        """Update the state of the space if it is older than `cache_seconds` seconds."""
        if self._deleted:
            raise ValueError('Space has been deleted')
        if timestamp() - self._latest_update > self.cache_seconds:
            print('updaring space cache')
            data = self._request(f'spaces/{self.id}')['results']
            try:
                type_ = SpaceType(data['type'])
            except (ValueError, KeyError):
                raise ValueError(f'Unexpected space type: {data["type"]}')
            self._cache = {
                'name': data['name'],
                'description': data['description'],
                'type': type_,
                'linked': data['linked'],
                'risk_limit': data['risk_limit'],
                'buying_power': data['buying_power'],
                'earnings': data['earnings'],
                'backfire': data['backfire']
            }
            self._latest_update = timestamp()

    def _get_space_cache(self) -> dict:
        """
        Get the state of the space.

        Returns
        -------
        dict
            The state of the space

        """
        self._update_space_cache()
        return self._cache

    def delete(self):
        if self._deleted:
            raise ValueError('Space has been deleted')
        """Delete the space."""
        self._request(f'spaces/{self.id}', method='DELETE', headers=self._account._authorize())
        del self

    def _alter(self, data: dict):
        if self._deleted:
            raise ValueError('Space has been deleted')
        """Alter the space."""
        data = self._request(f'spaces/{self.id}', method='PUT', data=data, headers=self._account._authorize())
        self._cache = self._parse(data['results'])
        self._latest_update = timestamp()

    @name.setter
    def name(self, name: str):
        """Set the name of the space."""
        self._alter({'name': name})

    @description.setter
    def description(self, description: str):
        """Set the description of the space."""
        self._alter({'description': description})

    @risk_limit.setter
    def risk_limit(self, risk_limit: float):
        """Set the risk limit of the space."""
        self._alter({'risk_limit': risk_limit})

    @linked.setter
    def linked(self, linked: str):
        """Set the linked spaces of the space."""
        self._alter({'linked': linked})


class Spaces(_ApiClient):
    def __init__(self, account: Account):
        super().__init__(account=account)

    def list_spaces(self, type: SpaceType = None) -> List[Space]:
        """
        List all spaces with matching criteria.

        Parameters
        ----------
        type : bool, optional
            Search for spaces of the specified type. See [the docs](https://docs.lemon.markets/spaces#automated-vs-manual-space) for more information.

        Returns
        -------
        List[Space]
            List of spaces matching your query

        """
        params = {}
        if type is not None:
            params['type'] = type.value
        result_pages = self._request_paged('spaces', params=params)
        return [Space._from_response(self._account, res) for res in result_pages]

    def get_space(self, id: str) -> Space:
        """
        Get a space by id.

        Parameters
        ----------
        id : str
            The id of the space

        Returns
        -------
        Space
            The space

        """
        data = self._request(f'spaces/{id}')
        return Space._from_response(self._account, data['results'])

    def create_space(self, name: str, type: SpaceType, risk_limit: float, description: str = None) -> Space:
        """
        Create a space.

        Parameters
        ----------
        name : str
            The name of the space
        type : SpaceType
            The type of the space
        risk_limit : float
            The risk limit of the space. In 1/1000 of your currency (so for 100 EUR risk limit, you should use 100000)
        description : str, optional
            The description of the space

        Returns
        -------
        Space
            The space

        """
        data = {
            'name': name,
            'type': type.value,
            'risk_limit': risk_limit
        }
        if description is not None:
            data['description'] = description

        data = self._request('spaces', method='POST', data=data, headers=self._account._authorize())
        return Space._from_response(self._account, data['results'])
