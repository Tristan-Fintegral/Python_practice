import enum
import logging
import QuantLib as ql
from matplotlib import pyplot
import scenario_generator

logger = logging.getLogger(__name__)

class OptionPricerType:
    ANALYTICAL = 'Analytical'
    MONTE_CARLO = 'Monte Carlo'
    A_THIRD_PRICER = 'Pricer Three'
    ALL_PRICERS = [ANALYTICAL, MONTE_CARLO, A_THIRD_PRICER]


class CallOrPut:
    CALL = 'Call'
    PUT = 'Put'
    ALL_TYPES = [CALL, PUT]


class PricerType(enum.Enum):
    Analytical = 1
    Monte_Carlo = 2
    Third = 3


def create_bsm_process(spot, vol, rfr, div):
    """
    This function creates BSM process given market values

    :param float div: flat forward dividend rate using actual/365 fixed
    :param int spot: spot price
    :param float vol: volatility
    :param float rfr: flat forward risk free rate using actual/365 fixed
    :return BlackScholesMertonProcess: Market data process
    """
    logger.info(
        f"Starting bsm process with spot: {spot}, vol: {vol}, "
        f"rfr: {rfr} and dividend rate: {div}."
    )

    if spot < 0:
        logger.warning(f"Expected spot price >=0, received {spot}.")

    initialValue = ql.QuoteHandle(ql.SimpleQuote(spot))
    today = ql.Date().todaysDate()
    riskFreeTS = ql.YieldTermStructureHandle(
        ql.FlatForward(today, rfr, ql.Actual365Fixed())
    )
    dividendTS = ql.YieldTermStructureHandle(
        ql.FlatForward(today, div, ql.Actual365Fixed())
    )
    volTS = ql.BlackVolTermStructureHandle(
        ql.BlackConstantVol(today, ql.NullCalendar(), vol, ql.Actual365Fixed())
    )
    bsm_process = ql.BlackScholesMertonProcess(
        initialValue, dividendTS, riskFreeTS, volTS
    )
    return bsm_process


def create_option(
        strike, maturity_date, process, pricer_type=None, payoff=None
):
    """
    This function creates call option using BSM pricer
    created by create_bsm_process with strike price and maturity date. This
    function uses an analytical approach

    :param int strike: strike price of option
    :param datetime maturity_date: maturity date of option
    """
    pricer_type = pricer_type or PricerType(1).name
    if pricer_type not in PricerType._member_names_:
        raise RuntimeError(f'Pricer Not Considered')
    if pricer_type == PricerType.Analytical.name:
        engine = ql.AnalyticEuropeanEngine(process)
    elif pricer_type == PricerType.Monte_Carlo.name:
        rng = "pseudorandom"  # could use "lowdiscrepancy"
        engine = ql.MCEuropeanEngine(
            process, rng, timeSteps=1, requiredSamples=10000
        )
    else:
        raise RuntimeError(f'Pricer considered but not yet implemented')

    payoff = payoff or CallOrPut.CALL
    if payoff not in CallOrPut.ALL_TYPES:
        raise RuntimeError(f'Payoff not implemented')
    if payoff == CallOrPut.CALL:
        option_type = ql.Option.Call
    elif payoff == CallOrPut.PUT:
        option_type = ql.Option.Put

    payoff = ql.PlainVanillaPayoff(option_type, strike)
    europeanExercise = ql.EuropeanExercise(maturity_date)
    call_option = ql.VanillaOption(payoff, europeanExercise)
    call_option.setPricingEngine(engine)
    return call_option


def main():
    base_spot = 100
    vol = 0.1
    strike = 100
    rfr = 0.05
    div = 0.01
    shocks = scenario_generator.generate_log_normal_shocks(
        vol=vol, num_shocks=780
    )
    rand_spot = base_spot * shocks

    npvs = []

    for spot in rand_spot:
        proc = create_bsm_process(spot, vol, rfr, div)
        option = create_option(strike, ql.Date(15, 6, 2025), proc,
                               pricer_type=PricerType.Analytical.name
                               , payoff=CallOrPut.CALL)
        npvs.append(option.NPV())

    # print(npvs)

    # pyplot.hist(npvs, bins=50)
    # pyplot.show()
    # pyplot.scatter(rand_spot, npvs)
    # pyplot.show()
    return npvs, rand_spot


if __name__ == '__main__':
    main()
