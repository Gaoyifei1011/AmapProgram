# -*- coding:utf-8 -*-
# 导入的库
import inspect
import json
import os
import time
import urllib.request
from http.client import IncompleteRead, RemoteDisconnected
from typing import Any
from urllib.error import HTTPError, URLError

import requests
from PIL import Image

from SelfExpection import CustomExpection
from SelfExpection.OfficialException import OfficialException
from logrecord.WriteLog import WriteLog


class SearchPOI:
    """
    Class:搜索POI
    搜索服务API是一类简单的HTTP接口，提供多种查询POI信息的能力，其中包括关键字搜索、周边搜索、多边形搜索、ID查询四种筛选机制。
    """

    def __init__(self):
        self.city = None
        self.cityLimit = None
        self.children = None
        self.extensions = None
        self.filename = None
        self.json_decode = None
        self.keyword = None
        self.keywords = None
        self.location = None
        self.num_retries = None
        self.offset = None
        self.output = None
        self.page = None
        self.poi = None
        self.polygon = None
        self.poi_id = None
        self.radius = None
        self.sortRule = None
        self.suggestion = None
        self.sug_address = None
        self.types = None
        self.url = None

        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    # 获取高德地图数据API的钥匙
    APIkey = '<请自己输入自己申请的API Key>'
    open_time = 0

    def get_search_poi_by_keywords(self, keywords: str,
                                   types: str,
                                   **kwargs: dict[str, Any]
                                   ) -> dict:
        """
        函数：关键字搜索。\n
        Args:
            keywords:查询关键字，必填(keywords和types两者至少必选其一)。规则： 多个关键字用“|”分割，若不指定city，并且搜索的为泛词（例如“美食”）的情况下，返回的内容为城市列表以及此城市内有多少结
                    果符合要求。
            types:查询POI类型，必填(keywords和types两者至少必选其一)。可选值：分类代码 或 汉字（若用汉字，请严格按照附件之中的汉字填写）
                分类代码由六位数字组成，一共分为三个部分，前两个数字代表大类；中间两个数字代表中类；最后两个数字代表小类。
                    若指定了某个大类，则所属的中类、小类都会被显示。
                    例如：010000为汽车服务（大类），010100为加油站（中类），010101为中国石化（小类），010900为汽车租赁（中类），010901为汽车租赁还车（小类）
                    当指定010000，则010100等中类、010101等小类都会被包含，当指定010900，则010901等小类都会被包含。
                    若不指定city，返回的内容为城市列表以及此城市内有多少结果符合要求。
                    当您的keywords和types都是空时，默认指定types为120000（商务住宅）&150000（交通设施服务）
            kwargs:
                city:查询城市,可选。可选值：城市中文、中文全拼、citycode、adcode。如：北京/beijing/010/110000。
                        填入此参数后，会尽量优先返回此城市数据，但是不一定仅局限此城市结果，若仅需要某个城市数据请调用citylimit参数。：在深圳市搜天安门，返回北京天安门结果。
                citylimit:仅返回指定城市数据，可选，默认为False。可选值：true/false
                children:是否按照层级展示子POI数据，可选，默认0。可选值：children=1，当为0的时候，子POI都会显示。当为1的时候，子POI会归类到父POI之中。仅在extensions=all的时候生效
                offset:每页记录数据，可选，默认20。强烈建议不超过25，若超过25可能造成访问报错
                page:当前页数，可选，默认1。最大翻页数100
                extensions:返回结果控制，可选，默认base。此项默认返回基本地址信息；取值为all返回地址信息、附近POI、道路以及道路交叉口信息。
                output:返回数据格式类型，可选，默认JSON格式。可选值：JSON，XML。
        Returns:返回获得的json格式数据或错误信息
        """

        self.keywords = keywords
        self.types = types

        if 'city' in kwargs:
            self.city = kwargs['city']
        if 'cityLimit' in kwargs:
            self.cityLimit = kwargs['cityLimit']
        if 'children' in kwargs:
            self.children = kwargs['children']
        if 'extensions' in kwargs:
            self.extensions = kwargs['extensions']
        if 'offset' in kwargs:
            self.offset = kwargs['offset']
        if 'output' in kwargs:
            self.output = kwargs['output']
        if 'page' in kwargs:
            self.page = kwargs['page']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': SearchPOI.APIkey,
                      'keywords': self.keywords,
                      'types': self.types,
                      }

        if self.city is not None:
            parameters.update(city=self.city)
        if self.cityLimit is not None:
            parameters.update(citylimit=self.cityLimit)
        if self.children is not None:
            parameters.update(children=self.children)
        if self.extensions is not None:
            parameters.update(extensions=self.extensions)
        if self.offset is not None:
            parameters.update(offset=self.offset)
        if self.output is not None:
            parameters.update(output=self.output)
        if self.page is not None:
            parameters.update(page=self.page)

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/place/text?parameters",
                                               params=parameters)
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
                                  context='Function name:{0} - Keywords search POI data successful get.'.format(
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

    def get_search_poi_by_around(self, location: str,
                                 **kwargs: dict[str, Any]
                                 ) -> dict:
        """
        函数：周边搜索。\n
        Args:
            location:中心点坐标，必填。规则： 经度和纬度用","分割，经度在前，纬度在后，经纬度小数点后不得超过6位
            kwargs:
                keywords:查询关键字，可选。规则： 多个关键字用“|”分割
                types:查询POI类型，可选。多个类型用“|”分割；可选值：分类代码 或 汉字 （若用汉字，请严格按照附件之中的汉字填写）。分类代码由六位数字组成，一共分为三个部分，前两个数字代表大类；中间两个数字代表中类；最后
                        两个数字代表小类。若指定了某个大类，则所属的中类、小类都会被显示。
                        例如：010000为汽车服务（大类），010100为加油站（中类），010101为中国石化（小类），010900为汽车租赁（中类），010901为汽车租赁还车（小类）
                        当指定010000，则010100等中类、010101等小类都会被包含。当指定010900，则010901等小类都会被包含
                        当keywords和types均为空的时候，默认指定types为050000（餐饮服务）、070000（生活服务）、120000（商务住宅）
                city:查询城市，可选，默认全国范围内搜索。可选值：城市中文、中文全拼、citycode、adcode。如：北京/beijing/010/110000
                        当用户指定的经纬度和city出现冲突，若范围内有用户指定city的数据，则返回相关数据，否则返回为空。
                        如：经纬度指定石家庄，而city却指定天津，若搜索范围内有天津的数据则返回相关数据，否则返回为空。
                radius:查询半径，可选，默认3000。取值范围:0-50000。规则：大于50000按默认值，单位：米
                sortRule:排序规则，可选，默认distance。规定返回结果的排序规则。按距离排序：distance；综合排序：weight
                offset:每页记录数据，可选，默认25。强烈建议不超过25，若超过25可能造成访问报错
                page:当前页数，可选，默认1。最大翻页数100
                extensions:返回结果控制，可选，默认base。此项默认返回基本地址信息；取值为all返回地址信息、附近POI、道路以及道路交叉口信息。
                output:返回数据格式类型，可选，默认JSON格式。可选值：JSON，XML
        Returns:返回获得的json格式数据或错误信息
        """

        self.location = location

        if 'city' in kwargs:
            self.city = kwargs['city']
        if 'extensions' in kwargs:
            self.extensions = kwargs['extensions']
        if 'keywords' in kwargs:
            self.keywords = kwargs['keywords']
        if 'offset' in kwargs:
            self.offset = kwargs['offset']
        if 'output' in kwargs:
            self.output = kwargs['output']
        if 'page' in kwargs:
            self.page = kwargs['page']
        if 'radius' in kwargs:
            self.radius = kwargs['radius']
        if 'sortRule' in kwargs:
            self.sortRule = kwargs['sortRule']
        if 'types' in kwargs:
            self.types = kwargs['types']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': SearchPOI.APIkey,
                      'location': self.location
                      }

        if self.city is not None:
            parameters.update(city=self.city)
        if self.extensions is not None:
            parameters.update(extensions=self.extensions)
        if self.keywords is not None:
            parameters.update(keywords=self.keywords)
        if self.offset is not None:
            parameters.update(output=self.output)
        if self.page is not None:
            parameters.update(page=self.page)
        if self.radius is not None:
            parameters.update(radius=self.radius)
        if self.sortRule is not None:
            parameters.update(sortrule=self.sortRule)
        if self.types is not None:
            parameters.update(types=self.types)

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/place/around?parameters",
                                               params=parameters)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - request_information:{1}'.format(function_name,
                                                                                               request_information)
                                  )
            request_information.close()  # 关闭访问
            request_information.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            json_decode = json.loads(request_information.text)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - Around search POI data successful get.'.format(
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

    def get_search_poi_by_polygon(self, polygon: str,
                                  **kwargs
                                  ) -> dict:
        """
        函数：多边形搜索。\n
        Args:
            polygon:经纬度坐标对，必填。规则：经度和纬度用","分割，经度在前，纬度在后，坐标对用"|"分割。经纬度小数点后不得超过6位。多边形为矩形时，可传入左上右下两顶点坐标对；其他情况下首尾坐标对需相同。
            kwargs:
                keywords:查询关键字，可选。规则： 多个关键字用“|”分割
                types:查询POI类型，可选。多个类型用“|”分割；可选值：分类代码 或 汉字 （若用汉字，请严格按照附件之中的汉字填写）。分类代码由六位数字组成，一共分为三个部分，前两个数字代表大类；中间两个数字代表中类；最后
                        两个数字代表小类。若指定了某个大类，则所属的中类、小类都会被显示。
                        例如：010000为汽车服务（大类），010100为加油站（中类），010101为中国石化（小类），010900为汽车租赁（中类），010901为汽车租赁还车（小类）
                        当指定010000，则010100等中类、010101等小类都会被包含。当指定010900，则010901等小类都会被包含
                        当keywords和types均为空的时候，默认指定types为050000（餐饮服务）、070000（生活服务）、120000（商务住宅）
                offset:每页记录数据，可选，默认20。强烈建议不超过25，若超过25可能造成访问报错
                page:当前页数，可选，默认1。最大翻页数100
                extensions:返回结果控制，可选，默认base。此项默认返回基本地址信息；取值为all返回地址信息、附近POI、道路以及道路交叉口信息。
                output:返回数据格式类型，可选，默认JSON格式。可选值：JSON，XML
        Returns:返回获得的json格式数据或错误信息
        """

        self.polygon = polygon

        if 'extensions' in kwargs:
            self.extensions = kwargs['extensions']
        if 'keywords' in kwargs:
            self.keywords = kwargs['keywords']
        if 'offset' in kwargs:
            self.offset = kwargs['offset']
        if 'output' in kwargs:
            self.output = kwargs['output']
        if 'page' in kwargs:
            self.page = kwargs['page']
        if 'types' in kwargs:
            self.types = kwargs['types']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': self.APIkey,
                      'polygon': self.polygon
                      }

        if self.extensions is not None:
            parameters.update(extensions=self.extensions)
        if self.keywords is not None:
            parameters.update(keywords=self.keywords)
        if self.offset is not None:
            parameters.update(offset=self.offset)
        if self.output is not None:
            parameters.update(output=self.output)
        if self.page is not None:
            parameters.update(page=self.page)
        if self.types is not None:
            parameters.update(types=self.types)

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/place/polygon?parameters",
                                               params=parameters)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - request_information:{1}'.format(function_name,
                                                                                               request_information)
                                  )
            request_information.close()  # 关闭访问
            request_information.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            # 返回格式化后的JSON数据
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - Polygon search POI data successful get.'.format(
                                      function_name)
                                  )
            json_decode = json.loads(request_information.text)
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

    def get_search_poi_by_id(self, poi_id: str,
                             ) -> dict:
        """
        函数：ID查询。\n
        Args:
            poi_id: 兴趣点ID，必填。兴趣点的唯一标识ID
        Returns:返回获得的json格式数据或错误信息
        """

        self.poi_id = poi_id

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': SearchPOI.APIkey,
                      'id': self.poi_id
                      }

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/place/detail?parameters",
                                               params=parameters)
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
                                  context='Function name:{0} - ID search POI data successful get.'.format(
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

    def parse_search_poi(self, json_decode: dict,
                         extensions: str,
                         keywords: str = ''
                         ) -> None:
        """
        函数：解析IP地址查询数据。
        Args:
            json_decode:get_ip_location()方法从网络中获取的数据
            keywords:查询的关键字
            extensions:获取的数据类型
        """

        self.extensions = extensions
        self.json_decode = json_decode
        self.keywords = keywords

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        try:
            if self.json_decode['status'] == '0':
                # 官方文档异常
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - status:{1}'.format(function_name,
                                                                                      self.json_decode['status'])
                                      )
                raise OfficialException

            elif self.json_decode['status'] == '2':
                # 自定义异常
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - status:{1}'.format(function_name,
                                                                                      self.json_decode['status'])
                                      )
                raise CustomExpection

            elif self.json_decode['status'] == '1':
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=6,
                                      context='Function name:{0} - status:{1}'.format(function_name,
                                                                                      self.json_decode['status'])
                                      )

                if self.json_decode['infocode'] == "10000":  # 请求数据成功的状态码
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=6,
                                          context='Function name:{0} - infocode:{1}'.format(function_name,
                                                                                            self.json_decode['infocode'])
                                          )
                    # 搜索方案的数目
                    search_count = self.json_decode['count']
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - search count:{1}'.format(function_name,
                                                                                                search_count)
                                          )

                    # 城市建议列表
                    if 'suggestion' in self.json_decode:
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=6,
                                              context='Function name:{0} - Suggestion data get successfully.'.format(
                                                  function_name)
                                              )

                        if self.json_decode['suggestion']['cities'] or self.json_decode['suggestion']['keywords']:
                            # only for debugging
                            writeLog.write_to_log(file_name=log_filename,
                                                  log_level=6,
                                                  context='Function name:{0} - Suggestion cities or keywords data get successfully.'.format(
                                                      function_name)
                                                  )
                            suggestions = self.json_decode['suggestion']
                            for suggestion in suggestions:
                                self.print_suggestion(suggestion, self.keywords)

                    # 建议地址结果
                    if 'sug_address' in self.json_decode:
                        sug_addresses = self.json_decode['sug_address']
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=6,
                                              context='Function name:{0} - Suggestion address get successfully.'.format(
                                                  function_name)
                                              )
                        for sug_address in sug_addresses:
                            self.print_sug_address(sug_address, self.keywords)

                    # 搜索POI信息列表
                    if self.json_decode['pois']:
                        pois = self.json_decode['pois']
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=6,
                                              context='Function name:{0} - POI data get successfully'.format(
                                                  function_name,
                                                  pois)
                                              )
                        for poi in pois:
                            self.print_poi(poi, extensions=self.extensions)

        except OfficialException as officialException:
            # 获得的错误信息
            errcode, errorInfo, solution = officialException.get_error_info(self.json_decode)
            # 打印到日志文件中
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - errcode:{1}'.format(function_name,
                                                                                   errcode)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - errorInfo:{1}'.format(function_name,
                                                                                     errorInfo)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - solution:{1}'.format(function_name,
                                                                                    solution)
                                  )

        except CustomExpection as customException:
            info, detail_information, error_prompt = customException.get_error_info(self.json_decode)
            # 打印到日志文件中
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - info:{1}'.format(function_name,
                                                                                info)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - detail_information:{1}'.format(function_name,
                                                                                              detail_information)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='error_prompt:{0}'.format(error_prompt)
                                  )

    def print_suggestion(self, suggestion: dict,
                         keyword: str
                         ) -> None:
        """
        函数：输出城市建议列表中的信息
        Args:
            suggestion: 城市建议列表，当搜索的文本关键字在限定城市中没有返回时会返回建议城市列表
            keyword:查询的关键字
        """

        self.keyword = keyword
        self.suggestion = suggestion

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        keywords = self.suggestion['keywords']
        cities = self.suggestion['cities']
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - keywords:{1}'.format(function_name,
                                                                                keywords)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - cities data get successfully'.format(function_name)
                              )
        print("您输入的关键字暂未查到具体信息，根据您提供的关键字已搜索到关键字对应的城市列表")
        for city in cities:
            # 城市名称，该城市包含此关键字的个数，该城市的citycode，该城市的adcode
            name = city['name']
            num = city['num']
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - city name:{1}'.format(function_name,
                                                                                     name)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - num:{1}'.format(function_name,
                                                                               num)
                                  )
            print("包含该关键字“{0}”城市有“{1}”，其中包含{2}条结果".format(self.keyword, name, num))

    def print_sug_address(self, sug_address: dict,
                          keyword: str = ''
                          ) -> None:
        """
        函数：建议地址结果，当搜索结果并非是POI（是地址时），且没有搜索到POI时返回
        Args:
            sug_address:建议地址结果，当搜索结果并非是POI（是地址时），且没有搜索到POI时返回
            keyword:查询的关键字
        """
        self.keyword = keyword
        self.sug_address = sug_address

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        name = sug_address['name']
        address = sug_address['address']
        country = sug_address['country']
        pname = sug_address['pname']
        cityname = sug_address['cityname']
        adname = sug_address['adname']
        # 暂未查询到相关信息，故目前不使用
        district = sug_address['district']
        street = sug_address['street']

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - address name:{1}'.format(function_name,
                                                                                    name)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - address:{1}'.format(function_name,
                                                                               address)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - country:{1}'.format(function_name,
                                                                               country)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - pname:{1}'.format(function_name,
                                                                             pname)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - city name:{1}'.format(function_name,
                                                                                 cityname)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - adname:{1}'.format(function_name,
                                                                              adname)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - street:{1}'.format(function_name,
                                                                              street)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - district:{1}'.format(function_name,
                                                                                district)
                              )
        print("您输入的关键字暂未查到具体信息，根据您提供的关键字已搜索到关键字对应的建议地址结果")
        print("查询的该关键字“{0}”的建议地址结果的名称为{1}，在{2}{3}省{4}市".format(self.keyword, name, country, pname, cityname))
        print("详细的地址描述是{0}，所属区域为{1}{2}".format(address, adname, street))

    def print_poi(self, poi: dict,
                  extensions: str
                  ) -> None:
        """
        函数：搜索POI信息列表
        Args:
            poi:POI信息
            extensions:查询的poi类型
        """

        self.extensions = extensions
        self.poi = poi

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        name = self.poi['name']
        poi_type = self.poi['type']
        typecode = self.poi['typecode']
        biz_type = self.poi['biz_type']
        address = self.poi['address']
        distance = self.poi['distance']
        tel = self.poi['tel']
        pname = self.poi['pname']
        cityname = self.poi['cityname']
        adname = self.poi['adname']
        alias = self.poi['alias']
        business_area = self.poi['business_area']

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - name:{1}'.format(function_name,
                                                                            name)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - poi type:{1}'.format(function_name,
                                                                                poi_type)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - type code:{1}'.format(function_name,
                                                                                 typecode)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - biztype:{1}'.format(function_name,
                                                                               biz_type)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - address:{1}'.format(function_name,
                                                                               address)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - distance:{1}'.format(function_name,
                                                                                distance)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - tel:{1}'.format(function_name,
                                                                           tel)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - province name:{1}'.format(function_name,
                                                                                     pname)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - city name:{1}'.format(function_name,
                                                                                 cityname)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - adname:{1}'.format(function_name,
                                                                              adname)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - alias:{1}'.format(function_name,
                                                                             alias)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - business area:{1}'.format(function_name,
                                                                                     business_area)
                              )

        print("=========================================================")
        print("您要查询的关键字名称为{0}，对应的地址是{1}{2}{3}{4}\n".format(name, pname, cityname, adname, address), end='')
        if tel:
            print("，电话号码：{0}".format(tel))
        print("所查询关键字的类型是{0}".format(poi_type), end='')
        if distance:
            print("离中心点距离大约{0}米".format(distance))
        if alias:
            print("它的另外的名称包括{0}".format(alias), end='')
        if business_area:
            print("所属商圈是{0}".format(business_area))
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=6,
                              context='Function name:{0} - POI data successfully print.'.format(function_name)
                              )

        # extensions为all返回
        if self.extensions == "all":
            postcode = self.poi['postcode']
            website = self.poi['website']
            email = self.poi['email']
            pcode = self.poi['pcode']
            adcode = self.poi['adcode']
            tag = self.poi['tag']
            indoor_map = self.poi['indoor_map']
            indoor_data = self.poi['indoor_data']
            biz_ext = self.poi['biz_ext']
            photos = self.poi['photos']

            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - post code:{1}'.format(function_name,
                                                                                     postcode)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - website:{1}'.format(function_name,
                                                                                   website)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - email:{1}'.format(function_name,
                                                                                 email)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - pcode:{1}'.format(function_name,
                                                                                 pcode)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - adcode:{1}'.format(function_name,
                                                                                  adcode)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - tag:{1}'.format(function_name,
                                                                               tag)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - indoor map:{1}'.format(function_name,
                                                                                      indoor_map)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - indoor data:{1}'.format(function_name,
                                                                                       indoor_data)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - biz ext:{1}'.format(function_name,
                                                                                   biz_ext)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - photos data successfully get.'.format(function_name)
                                  )

            if website:
                print("，对应的网页地址是{0}\n".format(website), end='')
            if email:
                print("，邮箱地址是{0}".format(email))
            if photos:
                for item, photo in enumerate(photos):
                    if photo['title']:
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - photo title:{1}'.format(function_name,
                                                                                                   photo['title'])
                                              )
                        print("{0}".format(photo['title']))
                    # 图片保存的位置
                    temp_directory = os.getenv('TEMP')
                    # Photo目录文件夹
                    list_photo = [temp_directory, 'Photo']
                    photo_directory = '\\'.join(list_photo)
                    if not os.path.exists(photo_directory):
                        os.mkdir(photo_directory)
                    # 子目录（各个名称对应的图片）
                    list_directory = [temp_directory, 'Photo\\{0}'.format(name)]
                    directory = '\\'.join(list_directory)
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - directory:{1}'.format(function_name,
                                                                                             directory)
                                          )
                    if not os.path.exists(directory):
                        os.mkdir(directory)
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - directory created.'.format(function_name)
                                              )
                    list_filename = [temp_directory, 'Photo\\{0}\\{0}{1}.jpg'.format(name, item)]
                    filename = '\\'.join(list_filename)
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - filename:{1}'.format(function_name,
                                                                                            filename)
                                          )
                    # 保存图片
                    self.save_photo(photo['url'], filename=filename)
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - photo saved.'.format(function_name)
                                          )
                    # 显示图片,只显示前8张照片
                    if SearchPOI.open_time < 8:
                        image = Image.open(filename)
                        image.show()
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - open time:{1}'.format(function_name,
                                                                                                 SearchPOI.open_time)
                                              )
                        print("已打开图片" + str(filename))  # TODO:保存到日志文件中
                        SearchPOI.open_time = SearchPOI.open_time + 1
        if SearchPOI.open_time >= 8:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - 由于用户指定和本地计算机网络资源的限制，不打开之后从网络下载的图片，请手动打开Windows资源管理器对应的目录查看'.format(
                                      function_name)
                                  )

    def save_photo(self, url: str,
                   filename: str,
                   num_retries: int = 3
                   ) -> None:
        """
        函数：将网页url对应的图片保存到本地目录下
        Args:
            url:网页图片连接
            filename:保存到本地图片的位置
            num_retries:重连次数
        """

        self.filename = filename
        self.num_retries = num_retries
        self.url = url

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        img_src = url
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - img_src:{1}'.format(function_name,
                                                                               img_src)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - filename:{1}'.format(function_name,
                                                                                self.filename)
                              )

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/35.0.1916.114 Safari/537.36',
            'Cookie': 'AspxAutoDetectCookieSupport=1'
        }
        # Request类可以使用给定的header访问URL
        result = urllib.request.Request(url=img_src, headers=header)

        try:
            response = urllib.request.urlopen(result)  # 得到访问的网址
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - response successfully'.format(function_name)
                                  )
            with open(self.filename, 'wb') as file:
                content = response.read()  # 获得图片
                file.write(content)  # 保存图片
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - picture saved successfully'.format(function_name)
                                  )
        except HTTPError as e:  # HTTP响应异常处理
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - error reason:{1}'.format(function_name,
                                                                                        e.reason)
                                  )
        except URLError as e:  # 一定要放到HTTPError之后，因为它包含了前者
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - error reason:{1}'.format(function_name,
                                                                                        e.reason)
                                  )
        except IncompleteRead or RemoteDisconnected:
            if self.num_retries == 0:  # 重连机制
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=1,
                                      context='Function name:{0} - retries time:{1}'.format(function_name,
                                                                                            self.num_retries)
                                      )
                return
            else:
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=1,
                                      context='Function name:{0} - retries time:{1}'.format(function_name,
                                                                                            self.num_retries)
                                      )
                self.save_photo(url, self.filename, self.num_retries - 1)
