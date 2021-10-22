import unittest

from .ctest_account import _TestAccount
from .ctest_instrument import _TestInstrument


def _suite():
    suite = unittest.TestSuite()
    suite.addTest(_TestInstrument())
    suite.addTest(_TestAccount())
    return suite


if __name__ == '__main__':
    runner = unittest.TextTestRunner()
    runner.run(_suite())
