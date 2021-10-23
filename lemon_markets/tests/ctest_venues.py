from os import environ
from unittest import TestCase

from lemon_markets.account import Account
from lemon_markets.trading_venue import TradingVenues, TradingVenue

client_id = environ.get('CLIENT_ID')
client_token = environ.get('CLIENT_TOKEN')
