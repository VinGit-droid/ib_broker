from IB_Broker import *
import datetime as dt


def ib_my_trader(my_ticker,tf):
	test = create_connection(ticker = my_ticker , timeframe= tf)
	test = calculate_total_price(ticker = my_ticker, test= test)
	IB_Trader(ticker = my_ticker, test = test)


def trading():
    
    now = dt.datetime.now()
    now = now.strftime ('%Y-%m-%d')
    market_open_time = (datetime.fromisoformat(now + ' 08:30')) 
    
    ib_my_trader(my_ticker='SPXL',tf='1 min')


while True:
    
    currenttime = dt.datetime.now() 
    
    now = dt.datetime.now()
    now = now.strftime ('%Y-%m-%d')
    
    market_open_time = (datetime.fromisoformat(now + ' 08:30')) 
    market_close_position = (datetime.fromisoformat(now + ' 09:35'))
    market_close_time = (datetime.fromisoformat(now + ' 09:45'))
    
    if currenttime.second  == 0 and currenttime.minute % 29 == 0 and currenttime < market_close_time and currenttime > market_open_time:   
        trading()
        print('I am trading right now')
        print(dt.datetime.now())
        
        print('I am sleeping fo a while now. Zzzzzzzzzzzzzzzzzzzzzz')
        time.sleep(14400)
        
    elif currenttime.hour == market_close_position.hour and currenttime.minute == market_close_position.minute and currenttime.second <= 45:
        try:
            print('We are closing all positions now. It is closing time.')
            close_all_positions()
        except:
            print('No positions to close.')
            
    elif currenttime > market_close_time:
        print('I am NOT trading right now')
        print(dt.datetime.now())
        clear_output(wait=True)
        time.sleep(1130)




'''
test = pd.read_csv('AAPL5MIN.csv')
#print(test)
test = test.tail(20)
ticker = 'GOLD5MIN'
test['symbol'] = ticker
test['date']= pd.to_datetime(test['date'])
test = test[['date','symbol','open','close']]
#print(test)
test.reset_index(inplace=True)
#print(test)
test['Minute'] = test.date.dt.minute
test = test[test['Minute'].isin([30, 50,10])]
print(test)
test = phase_2(test)
print(test)
test.to_csv(ticker+'.csv')
'''