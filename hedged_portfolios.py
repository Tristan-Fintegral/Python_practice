import numpy as np
import logging
import QuantLib as ql
from scipy import stats
import pla_stats
import scenario_generator
import option_price
from matplotlib import pyplot

#  FOCUS -> Logging, clean code, doc strings, well thought out functions

logger = logging.getLogger(__name__)


# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO

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
    n_ratios = 40
    ratios = np.linspace(0, 1, n_ratios)
    shocks = scenario_generator.generate_log_normal_shocks(
        vol=vol, num_shocks=200
    )
    rand_spot = base_spot * shocks

    proc = option_price.create_bsm_process(base_spot, vol, rfr, div)
    option = option_price.create_option(strike,
                                        ql.Date(15, 6, 2025),
                                        proc,
                                        pricer_type=option_price.PricerType.Analytical.name,
                                        payoff=option_price.CallOrPut.CALL
                                        )
    analytical_base_npv = option.NPV()
    option = option_price.create_option(strike,
                                        ql.Date(15, 6, 2025),
                                        proc,
                                        pricer_type=option_price.PricerType.Monte_Carlo.name,
                                        payoff=option_price.CallOrPut.CALL
                                        )
    mc_base_npv = option.NPV()

    sp_values = []
    kstest_values = []

    for k in ratios:
        logger.info(
            f"Calculating FO and Risk P&Ls with a hedge value of {k} "
        )
        analytical_npvs = []
        mc_npvs = []
        for spot in rand_spot:
            # PV for analytical shocked, PV for MC shocked
            proc = option_price.create_bsm_process(spot, vol, rfr, div)
            option = option_price.create_option(
                strike=strike,
                maturity_date=ql.Date(15, 6, 2025),
                process=proc,
                pricer_type=option_price.PricerType.Analytical.name,
                payoff=option_price.CallOrPut.CALL
            )
            analytical_npvs.append(option.NPV())

            proc = option_price.create_bsm_process(spot, vol, rfr, div)
            option = option_price.create_option(
                strike=strike,
                maturity_date=ql.Date(15, 6, 2025),
                process= proc,
                pricer_type=option_price.PricerType.Monte_Carlo.name,
                payoff=option_price.CallOrPut.CALL
            )
            mc_npvs.append(option.NPV())

        fo_option_pnl = [x - analytical_base_npv for x in analytical_npvs]

        risk_option_pnl = [x - mc_base_npv for x in mc_npvs]

        fo_portfolio_pnl = [x - k*(y-base_spot) for x, y in zip(fo_option_pnl, rand_spot)]

        risk_portfolio_pnl = [x - k*(y-base_spot) for x, y in zip(risk_option_pnl, rand_spot)]


        spear_values, ks_values = pla_stats.pla_stats(fo_portfolio_pnl, risk_portfolio_pnl)
        sp_values.append(spear_values)
        kstest_values.append(ks_values)

    pyplot.scatter(ratios, sp_values)
    pyplot.show()


if __name__ == '__main__':
    hedging_example()
