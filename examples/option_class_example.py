import datetime
from abc import ABC, abstractmethod
import QuantLib as ql


def to_ql_dt(dt):
    return ql.Date(dt.day, dt.month, dt.year)


class Option(ABC):

    def __init__(self, asset_name, strike, maturity):
        self.asset_name = asset_name
        self.strike = strike
        self.maturity = maturity
        self._option_object = None

    @property
    @abstractmethod
    def call_or_put(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def exercise_type(self):
        raise NotImplementedError()

    @property
    @abstractmethod
    def pay_off_type(self):
        raise NotImplementedError()

    @property
    def option_object(self):
        self._option_object = self._option_object or self.create_option_object()
        return self._option_object

    @abstractmethod
    def create_option_object(self):
        raise NotImplementedError()

    @abstractmethod
    def price(self, market_data_object):
        raise NotImplementedError()


class EuropeanOption(Option):

    ANALYTICAL = 'ANALYTICAL'
    MONTE_CARLO = 'MONTE_CARLO'

    def __init__(self, asset_name, strike, maturity, pricing_engine=ANALYTICAL):
        super(EuropeanOption, self).__init__(
            asset_name=asset_name, strike=strike, maturity=maturity
        )
        self.pricing_engine = pricing_engine

    @property
    def exercise_type(self):
        return ql.EuropeanExercise(to_ql_dt(self.maturity))

    @property
    def pay_off_type(self):
        return ql.PlainVanillaPayoff(self.call_or_put, self.strike)

    def create_option_object(self):
        return ql.VanillaOption(self.pay_off_type, self.exercise_type)

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

    def _price(self, spot, vol, rfr, div):
        bsm_process = self.bsm_process(
            spot=spot, vol=vol, rfr=rfr, div=div
        )

        engine = self.option_model(process=bsm_process)
        self.option_object.setPricingEngine(engine)
        return self.option_object.NPV()

    def price(self, market_data_object):
        # TODO -> unpack market_data_object later into self._price
        return self._price(spot=100, vol=0.1, rfr=0.02, div=0)


class EuropeanCallOption(EuropeanOption):

    @property
    def call_or_put(self):
        return ql.Option.Call


class EuropeanPutOption(EuropeanOption):

    @property
    def call_or_put(self):
        return ql.Option.Put


class EuropeanBinaryCallOption(EuropeanCallOption):

    @property
    def pay_off_type(self):
        return ql.CashOrNothingPayoff(self.call_or_put, self.strike, 1)


def main():
    asset_name = 'Asset'
    strike = 120
    maturity = datetime.date(2025, 11, 21)

    euro_bin_call = EuropeanBinaryCallOption(
        asset_name=asset_name,
        strike=strike,
        maturity=maturity
    )
    euro_bin_call.price('alex')


if __name__ == '__main__':
    main()
