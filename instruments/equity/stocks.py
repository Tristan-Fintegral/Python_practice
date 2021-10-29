"""
Create a class for storing stock holdings
"""
import logging
from instruments.instrument import BaseInstrument
from market_data import market_base
from market_data import asset_data

logger = logging.getLogger(__name__)


class Stock(BaseInstrument):

    def __init__(self, asset_name, num_shares):
        super().__init__()
        self.asset_name = asset_name
        self.num_shares = num_shares
        self.price_cache = {}

    def _price(self, spot, num_shares):
        if (spot, num_shares) in self.price_cache:
            logger.info(
                f'Fetching price for spot {spot} and '
                f'num_shares {num_shares} from cache.'
            )
            calc_price = self.price_cache[(spot, num_shares)]
        else:
            logger.info(
                f'Calling price with spot {spot} and num_shares {num_shares}.'
            )
            calc_price = num_shares * spot
            self.price_cache[(spot, num_shares)] = calc_price
        return calc_price

    def price(self, asset_data):
        '''
        To use the price method I need to input asset data
        I need to create a MarketDataObject (my mdo below)
        I pass the add_asset_data method to add my input data into the asset_data that we want to lookup
        Then i can use the asset_lookup method to lookup for my spot price
        '''
        mdo = market_base.MarketDataObject()
        mdo.add_asset_data(asset_data=asset_data)
        asset_data = mdo.asset_lookup(self.asset_name)
        return self._price(spot=asset_data.spot, num_shares=self.num_shares)


def stock_example():
    stock_name = 'aapl'
    num_shares = 50
    my_asset_data = asset_data.EquityAssetMarketData(
        asset_name=stock_name, spot=100000, volatility=0.1
    )
    aapl = Stock(stock_name,num_shares)
    print(f"I have {aapl.price(my_asset_data)} of {stock_name} stock")

if __name__ == '__main__':
    stock_example()
