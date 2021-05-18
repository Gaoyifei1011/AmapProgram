# -*- coding:utf-8 -*-
# 导入的库
import datetime
import inspect
import json
import time

import requests

from SelfExpection.CustomExpection import CustomExpection
from SelfExpection.OfficialException import OfficialException
from logrecord.WriteLog import WriteLog


class WeatherInformation:
    """
    Class:天气查询
    天气查询是一个简单的HTTP接口，根据用户输入的adcode，查询目标区域当前/未来的天气情况。
    """

    def __init__(self):
        self.city = None
        self.extensions = None
        self.json_decode = None
        self.output = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    # 获取高德地图数据API的钥匙
    APIkey = '<请自己输入自己申请的API Key>'

    def get_weather_information(self, city: str,
                                **kwargs
                                ) -> dict:
        """
        函数：获取天气查询数据。\n
        Args:
            city:城市编码，必填。输入城市的adcode，adcode信息可参考城市编码表
            kwargs:
                extensions:气象类型，选填，默认base。可选值：base/all，base:返回实况天气，all:返回预报天气
                output:返回格式，可选，默认JSON格式。可选值：JSON,XML。
        Returns:返回获得的json格式数据或错误信息
        """
        self.city = city

        if 'extensions' in kwargs:
            self.extensions = kwargs['extensions']
        if 'output' in kwargs:
            self.output = kwargs['output']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': self.APIkey,
                      'city': self.city,
                      }

        if self.extensions is not None:
            parameters.update(extensions=self.extensions)
        if self.output is not None:
            parameters.update(output=self.output)

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/weather/weatherInfo?parameters",
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
                                  context='Function name:{0} - Weather information data successful get.'.format(
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
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,
                                                                                        e.__class__.__name__)
                                  )
            # 异常信息
            error_information = 'Unfortunately -- An Unknown Error Happened, Please wait 3 seconds'
            error_information_dict = {'status': '2',
                                      'info': 'HTTPError',
                                      'detail_information': requests.exceptions.ChunkedEncodingError,
                                      'error_prompt': error_information
                                      }
            return error_information_dict

    def parse_weather_information(self, json_decode: dict,
                                  extensions: str
                                  ) -> list:
        """
        函数：解析天气查询数据。\n
        Args:
            json_decode:get_weather_information()方法从网络中获取的数据
            extensions:获取数据的类型
        Returns:
            返回获取到的天气信息
        """

        # TODO:优化代码，递归创建目录 os.mkdirs()
        self.extensions = extensions
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
                if self.json_decode['infocode'] == "10000":  # 请求数据成功的状态码

                    # 查询实况天气/预报天气
                    week_dict = {"1": "一", "2": "二", "3": "三", "4": "四", "5": "五", "6": "六", "7": "日"}
                    if self.extensions == 'base':
                        lives = self.json_decode['lives']
                        if lives:
                            # 实况天气
                            for live in lives:
                                # 查询的数据包括省份名，城市名，天气现象，实时气温，凤翔描述，风力级别，空气湿度，数据发布的时间
                                province = live['province']
                                city = live['city']
                                weather = live['weather']
                                temperature = live['temperature']
                                winddirection = live['winddirection']
                                windpower = live['windpower']
                                tempwindpower = []
                                humidity = live['humidity']
                                reporttime = live['reporttime']
                                datetime_reporttime = datetime.datetime.strptime(reporttime, '%Y-%m-%d %H:%M:%S')
                                formatted_reporttime = datetime_reporttime.strftime('%Y年%m月%d日%H时%M分%S秒')

                                # only for debugging
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - province:{1}'.format(function_name,
                                                                                                        province)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - city:{1}'.format(function_name,
                                                                                                    city)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - weather:{1}'.format(function_name,
                                                                                                       weather)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - temperature:{1}'.format(
                                                          function_name,
                                                          temperature)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - winddirection:{1}'.format(
                                                          function_name,
                                                          winddirection)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - windpower:{1}'.format(function_name,
                                                                                                         windpower)
                                                      )  # only for debugging
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - tempwindpower:{1}'.format(
                                                          function_name,
                                                          tempwindpower)
                                                      )  # only for debugging
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - humidity:{1}'.format(function_name,
                                                                                                        humidity)
                                                      )  # only for debugging
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - reporttime:{1}'.format(function_name,
                                                                                                          reporttime)
                                                      )

                                # 天气信息——风力
                                for item in windpower:
                                    tempwindpower.append(item)
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - tempwindpower:{1}'.format(
                                                          function_name,
                                                          tempwindpower)
                                                      )

                                resultContext.append("您查询{0}{1}的天气情况如下所示：".format(province, city))
                                if tempwindpower[0] == "<":
                                    resultContext.append(
                                        "今日天气{0}，温度{1}度，{2}风小于{3}级，空气湿度{4}".format(weather, temperature, winddirection,
                                                                                   tempwindpower[1], humidity))
                                elif tempwindpower[0] == "≤":
                                    resultContext.append(
                                        "今日天气{0}，温度{1}度，{2}风小于等于{3}级，空气湿度{4}".format(weather, temperature,
                                                                                     winddirection,
                                                                                     tempwindpower[1], humidity))
                                else:
                                    resultContext.append(
                                        "今日天气{0}，温度{1}度，{2}风{3}级，空气湿度{4}".format(weather, temperature, winddirection,
                                                                                 windpower,
                                                                                 humidity))
                                resultContext.append("天气数据已于{0}更新".format(formatted_reporttime))
                        else:
                            context = "暂未查到天气信息，换个词进行搜索吧"
                            resultContext.append(context)

                    elif self.extensions == 'all':
                        # 预测天气
                        forecasts = self.json_decode['forecasts']
                        if forecasts:
                            for forecast in forecasts:
                                province = forecast['province']
                                city = forecast['city']
                                reporttime = forecast['reporttime']
                                datetime_reporttime = datetime.datetime.strptime(reporttime, '%Y-%m-%d %H:%M:%S')
                                formatted_reporttime = datetime_reporttime.strftime('%Y年%m月%d日%H时%M分%S秒')
                                casts = forecast['casts']
                                # only for debugging
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - province:{1}'.format(function_name,
                                                                                                        province)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - city:{1}'.format(function_name,
                                                                                                    city)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - report time:{1}'.format(
                                                          function_name,
                                                          reporttime)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - datetime report time:{1}'.format(
                                                          function_name,
                                                          datetime_reporttime)
                                                      )
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - format report time:{1}'.format(
                                                          function_name,
                                                          formatted_reporttime)
                                                      )

                                # 预测数据
                                for item, cast in enumerate(casts):
                                    date = cast['date']
                                    datetime_date = datetime.datetime.strptime(date, '%Y-%m-%d')
                                    formatted_date = datetime_date.strftime('%Y年%m月%d日')
                                    week = cast['week']
                                    dayweather = cast['dayweather']
                                    nightweather = cast['nightweather']
                                    daytemp = cast['daytemp']
                                    nighttemp = cast['nighttemp']
                                    daywind = cast['daywind']
                                    nightwind = cast['nightwind']
                                    daypower = cast['daypower']
                                    tempdaywindpower = []
                                    nightpower = cast['nightpower']
                                    tempnightwindpower = []

                                    # only for debugging
                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} - date:{1}'.format(function_name,
                                                                                                        date)
                                                          )
                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} - date time:{1}'.format(
                                                              function_name,
                                                              datetime_date)
                                                          )
                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} - format date:{1}'.format(
                                                              function_name,
                                                              formatted_date)
                                                          )
                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} - week:{1}'.format(
                                                              function_name,
                                                              week)
                                                          )
                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} - dayweather:{1}'.format(
                                                              function_name,
                                                              dayweather)
                                                          )
                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} - night weather:{1}'.format(
                                                              function_name,
                                                              nightweather)
                                                          )
                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} - day temp:{1}'.format(
                                                              function_name,
                                                              daytemp)
                                                          )  # only for debugging
                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} - night temp:{1}'.format(
                                                              function_name,
                                                              nighttemp)
                                                          )  # only for debugging
                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} - day wind:{1}'.format(
                                                              function_name,
                                                              daywind)
                                                          )
                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} - night wind:{1}'.format(
                                                              function_name,
                                                              nightwind)
                                                          )
                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} - day power:{1}'.format(
                                                              function_name,
                                                              daypower)
                                                          )
                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} - night power:{1}'.format(
                                                              function_name,
                                                              nightpower)
                                                          )

                                    for sub_item in daypower:
                                        tempdaywindpower.append(sub_item)
                                    for sub_item in nightpower:
                                        tempnightwindpower.append(sub_item)

                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} -  tempdaywindpower:{1}'.format(
                                                              function_name,
                                                              tempdaywindpower)
                                                          )
                                    writeLog.write_to_log(file_name=log_filename,
                                                          log_level=3,
                                                          context='Function name:{0} - tempnightwindpower:{1}'.format(
                                                              function_name,
                                                              tempnightwindpower)
                                                          )

                                    # 今日天气
                                    if item == 0:
                                        resultContext.append("=========================================")
                                        resultContext.append("您查询{0}{1}的今天天气情况如下所示：".format(province, city))
                                        resultContext.append("今天是{0}，星期{1}".format(formatted_date, week_dict[week]))
                                        if tempdaywindpower[0] == "<":
                                            resultContext.append(
                                                "今天白天{0}，温度{1}度，{2}风小于{3}级".format(dayweather, daytemp, daywind,
                                                                                   tempdaywindpower[1]))
                                        elif tempdaywindpower[0] == "≤":
                                            resultContext.append(
                                                "今天白天{0}，温度{1}度，{2}风小于等于{3}级".format(dayweather, daytemp, daywind,
                                                                                     tempdaywindpower[1]))
                                        else:
                                            resultContext.append(
                                                "今天白天{0}，温度{1}度，{2}风{3}级".format(dayweather, daytemp, daywind,
                                                                                 tempdaywindpower[0]))
                                        if tempnightwindpower[0] == "<":
                                            resultContext.append(
                                                "今天夜间{0}，温度{1}度，{2}风小于{3}级".format(nightweather, nighttemp, nightwind,
                                                                                   tempnightwindpower[1]))
                                        elif tempdaywindpower[0] == "≤":
                                            resultContext.append(
                                                "今天夜间{0}，温度{1}度，{2}风小于等于{3}级".format(nightweather, nighttemp, nightwind,
                                                                                     tempnightwindpower[1]))
                                        else:
                                            resultContext.append(
                                                "今天夜间{0}，温度{1}度，{2}风{3}级".format(nightweather, nighttemp, nightwind,
                                                                                 nightpower))

                                    # 明天天气
                                    elif item == 1:
                                        resultContext.append("=========================================")
                                        resultContext.append("您查询{0}{1}的明天天气情况如下所示：".format(province, city))
                                        resultContext.append("明天是{0}，星期{1}".format(formatted_date, week_dict[week]))
                                        if tempdaywindpower[0] == "<":
                                            resultContext.append(
                                                "明天白天{0}，温度{1}度，{2}风小于{3}级".format(dayweather, daytemp, daywind,
                                                                                   tempdaywindpower[1]))
                                        elif tempdaywindpower[0] == "≤":
                                            resultContext.append(
                                                "明天白天{0}，温度{1}度，{2}风小于等于{3}级".format(dayweather, daytemp, daywind,
                                                                                     tempdaywindpower[1]))
                                        else:
                                            resultContext.append(
                                                "明天白天{0}，温度{1}度，{2}风{3}级".format(dayweather, daytemp, daywind,
                                                                                 daypower))
                                        if tempnightwindpower[0] == "<":
                                            resultContext.append(
                                                "明天夜间{0}，温度{1}度，{2}风小于{3}级".format(nightweather, nighttemp, nightwind,
                                                                                   tempnightwindpower[1]))
                                        elif tempdaywindpower[0] == "≤":
                                            resultContext.append(
                                                "明天夜间{0}，温度{1}度，{2}风小于等于{3}级".format(nightweather, nighttemp, nightwind,
                                                                                     tempnightwindpower[1]))
                                        else:
                                            resultContext.append(
                                                "明天夜间{0}，温度{1}度，{2}风{3}级".format(nightweather, nighttemp, nightwind,
                                                                                 nightpower))

                                    # 后天天气
                                    elif item == 2:
                                        resultContext.append("=========================================")
                                        resultContext.append("您查询{0}{1}的后天情况如下所示：".format(province, city))
                                        resultContext.append("后天是{0}，星期{1}".format(formatted_date, week_dict[week]))
                                        if tempdaywindpower[0] == "<":
                                            resultContext.append(
                                                "后天白天{0}，温度{1}度，{2}风小于{3}级".format(dayweather, daytemp, daywind,
                                                                                   tempdaywindpower[1]))
                                        elif tempdaywindpower[0] == "≤":
                                            resultContext.append(
                                                "后天白天{0}，温度{1}度，{2}风小于等于{3}级".format(dayweather, daytemp, daywind,
                                                                                     tempdaywindpower[1]))
                                        else:
                                            resultContext.append(
                                                "后天白天{0}，温度{1}度，{2}风{3}级".format(dayweather, daytemp, daywind,
                                                                                 daypower))
                                        if tempnightwindpower[0] == "<":
                                            resultContext.append(
                                                "后天夜间{0}，温度{1}度，{2}风小于{3}级".format(nightweather, nighttemp, nightwind,
                                                                                   tempnightwindpower[1]))
                                        elif tempdaywindpower[0] == "≤":
                                            resultContext.append(
                                                "后天夜间{0}，温度{1}度，{2}风小于等于{3}级".format(nightweather, nighttemp, nightwind,
                                                                                     tempnightwindpower[1]))
                                        else:
                                            resultContext.append(
                                                "后天夜间{0}，温度{1}度，{2}风{3}级".format(nightweather, nighttemp, nightwind,
                                                                                 nightpower))

                                    # 大后天天气
                                    elif item == 3:
                                        resultContext.append("=========================================")
                                        resultContext.append("您查询{0}{1}的大后天情况如下所示：".format(province, city))
                                        resultContext.append("大后天是{0}，星期{1}".format(formatted_date, week_dict[week]))
                                        if tempdaywindpower[0] == "<":
                                            resultContext.append(
                                                "大后天白天{0}，温度{1}度，{2}风小于{3}级".format(dayweather, daytemp, daywind,
                                                                                    tempdaywindpower[1]))
                                        elif tempdaywindpower[0] == "≤":
                                            resultContext.append(
                                                "大后天白天{0}，温度{1}度，{2}风小于等于{3}级".format(dayweather, daytemp, daywind,
                                                                                      tempdaywindpower[1]))
                                        else:
                                            resultContext.append(
                                                "大后天白天{0}，温度{1}度，{2}风{3}级".format(dayweather, daytemp, daywind,
                                                                                  daypower))
                                        if tempnightwindpower[0] == "<":
                                            resultContext.append(
                                                "大后天夜间{0}，温度{1}度，{2}风小于{3}级".format(nightweather, nighttemp, nightwind,
                                                                                    tempnightwindpower[1]))
                                        elif tempdaywindpower[0] == "≤":
                                            resultContext.append(
                                                "大后天夜间{0}，温度{1}度，{2}风小于等于{3}级".format(nightweather, nighttemp,
                                                                                      nightwind,
                                                                                      tempnightwindpower[1]))
                                        else:
                                            resultContext.append(
                                                "大后天夜间{0}，温度{1}度，{2}风{3}级".format(nightweather, nighttemp, nightwind,
                                                                                  nightpower))

                                    # 异常数据
                                    else:
                                        resultContext.append("天气数据异常")
                                resultContext.append("=========================================")
                                resultContext.append("天气数据已于{0}更新".format(formatted_reporttime))
                                writeLog.write_to_log(file_name=log_filename,
                                                      log_level=3,
                                                      context='Function name:{0} - weather information print successfully.'.format(
                                                          function_name)
                                                      )

                        # 查询暂无结果
                        else:
                            context = "暂未查到天气信息，换个词进行搜索吧"
                            resultContext.append(context)
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
            context = "天气信息查询失败，换个词进行搜索吧"
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

            context = "天气信息查询失败，换个词进行搜索吧"
            resultContext.append(context)
            return resultContext
