# undocumented on rtd

import json
from typing import List

import requests
from lemon_markets.account import Account
from lemon_markets.exceptions import (LemonAPIException,
                                      LemonConnectionException)


class _ApiClient:

    def __init__(
            self, account: Account, endpoint: str = None, is_data: bool = False):
        self._account = account
        ep = self._account._DATA_API_URL if is_data else self._account._DEFAULT_API_URL
        self._endpoint = endpoint or ep

    def _request_paged(self, endpoint, data_=None, params=None) -> List[dict]:

        # Keep requesting until there are no more pages
        next = None
        results = []

        try:

            while True:

                if next is not None:
                    data = self._request(next, data=data_, url_prefix=False)
                else:
                    data = self._request(endpoint, data=data_, params=params)

                results += data['results']

                if data['next'] is None or data['next'] == next:
                    break
                else:
                    next = data['next']
        except requests.Timeout:
            raise LemonConnectionException(
                "Network Timeout on url: %s" % endpoint)

        return results

    def _request(
            self, endpoint, method='GET', data=None, params=None,
            url_prefix=True) -> dict:
        method = method.lower()
        url = self._endpoint+endpoint if url_prefix else endpoint
        headers = self._account._authorization

        try:
            if method == 'get':
                response = requests.get(
                    url=url, params=params, headers=headers)
            elif method == 'post':
                response = requests.post(
                    url=url, data=data, params=params, headers=headers)
            elif method == 'put':
                response = requests.put(url=url, headers=headers)
            elif method == 'patch':
                response = requests.patch(
                    url=url, data=data, params=params, headers=headers)
            elif method == 'delete':
                response = requests.delete(
                    url=url, params=params, headers=headers)
            else:
                raise ValueError('Unknown method: %r' % method)

        except requests.Timeout:
            raise LemonConnectionException("Network Timeout on url: %s" % url)

        response.raise_for_status()

        if response.status_code > 399:      # will this ever be triggered? raise_for_status takes care of this case, or not?
            raise LemonAPIException(
                status=response.status_code, errormessage=response.reason)

        if method != 'delete':
            data = json.loads(response.content)
        return data
