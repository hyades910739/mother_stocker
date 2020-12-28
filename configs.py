# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SPREADSHEET_ID = 'THE/SPREADSHEET/PATH'
READ_RANGE = 'records'

#target_attrs = ['當盤成交價','當盤成交量','累積成交量','開盤價','最高價','最低價','昨收價']
#target_attr_keys = ['z','tv','v','o','h','l','y']  
STOCK_PRICE_ATTR_DICT = {
    'z': '當盤成交價',
    'tv': '當盤成交量',
    'v': '累積成交量',
    'o': '開盤價',
    'h': '最高價',
    'l': '最低價',
    'y': '昨收價'
 }

# only write these attrbutes to spreadsheet.
TARGET_ATTRS = [ '開盤價', '最高價', '最低價', '昨收價']
