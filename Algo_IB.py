#-------------------------------------------Importing Libraries------------------------------

from IB_Broker import *
import datetime as dt


def ib_my_trader(my_ticker,tf):
	test = create_connection(ticker = my_ticker , timeframe= tf)
	test = calculate_total_price(ticker = my_ticker, test= test)
	IB_Trader(ticker = my_ticker, test = test)


def trading():
    
    now = dt.datetime.now()
    now = now.strftime ('%Y-%m-%d')
    #market_open_time = (datetime.fromisoformat(now + ' 08:30')) 
    ib_my_trader(my_ticker='SPXL',tf='1 min')

while True:
    
    currenttime = dt.datetime.now() 
    
    now = dt.datetime.now()
    now = now.strftime ('%Y-%m-%d')
    
    market_open_time = (datetime.fromisoformat(now + ' 08:45')) 
    market_close_position = (datetime.fromisoformat(now + ' 14:50'))
    market_close_time = (datetime.fromisoformat(now + ' 14:55'))
    '''When changing current time minute also change time.sleep'''
    
    if currenttime.second  == 0 and currenttime.minute % 30 == 0 and currenttime < market_close_time and currenttime > market_open_time:   
        trading()
        print('I am trading right now')
        print(dt.datetime.now())
        
        print('I am sleeping fo a while now. Zzzzzzzzzzzzzzzzzzzzzz')
        time.sleep(3300)
        
    elif currenttime.hour == market_close_position.hour and currenttime.minute == market_close_position.minute and currenttime.second <= 3:
        try:
            print('We are closing all positions now. It is closing time.')
            close_all_positions()
        except:
            print('No positions to close.')
            
    elif currenttime > market_close_time:
        print('I am NOT trading right now')
        print(dt.datetime.now())
        clear_output(wait=True)
        time.sleep(57600)
