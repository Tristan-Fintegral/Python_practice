import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


class MarketData(ABC):

    def __init__(self, asset_name):
        self.asset_name = asset_name


class EquityAssetMarketData(MarketData):

    def __init__(self, asset_name, spot, volatility):
        super(EquityAssetMarketData, self).__init__(asset_name=asset_name)
        self.spot = spot
        self.volatility = volatility


class InterestRateMarketData(MarketData):

    def __init__(self, asset_name, interest_rate):
        super(InterestRateMarketData, self).__init__(asset_name=asset_name)
        self.interest_rate = interest_rate


class MarketDataObject:

    def __init__(self, scenario_date=None):
        self.scenario_date = scenario_date
        self.asset_data_store = {}

    def add_asset_data(self, asset_data):

        if asset_data.asset_name in self.asset_data_store.keys():
            overwritten_data = self.asset_data_store[asset_data.asset_name]
            logger.info(
                f'Overwriting asset market data {overwritten_data} '
                f'with asset name {asset_data.asset_name}.'
            )

        self.asset_data_store[asset_data.asset_name] = asset_data

    def asset_lookup(self, asset_name, error_if_missing=True):
        asset_data = self.asset_data_store[asset_name]
        if not asset_data:
            message = f'No asset {asset_name} found in asset data store.'
            if error_if_missing:
                raise KeyError(message)
            else:
                logger.warning(message)
        return asset_data


def main():
    eq_asset_md = EquityAssetMarketData(asset_name='example_stock', spot=100, volatility=0.1)
    ir_asset_md = InterestRateMarketData(asset_name='rfr', interest_rate=0.02)
    mdo = MarketDataObject()
    mdo.add_asset_data(asset_data=eq_asset_md)
    mdo.add_asset_data(asset_data=ir_asset_md)
    x = mdo.asset_lookup('example_stock')
    temp = 1

if __name__ == '__main__':
    main()