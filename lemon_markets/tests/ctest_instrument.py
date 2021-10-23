from os import environ
from unittest import TestCase

from lemon_markets.account import Account
from lemon_markets.instrument import Instrument, Instruments

client_id = environ.get('CLIENT_ID')
client_token = environ.get('CLIENT_TOKEN')


class _TestInstruments(TestCase):
    def setUp(self):
        try:
            self.account = Account(client_id, client_token)
            try:
                self.instruments = Instruments(self.account)
            except Exception as e:
                self._instruments_exception = e
        except Exception as e:
            self.skipTest(e)

    def skip_if_instrs_failed(self):
        if not hasattr(self, 'instruments'):
            self.skipTest('Instuments creation failed!')

    def test_create_instruments(self):
        if not hasattr(self, 'instruments'):
            self.fail(self._instruments_exception)

    def test_list_return_type(self):
        self.skip_if_instrs_failed()
        self.assertIs(type(self.instruments.list_instruments(search='tesla')), list)

    def test_instrument_type(self):
        self.skip_if_instrs_failed()
        self.assertIs(type(self.instruments.list_instruments(search='tesla')[0]), Instrument)


class _TestInstrument(TestCase):
    def setUp(self):
        try:
            self.account = Account(client_id, client_token)
            self.instruments = Instruments(self.account)
            try:
                self.instrument = self.instruments.list_instruments(search='tesla')[0]
            except Exception as e:
                self._instrument_exception = e
        except Exception as e:
            self.skipTest(e)

    def skip_if_instr_failed(self):
        if not hasattr(self, 'instrument'):
            self.skipTest('Instrument creation failed!')

    def test_create_instrument(self):
        if not hasattr(self, 'instrument'):
            self.fail(self._instrument_exception)

    def test_attr_isin_type(self):
        self.skip_if_instr_failed()
        self.assertIs(type(self.instrument.isin), str)

    def test_attr_wkn_type(self):
        self.skip_if_instr_failed()
        self.assertIs(type(self.instrument.wkn), str)

    def test_attr_name_type(self):
        self.skip_if_instr_failed()
        self.assertIs(type(self.instrument.name), str)

    def test_attr_title_type(self):
        self.skip_if_instr_failed()
        self.assertIs(type(self.instrument.title), str)

    def test_attr_symbol_type(self):
        self.skip_if_instr_failed()
        self.assertIs(type(self.instrument.symbol), str)

    def test_attr_trading_venues_type(self):
        self.skip_if_instr_failed()
        self.assertIs(type(self.instrument.trading_venues), list)
