import ccxt,schedule,warnings,time,ast,config
warnings.filterwarnings('ignore')
from dateutil.tz import tzlocal
from datetime import datetime
from random import randint
from random import seed
import pandas as pd
import numpy as np
from rich import print, pretty
pretty.install()

ccxt.binanceus({ 'options':{ 'adjustForTimeDifference':True}})
exchange = ccxt.binanceus({
"apiKey": config.BINANCE_KEY_v4,
"secret": config.BINANCE_SECRET_v4,
'enableRateLimit': True})

# let's add a little bit of interaction
time.sleep(1)
print("\n\n...Welcome to Sophie,")
time.sleep(0)
print("\n....Our very first Sohpisticated trading bot.")
time.sleep(0)
q0 = input("\n.....Would you like to meet Sohpie before getting started? Yes/No: ").capitalize()
time.sleep(1)
if q0 == "Yes":
    print()
    print("""'##::::'##:'########:'########:'########:::::'######:::'#######::'########::'##::::'##:'####:'########:'####:
 ###::'###: ##.....:: ##.....::... ##..:::::'##... ##:'##.... ##: ##.... ##: ##:::: ##:. ##:: ##.....:: ####:
 ####'####: ##::::::: ##:::::::::: ##::::::: ##:::..:: ##:::: ##: ##:::: ##: ##:::: ##:: ##:: ##::::::: ####:
 ## ### ##: ######::: ######:::::: ##:::::::. ######:: ##:::: ##: ########:: #########:: ##:: ######:::: ##::
 ##. #: ##: ##...:::: ##...::::::: ##::::::::..... ##: ##:::: ##: ##.....::: ##.... ##:: ##:: ##...:::::..:::
 ##:.:: ##: ##::::::: ##:::::::::: ##:::::::'##::: ##: ##:::: ##: ##:::::::: ##:::: ##:: ##:: ##:::::::'####:
 ##:::: ##: ########: ########:::: ##:::::::. ######::. #######:: ##:::::::: ##:::: ##:'####: ########: ####:
..:::::..::........::........:::::..:::::::::......::::.......:::..:::::::::..:::::..::....::........::....::""")
    ###########################################
    # meet sophie
    time.sleep(1)
    print("\n.")
    print("\n..Hi there! I'm Sophie, I'll be helping you trade your asset.")
    time.sleep(1)
    print("\n...Before we begin I have a few questions to help us get started.")
    time.sleep(1)
    q1 = input("\n....Would you like me to do all the trading for you? (Yes/No): ").capitalize()
    if q1 == "Yes":
        time.sleep(1)
        print(" \n.....Awesome! I'm sure you'll be happy with my performance.")
    if q1 == "No":
        time.sleep(1)
        print(" \n....Great! I'll certainly keep a very close watch on your asset.")
        time.sleep(1)
        print(" \n...Here are a few more questions for ya... ")
        print(" \n..")
        print(" \n.")
        time.sleep(1)
    ###########################################
else:
    pass

if q0 == "Yes":
    # introduce yourself to sophie
    name = input("\nWhat would you like me to call you: ")
    time.sleep(1)
    print("\nOh, what a wonderful name. Well, it's a pleasure doin' business with you",name,"!")
    time.sleep(1)
    print("\nWhat is the prefix of the asset you want to trade?")
    time.sleep(1)
    tick = input("\nSome popular ones are SHIB, DOGE, BTC, ETH, or VET: ").upper()
    time.sleep(1)
    print("\nNice! That's a great choice.")
    time.sleep(1)
    print("\n\n\nWhat denomination do you want to trade",tick,"in?")
    ticker =  tick+"/"+input("\nMaybe you have tradeable amounts of USD, BUSD, or USDT?: ")
    time.sleep(1)
    print("\n\n\nThis might be a silly question, but how often would you like to check up on this asset?")
    timeframe = input("\nYou can put anything like 1m, 5m, 15m, 30m, 1h, or 1d: ")
    
    if timeframe == "1m" or "5m":
        volatility = 0.654545454545454545454545454
        
    if timeframe == "15m" or "30m":
        volatility = 1.35454545454545454545454545454545
        
    else:
        volatility = 1.654545454545454545454545454
    time.sleep(1)
    print("\n\n\nAwesome! How many "+tick+" would you like me to continuously trade for you?")
    order_size = float(input("\nRemember, all trades on Binance.US must be above $10: "))
    og_size = order_size
    time.sleep(1)
    
    q2 = str(input("\n\n\nAre you already holding ~10% more than this amount of "+tick+" in your portfolio?: ")).capitalize()
    if q2 == "Yes":
        in_position = True
        min_sell_price = float(input("\nWhat was the price of "+tick+" when you bought them?: "))
    else:
        in_position = False
        min_sell_price = exchange.fetch_ohlcv('DOGE/USDT', timeframe="1m", limit=1)[0][4]
    
    time.sleep(1)
    
    max_loss = 0.5/100
    min_gain = 1.05/100
