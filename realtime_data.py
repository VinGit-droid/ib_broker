import datetime
import random
from ib_insync import *

print('tiity fuck')
client_id = random.randint(1,99)
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=client_id)

positions = ib.positions()

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
n = 25
sl = 67
parent = MarketOrder("BUY", n, orderId=ib.client.getReqId(), transmit=True, tif="GTC", )
stopLoss = StopOrder("SELL", n, sl, orderId=ib.client.getReqId(), transmit=True, parentId=parent.orderId, tif="GTC", )
trade = ib.placeOrder(contract, parent)
ib.sleep(2)
trade = ib.placeOrder(contract, stopLoss)

# save to CSV file
allBars = [b for bars in reversed(barsList) for b in bars]
df = util.df(allBars)
df.to_csv(contract.symbol + '.csv', index=False)
#ib.reqGlobalCancel
'''
raw_balance = ib.accountSummary()
for av in raw_balance:
    if av.tag == 'AvailableFunds':
        print(float(av.value))

#positions = ib.positions()  # A list of positions, according to IB
#for position in positions:
    #contract = position.contract
    #if position.position > 0: # Number of active Long positions
        #action = 'Sell' # to offset the long positions
    #elif position.position < 0: # Number of active Short positions
        #action = 'Buy' # to offset the short positions
    #else:
        #assert False
    #totalQuantity = abs(position.position)
    #order = MarketOrder(action=action, totalQuantity=totalQuantity)
    #trade = ib.placeOrder(contract, order)
    #print(f'Flatten Position: {action} {totalQuantity} {contract.localSymbol}')
    #assert trade in ib.trades(), 'trade not listed in ib.trades'
    '''