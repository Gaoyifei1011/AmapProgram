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
plt.title("晋中地区各城市道路通行情况")

# 使用pandas读取excel文件
df_taiyuan = pd.read_excel(r'F:/01.XLS', sheet_name='太原市')
df_jinzhong = pd.read_excel(r'F:/01.XLS', sheet_name='晋中市')
df_lvliang = pd.read_excel(r'F:/01.XLS', sheet_name='吕梁市')
df_yangquan = pd.read_excel(r'F:/01.XLS', sheet_name='阳泉市')

# 设置子图默认间距
plt.subplots_adjust(hspace=0.5)
# 太原市数据可视化
plt.subplot(2, 2, 1)
# 添加条形图的标题
plt.title('太原市各道路通行情况', fontsize=16)
plt.ylabel("拥堵路段信息统计（单位：出现次数）", fontsize=16)
plt.xlabel("道路名称", fontsize=16)

# 获取指定道路名称的拥堵评价信息
taiyuan_road_name = df_taiyuan.groupby(['道路名称']).agg({'道路名称': 'count'}).to_dict()
taiyuan_road_cong = df_taiyuan.groupby(['道路名称']).agg({'路段拥堵评价': 'count'}).to_dict()

# 两个道路信息进行合并
taiyuan_combination = tuple(zip(taiyuan_road_cong['路段拥堵评价'].values(), taiyuan_road_name['道路名称'].values()))

# 获取拥堵占比信息，道路通畅次数
taiyuan_cong_proportion = []
taiyuan_clear_road = []

for item in list(taiyuan_combination):
    # print("{:.2f}".format(item[0]/item[1]))
    taiyuan_cong_proportion.append(float("{:.2f}".format(item[0] / item[1])))
    taiyuan_clear_road.append(int("{0}".format(item[1] - item[0])))

taiyuan_information = df_taiyuan.groupby(['道路名称']).agg({'道路名称': 'count', '路段拥堵评价': 'count'})
# print(taiyuan_information)
# print(type(taiyuan_information))
taiyuan_information['拥堵占比'] = taiyuan_cong_proportion
taiyuan_information['道路畅通评价'] = taiyuan_clear_road
# print(taiyuan_information)
# print(list(taiyuan_information['道路名称']))
# print(list(taiyuan_information['路段拥堵评价']))
# print(list(taiyuan_information['拥堵占比']))
# print(taiyuan_information['道路畅通评价'])
# 纵轴列表数据
y = range(0, 101, 10)
# print(y)

# 太原市道路名称
taiyuan_road_name_list = ['东中环路', '五一路', '北中环街', '南中环街', '南内环街', '太榆路', '平阳路', '并州北路', '并州南路', '府东街', '建设北路', '建设南路',
                          '滨河东路', '滨河西路', '西中环路', '迎泽大街', '长风街']
plt.xticks(range(len(taiyuan_road_name_list)), taiyuan_road_name_list, rotation=70, fontsize=16)

plt.yticks(range(0, 101, 10), fontsize=16)

plt.bar(np.arange(17) - 0.3, height=list(taiyuan_road_name['道路名称'].values()), alpha=0.5, width=0.3, color='skyblue',
        edgecolor='red', label='道路获取次数')
plt.bar(np.arange(17), height=list(taiyuan_information['道路畅通评价']), alpha=0.5, width=0.3, color='green',
        edgecolor='blue', label='道路畅通次数')
plt.bar(np.arange(17) + 0.3, height=list(taiyuan_information['路段拥堵评价']), alpha=0.5, width=0.3, color='yellow',
        edgecolor='blue', label='道路拥堵次数')

# 晋中市数据可视化
plt.subplot(2, 2, 2)
# 添加条形图的标题
plt.title('晋中市各道路通行情况', fontsize=16)
plt.ylabel("拥堵路段信息统计（单位：出现次数）", fontsize=16)
plt.xlabel("道路名称", fontsize=16)

