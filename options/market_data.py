"""
Create market data dictionary
that will be used to feed the process
used for pricing options
"""

import pandas as pd


class MarketData:
    def __init__(self, date, spot, vol, rfr, div):
        self.date = date
        self.spot = spot
        self.vol = vol
        self.rfr = rfr
        self.div = div

    @property
    def make_market_data(self):
        df = pd.DataFrame(
            data={
                "Spot": self.spot,
                "Volatility": self.vol,
                "Risk Free Rate": self.rfr,
                "Dividend": self.div
            },
            index=[self.date],
            columns=[
                "Spot",
                "Volatility",
                "Risk Free Rate",
                "Dividend"
            ]
        )
        return df


def test_data():
    date = "2020Q4"
    spot = 100,
    vol = 0.1,
    rfr = 0.02,
    div = 0
    my_data = MarketData(date, spot, vol, rfr, div)
    model_market_data = my_data.make_market_data
    print(model_market_data)
    print(model_market_data.loc[date, "Spot"])

if __name__ == '__main__':
    test_data()
