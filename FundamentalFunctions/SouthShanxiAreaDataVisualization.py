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
plt.title("晋南地区各城市道路通行情况")

# 使用pandas读取excel文件
df_changzhi = pd.read_excel(r'F:/01.XLS', sheet_name='长治市')
df_jincheng = pd.read_excel(r'F:/01.XLS', sheet_name='晋城市')
df_linfeng = pd.read_excel(r'F:/01.XLS', sheet_name='临汾市')
df_yuncheng = pd.read_excel(r'F:/01.XLS', sheet_name='运城市')

# 设置子图默认间距
plt.subplots_adjust(hspace=0.5)
# 长治市数据可视化
plt.subplot(2, 2, 1)
# 添加条形图的标题
plt.title('长治市各道路通行情况', fontsize=16)
plt.ylabel("拥堵路段信息统计（单位：出现次数）", fontsize=16)
plt.xlabel("道路名称", fontsize=16)

# 获取指定道路名称的拥堵评价信息
changzhi_road_name = df_changzhi.groupby(['道路名称']).agg({'道路名称': 'count'}).to_dict()
changzhi_road_cong = df_changzhi.groupby(['道路名称']).agg({'路段拥堵评价': 'count'}).to_dict()

# 两个道路信息进行合并
changzhi_combination = tuple(zip(changzhi_road_cong['路段拥堵评价'].values(), changzhi_road_name['道路名称'].values()))

# 获取拥堵占比信息，道路通畅次数
changzhi_cong_proportion = []
changzhi_clear_road = []

for item in list(changzhi_combination):
    # print("{:.2f}".format(item[0]/item[1]))
    changzhi_cong_proportion.append(float("{:.2f}".format(item[0] / item[1])))
    changzhi_clear_road.append(int("{0}".format(item[1] - item[0])))

changzhi_information = df_changzhi.groupby(['道路名称']).agg({'道路名称': 'count', '路段拥堵评价': 'count'})
# print(changzhi_information)
# print(type(changzhi_information))
changzhi_information['拥堵占比'] = changzhi_cong_proportion
changzhi_information['道路畅通评价'] = changzhi_clear_road
# print(changzhi_information)
# print(list(changzhi_information['道路名称']))
# print(list(changzhi_information['路段拥堵评价']))
# print(list(changzhi_information['拥堵占比']))
# print(changzhi_information['道路畅通评价'])
# 纵轴列表数据
y = range(0, 101, 10)
# print(y)

# 长治市道路名称
changzhi_road_name_list = ['太行东街', '太行西街', '英雄中路', '英雄北路', '英雄南路']
plt.xticks(range(len(changzhi_road_name_list)), changzhi_road_name_list, rotation=70, fontsize=16)

plt.yticks(range(0, 101, 10), fontsize=16)

plt.bar(np.arange(5) - 0.3, height=list(changzhi_road_name['道路名称'].values()), alpha=0.5, width=0.3, color='skyblue',
        edgecolor='red', label='道路获取次数')
plt.bar(np.arange(5), height=list(changzhi_information['道路畅通评价']), alpha=0.5, width=0.3, color='green',
        edgecolor='blue', label='道路畅通次数')
plt.bar(np.arange(5) + 0.3, height=list(changzhi_information['路段拥堵评价']), alpha=0.5, width=0.3, color='yellow',
        edgecolor='blue', label='道路拥堵次数')

# 晋城市数据可视化
plt.subplot(2, 2, 2)
# 添加条形图的标题
plt.title('晋城市各道路通行情况', fontsize=16)
plt.ylabel("拥堵路段信息统计（单位：出现次数）", fontsize=16)
plt.xlabel("道路名称", fontsize=16)

# 获取指定道路名称的拥堵评价信息
jincheng_road_name = df_jincheng.groupby(['道路名称']).agg({'道路名称': 'count'}).to_dict()
jincheng_road_cong = df_jincheng.groupby(['道路名称']).agg({'路段拥堵评价': 'count'}).to_dict()

