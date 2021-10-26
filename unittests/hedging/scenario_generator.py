import unittest
from unittest import mock
import numpy as np
from hedging.scenario_generator import generate_log_normal_shocks


class TestScenarioGeneration(unittest.TestCase):

    def test_generate_log_normal_shocks_zero_vol(self):
        """If volatiltiy is zero, except array of all ones."""
        ret = generate_log_normal_shocks(vol=0, num_shocks=100)
        expected_ret = np.ones(100)
        self.assertEqual(len(ret), 100, "Expect 100 returned shocks.")
        self.assertTrue(
            np.allclose(ret, expected_ret),
            "Expect equal numpy arrays."
        )

    def test_generate_log_normal_shocks_all_positive(self):
        """Test that there are no negative shocks even for extreme vol."""
        num_of_shocks = 100000
        ret = generate_log_normal_shocks(vol=100, num_shocks=num_of_shocks)
        pos_or_zero_ret = ret[ret >= 0]
        neg_ret = ret[ret < 0]
        self.assertEqual(
            len(pos_or_zero_ret), num_of_shocks, "Expect all pos or zero shocks."
        )
        self.assertEqual(
            len(neg_ret), 0, "Expect zero negative shocks."
        )

    def test_generate_log_normal_shocks_neg_vol_error(self):
        """Test that error is thrown on negative volatility."""
        with self.assertRaises(TypeError):
            _ = generate_log_normal_shocks(vol=-0.5, num_shocks=100)

    @mock.patch('hedging.scenario_generator.np.random.normal')
    def test_generate_log_normal_shocks_standard(self, mock_rand_normal):
        expected_ret = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        required_shock = np.log(expected_ret)
        mock_rand_normal.return_value = required_shock

        ret = generate_log_normal_shocks(vol=1, num_shocks=10)

        mock_rand_normal.assert_called_once_with(loc=0, scale=1, size=10)
        self.assertEqual(
            len(ret), len(expected_ret), "Expect 10 returned shocks."
        )
        self.assertTrue(
            np.allclose(ret, expected_ret), "Expect equal numpy arrays."
        )




if __name__ == '__main__':
    unittest.main()