import QuantLib as ql
import scenario_generator

print('Delete this print statement, you should be using logger.')
print('This is the pricer module')
print('Nikolas is printing something to test Git')
print('Nikolas is printing something else to test Git')
print('here is another print!!!!!')
print('here is a fourth print!!!!!')

def create_bsm_process(spot, vol, rfr, div):
    bsm_process = None # TODO -> implement returning a bsm process
    return bsm_process


def create_call_option(strike, maturity_date, process):
    call_option = None # TODO -> implement
    return call_option


def main():
    base_spot = 100
    vol  = 0.1
    shocks = scenario_generator.generate_log_normal_shocks(vol=vol, num_shocks=100)
    rand_spot = base_spot * shocks

    npvs = []

    for spot in rand_spot:
        # TODO -> implement
        option = create_call_option()
        npvs.append(option.NPV())

    print(npvs)

if __name__ == '__main__':
    main()

def pricer_call(spot, vol, rfr, div, strike, date):
    initialValue = ql.QuoteHandle(ql.SimpleQuote(spot))
    sigma = vol
    today = ql.Date().todaysDate()
    riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, rfr, ql.Actual365Fixed()))
    dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, div, ql.Actual365Fixed()))
    volTS = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), sigma, ql.Actual365Fixed()))
    process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volTS)

    rng = "pseudorandom"  # could use "lowdiscrepancy"

    engine = ql.AnalyticEuropeanEngine(process)
    mc_eng=ql.MCEuropeanEngine(process,rng,timeSteps=2, requiredSamples=10000)

    strike = strike
    maturity = date
    option_type = ql.Option.Call

    payoff = ql.PlainVanillaPayoff(option_type, strike)

    europeanExercise = ql.EuropeanExercise(maturity)
    europeanOption = ql.VanillaOption(payoff, europeanExercise)
    europeanOption_mc = ql.VanillaOption(payoff, europeanExercise)

    europeanOption.setPricingEngine(engine)
    europeanOption_mc.setPricingEngine(mc_eng)

    print(europeanOption.NPV())
    print(europeanOption_mc.NPV())

pricer_call(100,0.2,0.05,0.01,100.0, ql.Date(15, 6, 2025))