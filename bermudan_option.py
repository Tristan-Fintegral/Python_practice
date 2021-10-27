import QuantLib as ql
from european_option import EuropeanOption


class BermudanOption(EuropeanOption):
    def __init__(self, asset_name, strike, maturity, right, payoff, start_date=ql.Date().todaysDate()):
        super().__init__(
            asset_name=asset_name,
            strike=strike,
            maturity=maturity,
            right=right,
            payoff=payoff
        )
        self.start_date = start_date

    @property
    def starting_date(self):
        return self.start_date or ql.Date().todaysDate()

    @property
    def exercise_type(self):
        return ql.BermudanExercise(self.starting_date, self.maturity)

    @property
    def model(self):
        return ql.BinomialVanillaEngine(self.process, "crr", 200)