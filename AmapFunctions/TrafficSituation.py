# -*- coding:utf-8 -*-
# 导入的库
import json

import requests


class TrafficSituation:
    """
    高德地图API已停止使用，该项目目前暂时停止使用，目前使用百度地图API爬取。
    """
    def __init__(self):
        pass

    # 获取高德地图数据API的钥匙
    APIkey = '<请自己输入自己申请的API Key>'
    fileitem = 1

    def get_traffic_situation_by_rectangle(self, rectangle: str,
                                           level: int = 5,
                                           extensions: str = 'base',
                                           output: str = 'JSON',
                                           ) -> dict:
        """
        函数：矩形区域交通态势
        Args:
            rectangle:代表此为矩形区域查询，必填。左下右上顶点坐标对。矩形对角线不能超过10公里。两个坐标对之间用”;”间隔。xy之间用”,”间隔
            level:道路等级。指定道路等级，可选，默认5。下面各值代表的含义：1：高速（京藏高速）2：城市快速路、国道(西三环、103国道)3：高速辅路（G6辅路）4：主要道路（长安街、三环辅路路）5：一般道路（彩和坊路）6：无名道路
            extensions:返回结果控制，可选，默认base。可选值：base,all
            output:返回数据格式类型，可选，默认JSON。可选值：JSON,XML
        Returns:返回矩形区域交通态势的json格式数据
        """

        self.rectangle = rectangle
        self.level = level
        self.extensions = extensions
        self.output = output

        # 传入参数
        parameters = {'key': TrafficSituation.APIkey,
                      'level': level,
                      'extensions': extensions,
                      'output': output,
                      'rectangle': rectangle
                      }

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/traffic/status/rectangle?parameters",
                                               params=parameters)
            request_information.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            # only for debugging
            # print("请求状态结果：" + str(request_information))
            # 返回格式化后的JSON数据
            json_decode = json.loads(request_information.text)
            return json_decode
        except requests.RequestException:
            return dict()

    def get_traffic_situation_by_circle(self, location: str,
                                        level: int = 5,
                                        extensions: str = 'base',
                                        output: str = 'JSON',
                                        radius: int = 1000,
                                        ) -> dict:
        """
        函数：圆形区域交通态势
        Args:
            location:中心点坐标，必填。经度在前，纬度在后。经度和纬度用","分割。经纬度小数点后不得超过6位。
            level:道路等级。指定道路等级，可选，默认5。下面各值代表的含义：1：高速（京藏高速）2：城市快速路、国道(西三环、103国道)3：高速辅路（G6辅路）4：主要道路（长安街、三环辅路路）5：一般道路（彩和坊路）6：无名道路
            extensions:返回结果控制，可选，默认base。可选值：base,all
            output:返回数据格式类型，可选，默认JSON。可选值：JSON,XML
            radius:半径，可选，默认1000。单位：米，最大取值5000米。
        Returns:返回圆形区域交通态势的json格式数据
        """

        self.location = location
        self.level = level
        self.extensions = extensions
        self.output = output
        self.radius = radius

        # 传入参数
        parameters = {'key': TrafficSituation.APIkey,
                      'level': level,
                      'extensions': extensions,
                      'output': output,
                      'radius': radius
                      }

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/traffic/status/circle?parameters",
                                               params=parameters)
            request_information.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            # only for debugging
            # print("请求状态结果：" + str(request_information))
            # 返回格式化后的JSON数据
            json_decode = json.loads(request_information.text)
            return json_decode
        except requests.RequestException:
            return dict()

    def get_traffic_situation_by_road(self, name: str,
                                      level: int = 5,
                                      extensions: str = 'base',
                                      output: str = 'JSON',
                                      city: str = '',
                                      adcode: str = ''
                                      ) -> dict:
        """
        函数：指定线路交通态势
        Args:
            name:道路名，必填。
            level:道路等级。指定道路等级，可选，默认5。下面各值代表的含义：1：高速（京藏高速）2：城市快速路、国道(西三环、103国道)3：高速辅路（G6辅路）4：主要道路（长安街、三环辅路路）5：一般道路（彩和坊路）6：无名道路
            extensions:返回结果控制，可选。可选值：base,all
            output:返回数据格式类型，可选。可选值：JSON,XML
            city:城市名，非必填（city和adcode必填一个）。由于开发者可能对城市称呼和高德的称呼存在差异（例如开发者称呼为深圳，但高德仅识别深圳市）故强烈建议使用adcode，不使用city字段。另外此处的adcode仅识别市级的adcode。
            adcode:城市编码，非必填（city和adcode必填一个）。由于开发者可能对城市称呼和高德的称呼存在差异（例如开发者称呼为深圳，但高德仅识别深圳市）故强烈建议使用adcode，不使用city字段。另外此处的adcode仅识别市级的adcode。
        Returns:返回指定线路交通态势的json格式数据
        """

        self.name = name
        self.level = level
        self.extensions = extensions
        self.output = output
        self.city = city
        self.adcode = adcode

        # 传入参数
        parameters = {'key': TrafficSituation.APIkey,
                      'name': name,
                      'level': level,
                      'extensions': extensions,
                      'output': output,
                      'city': city,
                      'adcode': adcode
                      }

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/traffic/status/road?parameters",
                                               params=parameters)
            request_information.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            # only for debugging
            # print("请求状态结果：" + str(request_information))
            # 返回格式化后的JSON数据
            json_decode = json.loads(request_information.text)
            return json_decode
        except requests.RequestException:
            return dict()

    def parse_traffic_situation(self, json_decode: dict,
                                extensions: str
                                ) -> None:
        """
        函数：解析交通态势的json格式数据
        Args:
            json_decode:交通态势的json格式数据
            extensions:返回结果控制，可选。可选值：base,all
        """

        self.json_decode = json_decode
        self.extensions = extensions

        if not json_decode:
            print("返回异常")
        if json_decode['status'] == '1':
            if json_decode['infocode'] == "10000":  # 请求数据成功的状态码
                trafficinfo = json_decode['trafficinfo']
                trafficinfo_description = trafficinfo['description']
                evaluation = trafficinfo['evaluation']

                expedite = evaluation['expedite']
                congested = evaluation['congested']
                blocked = evaluation['blocked']
                unknown = evaluation['unknown']
                status = evaluation['status']
                evaluation_description = evaluation['description']

                if extensions == 'all':
                    roads = trafficinfo['roads']
                    print(roads)
                    pass



