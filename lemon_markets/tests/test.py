import unittest

from .ctest_account import _TestAccount
from .ctest_instrument import _TestInstrument, _TestInstruments


def _suite():
    suite = unittest.TestSuite()
    suite.addTest(_TestAccount())
    suite.addTest(_TestInstruments())
    suite.addTest(_TestInstrument())
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(_suite())