# 两个道路信息进行合并
jincheng_combination = tuple(zip(jincheng_road_cong['路段拥堵评价'].values(), jincheng_road_name['道路名称'].values()))

# 获取拥堵占比信息，道路通畅次数
jincheng_cong_proportion = []
jincheng_clear_road = []

for item in list(jincheng_combination):
    # print("{:.2f}".format(item[0]/item[1]))
    jincheng_cong_proportion.append(float("{:.2f}".format(item[0] / item[1])))
    jincheng_clear_road.append(int("{0}".format(item[1] - item[0])))

jincheng_information = df_jincheng.groupby(['道路名称']).agg({'道路名称': 'count', '路段拥堵评价': 'count'})

# print(type(jincheng_information))
jincheng_information['拥堵占比'] = jincheng_cong_proportion
jincheng_information['道路畅通评价'] = jincheng_clear_road

# print(list(jincheng_information['道路名称']))
# print(list(jincheng_information['路段拥堵评价']))
# print(list(jincheng_information['拥堵占比']))
# print(list(jincheng_information['道路畅通评价']))
# 纵轴列表数据
y = range(0, 101, 10)
# print(y)

# 晋城市道路名称
jincheng_road_name_list = ['中原东街', '中原西街', '凤台东街', '凤台西街', '泽州南路', '泽州路']
plt.xticks(range(len(jincheng_road_name_list)), jincheng_road_name_list, rotation=70, fontsize=16)

plt.yticks(range(0, 101, 10), fontsize=16)

plt.bar(np.arange(6) - 0.3, height=list(jincheng_road_name['道路名称'].values()), alpha=0.5, width=0.3, color='skyblue',
        edgecolor='red', label='道路获取次数')
plt.bar(np.arange(6), height=list(jincheng_information['道路畅通评价']), alpha=0.5, width=0.3, color='green',
        edgecolor='blue', label='道路畅通次数')
plt.bar(np.arange(6) + 0.3, height=list(jincheng_information['路段拥堵评价']), alpha=0.5, width=0.3, color='yellow',
        edgecolor='blue', label='道路拥堵次数')

# 临汾市数据可视化
plt.subplot(2, 2, 3)
# 添加条形图的标题
plt.title('临汾市各道路通行情况', fontsize=16)
plt.ylabel("拥堵路段信息统计（单位：出现次数）", fontsize=16)
plt.xlabel("道路名称", fontsize=16)

# 获取指定道路名称的拥堵评价信息
linfeng_road_name = df_linfeng.groupby(['道路名称']).agg({'道路名称': 'count'}).to_dict()
linfeng_road_cong = df_linfeng.groupby(['道路名称']).agg({'路段拥堵评价': 'count'}).to_dict()

# 两个道路信息进行合并
linfeng_combination = tuple(zip(linfeng_road_cong['路段拥堵评价'].values(), linfeng_road_name['道路名称'].values()))

# 获取拥堵占比信息，道路通畅次数
linfeng_cong_proportion = []
linfeng_clear_road = []

for item in list(linfeng_combination):
    # print("{:.2f}".format(item[0]/item[1]))
    linfeng_cong_proportion.append(float("{:.2f}".format(item[0] / item[1])))
    linfeng_clear_road.append(int("{0}".format(item[1] - item[0])))

linfeng_information = df_linfeng.groupby(['道路名称']).agg({'道路名称': 'count', '路段拥堵评价': 'count'})

# print(type(linfeng_information))
linfeng_information['拥堵占比'] = linfeng_cong_proportion
linfeng_information['道路畅通评价'] = linfeng_clear_road

# print(list(linfeng_information['道路名称']))
# print(list(linfeng_information['路段拥堵评价']))
# print(list(linfeng_information['拥堵占比']))
# print(list(linfeng_information['道路畅通评价']))
# 纵轴列表数据
y = range(0, 101, 10)
# print(y)