# 获取指定道路名称的拥堵评价信息
jinzhong_road_name = df_jinzhong.groupby(['道路名称']).agg({'道路名称': 'count'}).to_dict()
jinzhong_road_cong = df_jinzhong.groupby(['道路名称']).agg({'路段拥堵评价': 'count'}).to_dict()

# 两个道路信息进行合并
jinzhong_combination = tuple(zip(jinzhong_road_cong['路段拥堵评价'].values(), jinzhong_road_name['道路名称'].values()))

# 获取拥堵占比信息，道路通畅次数
jinzhong_cong_proportion = []
jinzhong_clear_road = []

for item in list(jinzhong_combination):
    # print("{:.2f}".format(item[0]/item[1]))
    jinzhong_cong_proportion.append(float("{:.2f}".format(item[0] / item[1])))
    jinzhong_clear_road.append(int("{0}".format(item[1] - item[0])))

jinzhong_information = df_jinzhong.groupby(['道路名称']).agg({'道路名称': 'count', '路段拥堵评价': 'count'})

# print(type(jinzhong_information))
jinzhong_information['拥堵占比'] = jinzhong_cong_proportion
jinzhong_information['道路畅通评价'] = jinzhong_clear_road

# print(list(jinzhong_information['道路名称']))
# print(list(jinzhong_information['路段拥堵评价']))
# print(list(jinzhong_information['拥堵占比']))
# print(list(jinzhong_information['道路畅通评价']))
# 纵轴列表数据
y = range(0, 101, 10)
# print(y)

# 晋中市道路名称
jinzhong_road_name_list = ['中都路', '定阳路', '新建路', '汇通北路', '汇通南路', '汇通路', '蕴华街', '迎宾街', '锦纶路', '顺城街', '龙湖街']
plt.xticks(range(len(jinzhong_road_name_list)), jinzhong_road_name_list, rotation=70, fontsize=16)

plt.yticks(range(0, 101, 10), fontsize=16)

plt.bar(np.arange(11) - 0.3, height=list(jinzhong_road_name['道路名称'].values()), alpha=0.5, width=0.3, color='skyblue',
        edgecolor='red', label='道路获取次数')
plt.bar(np.arange(11), height=list(jinzhong_information['道路畅通评价']), alpha=0.5, width=0.3, color='green',
        edgecolor='blue', label='道路畅通次数')
plt.bar(np.arange(11) + 0.3, height=list(jinzhong_information['路段拥堵评价']), alpha=0.5, width=0.3, color='yellow',
        edgecolor='blue', label='道路拥堵次数')

# 阳泉市数据可视化
plt.subplot(2, 2, 3)
# 添加条形图的标题
plt.title('阳泉市各道路通行情况', fontsize=16)
plt.ylabel("拥堵路段信息统计（单位：出现次数）", fontsize=16)
plt.xlabel("道路名称", fontsize=16)

# 获取指定道路名称的拥堵评价信息
yangquan_road_name = df_yangquan.groupby(['道路名称']).agg({'道路名称': 'count'}).to_dict()
yangquan_road_cong = df_yangquan.groupby(['道路名称']).agg({'路段拥堵评价': 'count'}).to_dict()

# 两个道路信息进行合并
yangquan_combination = tuple(zip(yangquan_road_cong['路段拥堵评价'].values(), yangquan_road_name['道路名称'].values()))

# 获取拥堵占比信息，道路通畅次数
yangquan_cong_proportion = []
yangquan_clear_road = []

for item in list(yangquan_combination):
    # print("{:.2f}".format(item[0]/item[1]))
    yangquan_cong_proportion.append(float("{:.2f}".format(item[0] / item[1])))
    yangquan_clear_road.append(int("{0}".format(item[1] - item[0])))

yangquan_information = df_yangquan.groupby(['道路名称']).agg({'道路名称': 'count', '路段拥堵评价': 'count'})

# print(type(yangquan_information))
yangquan_information['拥堵占比'] = yangquan_cong_proportion
yangquan_information['道路畅通评价'] = yangquan_clear_road

