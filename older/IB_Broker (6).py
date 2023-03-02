import random
import datetime
from ib_insync import *
from ibapi.client import EClient
from ibapi.wrapper import EWrapper
import pandas as pd
import numpy as np
from IPython.display import clear_output
#import schedule
import time
import sys
import datetime as dt
from datetime import datetime 

################################################

def create_connection(ticker , timeframe):
    
    global contract
    tkr = ticker
    client_id = random.randint(1,99) 
    global ib
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=client_id)
    
    contract = Stock(tkr, 'SMART', 'USD')
    
    #ib.reqContractDetails(contract)
    #bars = ib.reqMktData(contract, genericTickList='', snapshot=False, regulatorySnapshot=False)
    #bars = ib.reqRealTimeBars(contract, 5, 'TRADES', False)
    #bars = ib.reqHistoricalData(contract, endDateTime='', durationStr='5 D', barSizeSetting=timeframe, 
    #                       whatToShow='MIDPOINT', useRTH=True, formatDate=2, keepUpToDate=True)
    
    dt = ''
    barsList = []
    bars = ib.reqHistoricalData(contract, endDateTime=dt, durationStr='1 D', barSizeSetting='1 min', whatToShow='TRADES', useRTH=True, formatDate=1)

    barsList.append(bars)
    dt = bars[0].date
    print(dt)

#--------------------------------------------------Save data to CSV file------------------------------------

    allBars = [b for bars in reversed(barsList) for b in bars]
    df = util.df(allBars)
    df['my_datetime'] = df['date'] - pd.Timedelta(hours=0, minutes=0, seconds=0)
    ib.disconnect()
    df.to_csv('C:/Users/XaoGo/Desktop/IBK Codes/log_files/' + tkr + '_raw_data.csv')
    return df


#----------------------------------------Buy-Sell------------------------------------

def create_buy_sell_signal(ticker, test):
    '''Creates new columns for long and short trade flags and a column signal where to trade and not to trade. It tells if time is right to either buy or sell'''
    #test = pd.read_csv('test.csv')
    tkr = ticker
    test['symbol'] = tkr
    test['date']= pd.to_datetime(test['date'])
    test['Minute'] = test.date.dt.minute
    test = test[test['Minute'].isin([29])]
    test['prev_close'] = test['close'].shift(1)
    test = test.tail(3)
    
    # Generate buy and sell signal for price increase and decrease respectively. And create consolidated 'signal' column by addition of both buy and sell signals
    
    test['long_signal'] = np.where(test['close'] < test['prev_close'], 1, 0)
    test.reset_index(inplace=True)
    test.loc[0,'long_signal'] = np.where(test.loc[0,'close'] < test.loc[0,'open'], 1, 0)
    
    for i in range(test.shape[0]):
        
        if i > 0:
            h = i-1
            if ( (test.loc[i, 'long_signal'] == 0) & (test.loc[h, 'long_signal'] == 0) ):
                test.loc[i,'short_signal'] = -1

            else:

                test.loc[i,'short_signal'] = 0

    test['signal'] = test['short_signal'] + test['long_signal']

    for i in range(test.shape[0]):
        if i > 0:
            h = i-1
            if ( (test.loc[i, 'short_signal'] == -1) & (test.loc[h, 'short_signal'] == -1) ):
                
                test.loc[i,'new_signal'] = 0

            else:
                
                test.loc[i,'new_signal'] = test.loc[i,'signal'] 
                
    test['BUY_SELL'] = np.where(test['new_signal'] == 1, 'Buy', test['new_signal'] )
    test['BUY_SELL'] = np.where(test['new_signal'] == -1, 'Sell', test['BUY_SELL'] )
    test.loc[0,'BUY_SELL'] = np.where(test.loc[0, 'long_signal'] == 1, 'Buy', 0 )
    test['my_datetime'] = test['date'] - pd.Timedelta(hours=0, minutes=0, seconds=0)
    test = test[['date','open','symbol','close','prev_close','BUY_SELL','my_datetime']]
    test.to_csv('C:/Users/XaoGo/Desktop/IBK Codes/log_files/' + tkr + '_buy_sell_flags.csv')

    return test

#---------------------------------------QUANTITY AND PRICE--------------------------------

def generate_buy_quantity(test,tkr):
    '''Uses the data generated from buy_sell(test) and decides the buy quantity as to how many shares to buy or sell. Returns as dataframe with trade_no and BUY_SELL'''
    test = create_buy_sell_signal(ticker = tkr, test= test)
    test = test.tail(7)
    test['Buy_Qty'] = 0
    n = 1
    t = 1
    for i,row in test.iterrows():
        print(n)
        clear_output(wait=True)
    
        if test.loc[i,'BUY_SELL'] == 'Buy':
            n *= 5
            test.loc[i,'Buy_Qty'] = n/5
            test.loc[i,'Trade_No'] = t

        elif test.loc[i,'BUY_SELL'] == 'Sell':

            test.loc[i,'Trade_No'] = t
            n = 1
            t += 1
            continue
    test.to_csv('C:/Users/XaoGo/Desktop/IBK Codes/log_files/' + tkr + '_buy_sell_quantity.csv')
    return test

