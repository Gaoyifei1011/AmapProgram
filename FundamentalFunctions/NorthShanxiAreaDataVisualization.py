import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

"""
Copy from Jupyter Notebook
"""
# TODO: In the future version will insert into the 山西省道路信息分析系统 page.

# 设置字体，否则中文会显示异常
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['figure.figsize'] = (22.0, 14.0)
plt.title("晋北地区各城市道路通行情况")

# 使用pandas读取excel文件
df_datong = pd.read_excel(r'F:/01.XLS', sheet_name='大同市')
df_shuozhou = pd.read_excel(r'F:/01.XLS', sheet_name='朔州市')
df_xinzhou = pd.read_excel(r'F:/01.XLS', sheet_name='忻州市')

# 设置子图默认间距
plt.subplots_adjust(hspace=0.5)
# 大同市数据可视化
plt.subplot(2, 2, 1)
# 添加条形图的标题
plt.title('大同市各道路通行情况', fontsize=16)
plt.ylabel("拥堵路段信息统计（单位：出现次数）", fontsize=16)
plt.xlabel("道路名称", fontsize=16)

# 获取指定道路名称的拥堵评价信息
datong_road_name = df_datong.groupby(['道路名称']).agg({'道路名称': 'count'}).to_dict()
datong_road_cong = df_datong.groupby(['道路名称']).agg({'路段拥堵评价': 'count'}).to_dict()

# 两个道路信息进行合并
datong_combination = tuple(zip(datong_road_cong['路段拥堵评价'].values(), datong_road_name['道路名称'].values()))

# 获取拥堵占比信息，道路通畅次数
datong_cong_proportion = []
datong_clear_road = []

for item in list(datong_combination):
    # print("{:.2f}".format(item[0]/item[1]))
    datong_cong_proportion.append(float("{:.2f}".format(item[0] / item[1])))
    datong_clear_road.append(int("{0}".format(item[1] - item[0])))

datong_information = df_datong.groupby(['道路名称']).agg({'道路名称': 'count', '路段拥堵评价': 'count'})
# print(datong_information)
# print(type(datong_information))
datong_information['拥堵占比'] = datong_cong_proportion
datong_information['道路畅通评价'] = datong_clear_road
# print(datong_information)
# print(list(datong_information['道路名称']))
# print(list(datong_information['路段拥堵评价']))
# print(list(datong_information['拥堵占比']))
# print(datong_information['道路畅通评价'])
# 纵轴列表数据
y = range(0, 101, 10)
# print(y)

# 大同市道路名称
datong_road_name_list = ['云中路', '北都街', '南环路', '同煤快线', '御河东路', '御河西路', '文兴路', '迎宾街', '魏都大道']
plt.xticks(range(len(datong_road_name_list)), datong_road_name_list, rotation=70, fontsize=16)

plt.yticks(range(0, 101, 10), fontsize=16)

plt.bar(np.arange(9) - 0.3, height=list(datong_road_name['道路名称'].values()), alpha=0.5, width=0.3, color='skyblue',
        edgecolor='red', label='道路获取次数')
plt.bar(np.arange(9), height=list(datong_information['道路畅通评价']), alpha=0.5, width=0.3, color='green', edgecolor='blue',
        label='道路畅通次数')
plt.bar(np.arange(9) + 0.3, height=list(datong_information['路段拥堵评价']), alpha=0.5, width=0.3, color='yellow',
        edgecolor='blue', label='道路拥堵次数')

# 朔州市数据可视化
plt.subplot(2, 2, 2)
# 添加条形图的标题
plt.title('朔州市各道路通行情况', fontsize=16)
plt.ylabel("拥堵路段信息统计（单位：出现次数）", fontsize=16)
plt.xlabel("道路名称", fontsize=16)

# 获取指定道路名称的拥堵评价信息
shuozhou_road_name = df_shuozhou.groupby(['道路名称']).agg({'道路名称': 'count'}).to_dict()
shuozhou_road_cong = df_shuozhou.groupby(['道路名称']).agg({'路段拥堵评价': 'count'}).to_dict()

# 两个道路信息进行合并
shuozhou_combination = tuple(zip(shuozhou_road_cong['路段拥堵评价'].values(), shuozhou_road_name['道路名称'].values()))

# 获取拥堵占比信息，道路通畅次数
shuozhou_cong_proportion = []
shuozhou_clear_road = []

for item in list(shuozhou_combination):
    # print("{:.2f}".format(item[0]/item[1]))
    shuozhou_cong_proportion.append(float("{:.2f}".format(item[0] / item[1])))
    shuozhou_clear_road.append(int("{0}".format(item[1] - item[0])))

