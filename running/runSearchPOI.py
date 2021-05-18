from AmapFunctions.SearchPOI import *

# 关键字搜索
# keywords = input("请输入您要查询的关键字（可选）：")
# types = input("请输入您要查询的类型（可选）：")
# city = input("请输入您要查询关键字对应的城市（可选）：")

# 周边搜索
# location = input("请输入您要查询的中心点坐标：")
# keywords = input("请输入您要查询的关键字（可选）：")
# types = input("请输入您要查询的类型（可选）：")
# city = input("请输入您要查询关键字对应的城市（可选）：")
# context = input("请输入您要查询距离中心点坐标的半径，默认为3000（可选）：")
# if context == '':
#     radius = 1000
# else:
#     radius = int(context)

# 多边形搜索
# polygon = input("请输入您要查询经纬度坐标对：")
# keywords = input("请输入您要查询的关键字（可选）：")
# types = input("请输入您要查询的类型（可选）：")

search_poi = SearchPOI()

# 获取数据——关键字搜索
# result_search_poi = search_poi.get_search_poi_by_keywords(keywords=keywords,types=types,city=city,extensions='all')
# search_poi.parse_search_poi(result_search_poi,keywords=keywords,extensions='all')

# 获取数据——周边搜索
# result_search_poi = search_poi.get_search_poi_by_arounds(location=location, keywords=keywords, types=types, city=city,
#                                                          radius=radius, extensions='all')
# search_poi.parse_search_poi(result_search_poi, keywords=keywords, extensions='all')

# 获取数据——多边形搜索
# result_search_poi = search_poi.get_search_poi_by_polygon(polygon=polygon, keywords=keywords, types=types,
#                                                          extensions='all')
# search_poi.parse_search_poi(result_search_poi, keywords=keywords, extensions='all')

# 获取数据——ID查询
poi_id = input("请输入您的兴趣点ID：")
result_search_poi = search_poi.get_search_poi_by_id(poi_id=poi_id)
search_poi.parse_search_poi(result_search_poi, extensions='all')
