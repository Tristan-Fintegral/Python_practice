import unittest
import datetime
from instruments.equity.options import EuropeanCallOption
from instruments.equity.options import AmericanCallOption
from instruments.equity.options import AmericanOption


class TestOptions(unittest.TestCase):

    def test_euro_options_models(self):
        """ if model is not implemented, throw NotImplementedError """
        asset_name = 'Asset'
        strike = 120
        maturity = datetime.date(2025, 11, 21)

        with self.assertRaises(NotImplementedError):
            _ = EuropeanCallOption(
                asset_name=asset_name,
                strike=strike,
                maturity=maturity,
                pricing_engine='Test'
            )

    def test_amer_options_models(self):
        """ if model is not implemented, throw NotImplementedError """
        asset_name = 'Asset'
        strike = 120
        maturity = datetime.date(2025, 11, 21)

        with self.assertRaises(NotImplementedError):
            _ = AmericanCallOption(
                asset_name=asset_name,
                strike=strike,
                maturity=maturity,
                earliest_date=datetime.date.today(),
                pricing_engine='Test'
            )

    def test_amer_no_analytical(self):
        """ Check that American Option has no Analytical model, returns
            NotImplementedError """
        asset_name = 'Asset'
        strike = 120
        maturity = datetime.date(2025, 11, 21)

        with self.assertRaises(NotImplementedError):
            _ = AmericanCallOption(
                asset_name=asset_name,
                strike=strike,
                maturity=maturity,
                earliest_date=datetime.date.today(),
                pricing_engine=AmericanOption.ANALYTICAL
            )

    def test_mc_default_values(self):
        """ Check that American Option has no Analytical model, returns
                    NotImplementedError """
        asset_name = 'Asset'
        strike = 120
        maturity = datetime.date(2025, 11, 21)

        option_ret = AmericanCallOption(
            asset_name=asset_name,
            strike=strike,
            maturity=maturity,
            earliest_date=datetime.date.today(),
            pricing_engine=AmericanOption.MONTE_CARLO
        )

        ret = option_ret.mc_params

        expected_ret = {'steps': 100, 'num_paths': 10000, 'rng': 'pseudorandom'}

        self.assertDictEqual(ret,expected_ret, 'Expect MC paramater dictionaries'
                                               'to be equal')







