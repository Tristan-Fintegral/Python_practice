import QuantLib as ql
from european_option import EuropeanOption


class AmericanOption(EuropeanOption):
    def __init__(self, asset_name, strike, maturity, right, payoff, early_exercise=ql.Date().todaysDate()):
        super().__init__(
            asset_name=asset_name,
            strike=strike,
            maturity=maturity,
            right=right,
            payoff=payoff
        )
        self.early_exercise = early_exercise

    @property
    def earliest_date(self):
        return self.early_exercise or ql.Date().todaysDate()

    @property
    def exercise_type(self):
        return ql.AmericanExercise(self.earliest_date, self.maturity)

    @property
    def model(self):
        return ql.BinomialVanillaEngine(self.process, "crr", 200)

