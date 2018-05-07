# encoding: utf-8
import pandas as pd

import currency.const as const
import currency.data as data

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Range1d, LinearAxis, HoverTool
from bokeh.plotting import figure
from bokeh.palettes import Spectral9

COLORS = Spectral9 + ["#053061", "#2166ac", "#4393c3" "#92c5de", "#d1e5f0"]
col2edb, edb2col = data.get_col2edb()

source_cny = ColumnDataSource(data=dict(date=[], ndf=[], ref=[], spot=[]))
def update_cny():
    fname = '%s/cny.xlsx'%(const.CURRENCY_DIR)
    df = pd.read_excel(fname)
    source_cny.data = {'date': df.index,
                       'ndf': df[u'USDCNY:NDF:1年'],
                       'ref': df[u'中间价:美元兑人民币'],
                       'spot': df[u'即期汇率:美元兑人民币']}

source_usdcny = ColumnDataSource(data=dict(date=[], off=[], on=[]))
def update_usdcny():
    fname = u'%s/usdcny.xlsx'%(const.CURRENCY_DIR)    
    df = pd.read_excel(fname)
    source_usdcny.data = {'date': df.index,
                          'off': df[u'美元兑离岸人民币'],
                          'on': df[u'美元兑在岸人民币']}
    source_usdcny.data['diff'] = source_usdcny.data['off'] - source_usdcny.data['on']

def update_all():
    update_cny()
    update_usdcny()

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

plot_cny = get_plot(u'美元兑人民币汇率')
plot_cny.line('date', 'ndf', source=source_cny, line_width=2, color='#d53e4f', legend=u'USDCNY:NDF:1年')
plot_cny.line('date', 'ref', source=source_cny, line_width=2, color=COLORS[0], legend=u'中间价:美元兑人民币')
plot_cny.line('date', 'spot', source=source_cny, line_width=2, color='#66CC66', legend=u'即期汇率:美元兑人民币')
hover_cny = plot_cny.select(dict(type=HoverTool))
hover_cny.tooltips = [(u'日期', '@date{%F}'), 
                      (u'USDCNY:NDF:1年', '@ndf{0.0000}'), 
                      (u'中间价:美元兑人民币', '@ref{0.0000}'),
                      (u'即期汇率:美元兑人民币', '@spot{0.0000}')]
hover_cny.formatters = {'date': 'datetime'}
hover_cny.mode = 'mouse'

plot_usdcny = get_plot(u'美元兑离岸/在岸人民币')
plot_usdcny.line('date', 'on', source=source_usdcny, line_width=2, color='#d53e4f', legend=u'美元兑在岸人民币')
plot_usdcny.line('date', 'off', source=source_usdcny, line_width=2, color='#66CC66', legend=u'美元兑离岸人民币')
plot_usdcny.y_range = Range1d(5.4, 7.2)
plot_usdcny.extra_y_ranges = {'diff': Range1d(start=-0.15, end=0.15)}
plot_usdcny.add_layout(LinearAxis(y_range_name='diff'), 'right')
plot_usdcny.vbar(x='date', top='diff', bottom=0, y_range_name='diff', width=1, source=source_usdcny, legend=u'价差')
hover_usdcny = plot_usdcny.select(dict(type=HoverTool))
hover_usdcny.tooltips = [(u'日期', '@date{%F}'),
                         (u'美元兑在岸人民币', '@on{0.0000}'),
                         (u'美元兑离岸人民币', '@off{0.0000}')]
hover_usdcny.formatters = {'date': 'datetime'}
hover_usdcny.mode = 'mouse'

update_all()

curdoc().add_root(column(plot_cny, plot_usdcny))
curdoc().title = u'外汇市场'