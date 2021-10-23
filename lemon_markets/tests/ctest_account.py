from os import environ
from unittest import TestCase

from lemon_markets.account import Account

client_id = environ.get('CLIENT_ID')
client_token = environ.get('CLIENT_TOKEN')


class _TestAccount(TestCase):
    def setUp(self):
        try:
            self.account = Account(client_id, client_token)
        except Exception as e:
            self._account_exception = e

    def skip_if_acc_failed(self):
        if not hasattr(self, 'account'):
            self.skipTest('Account creation failed!')

    def test_create_account(self):
        if not hasattr(self, 'account'):
            self.fail(self._account_exception)

    def test_auth_token_type(self):
        self.skip_if_acc_failed()
        self.assertIs(type(self.account.access_token), str)

    def test_auth_header_type(self):
        self.skip_if_acc_failed()
        self.assertIs(type(self.account._authorization), dict)
