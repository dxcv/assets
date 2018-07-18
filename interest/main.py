# encoding: utf-8
import pandas as pd
import numpy as np

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

source_fin = ColumnDataSource(data=dict(date=[], m2=[], fin=[]))
source_m2 = ColumnDataSource(data=dict(date=[], m2=[], fin=[]))
def update_m2():
    fname = '%s/m2.xlsx'%(const.INTEREST_DIR)
    df = pd.read_excel(fname)
    source_m2.data = {'date': df.index,
                      'm2': df[u'M2:同比'] / 100,
                      'fin': df[u'社会融资规模存量:同比'] / 100}
    df = df.copy()
    df.loc[df[u'社会融资规模存量:同比'].shift() == df[u'社会融资规模存量:同比'], u'社会融资规模存量:同比'] = np.NAN
    df = df.dropna()
    source_fin.data = {'date': df.index,
                      'm2': df[u'M2:同比'] / 100,
                      'fin': df[u'社会融资规模存量:同比'] / 100}

source_paper = ColumnDataSource(data=dict(date=[], dir=[], ind=[]))
def update_paper():
    fname = '%s/paper.xlsx'%(const.INTEREST_DIR)
    df = pd.read_excel(fname)
    source_paper.data = {'date': df.index,
                         'dir': df[u'票据直贴利率(月息):6个月:长三角'] / 100,
                         'ind': df[u'票据转贴利率(月息):6个月'] / 100}

source_dr = ColumnDataSource(data=dict(date=[], dr1=[], dr7=[], dr14=[]))
def update_dr():
    fname = '%s/dr.xlsx'%(const.INTEREST_DIR)
    df = pd.read_excel(fname)
    source_dr.data = {'date': df.index,
                      'dr1': df[u'银行间质押式回购加权利率:1天'] / 100,
                      'dr7': df[u'银行间质押式回购加权利率:7天'] / 100,
                      'dr14': df[u'银行间质押式回购加权利率:14天'] / 100}

source_repo = ColumnDataSource(data=dict(date=[], repo=[]))
def update_repo():
    fname = 'D:/Data/risk/weighted_repo.xlsx'
    df = pd.read_excel(fname)
    source_repo.data = {'date': df.index, 'repo': df['rolling mean']}

def update_all():
    update_multiplier()
    update_m2()
    update_paper()
    update_dr()
    update_repo()

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

plot_m2 = get_plot(u'M2和社融同比增速', pct=True)
plot_m2.line('date', 'm2', source=source_m2, line_width=2, color='#d53e4f', legend=u'M2同比')
plot_m2.line('date', 'fin', source=source_fin, line_width=2, legend=u'社融同比')
hover_m2 = plot_m2.select(dict(type=HoverTool))
hover_m2.tooltips = [(u'日期', '@date{%F}'),
                     (u'M2同比', '@m2{0.0%%}'),
                     (u'社融同比', '@fin{0.0%%}')]
hover_m2.formatters = {'date': 'datetime'}
hover_m2.mode = 'mouse'

plot_paper = get_plot(u'票据贴现利率', pct=True)
plot_paper.line('date', 'dir', source=source_paper, line_width=2, legend=u'票据直贴利率(月息):6个月:长三角')
plot_paper.line('date', 'ind', source=source_paper, line_width=2, color='#d53e4f', legend=u'票据转贴利率(月息):6个月')
hover_paper = plot_paper.select(dict(type=HoverTool))
hover_paper.formatters = {'date': 'datetime'}
hover_paper.tooltips = [(u'日期', '@date{%F}'),
                        (u'票据直贴利率(月息):6个月:长三角', '@dir{0.0%%}'),
                        (u'票据转贴利率(月息):6个月', '@ind{0.0%%}')]
hover_paper.mode = 'mouse'

plot_dr = get_plot(u'银行间市场各期限资金利率', pct=True)
plot_dr.line('date', 'dr1', source=source_dr, line_width=2, color='#6600FF', legend=u'银行间质押式回购加权利率:1天')
plot_dr.line('date', 'dr7', source=source_dr, line_width=2, color='#33CCFF', legend=u'银行间质押式回购加权利率:7天')
plot_dr.line('date', 'dr14', source=source_dr, line_width=2, color='#FF6600', legend=u'银行间质押式回购加权利率:14天')
hover_dr = plot_dr.select(dict(type=HoverTool))
hover_dr.formatters = {'date': 'datetime'}
hover_dr.tooltips = [(u'日期', '@date{%F}'),
                     (u'银行间质押式回购加权利率:1天', '@dr1{0.00%%}'),
                     (u'银行间质押式回购加权利率:7天', '@dr7{0.00%%}'),
                     (u'银行间质押式回购加权利率:14天', '@dr14{0.00%%}')]
hover_dr.mode = 'mouse'

plot_repo = get_plot(u'加权回购成交期限')
plot_repo.line('date', 'repo', source=source_repo, line_width=2, legend=u'加权回购成交期限')
hover_repo = plot_repo.select(dict(type=HoverTool))
hover_repo.formatters = {'date': 'datetime'}
hover_repo.tooltips = [(u'日期', '@date{%F}'), (u'期限', '@repo{0.00}')]
hover_repo.mode = 'vline'

update_all()

curdoc().add_root(column(plot_m2, plot_multiplier, plot_paper, plot_dr, plot_repo))
curdoc().title = u'利率体系'