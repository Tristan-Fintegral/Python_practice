import datetime
from datetime import date
from abc import ABC, abstractmethod
import QuantLib as ql
from QuantLib.QuantLib import PricingEngine

# TODO 1) Change American option to not inherit off European
# TODO 2) Consider adding a class below American and European, or moving code up to Option
# TODO 3) Switch Monte Carlo parameters to a named tuple and implement in European as well


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
        self.pricing_engine = self.validate_pricing_engine_input(pricing_engine)

    def validate_pricing_engine_input(self, pricing_engine_input):
        if pricing_engine_input not in [self.ANALYTICAL, self.MONTE_CARLO]:
            raise RuntimeError()        # TODO -> fill in error
        else:
            return pricing_engine_input

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
            steps = 1
            rng = "pseudorandom" # could use "lowdiscrepancy"
            numPaths = 10000 
            return ql.MCEuropeanEngine(process, rng, steps, requiredSamples=numPaths)
        else:
            raise RuntimeError()  # TODO ->

    def _price(self, spot, vol, rfr, div):
        bsm_process = self.bsm_process(
            spot=spot, vol=vol, rfr=rfr, div=div
        )

        engine = self.option_model(process=bsm_process)
        self.option_object.setPricingEngine(engine)
        return self.option_object.NPV()

    def price(self, market_data_object):
        # -> unpack market_data_object later into self._price
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


class AmericanOption(EuropeanOption):

    MONTE_CARLO = 'MONTE_CARLO'

    def __init__(
            self,
            asset_name,
            strike,
            maturity,
            earliest_date,
            pricing_engine=MONTE_CARLO
    ):
        super(EuropeanOption, self).__init__(
            asset_name=asset_name, strike=strike, maturity=maturity
        )
        self.pricing_engine = pricing_engine
        self.earliest_date = earliest_date
        self.mc_params = {'steps': 100, 'num_paths': 10000, 'rng': 'pseudorandom'}

    @property
    def exercise_type(self):
        return ql.AmericanExercise(to_ql_dt(self.earliest_date),to_ql_dt(self.maturity))

    def set_mc_params(self, steps=100, num_paths=10000, rng='pseudorandom'):
        mc_param_dict = {'steps': steps, 'num_paths': num_paths, 'rng': rng}
        self._mc_params = mc_param_dict

    def option_model(self, process):

        if self.pricing_engine == self.MONTE_CARLO:
            steps = self._mc_params['steps']
            rng = self._mc_params['rng']
            num_paths = self._mc_params['num_paths']
            return ql.MCAmericanEngine(process, rng, steps, requiredSamples=num_paths)
        elif self.pricing_engine == self.ANALYTICAL:
            return None


class AmericanCallOption(AmericanOption):
    @property
    def call_or_put(self):
        return ql.Option.Call



def main():
    asset_name = 'Asset'
    strike = 120
    maturity = datetime.date(2025, 11, 21)
    pricing_engine = 'MONTE_CARLO'

    euro_bin_call = EuropeanCallOption(
        asset_name=asset_name,
        strike=strike,
        maturity=maturity,
        pricing_engine='Nonsense'
    )

    amer_bin_call = AmericanCallOption(
        asset_name=asset_name,
        strike=strike,
        maturity=maturity,
        earliest_date=date.today()
    )

    print(euro_bin_call._price(spot=100, vol=0.1, rfr=0.02, div=0))
    print(amer_bin_call._price(spot=100, vol=0.1, rfr=0.02, div=0))



    


if __name__ == '__main__':
    main()
