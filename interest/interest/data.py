# encoding: utf-8

from WindPy import w
import datetime
import pandas as pd
import numpy as np

import const
import utils
import interest

w.start()

def get_col2edb():
    df = pd.read_excel(const.COL2EDB_FNAME)
    col2edb = {k: v for k, v in zip(df['col'], df['edb'])}
    edb2col = {k: v for k, v in zip(df['edb'], df['col'])}
    return col2edb, edb2col 

def new_df(df):
    start_date = pd.to_datetime(df.index[-1]) + datetime.timedelta(1)
    end_date = datetime.datetime.today() - datetime.timedelta(1)
    if start_date > end_date:
        return df
    col2edb, edb2col = get_col2edb()
    codes = [col2edb[col] for col in df.columns]
    # print df.tail()
    # print '\n'
    data = w.edb(codes, start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), "Fill=Previous")
    app_df = utils.wind2df(data)
    # print app_df
    app_df.columns = [edb2col[x] for x in app_df.columns]
    app_df = app_df[df.columns]
    app_df.index = app_df.index.map(lambda x: x - datetime.timedelta(seconds=0.005))
    # print app_df
    df = df.append(app_df)
    return df

def wind_df(columns, start_date, end_date):
    data = w.wsd(columns, 'close', start_date, end_date)
    df = pd.DataFrame(np.array(data.Data).T, index=data.Times, columns=data.Codes)
    return df

if __name__ == '__main__':
    interest.main()