# encoding: utf-8
import pandas as pd
import numpy as np

import commodity.const as const
import commodity.data as data

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models.widgets import Select
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Range1d, LinearAxis, HoverTool, TableColumn, NumberFormatter, DataTable
from bokeh.plotting import figure
from bokeh.palettes import Spectral9

COLORS = Spectral9 + ["#053061", "#2166ac", "#4393c3" "#92c5de", "#d1e5f0"]
col2edb, edb2col = data.get_col2edb()
df = pd.read_excel(const.YIWU_FNAME)
yiwu = df['name'].tolist()

source_bpi = ColumnDataSource(data=dict(date=[], tot=[], energy=[], steel=[], mineral=[], 
                                        metal=[], rubber=[], agr=[], ani=[], oil=[], sugar=[]))
def update_bpi():
    fname = '%s/bpi.xlsx'%(const.COMMODITY_DIR)
    df = pd.read_excel(fname)
    source_bpi.data = {'date': df.index,
                       'tot': df[u'中国大宗商品价格指数:总指数'],
                       'energy': df[u'中国大宗商品价格指数:能源类'],
                       'steel': df[u'中国大宗商品价格指数:钢铁类'],
                       'mineral': df[u'中国大宗商品价格指数:矿产类'],
                       'metal': df[u'中国大宗商品价格指数:有色类'],
                       'rubber': df[u'中国大宗商品价格指数:橡胶类'],
                       'agr': df[u'中国大宗商品价格指数:农产品类'],
                       'ani': df[u'中国大宗商品价格指数:牲畜类'],
                       'oil': df[u'中国大宗商品价格指数:油料油脂类'],
                       'sugar': df[u'中国大宗商品价格指数:食糖类']}

source_yiwu = ColumnDataSource(data=dict(date=[], val=[]))
def update_yiwu():
    fname = '%s/yiwu/%s.xlsx'%(const.COMMODITY_DIR, yiwu_select.value)
    df = pd.read_excel(fname, index_col=0)
    df.index = pd.to_datetime(df.index)
    source_yiwu.data = {'date': df.index, 'val': df[u'价格指数']}
    plot_yiwu.title.text = yiwu_select.value

source_yiwu_table = ColumnDataSource(data=dict())
def update_yiwu_table():
    df = pd.read_excel('%s/yiwu_percent.xlsx'%(const.COMMODITY_DIR))
    df = df.sort_values('all', ascending=False)
    source_yiwu_table.data = source_yiwu_table.from_df(df)

yiwu_columns = [
    TableColumn(field='name', title=u'类别'),
    TableColumn(field='all', title=u'全历史百分位', formatter=NumberFormatter(format='0.00%')),
    TableColumn(field='1-year', title=u'一年百分位', formatter=NumberFormatter(format='0.00%')),
    TableColumn(field='5-year', title=u'五年百分位', formatter=NumberFormatter(format='0.00%')),
]
yiwu_table = DataTable(source=source_yiwu_table, columns=yiwu_columns, width=900)

def update_all():
    update_bpi()
    update_yiwu()
    update_yiwu_table()

def get_plot(title, pct=False):
    tools = "pan,wheel_zoom,box_select,reset,hover"
    plot = figure(plot_height=500, plot_width=1200, tools=tools, x_axis_type='datetime', toolbar_location='above')
    plot.title.text_font_size = "15pt"
    plot.title.text_font = "Microsoft YaHei"
    # plot.yaxis.minor_tick_line_color = None
    plot.title.text = title
    if pct:
        plot.yaxis.formatter = NumeralTickFormatter(format='0.00%')
    else:
        plot.yaxis.formatter = NumeralTickFormatter(format='0.00')
    return plot

plot_bpi = get_plot(u'中国大宗商品价格指数')
plot_bpi.line('date', 'tot', source=source_bpi, line_width=3, legend=u'总指数')
plot_bpi.line('date', 'energy', source=source_bpi, line_width=2, color=COLORS[0], legend=u'能源类')
plot_bpi.line('date', 'steel', source=source_bpi, line_width=2, color=COLORS[1], legend=u'钢铁类')
plot_bpi.line('date', 'mineral', source=source_bpi, line_width=2, color=COLORS[2], legend=u'矿产类')
plot_bpi.line('date', 'metal', source=source_bpi, line_width=2, color=COLORS[3], legend=u'有色类')
plot_bpi.line('date', 'rubber', source=source_bpi, line_width=2, color=COLORS[4], legend=u'橡胶类')
plot_bpi.line('date', 'agr', source=source_bpi, line_width=2, color=COLORS[5], legend=u'农产品类')
plot_bpi.line('date', 'ani', source=source_bpi, line_width=2, color=COLORS[6], legend=u'牲畜类')
plot_bpi.line('date', 'oil', source=source_bpi, line_width=2, color=COLORS[7], legend=u'油料油脂类')
plot_bpi.line('date', 'sugar', source=source_bpi, line_width=2, color=COLORS[8], legend=u'食糖类')
hover_bpi = plot_bpi.select(dict(type=HoverTool))
hover_bpi.formatters = {'date': 'datetime'}
hover_bpi.tooltips = [(u'日期', '@date{%F}'),
                      (u'总指数', '@tot{0.00}'),
                      (u'能源类', '@energy{0.00}'),
                      (u'钢铁类', '@steel{0.00}'),
                      (u'矿产类', '@mineral{0.00}'),
                      (u'有色类', '@metal{0.00}'),
                      (u'橡胶类', '@rubber{0.00}'),
                      (u'农产品类', '@agr{0.00}'),
                      (u'牲畜类', '@ani{0.00}'),
                      (u'油料油脂类', '@ani{0.00}'),
                      (u'食糖类', '@sugar{0.00}')]
hover_bpi.mode = 'mouse'

yiwu_select = Select(value=u'总指数', title=u'义乌小商品指数', width=300, options=yiwu)
yiwu_select.on_change('value', lambda attr, old, new: update_yiwu())
plot_yiwu = get_plot(u'总指数')
plot_yiwu.line('date', 'val', source=source_yiwu, line_width=2, legend=u'价格指数')
hover_yiwu = plot_yiwu.select(dict(type=HoverTool))
hover_yiwu.formatters = {'date': 'datetime'}
hover_yiwu.tooltips = [(u'日期', '@date{%F}'),
                       (u'价格指数', '@val{0.00}')]
hover_yiwu.mode = 'vline'

update_all()

curdoc().add_root(column(plot_bpi, yiwu_select, yiwu_table, plot_yiwu))
curdoc().title = u'商品体系'