import QuantLib as ql
import scenario_generator
from matplotlib import pyplot


class OptionPricerType:
    ANALYTICAL = 'Analytical'
    MONTE_CARLO = 'Monte Carlo'
    A_THIRD_PRICER = 'Pricer Three'
    ALL_PRICERS = [ANALYTICAL, MONTE_CARLO, A_THIRD_PRICER]


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


def create_call_option(strike, maturity_date, process, pricer_type=None):
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
            process, rng, timeSteps=2, requiredSamples=10000
        )
    else:
        raise RuntimeError(f'PUT STATEMENT HERE')

    option_type = ql.Option.Call
    payoff = ql.PlainVanillaPayoff(option_type, strike)
    europeanExercise = ql.EuropeanExercise(maturity_date)
    call_option = ql.VanillaOption(payoff, europeanExercise)
    call_option.setPricingEngine(engine)
    return call_option

def create_call_option_mc(strike, maturity_date, process):
    """
        Add paramater for timesteps and samples
        This function creates call option using BSM pricer
        created by create_bsm_process with strike price and maturity date. This
        function uses a monte carlo approach

        :param int strike: strike price of option
        :param datetime maturity_date: maturity date of option

        """
    rng = "pseudorandom"  # could use "lowdiscrepancy"
    engine = ql.MCEuropeanEngine(process,rng,timeSteps=2, requiredSamples=10000)
    option_type = ql.Option.Call
    payoff = ql.PlainVanillaPayoff(option_type, strike)
    europeanExercise = ql.EuropeanExercise(maturity_date)
    call_option = ql.VanillaOption(payoff, europeanExercise)
    call_option.setPricingEngine(engine)

    return call_option

def create_put_option(strike, maturity_date, process):
    engine = ql.AnalyticEuropeanEngine(process)
    option_type = ql.Option.Put
    payoff = ql.PlainVanillaPayoff(option_type, strike)
    europeanExercise = ql.EuropeanExercise(maturity_date)
    put_option = ql.VanillaOption(payoff, europeanExercise)
    put_option.setPricingEngine(engine)
    return put_option


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
        option = create_call_option(strike, ql.Date(15, 6, 2025), proc)
        npvs.append(option.NPV())

    print(npvs)

    # pyplot.hist(npvs, bins=50)
    # pyplot.show()
    pyplot.scatter(rand_spot, npvs)
    pyplot.show()



if __name__ == '__main__':
    main()

# def pricer_call(spot, vol, rfr, div, strike, date):
#     initialValue = ql.QuoteHandle(ql.SimpleQuote(spot))
#     sigma = vol
#     today = ql.Date().todaysDate()
#     riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, rfr, ql.Actual365Fixed()))
#     dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, div, ql.Actual365Fixed()))
#     volTS = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), sigma, ql.Actual365Fixed()))
#     process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volTS)
#
#     rng = "pseudorandom"  # could use "lowdiscrepancy"
#
#     engine = ql.AnalyticEuropeanEngine(process)
#     mc_eng=ql.MCEuropeanEngine(process,rng,timeSteps=2, requiredSamples=10000)
#
#     strike = strike
#     maturity = date
#     option_type = ql.Option.Call
#
#     payoff = ql.PlainVanillaPayoff(option_type, strike)
#
#     europeanExercise = ql.EuropeanExercise(maturity)
#     europeanOption = ql.VanillaOption(payoff, europeanExercise)
#     europeanOption_mc = ql.VanillaOption(payoff, europeanExercise)
#
#     europeanOption.setPricingEngine(engine)
#     europeanOption_mc.setPricingEngine(mc_eng)
#
#     print(europeanOption.NPV())
#     print(europeanOption_mc.NPV())

