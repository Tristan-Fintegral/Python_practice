import numpy as np
import logging
import pla_stats
import scenario_generator
import options_t
from matplotlib import pyplot
import datetime

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
    asset_name = "Asset"
    base_spot = 100
    vol = 0.1
    strike = 100
    rfr = 0.05
    div = 0.05
    maturity = datetime.date(2025, 11, 21)
    mc_params = {"steps": 1, "num_paths": 10000, "rng": "pseudorandom"}

    n_ratios = 30
    ratios = np.linspace(0, 1, n_ratios)
    shocks = scenario_generator.generate_log_normal_shocks(vol=vol, num_shocks=100)
    rand_spot = base_spot * shocks

    option = options_t.EuropeanCallOption(
        asset_name=asset_name,
        strike=strike,
        maturity=maturity,
        pricing_engine=options_t.EuropeanOption.ANALYTICAL,
    )

    analytical_base_npv = option._price(base_spot, vol, rfr, div)

    option = options_t.EuropeanCallOption(
        asset_name=asset_name,
        strike=strike,
        maturity=maturity,
        pricing_engine=options_t.EuropeanOption.MONTE_CARLO,
        mc_params=mc_params
    )
    mc_base_npv = option._price(base_spot, vol, rfr, div)

    analytical_npvs = []
    mc_npvs = []
    for spot in rand_spot:
        # PV for analytical shocked, PV for MC shocked
        option = options_t.EuropeanCallOption(
            asset_name=asset_name,
            strike=strike,
            maturity=maturity,
            pricing_engine=options_t.EuropeanOption.ANALYTICAL,
        )

        analytical_npvs.append(option._price(spot, vol, rfr, div))

        option = options_t.EuropeanCallOption(
            asset_name=asset_name,
            strike=strike,
            maturity=maturity,
            pricing_engine=options_t.EuropeanOption.MONTE_CARLO,
            mc_params=mc_params
        )
        mc_npvs.append(option._price(spot, vol, rfr, div))

    fo_option_pnl = [x - analytical_base_npv for x in analytical_npvs]
    risk_option_pnl = [x - mc_base_npv for x in mc_npvs]

    sp_values = []
    kstest_values = []
    for k in ratios:
        logger.info(f"Calculating FO and Risk P&Ls with a hedge value of {k} ")
        fo_portfolio_pnl = [
            x - k * (y - base_spot) for x, y in zip(fo_option_pnl, rand_spot)
        ]
        risk_portfolio_pnl = [
            x - k * (y - base_spot) for x, y in zip(risk_option_pnl, rand_spot)
        ]
        sp_values.append(
            pla_stats.pla_stats(fo_portfolio_pnl, risk_portfolio_pnl).spearman_value
        )
        kstest_values.append(
            pla_stats.pla_stats(fo_portfolio_pnl, risk_portfolio_pnl).ks_value
        )

    fig = pyplot.figure()
    ax1 = fig.add_subplot(121)
    ax2 = fig.add_subplot(122)
    ax1.scatter(ratios, kstest_values)
    ax2.scatter(ratios, sp_values)

    ax1.set_title("FO Pnl vs Risk PnL")
    ax1.set_xlabel("Hedge Ratio")
    ax1.set_ylabel("KS Test")

    ax2.set_title("FO Pnl vs Risk PnL")
    ax2.set_xlabel("Hedge Ratio")
    ax2.set_ylabel("Spearman Correlation")
    pyplot.show()


if __name__ == "__main__":
    hedging_example()
