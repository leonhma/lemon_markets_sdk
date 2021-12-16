# undocumented on rtd

import json
from typing import List
from lemon_markets.helpers.url import full_url

from lemon_markets.account import Account
from requests import request


class _ApiClient:
    def __init__(self, account: Account, endpoint: str = None):
        self._account = account
        self._endpoint = endpoint or self._account._TRADING_REST_URL

    # TODO not tested
    def _request_paged(self, endpoint, data_=None, params=None) -> List[dict]:

        # Keep requesting until there are no more pages
        next = None
        results = []


        while True:
            if next:
                data = self._request(next, data=data_, url_prefix=False)
            else:
                data = self._request(endpoint, data=data_, params=params)
            results += data['results']
            if data['next'] in [None, next]:
                break
            else:
                next = data['next']
        return results

    def _request(self, endpoint, method='GET', data=None, params=None, headers=None) -> dict:
        """
        Make a request to the API.

        Parameters
        ----------
        endpoint : str
            Either a relative URL that starts with a `/` or an absolute URL.
        method : str, optional
            HTTP method to use, by default `GET`
        data : dict, optional
            Data to send with the request, by default `None`
        params : dict, optional
            Query parameters to send with the request, by default `None`
        headers : dict, optional
            Headers to send with the request, by default `None`

        Returns
        -------
        dict
            The json response from the API.
        """
        url = full_url(self._endpoint, endpoint)
        headers = self._account._authorize(headers)

        res = request(method.upper(), url, data=data, params=params, headers=headers)
        res.raise_for_status()

        if method != 'DELETE':
            data = json.loads(res.content)
        return data
