import unittest
import datetime
from hedging import portfolio_object
from unittest.mock import MagicMock


class TestPortfolio(unittest.TestCase):

    def setUp(self):
        self.pvs = [10, 20, 30]
        self.quantities = [10, 20, 30]
        self.instruments = [MagicMock() for pv in self.pvs]
        for i, _ in enumerate(self.instruments):
            self.instruments[i].price.return_value = self.pvs[i]
        self.market_data_object = MagicMock()

    def test_price_one_deal(self):
        """Test the pricing of a portfolio with one deal."""

        portfolio_A = portfolio_object.Portfolio()
        portfolio_A.create_deal(instrument=self.instruments[0], quantity=self.quantities[0])

        actual = portfolio_A.price(self.market_data_object)
        expected = 100
        self.assertEqual(expected, actual)


class TestDeal(unittest.TestCase):

    def test_deal_repr(self):
        """ if model is not implemented, throw NotImplementedError """
        instrument = 'Option'
        quantity = 10

        deal = portfolio_object.Deal(
            instrument=instrument,
            quantity=quantity,
            creation_time=datetime.datetime(2021, 10, 21, 10, 0, 0)
        )
        # check representation matches expected value
        actual = deal.__repr__()
        expected = 'Deal(instrument=Option, quantity=10, counterparty=Unknown, creation_time=2021-10-21 10:00:00)'
        self.assertEqual(expected, actual)
