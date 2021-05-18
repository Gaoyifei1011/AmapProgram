# -*- coding:utf-8 -*-
# 导入的库
import inspect
import json
import time
from typing import Any

import requests

from SelfExpection.CustomExpection import CustomExpection
from SelfExpection.OfficialException import OfficialException
from logrecord.WriteLog import WriteLog


class LocationTransformation:
    """
    Class:坐标转换（高德地图坐标转换为百度地图）
    坐标转换是一类简单的HTTP接口，能够将用户输入的非高德坐标（GPS坐标、mapBar坐标、baidu坐标）转换成高德坐标
    """

    def __init__(self) -> None:
        self.coordsys = None
        self.json_decode = None
        self.locations = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    # 获取高德地图数据API的钥匙
    APIkey = '<请自己输入自己申请的API Key>'

    def get_location_transform(self, locations: str,
                               **kwargs: dict[str, Any]
                               ) -> dict:
        """
        函数：获取转换格式后的地理位置数据
        Args:
            locations:坐标点,经度和纬度用“,”分割，经度在前，纬度在后，经纬度小数点后不得超过6位。多个坐标对之间用“|”进行分隔最多支持40对坐标
            kwargs:
                coordsys:原坐标系，可选值：gps;mapBar;baidu;autonavi(不进行转换)。默认autonavi
        Returns:转换格式后的地理位置数据
            """

        self.locations = locations

        if 'coordsys' in kwargs:
            self.coordsys = kwargs['coordsys']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': self.APIkey,
                      'locations': self.locations,
                      }

        if self.coordsys is not None:
            parameters.update(coordsys=self.coordsys)

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/assistant/coordinate/convert?parameters",
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
                                  context='Function name:{0} - IP Location data successful get.'.format(
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
            error_information = 'Unfortunately -- An unknown Error Happened, Please wait 3 seconds'
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

    def parse_location_transform(self, json_decode: dict
                                 ) -> list:
        """
        函数：解析转换格式后的地理位置数据。
        Args:
            json_decode:get_ip_location()方法从网络中获取的数据
        Returns:
            返回获取到的IP地址信息
        """

        self.json_decode = json_decode

        # 输出结果
        resultContext = []

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
                                                                                            self.json_decode[
                                                                                                'infocode'])
                                          )
                    locations = self.json_decode['locations']
                    resultContext.append(locations)
            return resultContext

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
            context = "Error"
            resultContext.append(context)
            return resultContext

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
            context = "Error"
            resultContext.append(context)
            return resultContext
