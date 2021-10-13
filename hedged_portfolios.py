import option_price
import scenario_generator
# TODO FOCUS -> Logging, clean code, doc strings, well thought out functions

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
    # TODO -> Tristan fill this out
    pass


if __name__ == '__main__':
    hedging_example()

