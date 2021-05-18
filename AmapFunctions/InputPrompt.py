# -*- coding:utf-8 -*-
# 导入的库
import inspect
import json
import time

import requests

from SelfExpection.CustomExpection import CustomExpection
from SelfExpection.OfficialException import OfficialException
from logrecord.WriteLog import WriteLog


class InputPrompt:
    """
    Class:输入提示
    输入提示是一类简单的HTTP接口，提供根据用户输入的关键词查询返回建议列表。
    """

    def __init__(self):
        self.city = None
        self.cityLimit = None
        self.datatype = None
        self.input_type = None
        self.json_decode = None
        self.keywords = None
        self.location = None
        self.output = None

        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    # 获取高德地图数据API的钥匙
    APIkey = '<请自己输入自己申请的API Key>'

    def get_input_prompt(self, keywords: str,
                         **kwargs
                         ) -> dict:
        """
        函数：提供根据用户输入的关键词查询返回建议列表。
        Args:
            keywords:查询关键词，必填。
            kwargs:
                input_type:POI分类，可选。服务可支持传入多个分类，多个类型剑用“|”分隔。可选值：POI分类名称、分类代码。此处强烈建议使用分类代码，否则可能会得到不符合预期的结果
                location:坐标，可选。格式：“X,Y”（经度,纬度），不可以包含空格。建议使用location参数，可在此location附近优先返回搜索关键词信息。在请求参数city不为空时生效
                city:搜索城市，可选，默认在全国范围内搜索。可选值：citycode、adcode，不支持县级市。如：010/110000
                    填入此参数后，会尽量优先返回此城市数据，但是不一定仅局限此城市结果，若仅需要某个城市数据请调用cityLimit参数。如：在深圳市搜天安门，返回北京天安门结果。
                cityLimit:仅返回指定城市数据，可选，默认false。可选值：true/false
                datatype:返回的数据类型，可选，默认all。多种数据类型用“|”分隔，可选值：all-返回所有数据类型、poi-返回POI数据类型、bus-返回公交站点数据类型、busLine-返回公交线路数据类型
                output:返回数据格式类型，可选，默认JSON格式。可选值：JSON,XML
        Returns:返回获得的json格式数据或错误信息
        """

        self.keywords = keywords

        if 'city' in kwargs:
            self.city = kwargs['city']
        if 'cityLimit' in kwargs:
            self.cityLimit = kwargs['cityLimit']
        if 'datatype' in kwargs:
            self.datatype = kwargs['datatype']
        if 'input_type' in kwargs:
            self.input_type = kwargs['input_type']
        if 'location' in kwargs:
            self.location = kwargs['location']
        if 'output' in kwargs:
            self.output = kwargs['output']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': InputPrompt.APIkey,
                      'keywords': self.keywords
                      }

        if self.city is not None:
            parameters.update(city=self.city)
        if self.cityLimit is not None:
            parameters.update(cityLimit=self.cityLimit)
        if self.datatype is not None:
            parameters.update(datatype=self.datatype)
        if self.input_type is not None:
            parameters.update(type=self.input_type)
        if self.location is not None:
            parameters.update(location=self.location)
        if self.output is not None:
            parameters.update(output=self.output)

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/assistant/inputtips?parameters",
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
                                  context='Function name:{0} - Input prompt data successful get.'.format(
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

    def parse_input_prompt(self, json_decode: dict,
                           datatype: str
                           ) -> None:
        """
        函数：解析提供根据用户输入的关键词得到的返回建议列表。
        Args:
            json_decode:get_input_prompt()方法从网络中获取的数据
            datatype:获取的数据类型
        """

        # TODO:未来版本升级为查询框输入的提示预备词
        self.datatype = datatype
        self.json_decode = json_decode

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        try:
            if json_decode['status'] == '0':
                # 官方文档异常
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - status:{1}'.format(function_name,
                                                                                      json_decode['status'])
                                      )
                raise OfficialException

            elif json_decode['status'] == '2':
                # 自定义异常
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - status:{1}'.format(function_name,
                                                                                      json_decode['status'])
                                      )
                raise CustomExpection

            elif json_decode['status'] == '1':
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=6,
                                      context='Function name:{0} - status:{1}'.format(function_name,
                                                                                      json_decode['status'])
                                      )
                if json_decode['infocode'] == "10000":  # 请求数据成功的状态码
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=6,
                                          context='Function name:{0} - infocode:{1}'.format(function_name,
                                                                                            json_decode['infocode'])
                                          )
                    # 提示信息，返回结果总数目
                    tips = json_decode['tips']
                    tips_count = json_decode['count']
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - tips_count:{1}'.format(function_name,
                                                                                              tips_count)
                                          )

                    if tips is not None:
                        # 所有数据类型
                        if datatype == 'all' or datatype == 'poi':
                            # only for debugging
                            writeLog.write_to_log(file_name=log_filename,
                                                  log_level=1,
                                                  context='Function name:{0} - all or poi:{1}'.format(function_name,
                                                                                                      1)
                                                  )
                            print("根据您的关键字已查询到以下相关信息")
                            print("共包含{0}条记录".format(tips_count))
                            for item, tip in enumerate(tips):
                                name = tip['name']
                                district = tip['district']
                                adcode = tip['adcode']
                                location = tip['location']
                                address = tip['address']
                                typeCode = tip['typeCode']

                                # only for debugging
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - name:{1}'.format(function_name,
                                                                                                    name)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - district:{1}'.format(function_name,
                                                                                                        district)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - adcode:{1}'.format(function_name,
                                                                                                      adcode)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - location:{1}'.format(function_name,
                                                                                                        location)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - address:{1}'.format(function_name,
                                                                                                       address)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - typeCode:{1}'.format(function_name,
                                                                                                        typeCode)
                                                      )

                                print("============================")
                                print("第{0}条".format(item + 1))
                                if address:
                                    print("名称：{0}，地址：{1}".format(name, address))
                                else:
                                    print("名称：{0}".format(name))
                                print("具体位置信息：{0}".format(district))

                        elif datatype == 'bus':
                            print("根据您的关键字已查询到以下相关公交站或地铁站")
                            print("共包含{0}条记录".format(tips_count))
                            for item, tip in enumerate(tips):
                                name = tip['name']
                                district = tip['district']
                                adcode = tip['adcode']
                                location = tip['location']
                                address = tip['address']
                                typeCode = tip['typeCode']

                                # only for debugging
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - name:{1}'.format(function_name,
                                                                                                    name)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - district:{1}'.format(function_name,
                                                                                                        district)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - adcode:{1}'.format(function_name,
                                                                                                      adcode)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - location:{1}'.format(function_name,
                                                                                                        location)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - address:{1}'.format(function_name,
                                                                                                       address)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - typeCode:{1}'.format(function_name,
                                                                                                        typeCode)
                                                      )

                                print("============================")
                                print("第{0}条".format(item + 1))
                                print("公交/地铁站名称：{0}，公交/地铁线路名称：{1}".format(name, address))
                                print("具体位置信息：{0}".format(district))

                        elif datatype == 'busline':
                            print("根据您的关键字已查询到以下相关公交线路")
                            print("共包含{0}条记录".format(tips_count))
                            for item, tip in enumerate(tips):
                                name = tip['name']
                                district = tip['district']
                                adcode = tip['adcode']
                                typeCode = tip['typeCode']

                                # only for debugging
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - name:{1}'.format(function_name,
                                                                                                    name)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - district:{1}'.format(function_name,
                                                                                                        district)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - adcode:{1}'.format(function_name,
                                                                                                      adcode)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=1,
                                                      context='Function name:{0} - typeCode:{1}'.format(function_name,
                                                                                                        typeCode)
                                                      )

                                print("============================")
                                print("第{0}条".format(item + 1))
                                print("公交/地铁线路名称：{0}".format(name))
                                print("具体位置信息：{0}".format(district))
                        else:
                            print("暂未查询到相关信息，请尝试更换关键字查询")
                    else:
                        print("暂未查询到相关信息，请尝试更换关键字查询")

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
