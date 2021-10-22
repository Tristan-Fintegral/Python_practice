
import QuantLib as ql
import datetime
from abc import ABC, abstractmethod

class Option(ABC):

    def __init__(self, name, strike, maturity):
        self.name=name 
        self.strike=strike
        self.maturity=maturity

    @property
    @abstractmethod
    def call_or_put(self):
        pass

    @property
    @abstractmethod
    def ex_type(self):
        pass

    @property
    @abstractmethod
    def payoff(self):
        pass

class EuropeanOption(Option, ABC):

    ANALYTICAL = 'ANALYTICAL'
    MONTE_CARLO = 'MONTE_CARLO'


    super(EuropeanOption, self).__init__(
            asset_name=asset_name, strike=strike, maturity=maturity
        )
        self.pricing_engine = pricing_engine

    @property
    def ex_type(self):
        return ql.EuropeanExercise(self.maturity)

    @property
    def payoff(self):
        return ql.PlainVanillaPayoff(self.call_or_put, self.strike)


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

    def option_model(self, process):
        if self.pricing_engine == self.ANALYTICAL:
            return ql.AnalyticEuropeanEngine(process)
        elif self.pricing_engine == self.MONTE_CARLO:
            return None



