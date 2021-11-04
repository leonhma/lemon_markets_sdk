from datetime import time, timedelta
from os import environ
from unittest import TestCase

from lemon_markets.account import Account
from lemon_markets.trading_venue import TradingVenue, TradingVenues

client_id = environ.get('CLIENT_ID')
client_token = environ.get('CLIENT_TOKEN')


class _TestVenues(TestCase):
    def setUp(self):
        try:
            self.account = Account(client_id, client_token)
            try:
                self.venues = TradingVenues(self.account)
            except Exception as e:
                self._venues_exception = e
        except Exception as e:
            self.skipTest(e)

    def skip_if_vens_failed(self):
        if not hasattr(self, 'venues'):
            self.skipTest('Venues creation failed!')

    def test_create_venues(self):
        if not hasattr(self, 'venues'):
            self.fail(self._venues_exception)

    def test_attr_venues_type(self):
        self.skip_if_vens_failed()
        self.assertIs(type(self.venues.trading_venues), list)

    def test_attr_venues_list_type(self):
        self.skip_if_vens_failed()
        self.assertIs(type(self.venues.trading_venues[0]), TradingVenue)


class _TestVenue(TestCase):
    def setUp(self):
        try:
            account = Account(client_id, client_token)
            venues = TradingVenues(account)
            try:
                self.venue = venues.trading_venues[0]
            except Exception as e:
                self._venue_exception = e
        except Exception as e:
            self.skipTest(e)

    def test_create_venues(self):
        if not hasattr(self, 'venue'):
            self.fail(self._venue_exception)

    def skip_if_ven_failed(self):
        if not hasattr(self, 'venue'):
            self.skipTest('Venue creation failed!')

    def test_attr_name_type(self):
        self.skip_if_ven_failed()
        self.assertIs(type(self.venue.name), str)

    def test_attr_title_type(self):
        self.skip_if_ven_failed()
        self.assertIs(type(self.venue.title), str)

    def test_attr_mic_type(self):
        self.skip_if_ven_failed()
        self.assertIs(type(self.venue.mic), str)

    def test_attr_open_days_type(self):
        self.skip_if_ven_failed()
        self.assertIs(type(self.venue.opening_days), list)

    def test_attr_open_days_list_type(self):
        self.skip_if_ven_failed()
        self.assertIs(type(self.venue.opening_days[0]), str)

    def test_attr_open_time_type(self):
        self.skip_if_ven_failed()
        self.assertIs(type(self.venue.opening_time), time)

    def test_attr_close_time_type(self):
        self.skip_if_ven_failed()
        self.assertIs(type(self.venue.closing_time), time)

    def test_attr_currency_type(self):
        self.skip_if_ven_failed()
        self.assertIs(type(self.venue.currency), type(None))

    def test_attr_tradable_type(self):
        self.skip_if_ven_failed()
        self.assertIs(type(self.venue.tradable), type(None))

    def test_prop_is_open_type(self):
        self.skip_if_ven_failed()
        self.assertIs(type(self.venue.is_open), bool)

    def test_prop_time_to_close_type(self):
        self.skip_if_ven_failed()
        self.assertIs(type(self.venue.time_until_close), timedelta)

    def test_prop_time_to_open_type(self):
        self.skip_if_ven_failed()
        self.assertIs(type(self.venue.time_until_open), timedelta)
