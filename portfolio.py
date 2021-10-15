
'''
MAJOR ASSUMPTION: ALL RISKFACTORS ARE UNCORRELATED
Portfolio Class:
Contains:
    - Instruments, quantity
Methods:
    - Add or remove instruments
    - PV = sum(PV(instrument) * quantity)
    - Shocked PV = PV(with shocked market data) [assume only spot changes]

In hedging example
1) Create portfolio
2) Add instruments
3) Calculate base PV
4) Simulate market/ market shocks
5) Iterate through market shocks to calculate PV
6) Calculate PnLs

Instrument 1 -> EqSpot
Instrument 2 -> APPL stock, rfr, vol
APPL -> S0=120, vol=0.2
GOOG -> S0=100, vol=0.3
corr(APPL, GOOGL) = 0.3
Shocks(vol)

'''

