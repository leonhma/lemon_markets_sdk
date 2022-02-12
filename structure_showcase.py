from lemon_markets.account import Account
from lemon_markets.client import TRADING_TYPE, Client
from lemon_markets.instrument import Instruments, INSTRUMENT_TYPE

client = Client('akdjbskvskjdhfkakaadas', TRADING_TYPE.PAPER)

# account
print('account----------------------')
account = Account(client)
print(vars(account))
print('-----------------------------')


