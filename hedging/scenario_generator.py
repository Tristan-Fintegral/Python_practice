"""
Module to produce shocks for risk factors.
"""
import numpy as np
from matplotlib import pyplot


def generate_log_normal_shocks(vol, num_shocks=780):
    """Generate a vector of log normal shocks with given volatility.

    Log shock = exp(vol * N(0,1))
    S1 = S0 * (Log shock)

    :param float vol: Volatility in standard units
    :param int num_shocks: Number of shocks to produce
    :return [int]: Vector of shocks
    """

    if vol < 0:
        raise TypeError(f"Vol must be zero or greater, not {vol}.")

    rand_norm_vector = np.random.normal(loc=0, scale=1, size=num_shocks)
    shock_vector = np.exp(vol * rand_norm_vector)

    return shock_vector



def main():
    shocks = generate_log_normal_shocks(vol=0.6, num_shocks=10000)
    rel_shocks = shocks + 1

    prices=[None]*len(shocks)
    prices[0]=1
    for i in range(1,len(shocks)):
        prices[i]=prices[i-1]*shocks[i-1]
    #X = np.linspace(0, len(shocks),10000)

    pyplot.plot(prices[0:500])
    pyplot.show()


if __name__ == '__main__':
    main()
