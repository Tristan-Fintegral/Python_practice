import QuantLib as ql

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