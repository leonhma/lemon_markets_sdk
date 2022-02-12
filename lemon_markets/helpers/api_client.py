# undocumented on rtd

import json
from typing import List
from lemon_markets.helpers.url import full_url

from lemon_markets.client import Client
from requests import request


class _ApiClient:
    def __init__(self, client: Client, endpoint: str = None):
        self._client = client
        self._endpoint = endpoint or self._client._TRADING_REST_URL

    # TODO not tested
    def _request_paged(self, endpoint, params=None) -> List[dict]:
            # TODO docstring
        # Keep requesting until there are no more pages
        next = None
        results = []


        while True:
            if next:
                data = self._request(next, url_prefix=False)
            else:
                data = self._request(endpoint, params=params)
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
            Either relative to the endpoint or absolute.
        method : str, optional
            HTTP method to use, by default `GET`
        data : dict, optional
            Data to send with the request (POST and PUT), by default `None`
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
        headers = self._client._authorize(headers)

        res = request(method.upper(), url, data=data, params=params, headers=headers)
        res.raise_for_status()

        if method != 'DELETE':
            data = json.loads(res.content)
        return data
