import random
import datetime
from ib_insync import *
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import pandas as pd
from IB_Broker import *

################################################
'''
client_id = random.randint(1,99)
ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)
ticker = "AAPL"
contract = Stock(ticker, 'SMART', 'USD')

ib.reqContractDetails(contract)
bars = ib.reqHistoricalData(contract, endDateTime='', durationStr='1 D', barSizeSetting='1 min', 
                            whatToShow='MIDPOINT', useRTH=True, formatDate=2, keepUpToDate=True)

df = util.df(bars)
#df.to_csv('C:/Users/XaoGo/Desktop/AAPL.csv')

print(df)
'''
df = pd.read_csv('SPXL1min5D.csv')
test = calculate_total_price(ticker = 'SPXL', test= df)
print(test.head())
test.to_csv('SPXL_testing_5d.csv')

