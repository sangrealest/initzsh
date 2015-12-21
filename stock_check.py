#!/bin/python

import requests
import time
import re
import sys

colors = {
    'grey': '1;30',
    'red': '0;31',
    'green': '0;32',
    'yellow': '1;33',
}


def parse_stock_data(stock_str):
    if not stock_str:
        return None
    sdata = stock_str.split(',')
    sname = ['name', 'open', 'close_yesterday', 'now', 'high', 'low', 'buy', 'sell', 'amount', 'volumn',
             'buy1-amount', 'buy1-price', 'buy2-amount', 'buy2-price', 'buy3-amount', 'buy3-price',
             'buy4-amount', 'buy4-price', 'buy5-amount', 'buy5-price',
             'sell1-amount', 'sell1-price', 'sell2-amount', 'sell2-price', 'sell3-amount', 'sell3-price',
             'sell4-amount', 'sell4-price', 'sell5-amount', 'sell5-price',
             'date', 'time']
    return dict(zip(sname, sdata))


def get_stock(stockid):
    if isinstance(stockid, list):
        stockid = ','.join(stockid)
    url = 'http://hq.sinajs.cn/list=' + stockid
    r = requests.get(url)
    if r.status_code != 200:
        return []
    results = []
    for s in r.text.split('\n'):
        s = s.strip()
        if not s:
            continue
        content = s.split('"')
        sre = re.match(r'^var +hq_str_(\w+)=$', content[0].strip())
        sid = sre.group(1)
        sval = parse_stock_data(content[1].strip())
        results.append((sid, sval))
    return results

def print_stock(stock_data, color=True):
    for sid, sval in stock_data:
        if sval is None:
            val_str = sid
            color_code = colors['grey']
        else:
            change = float(sval['now']) - float(sval['close_yesterday'])
            percent = 100 * change / float(sval['close_yesterday'])
            val_str = '%s %-8s %7.2f %6.3f%% %-10s %-8s  %-8s %s %s' %(sid,
                sval['now'], change, percent,
                sval['open'], sval['high'], sval['low'],
                sval['time'], sval['name'])
            if change > 0:
                color_code = colors['red']
            elif change < 0:
                color_code = colors['green']
            else:
                color_code = colors['yellow']
        if color:
            print('\033[%sm %s \033[0m' %(color_code, val_str))
        else:
            print(val_str)
    print('')

if __name__ == "__main__":

    while True:
        try:
            if len(sys.argv) == 1:
                sys.exit('No any stock,example:stock_check sz002407 sh600804 !')
            r = get_stock(sys.argv[1:])
            print_stock(r)
        finally:
            pass
        time.sleep(3)
