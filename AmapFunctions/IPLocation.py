# -*- coding:utf-8 -*-
# 导入的库
import inspect
import json
import time

import requests

from SelfExpection.CustomExpection import CustomExpection
from SelfExpection.OfficialException import OfficialException
from logrecord.WriteLog import WriteLog


class IPLocation:
    """
    Class:IP定位
    IP定位是一个简单的HTTP接口，根据用户输入的IP地址，能够快速的帮用户定位IP的所在位置。
    """

    def __init__(self) -> None:
        self.input_type = None
        self.ip = None
        self.json_decode = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    # 获取高德地图数据API的钥匙
    APIkey = '<请自己输入自己申请的API Key>'

    def get_ip_location(self, ip: str,
                        input_type: int
                        ) -> dict:
        """
        函数：IP地址查询数据。\n
        Args:
            ip:需要搜索的IP地址（仅支持国内），必填。若用户不填写IP，则取客户http之中的请求来进行定位
            input_type:IP类型，可选值4：ipv4，6：ipv6，必填。
        Returns:返回获得的json格式数据或错误信息
        """

        self.ip = ip
        self.input_type = input_type

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': self.APIkey,
                      'ip': self.ip,
                      'type': self.input_type
                      }

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v5/ip?parameters",
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

    def parse_ip_location(self, json_decode: dict
                          ) -> dict:
        """
        函数：解析IP地址查询数据。
        Args:
            json_decode:get_ip_location()方法从网络中获取的数据
        Returns:
            返回获取到的IP地址信息
        """

        self.json_decode = json_decode

        # 输出结果
        resultContext = {}

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        cityList = ['北京市', '上海市', '天津市', '重庆市']

        try:
            if self.json_decode['info'] != 'OK':
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

            elif self.json_decode['status'] == '0':
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=6,
                                      context='Function name:{0} - status:{1}'.format(function_name,
                                                                                      self.json_decode['status'])
                                      )

                # 国家、省份、城市、区县
                country = self.json_decode['country']
                province = self.json_decode['province']
                city = self.json_decode['city']
                district = self.json_decode['district']

                # 运营商、IP地址
                isp = self.json_decode['isp']
                ip = self.json_decode['ip']

                # 解析IP地址信息
                if province:
                    for item in cityList:
                        # 省份为直辖市
                        if item == province:
                            # only for debugging
                            writeLog.write_to_log(file_name=log_filename,
                                                  log_level=1,
                                                  context='Function name:{0} - province:{1}'.format(
                                                      function_name,
                                                      province)
                                                  )

                            netWorkInformation = "您当前的网络所位于的地区是{0}{1}".format(city, district)
                            ispInformation = "您当前使用的网络提供的运营商是{0}{1}".format(country, isp)
                            ipInformation = "您查询的IP地址是{0}".format(ip)

                            resultContext['netWorkInformation'] = netWorkInformation
                            resultContext['ispInformation'] = ispInformation
                            resultContext['ipInformation'] = ipInformation

                            return resultContext

                        # 其他地区
                        else:
                            # only for debugging
                            writeLog.write_to_log(file_name=log_filename,
                                                  log_level=1,
                                                  context='Function name:{0} - province:{1}'.format(function_name,
                                                                                                    province)
                                                  )
                            writeLog.write_to_log(file_name=log_filename,
                                                  log_level=1,
                                                  context='Function name:{0} - city:{1}'.format(function_name,
                                                                                                city)
                                                  )

                            netWorkInformation = "您当前的网络所处于的地区是{0}{1}{2}".format(province, city, district)
                            ispInformation = "您当前使用的网络提供的运营商是{0}{1}".format(country, isp)
                            ipInformation = "您查询的IP地址是{0}".format(ip)

                            resultContext['netWorkInformation'] = netWorkInformation
                            resultContext['ispInformation'] = ispInformation
                            resultContext['ipInformation'] = ipInformation

                            return resultContext

        except OfficialException as officialException:
            # 获得的错误信息
            errcode, errorInfo, solution = officialException.get_error_info(json_decode)
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

            context = "IP地址信息查询失败，换个地址进行搜索吧"
            resultContext['error_context'] = context
            return resultContext

        except CustomExpection as customException:
            info, detail_information, error_prompt = customException.get_error_info(json_decode)
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

            context = "IP地址信息查询失败，换个地址进行搜索吧"
            resultContext['error_context'] = context
            return resultContext
