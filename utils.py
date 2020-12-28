import pickle
import os.path
from datetime import datetime
import requests
from itertools import islice, groupby
import time

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from configs import SCOPES, SPREADSHEET_ID, READ_RANGE, STOCK_PRICE_ATTR_DICT, TARGET_ATTRS


def load_or_create_credentials():
    '''
    ref: https://developers.google.com/sheets/api/quickstart/python
    '''
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def read_tracking_stcoks(service): #-> List
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range='stocks!A:E').execute()
    values = result.get('values', [])
    return values

def read_selling_records(service): #-> List
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID,
                                range='records').execute()
    values = result.get('values', [])
    return values

def _query_stock_information(sids, date=None): #-> requests.models.Response
    if date:
        base = 'tse_{}.tw_' + date
    else:
        base = 'tse_{}.tw'
    params = '|'.join([base.format(sid) for sid in sids])
    l = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=' + params
    query = requests.get(l)     
    if query.status_code != 200:
        raise Exception('request failed : query status code: {}'.format(query.status_code))
    else:
        return query

def load_real_time_stock_price_by_requests(sids, date=None): #-> Dict[sid:str, Dict[str, float]]
    '''get price information of every stock by sid
       args:
       ----
       sids: List[str]. list of stock id. Note that sid is a str.
       date: str or None. specify date to get price for certain date.

       returns:  
       ----
       A dict of sid: price_information_dict. 
    '''
    query = _query_stock_information(sids, date)
    infos = query.json()['msgArray'] # List[Dict]
    sid_info_dic = {}
    for dic in infos:
        current_sid = dic['c']
        info_dic = {
            attr : None if dic[k] == '-' else float(dic[k]) 
            for k, attr in STOCK_PRICE_ATTR_DICT.items()
        }
        sid_info_dic[current_sid] = info_dic 
    return sid_info_dic    

def update_records_rows(service, rows ,n_row):
    WRITE_RANGE = 'records!G2:O{}'.format(n_row)    
    body = {
        'values': rows
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=WRITE_RANGE,
        valueInputOption='RAW', body=body
    ).execute()    
    print('{0} cells updated.'.format(result.get('updatedCells')))

def update_stocks_rows(service, rows , n_row):
    WRITE_RANGE = 'stocks!A2:F{}'.format(n_row)    
    body = {
        'values': rows
    }
    result = service.spreadsheets().values().update(
        spreadsheetId=SPREADSHEET_ID, range=WRITE_RANGE,
        valueInputOption='RAW', body=body
    ).execute()    
    print('{0} cells updated.'.format(result.get('updatedCells')))

def create_selling_record_info_rows(selling_records, stock_info_dic, update_time): #-> List[Tuple]    
    write_rows = []    
    for li in islice(selling_records, 1, None):        
        cur_sid = li[1]
        cur_info_dic = stock_info_dic.get(cur_sid, None)
        if cur_info_dic is None:
            continue
        else:
            cur_infos = tuple(cur_info_dic[k] for k in TARGET_ATTRS)
            sell_price = float(li[2])
            sell_count = float(li[3])
            profit = (sell_price - cur_infos[3]) * sell_count * 1000
        write_rows.append((update_time, profit,) + cur_infos)
    return write_rows

def get_total_stock_profit(selling_records): #-> Dict[str, float]
    col_names = selling_records[0]
    profit_idx = [idx for idx, col_name in enumerate(col_names) if col_name == '盈虧'][0]
    sid_idx = [idx for idx, col_name in enumerate(col_names) if col_name == '代號'][0]
    sid_profit_pairs = [
        (row[sid_idx], float(row[profit_idx])) for row in selling_records[1:]
    ]
    groupby_id_iter = groupby(sorted(sid_profit_pairs,key=lambda x: x[0]), key=lambda x: x[0])
    sid_profit_dic = dict()
    for sid, infos in groupby_id_iter:
        sid_profit_sum = sum([val[-1] for val in infos])
        sid_profit_dic[sid] = sid_profit_sum
    #total_profits = sum(sid_profit_dic.values())
    return sid_profit_dic#, total_profits
