# -*- coding:utf-8 -*-
# 导入的库
import inspect
import json
import time
from typing import Any

import requests

from SelfExpection import CustomExpection
from SelfExpection.OfficialException import OfficialException
from logrecord.WriteLog import WriteLog


class GeographicCoding:
    """
    Class:地理/逆地理编码
    地理编码:将详细的结构化地址转换为高德经纬度坐标。且支持对地标性名胜景区、建筑物名称解析为高德经纬度坐标。
    逆地理编码：将经纬度转换为详细结构化的地址，且返回附近周边的POI、AOI信息。
    """

    def __init__(self) -> None:
        self.address = None
        self.batch = None
        self.city = None
        self.extensions = None
        self.flag_batch = None
        self.homeorcrop = None
        self.inverse_json_decode = None
        self.json_decode = None
        self.location = None
        self.output = None
        self.poitype = None
        self.radius = None
        self.roadLevel = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    # 获取高德地图数据API的钥匙
    APIkey = '<请自己输入自己申请的API Key>'

    def get_geographic_coding(self, address: str,
                              city: str,
                              **kwargs: dict[str, Any]
                              ) -> dict:
        """
        函数：获取地理编码数据。\n
        Args:
            address:结构化地址信息，必填。规则遵循：国家、省份、城市、区县、城镇、乡村、街道、门牌号码、屋邨、大厦，如：北京市朝阳区阜通东大街6号。如果需要解析多个地址的话，请用"|"进行间隔，并且将 batch参数设置
                    为 true，最多支持 10 个地址进进行"|"分割形式的请求。
            city:指定查询的城市，可选。可选输入内容包括：指定城市的中文（如北京）、指定城市的中文全拼（beijing）、citycode（010）、adcode（110000），不支持县级市。当指定城市查询内容为空时，会进行全国范围内的地址转换检索。
            kwargs:
                output:返回数据格式类型，可选，默认JSON格式。可选输入内容包括：JSON，XML。设置 JSON 返回结果数据将会以JSON结构构成；如果设置 XML 返回结果数据将以 XML 结构构成。
                batch:批量查询控制，可选，默认False。batch 参数设置为 true 时进行批量查询操作，最多支持 10 个地址进行批量查询。batch 参数设置为 false 时进行单点查询，此时即使传入多个地址也只返
                    回第一个地址的解析查询结果。
        Returns:返回获得的json格式数据或错误信息
        """

        self.address = address
        self.city = city

        if 'batch' in kwargs:
            self.batch = kwargs['batch']
        if 'output' in kwargs:
            self.output = kwargs['output']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': self.APIkey,
                      'address': self.address,
                      'city': self.city
                      }

        if self.batch is not None:
            parameters.update(batch=self.batch)
        if self.output is not None:
            parameters.update(output=self.output)

        # 获取数据
        try:
            # 以下except都是用来捕获当requests请求出现异常时，
            # 通过捕获然后等待网络情况的变化，以此来保护程序的不间断运行
            request_information = requests.get("https://restapi.amap.com/v3/geocode/geo?parameters",
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
                                  context='Function name:{0} - Geographic coding data successful get.'.format(
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
                                                                                        e.__class__.__name__)
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

    def get_inverse_geographic_coding(self, location: str,
                                      **kwargs
                                      ) -> dict:

        """
        函数：获取逆地理编码数据。\n
        Args:
            location:经纬度坐标，必填。传入内容规则：经度在前，纬度在后，经纬度间以“,”分割，经纬度小数点后不要超过 6 位。如果需要解析多个经纬度的话，请用"|"进行间隔，并且将 batch 参数设置为 true，最
                    多支持传入 20 对坐标点。每对点坐标之间用"|"分割。
            kwargs:
                radius:搜索半径，可选，默认1000。radius取值范围在0~3000。单位：米。
                roadLevel:道路等级，可选。以下内容需要 extensions 参数为 all时才生效。可选值：0，1当roadlevel=0时，显示所有道路。当roadlevel=1时，过滤非主干道路，仅输出主干道路数据。
                extensions:返回结果控制，可选，默认base。extensions 参数默认取值是 base，也就是返回基本地址信息；extensions 参数取值为 all 时会返回基本地址信息、附近 POI内容、道路信息以及道路交叉
                        口信息。
                poitype:返回附近POI类型，可选。以下内容需要 extensions 参数为 all 时才生效。逆地理编码在进行坐标解析之后不仅可以返回地址描述，也可以返回经纬度附近符合限定要求的POI内容（在
                        extensions 字段值为 all 时才会返回POI内容）。设置 POI 类型参数相当于为上述操作限定要求。参数仅支持传入POI TYPECODE，可以传入多个POITYPECODE，相互之间用“|”分隔。该参
                        数在 batch 取值为 true 时不生效。
                output:返回数据格式类型，可选，默认JSON格式。可选输入内容包括：JSON，XML。设置JSON 返回结果数据将会以JSON结构构成；如果设置 XML 返回结果数据将以 XML 结构构成。
                batch:批量查询控制，可选，默认False。batch 参数设置为 true 时进行批量查询操作，最多支持 20 个经纬度点进行批量地址查询操作。batch 参数设置为 false 时进行单点查询，此时即使传入多个经纬度也只返回第一个
                        经纬度的地址解析查询结果。
                homeorcorp:是否优化POI返回顺序，可选，默认0。以下内容需要 extensions 参数为 all时才生效。homeorcorp 参数的设置可以影响召回 POI 内容的排序策略，目前提供三个可选参数：0：不对召回
                        的排序策略进行干扰。1：综合大数据分析将居家相关的 POI 内容优先返回，即优化返回结果中 pois字段的poi顺序。2：综合大数据分析将公司相关的 POI 内容优先返回，即优化返回结果中 pois
                        字段的poi顺序。
        Returns:返回获得的json格式数据或错误信息
        """

        self.location = location

        if 'batch' in kwargs:
            self.batch = kwargs['batch']
        if 'extensions' in kwargs:
            self.extensions = kwargs['extensions']
        if 'homeorcorp' in kwargs:
            self.homeorcrop = kwargs['homeorcorp']
        if 'poitype' in kwargs:
            self.poitype = kwargs['poitype']
        if 'radius' in kwargs:
            self.radius = kwargs['radius']
        if 'roadlevel' in kwargs:
            self.roadLevel = kwargs['roadlevel']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': GeographicCoding.APIkey,
                      'location': self.location,
                      }

        if self.batch is not None:
            parameters.update(batch=self.batch)
        if self.extensions is not None:
            parameters.update(extensions=self.extensions)
        if self.homeorcrop is not None:
            parameters.update(homeorcorp=self.homeorcrop)
        if self.poitype is not None:
            parameters.update(poitype=self.poitype)
        if self.radius is not None:
            parameters.update(radius=self.radius)
        if self.roadLevel is not None:
            parameters.update(roadlevel=self.roadLevel)

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/geocode/regeo?parameters",
                                               params=parameters)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - request_information:{1}'.format(function_name,
                                                                                               request_information)
                                  )
            request_information.close()  # 关闭访问
            request_information.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            inverse_json_decode = json.loads(request_information.text)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - Inverse geographic coding data successful get.'.format(
                                      function_name)
                                  )
            return inverse_json_decode

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
                                                                                        e.__class__.__name__)
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
            # only for debugging
            error_information = 'Unfortunately -- An unknown Error Happened, Please wait 3 seconds'
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

    def parse_geographic_coding(self, json_decode: dict
                                ) -> dict:
        """
        函数：解析地理编码数据
        Args:
            json_decode:get_geographic_coding()方法从网络中获取到的数据
        Returns:返回得到的经纬度值
        """

        self.json_decode = json_decode

        # 输出结果
        resultContext = {}

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

                    if self.json_decode['geocodes']:
                        # 地理位置
                        geographic_position = self.json_decode['geocodes'][0]['location']
                        # 地理位置对应的城市
                        geographic_city = self.json_decode['geocodes'][0]['city']
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - geographic_position:{1}'.format(
                                                  function_name,
                                                  geographic_position)
                                              )

                        resultContext['geographic_position'] = geographic_position
                        resultContext['geographic_city'] = geographic_city
                        return resultContext

                    else:
                        context = "您提供的地点信息查询失败，换个词进行搜索吧"
                        resultContext['error_context'] = context
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

            context = "您提供的地点信息查询失败，换个词进行搜索吧"
            resultContext['error_context'] = context
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

            context = "您提供的地点信息查询失败，换个词进行搜索吧"
            resultContext['error_context'] = context
            return resultContext

    def parse_inverse_geographic_coding(self, inverse_json_decode: dict,
                                        flag_batch: bool
                                        ) -> str or None:
        """
        函数：解析逆地理编码数据
        Args:
            inverse_json_decode:get_inverse_geographic_coding()方法从网络中获取到的数据
            flag_batch:是否为多值查询
        Returns:返回得到的经纬度值
        """

        # TODO:未来版本将返回数据从str/None升级为dict
        self.inverse_json_decode = inverse_json_decode

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        try:
            if inverse_json_decode['status'] == '0':
                # 官方文档异常
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - status:{1}'.format(function_name,
                                                                                      inverse_json_decode['status'])
                                      )
                raise OfficialException

            elif inverse_json_decode['status'] == '2':
                # 自定义异常
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - status:{1}'.format(function_name,
                                                                                      inverse_json_decode['status'])
                                      )
                raise CustomExpection

            elif inverse_json_decode['status'] == '1':
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=1,
                                      context='Function name:{0} - status:{1}'.format(function_name,
                                                                                      inverse_json_decode['status'])
                                      )

                if inverse_json_decode['infocode'] == "10000":  # 请求数据成功的状态码
                    if not flag_batch:  # 单点查询
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - flag_batch:{1}'.format(function_name,
                                                                                                  flag_batch)
                                              )
                        # 逆解析后的地理实际位置名称
                        inverse_geographic_information = inverse_json_decode['regeocode']['formatted_address']
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - inverse_geographic_information:{1}'.format(
                                                  function_name,
                                                  inverse_geographic_information)
                                              )

                        return inverse_geographic_information

                    else:  # 多值查询
                        len_regeocodes = len(inverse_json_decode['regeocodes'])
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - lenRegeocodes:{1}'.format(function_name,
                                                                                                     len_regeocodes)
                                              )

                        for item in range(len_regeocodes):
                            # 逆解析后的地理实际位置名称
                            formatted_address = inverse_json_decode['regeocodes'][item]['formatted_address']
                            # only for debugging
                            writeLog.write_to_log(file_name=log_filename,
                                                  log_level=1,
                                                  context='Function name:{0} - formatted_address:{1}'.format(
                                                      function_name,
                                                      formatted_address)
                                                  )

                        return inverse_json_decode['regeocodes']

        except OfficialException as officialException:
            # 获得的错误信息
            errcode, errorInfo, solution = officialException.get_error_info(inverse_json_decode)
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

            resultContext = "Error"
            return resultContext

        except CustomExpection as customException:
            info, detail_information, error_prompt = customException.get_error_info(inverse_json_decode)
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

            resultContext = "Error"
            return resultContext
