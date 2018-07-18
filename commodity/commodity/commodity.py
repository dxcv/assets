# encoding: utf-8

import pandas as pd
import datetime
import os

import data
import const
import yiwu

def bpi():
    fname = '%s/bpi.xlsx'%(const.COMMODITY_DIR)
    df = pd.read_excel(fname)
    df = data.new_df(df)
    df.to_excel(fname)    

def yiwu_index():
    df = pd.read_excel(const.YIWU_FNAME)
    for gccode, name in zip(df['code'], df['name']):
        print gccode, name
        tdf = yiwu.crawl_yiwu_index(gccode)
        fname = u'%s/yiwu/%s.xlsx'%(const.COMMODITY_DIR, name)
        tdf.to_excel(fname)

    dic = {}
    for i, name in enumerate(df['name']):
        fname = u'%s/yiwu/%s.xlsx'%(const.COMMODITY_DIR, name)
        tdf = pd.read_excel(fname, index_col=0)
        dic['g%d'%(i)] = tdf[u'价格指数']
    df = pd.DataFrame(dic)
    df.index.name = 'date'
    df.to_excel('%s/yiwu_index.xlsx'%(const.COMMODITY_DIR))

def yiwu_history_percentile():
    yiwu.history_percentile_all()

def main():
    bpi()
    yiwu_index()
    yiwu_history_percentile()
