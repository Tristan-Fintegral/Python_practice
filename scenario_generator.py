"""
Module to produce shocks for risk factors.
"""

import numpy as np


def generate_log_normal_shocks(spot, vol, num_shocks=780):
    """Generate a vector of log normal shocks with given volatility.

    :param float vol: Volatility in standard units
    :param int num_shocks: Number of shocks to produce
    :return [int]: Vector of shocks
    """
    shock_vector = [vol]*num_shocks

    return shock_vector