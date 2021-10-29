"""
Create a class for storing stock holdings
"""
from instruments.instrument import BaseInstrument


class Stock(BaseInstrument):

    def __init__(self, asset_name, num_shares):
        super().__init__()
        self.asset_name = asset_name
        self.num_shares = num_shares

    def price(self, spot):
        spot=100
        #asset = market_data_object.asset_lookup(self.asset_name)
        return self.num_shares * spot


def stock_example():
    stock_name = 'aapl'
    num_shares = 50
    aapl = Stock(stock_name,num_shares)
    print(f"I have {aapl.price(spot=100)} of {stock_name} stock")

if __name__ == '__main__':
    stock_example()
