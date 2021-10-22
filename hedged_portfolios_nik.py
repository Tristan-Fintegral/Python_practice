###########
import logging
import QuantLib as ql
import numpy as np
import option_price
import scenario_generator
from scenario_generator import generate_log_normal_shocks
from option_price import create_option
from option_price import create_bsm_process
from matplotlib import pyplot
import pla_stats


logger = logging.getLogger(__name__)

def hedging_example():
    """
    This example assumes:
    Portfolio = Call_Option(St) - k * Stock(St)
    Call_Option = Vanilla European Call (what strike?)
    PnL = Shocked PV - Base PV
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
    n_shocks = 300
    n_ratios = 20
    strike = 100
    maturity_date = ql.Date(15, 10, 2022)
    vol = 0.1
    rfr = 0.005
    div = 0
    payoff = option_price.CallOrPut.CALL
    shocks = generate_log_normal_shocks(vol=vol, num_shocks=n_shocks)
    process = create_bsm_process(base_spot, vol, rfr, div)
    simul_shocked_spots = base_spot*shocks
    k = [i for i in np.linspace(0,1,n_ratios)]

    base_call_option_an = create_option(
        strike=strike,
        maturity_date=maturity_date,
        process=process,
        pricer_type=option_price.PricerType.Analytical.name,
        payoff=payoff
    )
    an_base_call_option_npv = base_call_option_an.NPV()

    base_call_option_mc = create_option(strike=strike, maturity_date=maturity_date,
                                        process=process,
                                        pricer_type=option_price.PricerType.Monte_Carlo.name,
                                        payoff=payoff
                                        )
    mc_base_call_option_npv = base_call_option_mc.NPV()

    an_shocked_call_options_npvs =[]
    mc_shocked_call_options_npvs = []
    for i in simul_shocked_spots:
        an_shocked_call_option = create_option(
            strike=strike, maturity_date=maturity_date,
            process=create_bsm_process(i, vol, rfr, div),
            pricer_type=option_price.PricerType.Analytical.name, payoff=payoff
        )
        mc_shocked_call_option = create_option(
            strike=strike, maturity_date=maturity_date,
            process=create_bsm_process(i, vol, rfr, div),
            pricer_type=option_price.PricerType.Monte_Carlo.name, payoff=payoff
        )
        an_shocked_call_options_npvs.append(an_shocked_call_option.NPV())
        mc_shocked_call_options_npvs.append(mc_shocked_call_option.NPV())

    shocked_price_diff = [i - base_spot for i in simul_shocked_spots]
    an_option_pnl = [i - an_base_call_option_npv for i in an_shocked_call_options_npvs]
    mc_option_pnl = [i - mc_base_call_option_npv for i in mc_shocked_call_options_npvs]

    spearman_corr = []
    ks_test = []
    for k_i in k:
        logger.info(
            f"Calculate Analytical and Monte Carlo based PnLs with hedging ratio of {k_i}"
        )
        analytical_portfolio_pnl = [i - k_i*j for i, j in zip(an_option_pnl, shocked_price_diff)]
        monte_carlo_portfolio_pnl = [i - k_i*j for i, j in zip(mc_option_pnl, shocked_price_diff)]
        spearman_corr.append(pla_stats.pla_stats(analytical_portfolio_pnl,monte_carlo_portfolio_pnl).spearman_value)
        ks_test.append(pla_stats.pla_stats(analytical_portfolio_pnl,monte_carlo_portfolio_pnl).ks_value)

    fig = pyplot.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.scatter(k, ks_test)
    ax2.scatter(k, spearman_corr)

    ax1.set_title('Analytical Pnl vs Monte Carlo PnL')
    ax1.set_xlabel('Hedge Ratio')
    ax1.set_ylabel('KS Test')

    ax2.set_title('Analytical Pnl vs Monte Carlo PnL')
    ax2.set_xlabel('Hedge Ratio')
    ax2.set_ylabel('Spearman Correlation')
    pyplot.show()

    pass

if __name__ == '__main__':
    hedging_example()



