import datetime
from ib_insync import *

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)
position = ib.positions()
print(position)
[v for v in ib.accountValues() if v.tag == 'NetLiquidationByCurrency' and v.currency == 'BASE']
'''
contract = Stock('SPXL', 'SMART', 'USD')

dt = ''
barsList = []
#while True:
bars = ib.reqHistoricalData(
	contract,
	endDateTime=dt,
	durationStr='1 D',
	barSizeSetting='1 min',
	whatToShow='TRADES',
	useRTH=True,
	formatDate=1)
#if not bars:
	#break
barsList.append(bars)
dt = bars[0].date
print(dt)

# save to CSV file
allBars = [b for bars in reversed(barsList) for b in bars]
df = util.df(allBars)
df.to_csv(contract.symbol + '.csv', index=False)
ib.reqGlobalCancel'''