else:
    # introduce yourself to bot
    name = input("\nEnter name: ")
    tick = input("\nInsert ticker: ")
    ticker=  tick+"/"+input("\nEnter the denomination of your trade, i.e. USD, BUSD, or USDT?: ")
    timeframe = input("\nYou can put anything like 1m, 5m, 15m, 30m, 1h, or 1d: ")
    
    # presets for volatility
    if timeframe == "1m" or "5m":
        volatility = 0.654545454545454545454545454
        
    if timeframe == "15m" or "30m":
        volatility = 1.35454545454545454545454545454545
        
    else:
        volatility = 1.654545454545454545454545454
    
    order_size = float(input("\nOrder size in "+tick+": "))
    og_size = order_size
    in_position = ast.literal_eval(input("\nAleady in desired holding position? - True/False: ").capitalize())
    
    min_sell_price = float(input("\nEnter average_price or most recent purchase price: "))
    max_loss = float(input("\nMax loss (example 0.51): "))/100
    min_gain = float(input("\nMin gain: (example 1.05)"))/100

# let's start!
if q0 == "Yes":
    print("\n\nOkay! I have everything I need. Now you can just sit back and relax and watch me do what I do, I guess... you'll see my first analysis in",str(timeframe),".")
else:
    print("\n\n Great! I'll start analyzing incoming data in",str(timeframe),".")
print("\n#########################################################################################################")
# Randomizer for schedule. I know it's weird, but somehow it works nicely for me. 
#Feel free to remove randint(a,b) downstairs, and just let schedule(a).minutes.. 
if timeframe == "1m":
    a = 55
    b = 60
if timeframe == "5m":
    a = 275
    b = 300
if timeframe == "15m":
    a = 850
    b = 900
if timeframe == "30m":
    a = 1775
    b = 1800
if timeframe == "1h":
    a = 3575
    b = 3600

# Supertrend
# (TR) The true range indicator is taken as the greatest of the following: current high less the current low; the absolute value of the current high less the previous close; and the absolute value of the current low less the previous close
def tr(data):
    data['previous_close'] = data['close'].shift(1)
    data['high-low'] = abs(data['high'] - data['low'])
    data['high-pc'] = abs(data['high'] - data['previous_close'])
    data['low-pc'] = abs(data['low'] - data['previous_close'])
    tr = data[['high-low','high-pc','low-pc']].max(axis=1)
    return tr

#TR rolling average
def atr(data, period):
    data['tr'] = tr(data)
    atr = data['tr'].rolling(period).mean()
    return atr

# https://www.tradingfuel.com/supertrend-indicator-formula-and-calculation/ #It's important to treat the atr_multiplier as a variable. See supertrend_visualizer_parquet.py to see how atr_mult affects indication. Volatility rate varies from 0.0001 - 3. Smaller numbers for 1m intervals. Larger number for day or swing trades.
def supertrend(df, period = 7, atr_multiplier = volatility):
    hl2 = (df['high'] + df['low'])/2
    df['atr'] = atr(df, period)
    df['upperband'] = hl2 + (atr_multiplier * df['atr'])
    df['lowerband'] = hl2 - (atr_multiplier * df['atr'])
    df['in_uptrend'] = True
    for current in range(1, len(df.index)):
        previous = current - 1
        if df['close'][current] > df['upperband'][previous]:
            df['in_uptrend'][current] = True
        elif df['close'][current] < df['lowerband'][previous]:
            df['in_uptrend'][current] = False
        else:
            df['in_uptrend'][current] = df['in_uptrend'][previous]
            if (df['in_uptrend'][current]) and (df['lowerband'][current] < df['lowerband'][previous]):
                df['lowerband'][current] = df['lowerband'][previous]
            if not df['in_uptrend'][current] and df['upperband'][current] > df['upperband'][previous]:
                df['upperband'][current] = df['upperband'][previous]
    return df

