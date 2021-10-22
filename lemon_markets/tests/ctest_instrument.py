from os import environ
from unittest import TestCase

from lemon_markets.account import Account
from lemon_markets.instrument import Instruments

client_id = environ.get('CLIENT_ID')
client_token = environ.get('CLIENT_TOKEN')


class _TestInstrument(TestCase):
    def setUp(self):
        try:
            self.account = Account(client_id, client_token)
        except Exception as e:
            self.skipTest(e)

    def test_search(self):
        instr = Instruments(self.account)
        tsla = instr.list_instruments(search='Tesla', type='stock')[0]
        self.assertEqual(tsla.isin, 'US88160R1014')
