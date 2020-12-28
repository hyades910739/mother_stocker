
from datetime import datetime
from itertools import islice

import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from utils import (
    load_or_create_credentials, 
    read_selling_records, 
    load_real_time_stock_price_by_requests,
    create_selling_record_info_rows, 
    update_records_rows, 
    read_tracking_stcoks,
    get_total_stock_profit,
    update_stocks_rows
)

def update_stock_price_by_crawler():
    creds = load_or_create_credentials()
    service = build('sheets', 'v4', credentials=creds)    
    selling_records = read_selling_records(service)    
    update_time = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")
    n_row = len(selling_records)
    sids = list(set(
        [li[1] for li in islice(selling_records, 1, None)]
    ))    
    stock_info_dic = load_real_time_stock_price_by_requests(sids)  

    write_rows = create_selling_record_info_rows(selling_records, stock_info_dic, update_time)
    update_records_rows(service, write_rows, n_row)

def update_revenue_stats():
    creds = load_or_create_credentials()
    service = build('sheets', 'v4', credentials=creds)    
    selling_records = read_selling_records(service)
    update_time = datetime.now().strftime("%Y/%m/%d, %H:%M:%S")    
    tracking_stocks = read_tracking_stcoks(service)
    sid_profit_dic = get_total_stock_profit(selling_records)
    stock_rows = [ (row[0], row[1], sid_profit_dic[row[1]],  update_time) for row in tracking_stocks[1:]]
    update_stocks_rows(service, stock_rows , len(stock_rows)+1)
    

if __name__ == "__main__":
    #creds = load_or_create_credentials()
    #service = build('sheets', 'v4', credentials=creds)    
    
    args = sys.argv[1:]
    if not args:
        raise ValueError('please provide args')
    if len(args) >1:
        raise ValueError('too many args')
    arg = args[0]
    if arg == 'all':
        update_stock_price_by_crawler()
        update_revenue_stats()
    elif arg == 'price':
        update_stock_price_by_crawler()
    elif arg == 'stats':
        update_revenue_stats()
    else:
        raise ValueError('args should be "all" or "price", or "stats".')    
    #creds = load_or_create_credentials()
    #service = build('sheets', 'v4', credentials=creds)    
    #update_stock_price_by_crawler()
    #update_revenue_stats()
    sys.exit(0) 
