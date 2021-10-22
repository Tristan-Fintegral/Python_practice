import numpy as np
from matplotlib import pyplot

# create a shock vector

def generate_log_normal_shocks(vol, num_shocks=780):
    # log normal shock = exp(vol* N(0,1))
    # s1 = S0*(log normal shock)
    rand_norm_vector = np.random.normal(loc=0, scale=1, size=num_shocks)
    shock_vector = np.exp(vol*rand_norm_vector)

    return shock_vector

generate_log_normal_shocks(1,780)

new_shock = generate_log_normal_shocks(1,780)