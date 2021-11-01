import datetime
from abc import ABC, abstractmethod
import QuantLib as ql
from datetime import date
from instruments.instrument import BaseInstrument
from QuantLib.QuantLib import Payoff, StrikedTypePayoff
from functools import lru_cache
import logging

logger = logging.getLogger(__name__)


def to_ql_dt(dt):
    return ql.Date(dt.day, dt.month, dt.year)


class Option(BaseInstrument, ABC):
    
    def __init__(self, asset_name, strike, maturity):
        super().__init__()
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

    @property
    @abstractmethod
    def valid_pricing_engines(self):
        raise NotImplementedError()

    def validate_pricing_engine_input(self, pricing_engine_input):
        if pricing_engine_input not in self.valid_pricing_engines:
            raise NotImplementedError("MODEL HAS NOT BEEN IMPLEMENTED")
        else:
            return pricing_engine_input

    def __eq__(self, other):

        equal_params = ["asset_name", "strike", "maturity"]
        option1_values = [self.__dict__[x] for x in equal_params]
        option2_values = [other.__dict__[x] for x in equal_params]

        return (
            option1_values == option2_values and self.__class__ == other.__class__
        )


class VanillaOption(Option, ABC):
    
    def __init__(self, asset_name, strike, maturity, mc_params=None):
        super(VanillaOption, self).__init__(
            asset_name=asset_name, strike=strike, maturity=maturity
        )
        self.mc_params = self.default_mc(mc_params)

    @property
    def pay_off_type(self):
        return ql.PlainVanillaPayoff(self.call_or_put, self.strike)

    def create_option_object(self):
        return ql.VanillaOption(self.pay_off_type, self.exercise_type)

    def default_mc(self, mc_param_input):
        if mc_param_input is None:
            return {"steps": 10, "num_paths": 10000, "rng": "pseudorandom"}
        else:
            return mc_param_input


class EuropeanOption(VanillaOption):

    ANALYTICAL = "ANALYTICAL"
    MONTE_CARLO = "MONTE_CARLO"

    def __init__(self, asset_name, strike, maturity, pricing_engine, mc_params=None):
        super(EuropeanOption, self).__init__(
            asset_name=asset_name, strike=strike, maturity=maturity, mc_params=mc_params
        )
        self.pricing_engine = self.validate_pricing_engine_input(pricing_engine)
        self.price_cache = {}

    @property
    def exercise_type(self):
        return ql.EuropeanExercise(to_ql_dt(self.maturity))

    @property
    def valid_pricing_engines(self):
        return [self.ANALYTICAL, self.MONTE_CARLO]

    def option_model(self, process):
        if self.pricing_engine == self.ANALYTICAL:
            return ql.AnalyticEuropeanEngine(process)
        elif self.pricing_engine == self.MONTE_CARLO:
            steps = self.mc_params["steps"]
            rng = self.mc_params["rng"]
            num_paths = self.mc_params["num_paths"]
            return ql.MCEuropeanEngine(process, rng, steps, requiredSamples=num_paths)

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
            ql.BlackConstantVol(today, ql.NullCalendar(), vol, ql.Actual365Fixed())
        )
        bsm_process = ql.BlackScholesMertonProcess(init_spot, div_ts, rfr_ts, vol_ts)
        return bsm_process

    def _price(self, spot, vol, rfr, div):
        # add code for call or put
        if (spot, vol, rfr, div, self.pricing_engine) in self.price_cache:
            logger.info(
                f'Fetching price for spot {spot} and '
                f'vol {vol} from cache with engine {self.pricing_engine}'
            )
            calc_price = self.price_cache[(spot, vol, rfr, div, self.pricing_engine)]
        else:
            logger.info(
                f'Calling price with spot {spot} and vol {vol} with engine {self.pricing_engine}.'
            )
            bsm_process = self.bsm_process(spot=spot, vol=vol, rfr=rfr, div=div)
            engine = self.option_model(process=bsm_process)
            self.option_object.setPricingEngine(engine)
            calc_price =  self.option_object.NPV()
            self.price_cache[(spot, vol, rfr, div, self.pricing_engine)] = calc_price
        return calc_price


    def price(self, market_data_object):

        asset = market_data_object.asset_lookup(self.asset_name)

        rfr = market_data_object.asset_lookup('rfr')
        return self._price(
            spot=asset.spot, vol=asset.volatility, rfr=rfr.interest_rate, div=0
        )


class AmericanOption(VanillaOption, ABC):

    MONTE_CARLO = "MONTE_CARLO"
    ANALYTICAL = "ANALYTICAL"

    def __init__(
        self,
        asset_name,
        strike,
        maturity,
        pricing_engine,
        earliest_date,
        mc_params=None,
    ):
        super(AmericanOption, self).__init__(
            asset_name=asset_name, strike=strike, maturity=maturity
        )
        self.pricing_engine = self.validate_pricing_engine_input(pricing_engine)
        self.mc_params = self.default_mc(mc_params)
        self.earliest_date = earliest_date

    @property
    def valid_pricing_engines(self):
        return [self.MONTE_CARLO, self.ANALYTICAL]

    @property
    def exercise_type(self):
        return ql.AmericanExercise(
            to_ql_dt(self.earliest_date), to_ql_dt(self.maturity)
        )

    def option_model(self, process):

        if self.pricing_engine == self.MONTE_CARLO:
            steps = self.mc_params["steps"]
            rng = self.mc_params["rng"]
            num_paths = self.mc_params["num_paths"]
            return ql.MCAmericanEngine(process, rng, steps, requiredSamples=num_paths)
        elif self.pricing_engine == self.ANALYTICAL:
            raise NotImplementedError(
                "ANALYTICAL MODEL IS NOT IMPLEMENTED WITH AMERICAN OPTIONS"
            )
        else:
            raise NotImplementedError

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
            ql.BlackConstantVol(today, ql.NullCalendar(), vol, ql.Actual365Fixed())
        )
        bsm_process = ql.BlackScholesMertonProcess(init_spot, div_ts, rfr_ts, vol_ts)
        return bsm_process

    def _price(self, spot, vol, rfr, div):
        bsm_process = self.bsm_process(spot=spot, vol=vol, rfr=rfr, div=div)

        engine = self.option_model(process=bsm_process)
        self.option_object.setPricingEngine(engine)
        return self.option_object.NPV()

    def price(self, market_data_object):
        # -> unpack market_data_object later into self._price
        return self._price(spot=100, vol=0.1, rfr=0.02, div=0)


class AmericanCallOption(AmericanOption):
    @property
    def call_or_put(self):
        return ql.Option.Call


class EuropeanCallOption(EuropeanOption):
    @property
    def call_or_put(self):
        return ql.Option.Call


class EuropeanPutOption(EuropeanOption):
    @property
    def call_or_put(self):
        return ql.Option.Put


def main():

    asset_name = "Asset"
    strike = 120
    maturity = datetime.date(2025, 11, 21)

    euro_call_1 = EuropeanCallOption(
        asset_name=asset_name,
        strike=strike,
        maturity=maturity,
        pricing_engine=EuropeanOption.ANALYTICAL)

    print(euro_call_1._price(spot=100, vol=0.1, rfr=0.02, div=0))


if __name__ == "__main__":
    main()
