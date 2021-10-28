"""
Options common characteristics:
asset name, strike, maturity

Options can differ in:
i. exercise type:
European (exercise at expiry)
American (exercise at any time)
Bermudan (exercise at specific days)

ii. payoff type:
Binary, Vanilla

iii. right type:
call, put
"""

import QuantLib as ql
from european_option import EuropeanOption
from american_option import AmericanOption
from bermudan_option import BermudanOption
import market_data


def option_example():
    asset_name = 'aapl'
    strike = 100
    maturity = ql.Date(25, 10, 2025)
    a = EuropeanOption(asset_name, strike, maturity, 'call', 'vanilla')
    print(f"The price of the European Vanilla Call Option is {format(a.price(), '.3f')}")
    b = EuropeanOption(asset_name, strike, maturity, 'put', 'vanilla')
    print(f"The price of the European Vanilla Put Option is {format(b.price(), '.3f')}")
    c = EuropeanOption(asset_name, strike, maturity, 'call', 'binary')
    print(f"The price of the European Binary Call Option is {format(c.price(), '.3f')}")
    d = EuropeanOption(asset_name, strike, maturity, 'put', 'binary')
    print(f"The price of the European Binary Put Option is {format(d.price(), '.3f')}")
    e = AmericanOption(asset_name, strike, maturity, 'call', 'vanilla')
    print(f"The price of the American Vanilla Call Option is {format(e.price(), '.3f')}")
    f = AmericanOption(asset_name, strike, maturity, 'put', 'vanilla')
    print(f"The price of the American Vanilla Put Option is {format(f.price(), '.3f')}")
    print("=="*35)
    print("Cannot price a Bermudan option as I cannot find the right engine!")
    print("==" * 35)
    my_data = a.get_market_data()
   # my_data.loc[, "Spot"]
    #print(my_data)


if __name__ == '__main__':
    option_example()

