from os import environ
from unittest import TestCase

from lemon_markets.account import Account
from lemon_markets.instrument import Instruments
from lemon_markets.market_data import OHLC
from pandas import DataFrame

client_id = environ.get('CLIENT_ID')
client_token = environ.get('CLIENT_TOKEN')


class _TestOHLC(TestCase):
    def setUp(self):
        try:
            account = Account(client_id, client_token)
            instruments = Instruments(account)
            instrument = instruments.list_instruments(search='tesla')[0]
            try:
                ohlc = OHLC(account)
                self.data = ohlc.get_data(instrument, 'D1')
            except Exception as e:
                self._ohlc_exception = e
        except Exception as e:
            self.skipTest(e)

    def skip_if_ohlc_failed(self):
        if not hasattr(self, 'data'):
            self.skipTest('OHLC data creation failed!')

    def test_create_ohlc(self):
        if not hasattr(self, 'data'):
            self.fail(self._ohlc_exception)

    def test_data_type(self):
        self.skip_if_ohlc_failed()
        self.assertIs(type(self.data), DataFrame)
