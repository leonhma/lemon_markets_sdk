import unittest

from .ctest_account import _TestAccount
from .ctest_instrument import _TestInstrument, _TestInstruments
from .ctest_market_data import _TestOHLC
from .ctest_venues import _TestVenue, _TestVenues


def _suite():
    suite = unittest.TestSuite()
    suite.addTest(_TestAccount())
    suite.addTest(_TestInstruments())
    suite.addTest(_TestInstrument())
    suite.addTest(_TestVenues())
    suite.addTest(_TestVenue())
    suite.addTest(_TestOHLC())
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(_suite())