# Analysis & decision making. This part could be extracted out into it's own class.
def check_buy_sell_signals(df):
    
    # Establish bot parameters
    global in_position,ticker,timeframe,min_sell_price,max_loss,min_gain,order_size
    print("Calculating", ticker ,"data...")
    print(df.tail(3)[['timestamp','close','low','in_uptrend']])
    
    # {start of peak & trough - analysis}
    # most current open, high, & low prices
    open_price = df[-1:].reset_index(drop=True)['open'][0]
    high_price = df[-1:].reset_index(drop=True)['high'][0]
    low_price = df[-1:].reset_index(drop=True)['low'][0]

    # i wanted to see if it's possible to catch a massive drop from which to sell
    # so i took the highest low in df & current_low:
    max_low = df.max()['low'] * (1 - max_loss)

    # a sell point from peak could be discovered when low price goes farther than recent max_low(1 - max_loss): 
    peak_sell = low_price < max_low
    
    print("\nLow price: ", str(low_price)," Max low: ", str(max_low))
    print("Peak breached: ", str(peak_sell))
    
    # a sell point from trough could be discovered when low price goes above min_sell_price(1 + min_gain): 
    trough_sell = min_sell_price * (1 + min_gain) < low_price
    print("\nMinimum sell price:", min_sell_price * (1 + min_gain))
    
    # check if min_sell_price < low_price - which would thus execute a sell
    print("Trough breached: ",trough_sell)
    # {end of peak & trough - analysis}
    
    # extract last row for df
    last_row_index = len(df.index) - 1
    previous_row_index = last_row_index - 1 

    # check for uptrend - if in_uptrend goes from False to True
    if not df['in_uptrend'][previous_row_index] and df['in_uptrend'][last_row_index]:
        print("\n\nChanged to uptrend - Buy.")

        # enter position when in_uptrend True
        if not in_position:

            # send binance buy order
            order = exchange.create_market_buy_order(f'{ticker}', order_size)
            
            print('\nStatus:' + order['info']['status'],
                  'Price:' + order['trades'][0]['info']['price'],
                  'Quantity:' + order['info']['executedQty'],
                  'Type:' + order['info']['side'])
            
            # just catching how many i caught
            quant = float(order['info']['executedQty'])
            
            # replaces min_sell_price by purchase_price
            min_sell_price = float(order['trades'][0]['info']['price'])
            
            # we are now in_position
            in_position = True
            
            print("Purchased @ $",str(min_sell_price),"for $",str(min_sell_price * quant))
        else:
            print("Already in position.")
   
    
    # check for downtrend - if in_uptrend goes from True to False
    if df['in_uptrend'][previous_row_index] and not df['in_uptrend'][last_row_index]:
        print("Changed to downtrend - Sell.")
        
        # only sells if price is greater than (min_sell_price)*(markup)*(max_loss) or peak_sell = True
        if in_position and (trough_sell or peak_sell):
            
            # send binance sell order
            order = exchange.create_market_sell_order(f'{ticker}',order_size)
            
            # i really should just output this as a dataframe()
            print('Status:' + order['info']['status'],
                  'Price:' + order['trades'][0]['info']['price'],
                  'Quantity:' + order['info']['executedQty'],
                  'Type:' + order['info']['side'])
            
            # we are no longer in_position
            in_position = False
            
            # reduces order size to mitigate Insufficient Funds error
            order_size = order_size*(1-0.05)
            
            # limits the size reduction from above
            if order_size < og_size:
                order_size = og_size
            else:
                pass
            
            print("Loss/gain:",str(float(min_sell_price)/float(order['trades'][0]['info']['price'])-1))
        else:
            print("Did not find an opportunity to sell, no task.")  

# do it... just do it
def run_bot():
    print()
    print("########################################")
    print()
    print(datetime.now(tzlocal()).isoformat())
    print("In position:", in_position, "\nTimeframe:", timeframe,"\n")
    
    # pulls in df to be used for calculations
    bars = exchange.fetch_ohlcv(f'{ticker}', timeframe=timeframe, limit=50)
    df = pd.DataFrame(bars[:-1], columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms').dt.tz_localize(None)
    
    supertrend_data = supertrend(df)
    check_buy_sell_signals(supertrend_data)
    
    # used to get balance of ticker. For future use; allow order_size to be dynamic variable.
    bal = pd.DataFrame(exchange.fetch_balance()['info']['balances'])
    bal['free'] = pd.to_numeric(bal['free'])
    bal = bal[bal.free!=0].drop(columns='locked').reset_index(drop=True)
    bal = bal[bal['asset']==ticker[:4].replace('/','')].reset_index(drop=True).free[0]

    # printouts 
    print("\nBalance:$", bal*bars[-1][1], "\tPosition:", bal)
    print("Order size:", order_size)
    print("Volatility:", volatility, "Max loss:", max_loss)

"""
Run Bot, To the Moon
"""
schedule.every(randint(a,b)).seconds.do(run_bot)

# variable assigned to exercising the bot
bot = True
while bot:
    schedule.run_pending()
    time.sleep(0)