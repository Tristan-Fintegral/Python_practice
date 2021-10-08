


def main():
    initialValue = ql.QuoteHandle(ql.SimpleQuote(100))
    sigma = 0.2
    today = ql.Date().todaysDate()
    riskFreeTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.05, ql.Actual365Fixed()))
    dividendTS = ql.YieldTermStructureHandle(ql.FlatForward(today, 0.01, ql.Actual365Fixed()))
    volTS = ql.BlackVolTermStructureHandle(ql.BlackConstantVol(today, ql.NullCalendar(), sigma, ql.Actual365Fixed()))
    process = ql.BlackScholesMertonProcess(initialValue, dividendTS, riskFreeTS, volTS)

    engine = ql.AnalyticEuropeanEngine(process)

    strike = 100.0
    maturity = ql.Date(15, 6, 2025)
    option_type = ql.Option.Call

    payoff = ql.PlainVanillaPayoff(option_type, strike)

    europeanExercise = ql.EuropeanExercise(maturity)
    europeanOption = ql.VanillaOption(payoff, europeanExercise)


    europeanOption.setPricingEngine(engine)
    europeanOption.NPV()
    temp=1

if __name__ == '__main__':
    main()