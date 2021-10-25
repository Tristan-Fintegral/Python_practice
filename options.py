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


class Option:
    def __init__(self, asset_name, strike, maturity):
        self.asset_name = asset_name
        self.strike = strike
        self.maturity = maturity


class EuropeanOption(Option):
    def __init__(self, asset_name, strike, maturity, right, payoff):
        super().__init__(
            asset_name=asset_name,
            strike=strike,
            maturity=maturity
        )
        self.right = self.validate_right(right)
        self.payoff = self.validate_payoff(payoff)

    @property
    def option_object(self):
        option_obj = ql.VanillaOption(self.payoff, self.exercise_type)
        return option_obj

    @property
    def exercise_type(self):
        return ql.EuropeanExercise(self.maturity)

    @staticmethod
    def validate_right(right_in):
        call = 'call'
        put = 'put'

        if right_in == call:
            return ql.Option.Call
        elif right_in == put:
            return ql.Option.Put
        else:
            raise RuntimeError(f"Right must be either 'call' or 'put', not {right_in}.")

    def validate_payoff(self, payoff_in):
        binary = 'binary'
        vanilla = 'vanilla'

        if payoff_in == binary:
            return ql.CashOrNothingPayoff(self.right, self.strike, 1)
        elif payoff_in == vanilla:
            return ql.PlainVanillaPayoff(self.right, self.strike)
        else:
            raise RuntimeError(f"Payoff_type must be either 'binary' or 'vanilla' and not {payoff_in}.")

    @staticmethod
    def bsm_process(spot, vol, rfr, div):
        init_spot = ql.QuoteHandle(ql.SimpleQuote(spot))
        today = ql.Date().todaysDate()
        rfr_ts = ql.YieldTermStructureHandle(
            ql.FlatForward(today, rfr, ql.Actual365Fixed())
        )
        div_ts = ql.YieldTermStructureHandle(
            ql.FlatForward(today, div, ql.Actual365Fixed())
        )
        vol_ts = ql.BlackVolTermStructureHandle(
            ql.BlackConstantVol(
                today, ql.NullCalendar(), vol, ql.Actual365Fixed()
            )
        )
        bsm_process = ql.BlackScholesMertonProcess(
            init_spot, div_ts, rfr_ts, vol_ts
        )
        return bsm_process

    @property
    def process(self):
        return self.bsm_process(spot=100, vol=0.1, rfr=0.02, div=0)

    @property
    def model(self):
        return ql.AnalyticEuropeanEngine(self.process)

    def price(self):
        option_obj = self.option_object
        option_obj.setPricingEngine(self.model)
        return option_obj.NPV()


def option_example():
    asset_name = 'aapl'
    strike = 100
    maturity = ql.Date(25, 10, 2025)
    a = EuropeanOption(asset_name, strike, maturity,'call', 'vanilla')
    print(f"The price of the European Vanilla Call Option is {format(a.price(), '.3f')}")
    b = EuropeanOption(asset_name, strike, maturity, 'put', 'vanilla')
    print(f"The price of the European Vanilla Put Option is {format(b.price(), '.3f')}")
    c = EuropeanOption(asset_name, strike, maturity, 'call', 'binary')
    print(f"The price of the European Binary Call Option is {format(c.price(), '.3f')}")
    d = EuropeanOption(asset_name, strike, maturity, 'put', 'binary')
    print(f"The price of the European Binary Put Option is {format(d.price(), '.3f')}")


if __name__ == '__main__':
    option_example()

