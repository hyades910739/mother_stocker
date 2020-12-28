import twstock
from twstock import Stock

def _load_daily_stock_price(stock_id, sleep=1): #-> Tuple
    stock = Stock(str(stock_id))
    date = stock.date[-1].strftime('%Y/%m/%d')
    low_price = stock.low[-1]
    high_price = stock.high[-1]
    price = stock.price[-1]
    latest_5_mv_avg_price = stock.moving_average(stock.price[-5:], days=5)[0]  
    if sleep:
        time.sleep(sleep)
    return (date, price, low_price, high_price, latest_5_mv_avg_price)

def _load_real_time_stock_price(stock_ids): #-> Dict[str, Tuple]
    #info_dic = {sid: twstock.realtime.get(str(sid)) for sid in stock_ids}
    info_dic = dict()
    for sid in stock_ids:
        print(stock_ids)
        info_dic[sid] = twstock.realtime.get(str(sid))
        time.sleep(1)
    res_dic = {}
    for k, val in info_dic.items():
        if val['success']:
            update_time = val['info']['time']
            cur_price = val['realtime']['latest_trade_price']        
            low =  val['realtime']['low']        
            high = val['realtime']['high']
            res_dic[k] = (update_time, cur_price, low, high)
    return res_dic