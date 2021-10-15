import logging
import QuantLib as ql
import option_price

logger = logging.getLogger(__name__)
'''
MAJOR ASSUMPTION: ALL RISKFACTORS ARE UNCORRELATED
Portfolio Class:
Contains:
    - Instruments, quantity
Methods:
    - Add or remove instruments
    - PV = sum(PV(instrument) * quantity)
    - Shocked PV = PV(with shocked market data) [assume only spot changes]

In hedging example
1) Create portfolio
2) Add instruments
3) Calculate base PV
4) Simulate market/ market shocks
5) Iterate through market shocks to calculate PV
6) Calculate PnLs

Instrument 1 -> EqSpot
Instrument 2 -> APPL stock, rfr, vol
APPL -> S0=120, vol=0.2
GOOG -> S0=100, vol=0.3
corr(APPL, GOOGL) = 0.3
Shocks(vol)

'''


class Instrument:

    def price(self):
        pass


class EuropeanOption:

    def __init__(self, asset, strike, maturity, option_type):
        self.asset = asset
        payoff = ql.PlainVanillaPayoff(option_type, strike)
        europeanExercise = ql.EuropeanExercise(maturity)
        self.vanilla_option = ql.VanillaOption(payoff, europeanExercise)

    def pricer(self, spot, vol, rfr, div):
        bsm_process = option_price.create_bsm_process(
            spot=spot, vol=vol, rfr=rfr, div=div
        )
        engine = ql.AnalyticEuropeanEngine(bsm_process)
        self.vanilla_option.setPricingEngine(engine)
        return self.vanilla_option.NPV()

    def price(self, market_data):
        eq_asset = market_data.equity_lookup(self.asset)
        return self.pricer(
            spot=eq_asset.eq_spot,
            vol=eq_asset.eq_vol,
            rfr=market_data.rfr,
            div=0
        )


class Stock:

    def __init__(self, asset):
        pass

    def price(self, market_data):
        return market_data.eq_spot


class Portfolio:

    def __init__(self):
        self.instrs = {}

    def add_instrument(self, instrument, quantity):
        self.instrs[instrument] = self.instrs.get(instrument, 0) + quantity

    def npv(self, market_data):
        total_pv = 0
        for instrument, quantity in self.instrs.items():
            instr_npv = instrument.price(market_data)
            position_npv = instr_npv * quantity
            total_pv = total_pv + position_npv

        return total_pv


class MarketData:

    def __init__(self, eq_spot, eq_vol, rfr):
        self.eq_spot = eq_spot
        self.eq_vol = eq_vol
        self.rfr = rfr


def main():
    mkt_data_obj = MarketData(eq_spot=100, eq_vol=0.1, rfr=0.01)
    my_portfolio = Portfolio()
    option = EuropeanOption(
        strike=100,
        maturity=ql.Date(15, 6, 2025),
        option_type=ql.Option.Call
    )
    option.price(market_data=mkt_data_obj)
    stock = Stock()
    my_portfolio.add_instrument(stock, 40)
    my_portfolio.add_instrument(option, -20)
    temp = 1


if __name__ == '__main__':
    main()
