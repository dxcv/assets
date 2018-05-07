# encoding: utf-8

import pandas as pd
import datetime
import os

import data
import const

def multiplier():
    fname = '%s/multiplier.xlsx'%(const.INTEREST_DIR)
    df = pd.read_excel(fname)
    df = data.new_df(df)
    df.to_excel(fname)

def main():
    multiplier()

if __name__ == '__main__':
    main()