# 临汾市道路名称
linfeng_road_name_list = ['滨河西路', '滨河路', '鼓楼北大街', '鼓楼南大街']
plt.xticks(range(len(linfeng_road_name_list)), linfeng_road_name_list, rotation=70, fontsize=16)

plt.yticks(range(0, 101, 10), fontsize=16)

plt.bar(np.arange(4) - 0.3, height=list(linfeng_road_name['道路名称'].values()), alpha=0.5, width=0.3, color='skyblue',
        edgecolor='red', label='道路获取次数')
plt.bar(np.arange(4), height=list(linfeng_information['道路畅通评价']), alpha=0.5, width=0.3, color='green', edgecolor='blue',
        label='道路畅通次数')
plt.bar(np.arange(4) + 0.3, height=list(linfeng_information['路段拥堵评价']), alpha=0.5, width=0.3, color='yellow',
        edgecolor='blue', label='道路拥堵次数')

# 运城市数据可视化
plt.subplot(2, 2, 4)
# 添加条形图的标题
plt.title('运城市各道路通行情况', fontsize=16)
plt.ylabel("拥堵路段信息统计（单位：出现次数）", fontsize=16)
plt.xlabel("道路名称", fontsize=16)

# 获取指定道路名称的拥堵评价信息
yuncheng_road_name = df_yuncheng.groupby(['道路名称']).agg({'道路名称': 'count'}).to_dict()
yuncheng_road_cong = df_yuncheng.groupby(['道路名称']).agg({'路段拥堵评价': 'count'}).to_dict()

# 两个道路信息进行合并
yuncheng_combination = tuple(zip(yuncheng_road_cong['路段拥堵评价'].values(), yuncheng_road_name['道路名称'].values()))

# 获取拥堵占比信息，道路通畅次数
yuncheng_cong_proportion = []
yuncheng_clear_road = []

for item in list(yuncheng_combination):
    # print("{:.2f}".format(item[0]/item[1]))
    yuncheng_cong_proportion.append(float("{:.2f}".format(item[0] / item[1])))
    yuncheng_clear_road.append(int("{0}".format(item[1] - item[0])))

yuncheng_information = df_yuncheng.groupby(['道路名称']).agg({'道路名称': 'count', '路段拥堵评价': 'count'})

# print(type(yuncheng_information))
yuncheng_information['拥堵占比'] = yuncheng_cong_proportion
yuncheng_information['道路畅通评价'] = yuncheng_clear_road

# print(list(yuncheng_information['道路名称']))
# print(list(yuncheng_information['路段拥堵评价']))
# print(list(yuncheng_information['拥堵占比']))
# print(list(yuncheng_information['道路畅通评价']))
# 纵轴列表数据
y = range(0, 101, 10)
# print(y)

# 运城市道路名称
yuncheng_road_name_list = ['中银北路', '中银南路', '人民北路', '学苑路', '工农东街', '机场路', '解放北路', '解放南路']
plt.xticks(range(len(yuncheng_road_name_list)), yuncheng_road_name_list, rotation=70, fontsize=16)

plt.yticks(range(0, 101, 10), fontsize=16)

plt.bar(np.arange(8) - 0.3, height=list(yuncheng_road_name['道路名称'].values()), alpha=0.5, width=0.3, color='skyblue',
        edgecolor='red', label='道路获取次数')
plt.bar(np.arange(8), height=list(yuncheng_information['道路畅通评价']), alpha=0.5, width=0.3, color='green',
        edgecolor='blue', label='道路畅通次数')
plt.bar(np.arange(8) + 0.3, height=list(yuncheng_information['路段拥堵评价']), alpha=0.5, width=0.3, color='yellow',
        edgecolor='blue', label='道路拥堵次数')
plt.savefig(r"C:\Users\高怡飞\Desktop\03.png", dpi=600)
