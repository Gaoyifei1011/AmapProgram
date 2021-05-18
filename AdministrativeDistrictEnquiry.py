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


class AdministrativeDistrictEnquiry:
    """
    Class:行政区域查询
    行政区域查询是一类简单的HTTP接口，根据用户输入的搜索条件可以帮助用户快速的查找特定的行政区域信息。
    """

    def __init__(self) -> None:
        self.district = None
        self.district_level = None
        self.extensions = None
        self.filter = None
        self.global_sub_district_value = None
        self.json_decode = None
        self.keywords = None
        self.offset = None
        self.output = None
        self.page = None
        self.sub_district = None
        self.sub_district_value = None
        self.global_sub_district_value = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    # 获取高德地图数据API的钥匙
    APIkey = '<请自己输入自己申请的API Key>'

    def get_administrative_district(self, keywords: str,
                                    sub_district: int,
                                    **kwargs: dict[str, Any]
                                    ) -> dict:
        """
        函数：行政区域查询数据。\n
        Args:
            keywords:查询关键字，可选。规则：只支持单个关键词语搜索关键词支持：行政区名称、citycode、adcode。例如，在subdistrict=2，搜索省份（例如山东），能够显示市（例如济南），区（例如历下区）。adcode信息可参考城市编码表获取
            sub_district:子级行政区，可选。规则：设置显示下级行政区级数（行政区级别包括：国家、省/直辖市、市、区/县、乡镇/街道多级数据）。可选值：0、1、2、3等数字，并以此类推
                0：不返回下级行政区；1：返回下一级行政区；2：返回下两级行政区；3：返回下三级行政区。
                需要在此特殊说明，目前部分城市和省直辖县因为没有区县的概念，故在市级下方直接显示街道。例如：广东-东莞、海南-文昌市
            kwargs:
                page:需要第几页数据，可选。最外层的districts最多会返回20个数据，若超过限制，请用page请求下一页数据。例如page=2；page=3。默认page=1
                offset:最外层返回数据个数，可选。
                extensions:返回结果控制，可选。此项控制行政区信息中返回行政区边界坐标点； 可选值：base、all;base:不返回行政区边界坐标点；all:只返回当前查询district的边界值，不返回子节点的边界值；
                    目前不能返回乡镇/街道级别的边界值。
                filter:根据区划过滤，可选。按照指定行政区划进行过滤，填入后则只返回该省/直辖市信息。填入adcode，为了保证数据的正确，强烈建议填入此参数
                output:返回数据格式类型，可选。可选值：JSON，XML。
        """

        self.keywords = keywords
        self.sub_district = sub_district

        if 'extensions' in kwargs:
            self.extensions = kwargs['extensions']
        if 'filter' in kwargs:
            self.filter = kwargs['filter']
        if 'output' in kwargs:
            self.output = kwargs['output']
        if 'offset' in kwargs:
            self.offset = kwargs['offset']
        if 'page' in kwargs:
            self.page = kwargs['page']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': self.APIkey,
                      'keywords': self.keywords,
                      'subdistrict': self.sub_district,
                      }

        if self.extensions is not None:
            parameters.update(extensions=self.extensions)
        if self.filter is not None:
            parameters.update(filter=self.filter)
        if self.output is not None:
            parameters.update(output=self.output)
        if self.offset is not None:
            parameters.update(offset=self.offset)
        if self.page is not None:
            parameters.update(page=self.page)

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/config/district?parameters",
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
                                  context='Function name:{0} - Administrative district data successful get.'.format(
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

    def parse_administrative_district(self, json_decode: dict,
                                      sub_district: int
                                      ) -> list:
        """
        函数：解析行政区域查询数据。
        Args:
            json_decode:get_administrative_district()方法从网络中获取的数据
            sub_district:返回的下几级行政区域的标志
        """

        # TODO:未来版本将返回数据从list升级为dict
        self.json_decode = json_decode
        self.sub_district = sub_district

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
                    district_level = {'country': '国',
                                      'province': '省',
                                      'city': '市',
                                      'district': '区/县级市/县',
                                      'street': '街道/镇/乡'
                                      }

                    # 请求结果
                    keywords_count = self.json_decode['count']
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - keywords count:{1}'.format(function_name,
                                                                                                  keywords_count)
                                          )
                    resultContext.append("根据您提供的关键字已为您查找到{0}个结果".format(keywords_count))

                    # 行政区域数目
                    districts = self.json_decode['districts']
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=6,
                                          context='Function name:{0} - districts acquired successfully'.format(
                                              function_name)
                                          )

                    # 输出行政区信息
                    sub_district_value = self.sub_district
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - sub_district_value:{1}'.format(function_name,
                                                                                                      sub_district_value)
                                          )

                    global_sub = self.sub_district
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename, log_level=1,
                                          context='Function name:{0} - global_sub:{1}'.format(function_name,
                                                                                              global_sub)
                                          )

                    if districts and sub_district_value >= 0:  # 里面的信息不为空
                        for district in districts:
                            # only for debugging
                            writeLog.write_to_log(file_name=log_filename,
                                                  log_level=1,
                                                  context='Function name:{0} - {1}'.format(function_name,
                                                                                           self.print_subdistrict.__name__
                                                                                           )
                                                  )
                            context = self.print_subdistrict(district, sub_district_value - 1, district_level,
                                                             global_sub)
                            resultContext.extend(context)

            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - print district successful run.'.format(function_name)
                                  )
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

            resultContext.append(errorInfo)
            context = "行政区域信息查询失败，换个词进行搜索吧"
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

            context = "行政区域信息查询失败，换个词进行搜索吧"
            resultContext.append(context)
            return resultContext

    def print_subdistrict(self, district: dict,
                          sub_district_value: int,
                          district_level: dict,
                          global_sub_district_value: int
                          ) -> list:
        """
        函数：打印查询的行政区域
        Args:
            district: 传入的关键字查询对应的行政区域
            sub_district_value:代表当前下一级行政区域的位置
            district_level:行政区域级别
            global_sub_district_value:传入全局查询的行政区域
        """

        # TODO:未来版本由于数据量巨大，将其放入子线程中进行，防止卡父GUI进程
        # TODO:未来版本将返回数据从list升级为dict
        self.district = district
        self.district_level = district_level
        self.global_sub_district_value = global_sub_district_value
        self.sub_district_value = sub_district_value

        # 输出结果
        resultContext = []

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        name = self.district['name']
        level = self.district_level[self.district['level']]

        # 当前行政区域
        subtraction = global_sub_district_value - sub_district_value - 1

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - global:{1}'.format(function_name,
                                                                              str(self.global_sub_district_value))
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - sub_district_value:{1}'.format(function_name,
                                                                                          sub_district_value)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - subtraction:{1}'.format(function_name,
                                                                                   str(subtraction))
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=6,
                              context='Function name:{0} - district search successfully'.format(function_name)
                              )

        # 同级行政区域
        if subtraction == 0:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - context:{1} - {2} - {3}'.format(function_name,
                                                                                               subtraction, name,
                                                                                               level)
                                  )
            resultContext.append("您提供的关键字查询名为“{0}”的行政区级别为“{1}”".format(name, level))

        # 下一级行政区域
        elif subtraction == 1:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - context:{1} - {2} - {3}'.format(function_name,
                                                                                               subtraction,
                                                                                               name,
                                                                                               level)
                                  )
            resultContext.append("您查询的关键字的下一级行政区名为“{0}”的行政区级别为“{1}”".format(name, level))

        # 下二级行政区域
        elif subtraction == 2:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - context:{1} - {2} - {3}'.format(function_name,
                                                                                               subtraction,
                                                                                               name,
                                                                                               level)
                                  )
            resultContext.append("您查询的关键字的下二级行政区名为“{0}”的行政区级别为“{1}”".format(name, level))

        # 下三级行政区域
        elif subtraction == 3:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - context:{1} - {2} - {3}'.format(function_name,
                                                                                               subtraction,
                                                                                               name,
                                                                                               level
                                                                                               )
                                  )
            resultContext.append("您查询的关键字的下三级行政区名为“{0}”的行政区级别为“{1}”".format(name, level))

        else:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - Query Failed'.format(function_name)
                                  )
            resultContext.append("查询错误")

        # 条件成立，继续搜索下一级行政区
        sub_districts = self.district['districts']
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - search sub districts'.format(function_name)
                              )

        # 行政区域结果数目
        len_sub_districts = len(self.district['districts'])

        if len_sub_districts > 0:
            resultContext.append("该行政区域包括{0}个结果".format(len_sub_districts))

        if sub_districts and self.sub_district_value >= 0:
            for sub_district in sub_districts:
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=1,
                                      context='Function name:{0} - {1}'.format(function_name,
                                                                               self.print_subdistrict.__name__)
                                      )
                context = self.print_subdistrict(sub_district, self.sub_district_value - 1, self.district_level,
                                                 self.global_sub_district_value)
                resultContext.extend(context)

        return resultContext

    def get_sub_administrative_district(self, json_decode
                                        ) -> list:
        """
        函数：解析行政区域下一级数据。
        Args:
            json_decode:get_administrative_district()方法从网络中获取的数据
        """

        # TODO:未来版本将返回数据从list升级为dict
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

                    # 请求结果
                    keywords_count = self.json_decode['count']
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - keywords count:{1}'.format(function_name,
                                                                                                  keywords_count)
                                          )

                    # 行政区域数目
                    districts = self.json_decode['districts']
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=6,
                                          context='Function name:{0} - districts acquired successfully'.format(
                                              function_name)
                                          )

                    # 输出行政区信息
                    if districts:  # 里面的信息不为空
                        for district in districts:
                            # 下一级行政区域列表
                            sub_districts = district['districts']
                            sub_districts.sort(key=lambda x: x['adcode'])
                            for subdistrict in sub_districts:
                                resultContext.append(subdistrict['name'])

            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - print district successful run.'.format(function_name)
                                  )
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

            resultContext.append(errorInfo)
            context = "行政区域信息查询失败，换个词进行搜索吧"
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

            context = "行政区域信息查询失败，换个词进行搜索吧"
            resultContext.append(context)
            return resultContext
