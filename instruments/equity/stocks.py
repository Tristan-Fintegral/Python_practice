"""
Create a class for storing stock holdings
"""
import logging
from instruments.instrument import BaseInstrument
from functools import lru_cache

logger = logging.getLogger(__name__)


class Stock(BaseInstrument):

    def __init__(self, asset_name, num_shares):
        super().__init__()
        self.asset_name = asset_name
        self.num_shares = num_shares

    @lru_cache(maxsize=128)
    def _price(self, spot, num_shares):
        print(self._price.cache_info())
        return num_shares * spot

    def price(self, market_data_object):
        asset = market_data_object.asset_lookup(self.asset_name)
        return self._price(spot=asset.spot, num_shares=self.num_shares)


def stock_example():
    stock_name = 'aapl'
    num_shares = 50
    aapl = Stock(stock_name,num_shares)
    print(f"I have {aapl.price()} of {stock_name} stock")

if __name__ == '__main__':
    stock_example()