# print(list(yangquan_information['道路名称']))
# print(list(yangquan_information['路段拥堵评价']))
# print(list(yangquan_information['拥堵占比']))
# print(list(yangquan_information['道路畅通评价']))
# 纵轴列表数据
y = range(0, 101, 10)
# print(y)

# 阳泉市道路名称
yangquan_road_name_list = ['东环路', '南大街', '桃北东街', '桃北中街', '泉中路']
plt.xticks(range(len(yangquan_road_name_list)), yangquan_road_name_list, rotation=70, fontsize=16)

plt.yticks(range(0, 101, 10), fontsize=16)

plt.bar(np.arange(5) - 0.3, height=list(yangquan_road_name['道路名称'].values()), alpha=0.5, width=0.3, color='skyblue',
        edgecolor='red', label='道路获取次数')
plt.bar(np.arange(5), height=list(yangquan_information['道路畅通评价']), alpha=0.5, width=0.3, color='green',
        edgecolor='blue', label='道路畅通次数')
plt.bar(np.arange(5) + 0.3, height=list(yangquan_information['路段拥堵评价']), alpha=0.5, width=0.3, color='yellow',
        edgecolor='blue', label='道路拥堵次数')

# 吕梁市数据可视化
plt.subplot(2, 2, 4)
# 添加条形图的标题
plt.title('吕梁市各道路通行情况', fontsize=16)
plt.ylabel("拥堵路段信息统计（单位：出现次数）", fontsize=16)
plt.xlabel("道路名称", fontsize=16)

# 获取指定道路名称的拥堵评价信息
lvliang_road_name = df_lvliang.groupby(['道路名称']).agg({'道路名称': 'count'}).to_dict()
lvliang_road_cong = df_lvliang.groupby(['道路名称']).agg({'路段拥堵评价': 'count'}).to_dict()

# 两个道路信息进行合并
lvliang_combination = tuple(zip(lvliang_road_cong['路段拥堵评价'].values(), lvliang_road_name['道路名称'].values()))

# 获取拥堵占比信息，道路通畅次数
lvliang_cong_proportion = []
lvliang_clear_road = []

for item in list(lvliang_combination):
    # print("{:.2f}".format(item[0]/item[1]))
    lvliang_cong_proportion.append(float("{:.2f}".format(item[0] / item[1])))
    lvliang_clear_road.append(int("{0}".format(item[1] - item[0])))

lvliang_information = df_lvliang.groupby(['道路名称']).agg({'道路名称': 'count', '路段拥堵评价': 'count'})

# print(type(lvliang_information))
lvliang_information['拥堵占比'] = lvliang_cong_proportion
lvliang_information['道路畅通评价'] = lvliang_clear_road

# print(list(lvliang_information['道路名称']))
# print(list(lvliang_information['路段拥堵评价']))
# print(list(lvliang_information['拥堵占比']))
# print(list(lvliang_information['道路畅通评价']))
# 纵轴列表数据
y = range(0, 101, 10)
# print(y)

# 吕梁市道路名称
lvliang_road_name_list = ['北川河西路', '吕梁大道', '滨河北东路', '滨河北中路', '滨河北西路', '龙凤北大街', '龙凤南大街']
plt.xticks(range(len(lvliang_road_name_list)), lvliang_road_name_list, rotation=70, fontsize=16)

plt.yticks(range(0, 101, 10), fontsize=16)

plt.bar(np.arange(7) - 0.3, height=list(lvliang_road_name['道路名称'].values()), alpha=0.5, width=0.3, color='skyblue',
        edgecolor='red', label='道路获取次数')
plt.bar(np.arange(7), height=list(lvliang_information['道路畅通评价']), alpha=0.5, width=0.3, color='green', edgecolor='blue',
        label='道路畅通次数')
plt.bar(np.arange(7) + 0.3, height=list(lvliang_information['路段拥堵评价']), alpha=0.5, width=0.3, color='yellow',
        edgecolor='blue', label='道路拥堵次数')
plt.savefig(r"C:\Users\高怡飞\Desktop\01.png", dpi=600)