def calculate_total_price(ticker, test):
    '''Uses data generated fro phase_1(test) and decides buy quanity and sell quantity and total price to buy that share or shares'''
    test = generate_buy_quantity(test, tkr=ticker)
    test['Trade_No'] = test['Trade_No'].fillna(0)
    test["Trade_No"] = test["Trade_No"].astype(int)
    
    test['Sell_Qty'] = test.groupby(['Trade_No'])['Buy_Qty'].transform('sum')
    
    for i,row in test.iterrows():
        
        print(i)
        clear_output(wait=True)
        
        if test.loc[i,'BUY_SELL'] == 'Buy':
            
            test.loc[i,'Quantity'] = test.loc[i,'Buy_Qty']
            
        elif test.loc[i,'BUY_SELL'] == 'Sell':
            
            test.loc[i,'Quantity'] = test.loc[i,'Sell_Qty']
            
        else:
            
            test.loc[i,'Quantity'] = 0
    tkr = ticker
    test['symbol'] = tkr
    test = test[['date','symbol','open','close','prev_close','Trade_No','BUY_SELL','Quantity']]
    test['Price'] = test['Quantity'] * test['close']
    test["Quantity"] = test["Quantity"].astype(int)
    test["BUY_SELL"] = test["BUY_SELL"].astype(str)
    test['Total_Price'] = test.groupby(['Trade_No','BUY_SELL'])['Price'].transform('sum')
    test.to_csv('C:/Users/XaoGo/Desktop/IBK Codes/log_files/' + tkr + '_current_price_data.csv')

    return test


#-------------------------------------------------IB TRADER--------------------------------------------------

def IB_Trader(ticker, test):
    '''Uses last row from test dataset and is signal is Buy it buys the quantity indicated, 
    specifies the trade number and price for that particular deal. Submits the order based on Buy or Sell value. 
    Generates a new dataset for evry trade placed and saves it as symbol+_trade.csv'''
    
    final = pd.DataFrame()
    test = test.tail(1)
    
    client_id = random.randint(1,99)
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=client_id)
    tkr = ticker
    global contract
    contract = Stock(ticker, 'SMART', 'USD')

    for i, row in test.iterrows():
        
        print(i)
        global n
        
        if test.loc[i,'BUY_SELL'] == 'Buy':
            
            n = test.loc[i,'Quantity']
            print(n)
            Trade_No = test.loc[i,'Trade_No']
            Current_Price = test.loc[i,'Price']
            Total_Price = test.loc[i,'Total_Price']


            print('********************************************')
            print('Buy for Trade Number',Trade_No)
            print('Buy Quantity',n)
            print('Current Price is',Current_Price)
            print('Total_Price for this trade is ',Total_Price)

            close = test.loc[i,'close']
            sym = str(test.loc[i,'symbol'])
            n = int(n)
            
            my_order = MarketOrder('BUY', n)
            trade = ib.placeOrder(contract, my_order)
            final = pd.concat([final,test])

        elif (test.loc[i,'BUY_SELL'] == 'Sell') and (test.loc[i,'Quantity'] > 0) :
            n = test.loc[i,'Quantity']
            Trade_No = test.loc[i,'Trade_No']
            Current_Price = test.loc[i,'Price']
            Total_Price = test.loc[i,'Total_Price']


            print('********************************************')
            print('Sell for Trade Number',Trade_No)
            print('Sell Quantity',n)
            print('Current Price is',Current_Price)
            print('Total_Price for this trade is ',Total_Price)

            close = test.loc[i,'close']
            sym = str(test.loc[i,'symbol'])
            n = int(n)
            
            #my_order = MarketOrder('SELL', n)
            #trade = ib.placeOrder(contract, my_order)
            close_all_positions()
            final = pd.concat([final,test])

            #break

        else:
            
            sym = str(test.loc[i,'symbol'])

            print('*******************************************')
            print('*********Neither Buy nor Sell**************')
            #final = final.append(test)
            final = pd.concat([final,test])

    final.to_csv('C:/Users/XaoGo/Desktop/IBK Codes/log_files/' + sym+'_final_trades.csv')

def close_all_positions():
    client_id = random.randint(1,99)
    ib = IB()
    ib.connect('127.0.0.1', 7497, clientId=client_id)
    positions = ib.positions()                                            # A list of positions, according to IB
    for position in positions:
        print(position)
        contract = position.contract
        if position.position > 0:                                        # Number of active Long positions
            action = 'Sell'                                              # to offset the long positions
        elif position.position < 0:                                      # Number of active Short positions
            action = 'Buy'                                               # to offset the short positions
        else:
            assert False
        totalQuantity = abs(position.position)
        order = MarketOrder(action=action, totalQuantity=totalQuantity)
        trade = ib.placeOrder(contract, order)
        print(f'Flatten Position: {action} {totalQuantity} {contract.localSymbol}')
        assert trade in ib.trades(), 'trade not listed in ib.trades'
