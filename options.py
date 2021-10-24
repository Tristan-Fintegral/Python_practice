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
        print("This is a test option")


class EuropeanOption(Option):
    def __init__(self, asset_name, strike, maturity, right_type):
        self.right_type = right_type
        super().__init__(asset_name=asset_name,
                         strike=strike,
                         maturity=maturity
                         )

    def option_object(self):
        exercise_type = ql.EuropeanExercise(self.maturity)
        return ql.VanillaOption(self.payoff, self.exercise_type)

    def exercise_type(self):
        return ql.EuropeanExercise(self.maturity)

    def payoff(self, payoff_type):
        binary = 'binary'
        vanilla = 'vanilla'
        payoff_types = [binary, vanilla]

        if payoff_type not in payoff_types:
            raise RuntimeError(f"payoff_type must be either 'binary' or 'vanilla'.")
        elif payoff_type == binary:
            return ql.CashOrNothingPayoff(self.right(self.right_type), self.strike, 1)
        elif payoff_type == vanilla:
            return ql.PlainVanillaPayoff(self.right(self.right_type), self.strike)

    def right(self, right_type):
        call = 'call'
        put = 'put'
        all_rights = [call, put]

        if right_type not in all_rights:
            raise RuntimeError(f"right_type must be either 'call' or 'put'.")
        elif right_type == call:
            return ql.Option.Call
        elif right_type == put:
            return ql.Option.Put

    def bsm_process(self, spot, vol, rfr, div):
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

    def process(self):
        process = self.bsm_process(spot=100, vol=0.1, rfr=0.02, div=0)
        return process

    def model(self):
        return ql.AnalyticEuropeanEngine(self.process)

    def price(self):
        self.option_object.setPricingEngine(self.model())
        return self.option_object.NPV()




def option_example():
    asset_name = 'aapl'
    strike = 100
    maturity = ql.Date(25, 10, 2025)
    spot = 100
    vol = 0.1
    rfr = 0.02
    div = 0.1
    right_type = 'call'
    payoff_type = 'vanilla'
    a = EuropeanOption(asset_name, strike, maturity, right_type)
    print(a.asset_name)
    print(a.maturity)
    print(a.strike)
    print(a.right(right_type))
    print(a.payoff(payoff_type))
    print(a.bsm_process(spot, vol, rfr, div))
    print(a.model())
    print(a.price())



if __name__ == '__main__':
    option_example()