shuozhou_information = df_shuozhou.groupby(['道路名称']).agg({'道路名称': 'count', '路段拥堵评价': 'count'})

# print(type(shuozhou_information))
shuozhou_information['拥堵占比'] = shuozhou_cong_proportion
shuozhou_information['道路畅通评价'] = shuozhou_clear_road

# print(list(shuozhou_information['道路名称']))
# print(list(shuozhou_information['路段拥堵评价']))
# print(list(shuozhou_information['拥堵占比']))
# print(list(shuozhou_information['道路畅通评价']))
# 纵轴列表数据
y = range(0, 101, 10)
# print(y)

# 朔州市道路名称
shuozhou_road_name_list = ['开发北路', '开发南路', '张辽北路', '张辽南路', '文远路', '民福东街', '民福西街']
plt.xticks(range(len(shuozhou_road_name_list)), shuozhou_road_name_list, rotation=70, fontsize=16)

plt.yticks(range(0, 101, 10), fontsize=16)

plt.bar(np.arange(7) - 0.3, height=list(shuozhou_road_name['道路名称'].values()), alpha=0.5, width=0.3, color='skyblue',
        edgecolor='red', label='道路获取次数')
plt.bar(np.arange(7), height=list(shuozhou_information['道路畅通评价']), alpha=0.5, width=0.3, color='green',
        edgecolor='blue', label='道路畅通次数')
plt.bar(np.arange(7) + 0.3, height=list(shuozhou_information['路段拥堵评价']), alpha=0.5, width=0.3, color='yellow',
        edgecolor='blue', label='道路拥堵次数')

# 忻州市数据可视化
plt.subplot(2, 2, 3)
# 添加条形图的标题
plt.title('忻州市各道路通行情况', fontsize=16)
plt.ylabel("拥堵路段信息统计（单位：出现次数）", fontsize=16)
plt.xlabel("道路名称", fontsize=16)

# 获取指定道路名称的拥堵评价信息
xinzhou_road_name = df_xinzhou.groupby(['道路名称']).agg({'道路名称': 'count'}).to_dict()
xinzhou_road_cong = df_xinzhou.groupby(['道路名称']).agg({'路段拥堵评价': 'count'}).to_dict()

# 两个道路信息进行合并
xinzhou_combination = tuple(zip(xinzhou_road_cong['路段拥堵评价'].values(), xinzhou_road_name['道路名称'].values()))

# 获取拥堵占比信息，道路通畅次数
xinzhou_cong_proportion = []
xinzhou_clear_road = []

for item in list(xinzhou_combination):
    # print("{:.2f}".format(item[0]/item[1]))
    xinzhou_cong_proportion.append(float("{:.2f}".format(item[0] / item[1])))
    xinzhou_clear_road.append(int("{0}".format(item[1] - item[0])))

xinzhou_information = df_xinzhou.groupby(['道路名称']).agg({'道路名称': 'count', '路段拥堵评价': 'count'})

# print(type(xinzhou_information))
xinzhou_information['拥堵占比'] = xinzhou_cong_proportion
xinzhou_information['道路畅通评价'] = xinzhou_clear_road

# print(list(xinzhou_information['道路名称']))
# print(list(xinzhou_information['路段拥堵评价']))
# print(list(xinzhou_information['拥堵占比']))
# print(list(xinzhou_information['道路畅通评价']))
# 纵轴列表数据
y = range(0, 101, 10)
# print(y)

# 忻州市道路名称
xinzhou_road_name_list = ['七一北路', '七一南路', '和平东街', '和平西街', '建设北路', '建设南路', '慕山北路', '慕山南路', '雁门西大道']
plt.xticks(range(len(xinzhou_road_name_list)), xinzhou_road_name_list, rotation=70, fontsize=16)

plt.yticks(range(0, 101, 10), fontsize=16)

plt.bar(np.arange(9) - 0.3, height=list(xinzhou_road_name['道路名称'].values()), alpha=0.5, width=0.3, color='skyblue',
        edgecolor='red', label='道路获取次数')
plt.bar(np.arange(9), height=list(xinzhou_information['道路畅通评价']), alpha=0.5, width=0.3, color='green', edgecolor='blue',
        label='道路畅通次数')
plt.bar(np.arange(9) + 0.3, height=list(xinzhou_information['路段拥堵评价']), alpha=0.5, width=0.3, color='yellow',
        edgecolor='blue', label='道路拥堵次数')

plt.savefig(r"C:\Users\高怡飞\Desktop\02.png", dpi=600)
