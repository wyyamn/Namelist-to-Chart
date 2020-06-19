# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 11:48:15 2020

@author: natuk
"""

#------------------------------------------
# 将分散的CSV文件中参会人员信息汇总到一个CSV文件中
import os
import pandas as pd
import re

dir_name = './参会名单汇总'
#print(dir_name)

df_list = pd.DataFrame(columns=['姓名','性别','年龄','国家','省市','缴费','衣服尺码'])
column_names = ['c{0:02d}'.format(i) for i in range (10)]
#print(df_list)

for parents, dirnames, filenames in os.walk(dir_name):
    for filename in filenames:
        # 正则匹配 跳过不是.csv 后缀的文件
        if not(re.match('.*\.csv', filename)):
            #print(filename+' not match!!!')
            continue
        #print(filename)
        df = pd.read_csv(os.path.join(parents, filename), encoding='gb18030')
        df['备注'] = filename #信息来源
        #print(df)
        df_list = df_list.append(df, ignore_index=True, sort=False)
        #print(df_list)
        
df_list.dropna(axis=0, thresh=2, how='all', inplace=True)  # 我只想把空行删掉，但是它会把所有行删掉
df_list.to_csv('./sum.csv', encoding='utf-8-sig', index=False)

#-------------------------------------------
#柱状图和折线图
from pyecharts import options as opts
from pyecharts.charts import Bar, Line


men_ages = df_list[df_list['性别'] == '男']['年龄'].tolist()
women_ages = df_list[df_list['性别'] == '女']['年龄'].tolist()

men_age_cnt = [0, 0, 0, 0, 0, 0]
women_age_cnt = [0, 0, 0, 0, 0, 0]

for men_age in men_ages:
    men_age_cnt[men_age // 10 - 1] += 1

for women_age in women_ages:
    women_age_cnt[women_age // 10 - 1] += 1


fee_paid_cnt = [0, 0, 0, 0, 0, 0]

for row in df_list.iterrows():
    if row[1][5] == '是':
        fee_paid_cnt[row[1][2] // 10 - 1] += 1

all_cnt = []
for i in range(6):
    all_cnt.append(men_age_cnt[i] + women_age_cnt[i])

paid_percent = []
for i in range(6):
    paid_percent.append(round(fee_paid_cnt[i] / all_cnt[i] * 100, 2))
    
print(paid_percent)

bar = (
    Bar()
    .add_yaxis("男", men_age_cnt, stack="stack1")
    .add_yaxis("女", women_age_cnt, stack="stack1")
    .add_xaxis(['10~19岁', '20~29岁', '30~39岁', '40~49岁', '50~59岁', '60~69岁'])
    .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
    .set_global_opts(title_opts=opts.TitleOpts(title="参会人员男女分布"),
                     legend_opts=opts.LegendOpts(is_show=True),
                     datazoom_opts=opts.DataZoomOpts())
)

line = (
    Line()
    .add_xaxis(['10~19岁', '20~29岁', '30~39岁', '40~49岁', '50~59岁', '60~69岁'])
    .add_yaxis('缴费比率', paid_percent)
)

bar.overlap(line)
bar.render("./参会男女缴费分布图.html")

#------------------------------------------
#中国地图
prov_dict = {}
for row in df_list.iterrows():
    if row[1][3] == '中国':
        if row[1][4] in prov_dict:
            prov_dict[row[1][4]] += 1
        else:
            prov_dict[row[1][4]] = 1
prov_tuple = list(prov_dict.items())

from pyecharts.charts import Geo

c = (
    Geo()
    .add_schema(maptype="china")
    .add('geo',
         prov_tuple,
         )
    .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(),
        title_opts=opts.TitleOpts(title="Geo-基本示例")
    )
    .render("./省份分布.html")
)

#-----------------------------------------
#世界地图

from pyecharts.globals import ChartType, SymbolType

geo = Geo()
geo.add_schema(maptype="world")

# 可以在网上查找城市的经纬度
geo.add_coordinate(name="洛杉矶", longitude=-118.15, latitude=34.04)
geo.add_coordinate(name="巴塞罗那", longitude=2.17, latitude=41.38)
geo.add_coordinate(name="孟买", longitude=72.87, latitude=19.07)
geo.add_coordinate(name="墨尔本", longitude=144.96, latitude=-37.81)
geo.add_coordinate(name="圣彼得堡", longitude=30.36, latitude=59.93)
geo.add_coordinate(name="斯图加特", longitude=9.18, latitude=48.77)
geo.add_coordinate(name="圣地亚哥", longitude=-117.16, latitude=32.71)
geo.add_coordinate(name="里约热内卢", longitude=-43.17, latitude=-22.90)
geo.add_coordinate(name="伊尔库斯克", longitude=104.28, latitude=52.28)
geo.add_coordinate(name="曼谷", longitude=100.50, latitude=13.75)
geo.add_coordinate(name="开普敦", longitude=18.42, latitude=-33.92)
geo.add_coordinate(name="阿布扎比", longitude=54.37, latitude=24.45)
geo.add_coordinate(name="檀香山", longitude=-157.85, latitude=21.30)
geo.add_coordinate(name="安克雷奇", longitude=-149.90, latitude=61.21)
geo.add_coordinate(name="东京", longitude=139.76, latitude=35.68)
geo.add_coordinate(name="北京", longitude=116.40, latitude=39.90)

geo.add('geo',
        [("洛杉矶", "北京"),
         ("巴塞罗那", "北京"),
         ("孟买", "北京"),
         ("墨尔本", "北京"),
         ("圣彼得堡", "北京"),
         ("斯图加特", "北京"),
         ("圣地亚哥", "北京"),
         ("里约热内卢", "北京"),
         ("伊尔库斯克", "北京"),
         ("曼谷", "北京"),
         ("开普敦", "北京"),
         ("阿布扎比", "北京"),
         ("檀香山", "北京"),
         ("安克雷奇", "北京"),
         ("东京", "北京"),
         ],
        type_=ChartType.LINES,
        effect_opts=opts.EffectOpts(symbol=SymbolType.ARROW, symbol_size=6, color="blue")
    )
geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
geo.set_global_opts(visualmap_opts=opts.VisualMapOpts(),
        title_opts=opts.TitleOpts(title="Geo-世界地图"))
geo.render('./世界地图.html')

