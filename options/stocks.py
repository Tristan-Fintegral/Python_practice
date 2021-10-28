"""
Create a class for storing stock holdings
"""


class Stock:
    def __init__(self, stock_name, num_shares):
        self.stock_name = stock_name
        self.num_shares = num_shares

    def price(self, spot=100):
        return self.num_shares * spot


def stock_example():
    stock_name = 'aapl'
    num_shares = 50
    aapl = Stock(stock_name,num_shares)
    print(f"I have {aapl.price()} of {stock_name} stock")


if __name__ == '__main__':
    stock_example()
