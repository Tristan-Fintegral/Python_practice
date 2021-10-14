import numpy as np
import QuantLib as ql
from scipy import stats
import scenario_generator
import option_price
from matplotlib import pyplot
#  FOCUS -> Logging, clean code, doc strings, well thought out functions

def hedging_example():
    """
    This example assumes:
    Portfolio PV = Call_Option(St) - k * Stock(St)
    Call_Option = Vanilla European Call (what strike?)
    PnL = Shocked PV - Base PV
    PnL = [Call_Option(St) - k * Stock(St)] - [Call_Option(S0) - k * Stock(S0)]
    k = hedging ratio
    Stock value = spot

    Initial Spot = S0
    Underlying volatility = vol
    Number of simulations of spot price shocks = n_shocks
    Number of hedging ratios to test = n_ratios

    1) Simulate a set of spot prices
    2) Select a set of hedging ratios (0 to 1)
    3) For each hedging
        a) Calculate portfolio PnLs for n_shocks using analytical pricer
        b) Calculate portfolio PnLs for n_shocks using Monte Carlo pricer
        c) PLA test on the PnLs
            - KS test
            - Spearman Corr
    4) Plot KS test and Spearman Corr as a function of k
    :return:
    """
    base_spot = 100
    vol = 0.1
    strike = 100
    rfr = 0.05
    div = 0.01
    n_ratios=50
    ratios= np.linspace(0,1, n_ratios)
    shocks = scenario_generator.generate_log_normal_shocks(
        vol=vol, num_shocks=100
    )
    rand_spot = base_spot * shocks
    analytical_npvs=[]
    mc_npvs=[]
    spear_values=[]
    ks_values=[]

    for k in ratios:
        analytical_npvs = []
        mc_npvs = []
        for spot in rand_spot:
            proc = option_price.create_bsm_process(spot, vol, rfr, div)
            option = option_price.create_option(strike, ql.Date(15, 6, 2025), proc,
                                   pricer_type=option_price.PricerType.Analytical.name
                                   , payoff=option_price.CallOrPut.CALL)
            analytical_npvs.append(option.NPV())
            option = option_price.create_option(strike, ql.Date(15, 6, 2025), proc,
                                                pricer_type=option_price.PricerType.Monte_Carlo.name
                                                , payoff=option_price.CallOrPut.CALL)
            mc_npvs.append(option.NPV())
        analytical_portfolio=[]
        mc_portfolio=[]
        for i in range(0,len(analytical_npvs)):
            analytical_portfolio.append(analytical_npvs[i]-k*rand_spot[i])
            mc_portfolio.append(mc_npvs[i] - k * rand_spot[i])


        spear_values.append(stats.spearmanr(analytical_portfolio, mc_portfolio)[0])
        ks_values.append(stats.ks_2samp(analytical_portfolio, mc_portfolio)[0])

    # spear_values1=[]
    # ks_values1=[]
    # spear_values1.append(pla_tests.pla_tests(analytical_portfolio,mc_portfolio))
    # ks_values1.append(pla_tests.pla_tests(manalytical_portfolio, mc_portfolio))

    pyplot.scatter(spear_values, ks_values)
    pyplot.show()

if __name__ == '__main__':
    hedging_example()

