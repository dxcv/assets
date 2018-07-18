# encoding: utf-8
# 爬取义乌小商品指数数据

import pandas as pd
import requests
import datetime
from bs4 import BeautifulSoup
import os

import const
import utils

def crawl_yiwu_index(gccode):
    '''
    爬取gccode类别的义乌小商品指数
    返回DataFrame
    '''
    start = '2006-01-01'
    today = datetime.date.today().strftime('%Y-%m-%d')
    names = [u'日期', u'价格指数', u'场内价格指数', u'网上价格指数', u'订单价格指数', u'出口价格指数']
    df = pd.DataFrame(columns=names)
    for page in range(1, 100):
        url = 'http://www.ywindex.com/cisweb/publish/queryList.htm?y=6&x=34&\
               startdate=%s&gccode=%s&enddate=%s&perpagenum=10&page=%d'%(start, gccode, today, page)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        response.encoding = 'gb2312'
        tables = soup.find_all('table')
        table = tables[-1]

        data = []
        for row in table.find_all('tr'):
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        data = data[2:]

        add_df = pd.DataFrame(data, columns=names)
        df = df.append(add_df)
    df = df.set_index(u'日期')
    df = df[~df.index.duplicated(keep='first')]
    df = df.sort_index()
    return df

def history_percentile(name):
    fname = '%s/yiwu/%s.xlsx'%(const.COMMODITY_DIR, name)
    df = pd.read_excel(fname, index_col=0)
    s0 = df[u'价格指数'].rank(pct=True)
    s1 = df[u'价格指数'].rolling(window=243, min_periods=1).apply(lambda x: utils.get_percentile(x))
    s2 = df[u'价格指数'].rolling(window=1000, min_periods=1).apply(lambda x: utils.get_percentile(x))
    return s0.iloc[-1], s1.iloc[-1], s2.iloc[-1]

def history_percentile_all():
    files = [f.rstrip('.xlsx') for f in os.listdir('%s/yiwu/'%(const.COMMODITY_DIR))]
    df = pd.DataFrame(columns=['name', 'all', '1-year', '5-year'])
    for i, f in enumerate(files):
        s0, s1, s2 = history_percentile(f)
        df.loc[i] = [f.decode('gbk'), s0, s1, s2]
    df.to_excel('%s/yiwu_percent.xlsx'%(const.COMMODITY_DIR), index=False, encoding='utf-8')