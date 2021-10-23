import logging
from datetime import datetime
from os.path import join
from tempfile import gettempdir

__version__ = '0.4.0a1'


logging.basicConfig(
    filename=join(gettempdir(),
                  f'lemon_markets_{datetime.now().strftime("%d-%m-%Y-%H-%M-%S")}.log'),
    format='%(asctime)s:%(levelname)s:%(name)s:%(message)s', level=logging.DEBUG)
