# -*- coding:utf-8 -*-
# 导入的库
import hashlib
import inspect
import json
import time
import urllib.parse as parse

import requests

from logrecord.WriteLog import WriteLog


class TrafficSituationByBaiduMap:
    def __init__(self):
        self.bounds = None
        self.center = None
        self.city = None
        self.congestion_section = None
        self.coord_type_input = None
        self.coord_type_output = None
        self.json_decode = None
        self.radius = None
        self.road_name = None
        self.road_grade = None
        self.vertexes = None

        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    # 获取百度地图数据API的钥匙
    APIkey = '<请自己输入自己申请的API Key>'
    sk = '<请自己输入自己申请的sk 校验码>'

    def get_traffic_situation_by_road(self, road_name: str,
                                      city: str,
                                      ) -> dict:
        """
        函数：道路路况查询
        Args:
            road_name:道路名称，必填。	如："北五环"、"信息路"。目前支持除多方向立交桥和多方向道路以外的各类道路名称（注：多方向是指道路方向多于2个方向，如：南向北、北向南、西向东、东向西，称为4方向）。
            city:城市名，必填。1. 全国城市名称，如："北京市"、"上海市"等。2. 百度地图行政区划adcode，仅支持城市级别（adcode映射表），如"110000"
        Returns:返回道路路况查询的json格式数据
        """

        self.road_name = road_name
        self.city = city

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        queryStr = '/traffic/v1/road?road_name={0}&city={1}&ak={2}'.format(self.road_name, self.city, self.APIkey)
        # 对queryStr进行转码，safe内的保留字符不转换
        encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
        # 在最后直接追加上yoursk
        rawStr = encodedStr + self.sk
        # 计算sn
        sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
        # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
        url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")

        # 获取数据
        try:
            request_information = requests.get(url, headers={"content-type": "application/json"})
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - request_information:{1}'.format(function_name,
                                                                                               request_information)
                                  )
            request_information.close()  # 关闭访问
            request_information.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            # 返回格式化后的JSON数据
            json_decode = json.loads(request_information.text)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - Traffic road situation data successful get.'.format(
                                      function_name)
                                  )
            return json_decode

        except requests.exceptions.ConnectionError as e:
            time.sleep(1)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,
                                                                                        e.__class__.__name__)
                                  )
            # 异常信息
            error_connection = 'ConnectionError -- please wait 3 seconds'
            error_connection_dict = {'status': '2',
                                     'info': 'requests.exceptions.ConnectionError',
                                     'detail_information': requests.exceptions.ConnectionError,
                                     'error_prompt': error_connection
                                     }
            return error_connection_dict

        except requests.exceptions.ChunkedEncodingError as e:
            time.sleep(1)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,
                                                                                        e.__class__.__name__
                                                                                        )
                                  )
            # 异常信息
            error_chuck_encoding = 'ChunkedEncodingError -- please wait 3 seconds'
            error_chuck_encoding_dict = {'status': '2',
                                         'info': 'HTTPError',
                                         'detail_information': requests.exceptions.ChunkedEncodingError,
                                         'error_prompt': error_chuck_encoding
                                         }
            return error_chuck_encoding_dict

        except Exception as e:
            time.sleep(1)
            error_information = 'Unfortunately -- An Unknown Error Happened, Please wait 3 seconds'
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,
                                                                                        e.__class__.__name__)
                                  )
            # 异常信息
            error_information_dict = {'status': '2',
                                      'info': 'HTTPError',
                                      'detail_information': requests.exceptions.ChunkedEncodingError,
                                      'error_prompt': error_information
                                      }
            return error_information_dict

    # 这里有一些异常发生，将在未来的某一个版本进行修复
    # There are some exceptions occurring here that will be fixed in a future release
    # def get_traffic_situation_by_rectangle(self, bounds: str,
    #                                        road_grade: int = 0,
    #                                        coord_type_input: str = 'bd09ll',
    #                                        coord_type_output: str = 'bd09ll',
    #                                        ) -> dict:
    #     """
    #     函数：矩形区域交通态势
    #     Args:
    #         bounds:矩形区域, 左下角和右上角的经纬度坐标点，必填。坐标点顺序为"左下;右上"，坐标对间使用;号分隔，格式为：纬度,经度;纬度,经度。对角线距离不超过2公里。示例： 39.912078,116.464303
    #                 ;39.918276,116.475442。
    #         road_grade:道路等级，可选。用户可进行道路等级筛选，支持选择多个道路等级。道路等级之间使用英文“,”分隔。默认值：road_grade=0 道路等级对应表如下： 0：全部驾车道路 1：高速路 2：环路及快速
    #                 路 3：主干路 4：次干路 5：支干路。示例： 查询全部驾车道路路况：road_grade:0 查询高速道路路况：road_grade:1 查询高速路、环路及快速路、主干路的路况：road_grade
    #                 =1,2,3。
    #         coord_type_input:请求参数 bounds的坐标类型，可选。默认值：bd09ll。bd09ll：百度经纬度坐标 gcj02：国测局加密坐标 wgs84：gps 坐标
    #         coord_type_output:返回结果的坐标类型，可选。默认值：bd09ll。该字段用于控制返回结果中坐标的类型。可选值为： bd09ll：百度经纬度坐标 gcj02：国测局加密坐标
    #     Returns:返回矩形区域交通态势的json格式数据
    #     """
    #
    #     self.bounds = bounds
    #     self.coord_type_input = coord_type_input
    #     self.coord_type_output = coord_type_output
    #     self.road_grade = road_grade
    #
    #     # 写入日志
    #     writeLog = WriteLog()
    #     class_name = self.__class__.__name__
    #     function_name = inspect.stack()[0][3]
    #     log_filename = writeLog.create_filename(class_name=class_name)
    #
    #     queryStr = '/traffic/v1/bound?bounds={0}&road_grade={1}&coord_type_input={2}&coord_type_output={3}&ak={4}'.format(
    #         bounds, road_grade, coord_type_input, coord_type_output, self.APIkey)
    #     # 对queryStr进行转码，safe内的保留字符不转换
    #     encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    #     # 在最后直接追加上yoursk
    #     rawStr = encodedStr + self.sk
    #     # 计算sn
    #     sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
    #     # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    #     url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")
    #     print(url)
    #
    #     # 获取数据
    #     try:
    #         request_information = requests.get(url, headers={"content-type": "application/json"})
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=1,
    #                               context='Function name:{0} - request_information:{1}'.format(function_name,
    #                                                                                            request_information)
    #                               )
    #         request_information.close()  # 关闭访问
    #         request_information.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
    #         json_decode = json.loads(request_information.text)
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=6,
    #                               context='Function name:{0} - Traffic rectangle situation data successful get.'.format(
    #                                   function_name)
    #                               )
    #         return json_decode
    #
    #     except requests.exceptions.ConnectionError as e:
    #         time.sleep(1)
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=5,
    #                               context='Function name:{0} - {1} has occured.'.format(function_name,
    #                                                                                     e.__class__.__name__)
    #                               )
    #         error_connection = 'ConnectionError -- please wait 3 seconds'
    #         error_connection_dict = {'status': '2',
    #                                  'info': 'requests.exceptions.ConnectionError',
    #                                  'detail_information': requests.exceptions.ConnectionError,
    #                                  'error_prompt': error_connection
    #                                  }
    #         return error_connection_dict
    #
    #     except requests.exceptions.ChunkedEncodingError as e:
    #         time.sleep(1)
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=5,
    #                               context='Function name:{0} - {1} has occured.'.format(function_name,
    #                                                                                     e.__class__.__name__
    #                                                                                     )
    #                               )
    #         error_chuck_encoding = 'ChunkedEncodingError -- please wait 3 seconds'
    #         error_chuck_encoding_dict = {'status': '2',
    #                                      'info': 'HTTPError',
    #                                      'detail_information': requests.exceptions.ChunkedEncodingError,
    #                                      'error_prompt': error_chuck_encoding
    #                                      }
    #         return error_chuck_encoding_dict
    #
    #     except Exception as e:
    #         time.sleep(1)
    #         error_information = 'Unfortunately -- An Unknown Error Happened, Please wait 3 seconds'
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=5,
    #                               context='Function name:{0} - {1} has occured.'.format(function_name,
    #                                                                                     e.__class__.__name__)
    #                               )
    #         error_information_dict = {'status': '2',
    #                                   'info': 'HTTPError',
    #                                   'detail_information': requests.exceptions.ChunkedEncodingError,
    #                                   'error_prompt': error_information
    #                                   }
    #         return error_information_dict
    #
    # def get_traffic_situation_by_polygon(self, vertexes: str,
    #                                      road_grade: int = 0,
    #                                      coord_type_input: str = 'bd09ll',
    #                                      coord_type_output: str = 'bd09ll',
    #                                      ) -> dict:
    #     """
    #     函数：矩形区域交通态势
    #     Args:
    #         vertexes:多边形边界点, 必填。多边形顶点，规则： 经纬度顺序为：纬度,经度； 顶点顺序需按逆时针排列。多边形外接矩形对角线距离不超过2公里。 示例： vertexes=39.910528,116.47292
    #                 6;39.918276,116.475442;39.916671,116.459056;39.912078,116.464303
    #         road_grade:道路等级，可选。用户可进行道路等级筛选，支持选择多个道路等级。道路等级之间使用英文“,”分隔。默认值：road_grade=0 道路等级对应表如下： 0：全部驾车道路 1：高速路 2：环路及快速
    #                 路 3：主干路 4：次干路 5：支干路。示例： 查询全部驾车道路路况：road_grade:0 查询高速道路路况：road_grade:1 查询高速路、环路及快速路、主干路的路况：road_grade
    #                 =1,2,3。
    #         coord_type_input:请求参数 bounds的坐标类型，可选。默认值：bd09ll。bd09ll：百度经纬度坐标 gcj02：国测局加密坐标 wgs84：gps 坐标
    #         coord_type_output:返回结果的坐标类型，可选。默认值：bd09ll。该字段用于控制返回结果中坐标的类型。可选值为： bd09ll：百度经纬度坐标 gcj02：国测局加密坐标
    #     Returns:返回矩形区域交通态势的json格式数据
    #     """
    #
    #     self.coord_type_input = coord_type_input
    #     self.coord_type_output = coord_type_output
    #     self.road_grade = road_grade
    #     self.vertexes = vertexes
    #
    #     # 写入日志
    #     writeLog = WriteLog()
    #     class_name = self.__class__.__name__
    #     function_name = inspect.stack()[0][3]
    #     log_filename = writeLog.create_filename(class_name=class_name)
    #
    #     queryStr = '/traffic/v1/polygon?vertexes={0}&road_grade={1}&coord_type_input={2}&coord_type_output={3}&ak={4}'.format(
    #         vertexes, road_grade, coord_type_input, coord_type_output, self.APIkey)
    #     # 对queryStr进行转码，safe内的保留字符不转换
    #     encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    #     # 在最后直接追加上yoursk
    #     rawStr = encodedStr + self.sk
    #     # 计算sn
    #     sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
    #     # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    #     url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")
    #
    #     # 获取数据
    #     try:
    #         request_information = requests.get(url, headers={"content-type": "application/json"})
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=1,
    #                               context='Function name:{0} - request_information:{1}'.format(function_name,
    #                                                                                            request_information)
    #                               )
    #         request_information.close()  # 关闭访问
    #         request_information.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
    #         # 返回格式化后的JSON数据
    #         json_decode = json.loads(request_information.text)
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=6,
    #                               context='Function name:{0} - Traffic polygon situation data successful get.'.format(
    #                                   function_name)
    #                               )
    #         return json_decode
    #
    #     except requests.exceptions.ConnectionError as e:
    #         time.sleep(1)
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=5,
    #                               context='Function name:{0} - {1} has occured.'.format(function_name,
    #                                                                                     e.__class__.__name__)
    #                               )
    #         error_connection = 'ConnectionError -- please wait 3 seconds'
    #         error_connection_dict = {'status': '2',
    #                                  'info': 'requests.exceptions.ConnectionError',
    #                                  'detail_information': requests.exceptions.ConnectionError,
    #                                  'error_prompt': error_connection
    #                                  }
    #         return error_connection_dict
    #
    #     except requests.exceptions.ChunkedEncodingError as e:
    #         time.sleep(1)
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=5,
    #                               context='Function name:{0} - {1} has occured.'.format(function_name,
    #                                                                                     e.__class__.__name__
    #                                                                                     )
    #                               )
    #         error_chuck_encoding = 'ChunkedEncodingError -- please wait 3 seconds'
    #         error_chuck_encoding_dict = {'status': '2',
    #                                      'info': 'HTTPError',
    #                                      'detail_information': requests.exceptions.ChunkedEncodingError,
    #                                      'error_prompt': error_chuck_encoding
    #                                      }
    #         return error_chuck_encoding_dict
    #
    #     except Exception as e:
    #         time.sleep(1)
    #         error_information = 'Unfortunately -- An Unknown Error Happened, Please wait 3 seconds'
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=5,
    #                               context='Function name:{0} - {1} has occured.'.format(function_name,
    #                                                                                     e.__class__.__name__)
    #                               )
    #         error_information_dict = {'status': '2',
    #                                   'info': 'HTTPError',
    #                                   'detail_information': requests.exceptions.ChunkedEncodingError,
    #                                   'error_prompt': error_information
    #                                   }
    #         return error_information_dict
    #
    # def get_traffic_situation_by_circle(self, center: str,
    #                                     radius: int,
    #                                     road_grade: int = 0,
    #                                     coord_type_input: str = 'bd09ll',
    #                                     coord_type_output: str = 'bd09ll',
    #                                     ) -> dict:
    #     """
    #     函数：矩形区域交通态势
    #     Args:
    #         center:中心点坐标，必填。示例：center=39.912078,116.464303
    #         radius:查询半径，必填。单位：米，取值范围[1,1000]，示例： radius=200。
    #         road_grade:道路等级，可选。用户可进行道路等级筛选，支持选择多个道路等级。道路等级之间使用英文“,”分隔。默认值：road_grade=0 道路等级对应表如下： 0：全部驾车道路 1：高速路 2：环路及快速路 3：主干路 4：次干路 5：支干路。示例： 查询全部驾车道路路况：road_grade:0 查询高速道路路况：road_grade:1 查询高速路、环路及快速路、主干路的路况：road_grade=1,2,3。
    #         coord_type_input:请求参数 bounds的坐标类型，可选。默认值：bd09ll。bd09ll：百度经纬度坐标 gcj02：国测局加密坐标 wgs84：gps 坐标
    #         coord_type_output:返回结果的坐标类型，可选。默认值：bd09ll。该字段用于控制返回结果中坐标的类型。可选值为： bd09ll：百度经纬度坐标 gcj02：国测局加密坐标
    #     Returns:返回矩形区域交通态势的json格式数据
    #     """
    #
    #     self.center = center
    #     self.coord_type_input = coord_type_input
    #     self.coord_type_output = coord_type_output
    #     self.radius = radius
    #     self.road_grade = road_grade
    #
    #     # 写入日志
    #     writeLog = WriteLog()
    #     class_name = self.__class__.__name__
    #     function_name = inspect.stack()[0][3]
    #     log_filename = writeLog.create_filename(class_name=class_name)
    #
    #     queryStr = '/traffic/v1/around?center={0}&radius={1}&road_grade={2}&coord_type_input={3}&coord_type_output={4}&ak={5}' \
    #         .format(center, radius, road_grade, coord_type_input, coord_type_output, self.APIkey)
    #     # 对queryStr进行转码，safe内的保留字符不转换
    #     encodedStr = parse.quote(queryStr, safe="/:=&?#+!$,;'@()*[]")
    #     # 在最后直接追加上yoursk
    #     rawStr = encodedStr + self.sk
    #     # 计算sn
    #     sn = (hashlib.md5(parse.quote_plus(rawStr).encode("utf8")).hexdigest())
    #     # 由于URL里面含有中文，所以需要用parse.quote进行处理，然后返回最终可调用的url
    #     url = parse.quote("http://api.map.baidu.com" + queryStr + "&sn=" + sn, safe="/:=&?#+!$,;'@()*[]")
    #
    #     # 获取数据
    #     try:
    #         request_information = requests.get(url, headers={"content-type": "application/json"})  # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=1,
    #                               context='Function name:{0} - request_information:{1}'.format(function_name,
    #                                                                                            request_information)
    #                               )
    #         request_information.close()  # 关闭访问
    #         request_information.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
    #         # 返回格式化后的JSON数据
    #         json_decode = json.loads(request_information.text)
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=6,
    #                               context='Function name:{0} - Traffic circle situation data successful get.'.format(
    #                                   function_name)
    #                               )
    #         return json_decode
    #
    #     except requests.exceptions.ConnectionError as e:
    #         time.sleep(1)
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=5,
    #                               context='Function name:{0} - {1} has occured.'.format(function_name,
    #                                                                                     e.__class__.__name__)
    #                               )
    #         error_connection = 'ConnectionError -- please wait 3 seconds'
    #         error_connection_dict = {'status': '2',
    #                                  'info': 'requests.exceptions.ConnectionError',
    #                                  'detail_information': requests.exceptions.ConnectionError,
    #                                  'error_prompt': error_connection
    #                                  }
    #         return error_connection_dict
    #
    #     except requests.exceptions.ChunkedEncodingError as e:
    #         time.sleep(1)
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=5,
    #                               context='Function name:{0} - {1} has occured.'.format(function_name,
    #                                                                                     e.__class__.__name__
    #                                                                                     )
    #                               )
    #         error_chuck_encoding = 'ChunkedEncodingError -- please wait 3 seconds'
    #         error_chuck_encoding_dict = {'status': '2',
    #                                      'info': 'HTTPError',
    #                                      'detail_information': requests.exceptions.ChunkedEncodingError,
    #                                      'error_prompt': error_chuck_encoding
    #                                      }
    #         return error_chuck_encoding_dict
    #
    #     except Exception as e:
    #         time.sleep(1)
    #         error_information = 'Unfortunately -- An Unknown Error Happened, Please wait 3 seconds'
    #         # only for debugging
    #         writeLog.write_to_log(file_name=log_filename,
    #                               log_level=5,
    #                               context='Function name:{0} - {1} has occured.'.format(function_name,
    #                                                                                     e.__class__.__name__)
    #                               )
    #         error_information_dict = {'status': '2',
    #                                   'info': 'HTTPError',
    #                                   'detail_information': requests.exceptions.ChunkedEncodingError,
    #                                   'error_prompt': error_information
    #                                   }
    #         return error_information_dict

    def parse_traffic_situation(self, json_decode: dict,
                                ) -> list:
        """
        函数：解析交通态势的json格式数据
        Args:
            json_decode:交通态势的json格式数据
        """

        # TODO:未来版本将返回数据从list升级为dict
        self.json_decode = json_decode

        resultContext = []

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        if not self.json_decode:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - data error'.format(function_name)
                                  )
        if self.json_decode['status'] == 0:
            description = self.json_decode['description']
            evaluation = self.json_decode['evaluation']
            road_traffic = self.json_decode['road_traffic']
            status = evaluation['status']
            status_desc = evaluation['status_desc']

            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - description:{1}'.format(function_name,
                                                                                       description)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - evaluation:{1}'.format(function_name,
                                                                                      evaluation)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - road traffic:{1}'.format(function_name,
                                                                                        road_traffic)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - status:{1}'.format(function_name,
                                                                                  status)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - status desc:{1}'.format(function_name,
                                                                                       status_desc)
                                  )

            resultContext.append("当前区域路况信息整体如下：")
            resultContext.append(description)
            resultContext.append("该区域的所有道路整体通行情况是{0}".format(status_desc))

            resultContext.append("您查询的信息包含以下道路")
            for item in road_traffic:
                road_name = item['road_name']
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=1,
                                      context='Function name:{0} - road name:{1}'.format(function_name,
                                                                                         road_name)
                                      )
                # 显示道路名称
                if road_name != 'UNKNOWN' or '':
                    resultContext.append(road_name)

                if 'congestion_sections' in item:
                    # 若有congestion_sections该字段
                    congestion_sections = item['congestion_sections']
                    for congestion_section in congestion_sections:
                        context = self.condition_analysis(congestion_section, road_name)
                        resultContext.extend(context)
                # else:
                #     print("该区域道路名为{0}的道路暂无路况数据。".format(road_name))
        return resultContext

    def condition_analysis(self, congestion_section: dict,
                           road_name: str
                           ) -> list:
        """
        函数：路况分析
        Args:
            congestion_section:拥堵路段详情
            road_name:道路名称
        """
        self.congestion_section = congestion_section
        self.road_name = road_name

        resultContext = []

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        status_dict = {0: '未知路况', 1: '畅通', 2: '缓行', 3: '拥堵', 4: '严重拥堵'}

        section_desc = self.congestion_section['section_desc']
        congestion_status = self.congestion_section['status']
        speed = self.congestion_section['speed']
        congestion_distance = self.congestion_section['congestion_distance']
        congestion_trend = self.congestion_section['congestion_trend']

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - section desc:{1}'.format(function_name,
                                                                                    section_desc)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - congestion status:{1}'.format(function_name,
                                                                                         congestion_status)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - speed:{1}'.format(function_name,
                                                                             speed)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - congestion distance:{1}'.format(function_name,
                                                                                           congestion_distance)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - congestion trend:{1}'.format(function_name,
                                                                                        congestion_trend)
                              )

        resultContext.append("==================")
        resultContext.append(
            "当前区域拥堵路段位于{0}，大体方向是{1}，相比于10分钟前拥堵趋势{2}".format(self.road_name, section_desc, congestion_trend))
        resultContext.append("{0}拥堵距离大约是{1}米，平均车速是{2}km/h".format(self.road_name, congestion_distance, speed))
        resultContext.append("当前道路整体通行状况是{0}".format(status_dict[congestion_status]))
        return resultContext
