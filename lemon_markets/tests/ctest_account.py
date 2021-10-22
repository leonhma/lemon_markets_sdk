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
            self.fail(e)

    def test_token_type(self):
        self.assertEqual(
            self.account.access_token_type, 'bearer',
            'Incorrect acount token type.')

    def test_auth_header(self):
        self.assertIs(type(self.account._authorization), dict)
