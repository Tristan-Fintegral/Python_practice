import QuantLib as ql
import scenario_generator
from matplotlib import pyplot


class OptionPricerType:
    ANALYTICAL = 'Analytical'
    MONTE_CARLO = 'Monte Carlo'
    A_THIRD_PRICER = 'Pricer Three'
    ALL_PRICERS = [ANALYTICAL, MONTE_CARLO, A_THIRD_PRICER]

class call_or_put:
    CALL = 'Call'
    PUT = 'Put'
    ALL_TYPES  = [CALL, PUT]


def create_bsm_process(spot, vol, rfr, div):
    """
    This function creates BSM process given market values

    :param float div: flat forward dividend rate using actual/365 fixed
    :param int spot: spot price
    :param float vol: volatility
    :param float rfr: flat forward risk free rate using actual/365 fixed
    :return BlackScholesMertonProcess: Market data process
    """
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


def create_option(strike, maturity_date, process, pricer_type=None, o_type=None):
    """
       This function creates call option using BSM pricer
       created by create_bsm_process with strike price and maturity date. This
       function uses an analytical approach

       :param int strike: strike price of option
       :param datetime maturity_date: maturity date of option
       """
    pricer_type = pricer_type or OptionPricerType.ANALYTICAL
    if pricer_type not in OptionPricerType.ALL_PRICERS:
        raise RuntimeError(f'PUT STATEMENT HERE')

    if pricer_type == OptionPricerType.ANALYTICAL:
        engine = ql.AnalyticEuropeanEngine(process)
    elif pricer_type == OptionPricerType.MONTE_CARLO:
        rng = "pseudorandom"  # could use "lowdiscrepancy"
        engine = ql.MCEuropeanEngine(
            process, rng, timeSteps=1, requiredSamples=10000
        )
    else:
        raise RuntimeError(f'PUT STATEMENT HERE')

    o_type = o_type or call_or_put.CALL
    if o_type not in call_or_put.ALL_TYPES:
        raise RuntimeError(f'PUT STATEMENT HERE')
    if o_type == call_or_put.CALL:
        option_type = ql.Option.Call
    elif o_type == call_or_put.PUT:
        option_type = ql.Option.Put
    else:
        raise RuntimeError(f'PUT STATEMENT HERE')


    payoff = ql.PlainVanillaPayoff(option_type, strike)
    europeanExercise = ql.EuropeanExercise(maturity_date)
    call_option = ql.VanillaOption(payoff, europeanExercise)
    call_option.setPricingEngine(engine)
    return call_option



def main():
    base_spot = 100
    vol  = 0.1
    strike=100
    rfr=0.05
    div=0.01
    shocks = scenario_generator.generate_log_normal_shocks(vol=vol, num_shocks=780)
    rand_spot = base_spot * shocks

    npvs = []

    for spot in rand_spot:
        proc = create_bsm_process(spot, vol, rfr, div)
        option = create_option(strike, ql.Date(15, 6, 2025), proc, pricer_type=OptionPricerType.ANALYTICAL
                               ,o_type=call_or_put.PUT)
        npvs.append(option.NPV())

    print(npvs)

    # pyplot.hist(npvs, bins=50)
    # pyplot.show()
    pyplot.scatter(rand_spot, npvs)
    pyplot.show()



if __name__ == '__main__':
    main()


