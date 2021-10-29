import logging
import datetime
from instruments.equity import stocks
from market_data import asset_data, market_base

logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

INPUT_CACHE = {}


def caching_example():
    asset_name = 'TestAsset'
    base_spot = 100
    vol = 0.2
    rfr = 0.05

    stock_a = stocks.Stock(asset_name=asset_name, num_shares=10)
    stock_b = stocks.Stock(asset_name=asset_name, num_shares=10)

    mdo = market_base.MarketDataObject()
    eq_asset = asset_data.EquityAssetMarketData(
        asset_name=asset_name,
        spot=base_spot,
        volatility=vol
    )
    rfr_asset = asset_data.InterestRateAssetMarketData(
        asset_name='rfr', interest_rate=rfr
    )
    mdo.add_asset_data([rfr_asset, eq_asset])

    mdo2 = market_base.MarketDataObject()
    eq_asset = asset_data.EquityAssetMarketData(
        asset_name=asset_name,
        spot=2*base_spot,
        volatility=vol
    )
    rfr_asset = asset_data.InterestRateAssetMarketData(
        asset_name='rfr', interest_rate=rfr
    )
    mdo2.add_asset_data([rfr_asset, eq_asset])

    price_1 = stock_a.price(mdo)
    price_2 = stock_a.price(mdo)
    price_3 = stock_a.price(mdo2)

    stock_a.num_shares = 100

    price_4 = stock_a.price(mdo)
    price_5 = stock_a.price(mdo)
    price_6 = stock_a.price(mdo2)

    logger.info(f'Prices at 10 shares {price_1, price_2, price_3}.')
    logger.info(f'Prices at 100 shares {price_4, price_5, price_6}.')

    price_x = stock_b.price(mdo)

    TEMP = 1


def sum_list_cache(list_in):
    if list_in in INPUT_CACHE:
        logger.info(f'Fetching sum for list {list_in}.')
        sum_of_list = INPUT_CACHE[list_in]
    else:
        logger.info(f'Calculating sum for list {list_in}.')
        sum_of_list = sum(list_in)
        INPUT_CACHE[list_in] = sum_of_list
    return sum_of_list


def list_example():
    our_list = [1, 2, 3]
    sum = sum_list_cache(our_list)


if __name__ == '__main__':
    list_example()