# encoding: utf-8
import pandas as pd

import interest.const as const
import interest.data as data

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import ColumnDataSource, NumeralTickFormatter, Range1d, LinearAxis, HoverTool
from bokeh.plotting import figure
from bokeh.palettes import Spectral9

COLORS = Spectral9 + ["#053061", "#2166ac", "#4393c3" "#92c5de", "#d1e5f0"]
col2edb, edb2col = data.get_col2edb()

source_multiplier = ColumnDataSource(data=dict(date=[], mul=[]))
def update_multiplier():
    fname = '%s/multiplier.xlsx'%(const.INTEREST_DIR)
    df = pd.read_excel(fname)
    source_multiplier.data = {'date': df.index,
                              'mul': df[u'货币乘数']}

def update_all():
    update_multiplier()

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

plot_multiplier = get_plot(u'货币乘数')
plot_multiplier.line('date', 'mul', source=source_multiplier, line_width=2, color='#d53e4f', legend=u'货币乘数')
hover_multiplier = plot_multiplier.select(dict(type=HoverTool))
hover_multiplier.tooltips = [(u'日期', '@date{%F}'),
                             (u'货币乘数', '@mul{0.0000}')]
hover_multiplier.formatters = {'date': 'datetime'}
hover_multiplier.mode = 'vline'

update_all()

curdoc().add_root(plot_multiplier)
curdoc().title = u'利率体系'