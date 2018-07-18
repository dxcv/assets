# encoding: utf-8

import pandas as pd
import datetime
import os

import data
import const

def cny():
    fname = '%s/cny.xlsx'%(const.CURRENCY_DIR)
    df = pd.read_excel(fname)
    df = data.new_df(df)
    df.to_excel(fname)    

def usdcny():
    fname = '%s/usdcny.xlsx'%(const.CURRENCY_DIR)
    columns = 'USDCNH.FX,USDCNY.IB'
    start_date = '2013-03-28'
    end_date = datetime.date.today()
    df = data.wind_df(columns, start_date, end_date)
    df.columns = [u'美元兑离岸人民币', u'美元兑在岸人民币']
    df.to_excel(fname)

def cfets():
    fname = '%s/cfets.xlsx'%(const.CURRENCY_DIR)
    columns = 'USDX.FX,CNYX.IB'
    start_date = '2013-03-28'
    end_date = datetime.date.today()
    df = data.wind_df(columns, start_date, end_date)
    df.columns = [u'美元指数', u'CFETS人民币汇率指数']
    df.to_excel(fname)

def main():
    cny()
    usdcny()
    cfets()