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

def m2():
    fname = '%s/m2.xlsx'%(const.INTEREST_DIR)
    df = pd.read_excel(fname)
    df = data.new_df(df)
    df.to_excel(fname)

def paper():
    fname = '%s/paper.xlsx'%(const.INTEREST_DIR)
    df = pd.read_excel(fname)
    df = data.new_df(df)
    df.to_excel(fname)

def dr():
    fname = '%s/dr.xlsx'%(const.INTEREST_DIR)
    df = pd.read_excel(fname)
    df = data.new_df(df)
    df.to_excel(fname)

def main():
    multiplier()
    m2()
    paper()
    dr()

if __name__ == '__main__':
    main()