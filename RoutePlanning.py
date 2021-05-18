# -*- coding:utf-8 -*-
# 导入的库
import datetime
import inspect
import json
import time

import requests

from AmapFunctions.GeographicCoding import GeographicCoding  # 导入地理编码模块
from SelfExpection import CustomExpection
from SelfExpection.OfficialException import OfficialException
from logrecord.WriteLog import WriteLog


class RoutePlanning:
    """
    Class:路径规划
    无需展现地图的场景下，进行线路查询，如以线路结果页形式展现换乘方案
    根据返回线路数据，自行开发线路导航
    """

    def __init__(self) -> None:
        self.avoidPolygons = None
        self.avoidRoad = None
        self.batch = None
        self.busLine = None
        self.bus_entrance = None
        self.bus_exit = None
        self.bus_time = None
        self.city = None
        self.cityd = None
        self.carType = None
        self.date = None
        self.destination = None
        self.destinationId = None
        self.destinationType = None
        self.extensions = None
        self.ferry = None
        self.json_decode = None
        self.nightFlag = None
        self.noSteps = None
        self.number = None
        self.origin = None
        self.originId = None
        self.originType = None
        self.output = None
        self.province = None
        self.railway = None
        self.roadAggregation = None
        self.segment = None
        self.strategy = None
        self.waypoints = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    # 获取高德地图数据API的钥匙
    APIkey = '<请自己输入自己申请的API Key>'

    def get_walking_route_planning(self, origin: str,
                                   destination: str,
                                   **kwargs
                                   ) -> dict:
        """
        函数：获取步行路径规划数据。\n
        Args:
            origin:出发点，必填。规则： lon，lat（经度，纬度）， “,”分割，如117.500244, 40.417801。经纬度小数点不超过6位。
            destination:目的地，必填。规则： lon，lat（经度，纬度）， “,”分割，如117.500244, 40.417801。经纬度小数点不超过6位。
            kwargs:
                output:返回数据格式类型，可选，默认JSON格式。可选值：JSON，XML
        Returns:返回获得的json格式数据或错误信息
        """

        self.destination = destination
        self.origin = origin

        if 'output' in kwargs:
            self.output = kwargs['output']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': self.APIkey,
                      'origin': self.origin,
                      'destination': self.destination,
                      }

        if self.output is not None:
            parameters.update(output=self.output)

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/direction/walking?parameters",
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
                                  context='Function name:{0} - Walking route Planning data successful get.'.format(
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

    def parse_walking_route_planning(self, json_decode: dict
                                     ) -> list:
        """
        函数：解析步行路径规划数据。\n
        Args:
            json_decode:get_walking_route_planning()方法从网络中获取到的数据
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
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - status:{1}'.format(function_name,
                                                                                      self.json_decode['status'])
                                      )
                # 自定义异常
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
                    # 步行方案路线信息列表
                    paths = self.json_decode['route']['paths']
                    len_paths = len(paths)
                    resultContext.append("已为您智能生成{0}种步行方案".format(len_paths))
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - path length:{1}'.format(function_name,
                                                                                               len_paths)
                                          )

                    # 步行方案
                    for path in paths:
                        # 步行距离
                        distance = path['distance']
                        resultContext.append("本次步行规划步行的长度为{0:.0f}米".format(int(distance)))
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - distance:{1}'.format(function_name,
                                                                                                distance)
                                              )

                        # 步行时长
                        duration = str(datetime.timedelta(seconds=int(path['duration']))).split(":")
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - duration:{1}'.format(function_name,
                                                                                                duration)
                                              )
                        if duration[1] == '0':  # 在60秒以内
                            resultContext.append("本次步行规划步行的时长为{0}秒".format(duration[2]))
                        elif duration[0] == '0':  # 在一小时以内
                            resultContext.append("本次步行规划步行的时长为{0}分{1}秒".format(duration[1], duration[2]))
                        else:
                            if duration[1] == '0':
                                resultContext.append("本次步行规划步行的时长为{0}时{1}秒".format(duration[0], duration[2]))
                            else:
                                resultContext.append("本次步行规划步行的时长为{0}时{1}分{2}秒".format(duration[0], duration[1],
                                                                                       duration[2]))

                        # 步行结果列表
                        steps = path['steps']
                        len_steps = len(steps)
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - step length:{1}'.format(function_name,
                                                                                                   len_steps)
                                              )
                        resultContext.append("本次路径规划共分为{0}步".format(len_steps))

                        for item, step in enumerate(steps):
                            # 路段步行指示
                            instruction = step['instruction']
                            # only for debugging
                            writeLog.write_to_log(file_name=log_filename,
                                                  log_level=1,
                                                  context='Function name:{0} - instruction:{1}'.format(function_name,
                                                                                                       instruction)
                                                  )
                            resultContext.append("第{0}步：{1}".format(item + 1, instruction))
                    resultContext.append("步行导航结束")
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
            # 异常信息
            resultContext.append(errorInfo)
            context = "步行导航查询失败，换个词进行搜索吧"
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
            # 异常信息
            context = "步行导航查询失败，换个词进行搜索吧"
            resultContext.append(context)
            return resultContext

    def get_bus_route_planning(self, origin: str,
                               destination: str,
                               city: str,
                               **kwargs
                               ) -> dict:
        """
        函数：获取公交路径规划数据。\n
        Args:
            origin:出发点，必填。规则： lon，lat（经度，纬度）， “,”分割，如117.500244, 40.417801。经纬度小数点不超过6位。
            destination:目的地，必填。规则： lon，lat（经度，纬度）， “,”分割，如117.500244, 40.417801。经纬度小数点不超过6位。
            city:城市/跨城规划时的起点城市，必填。目前支持市内公交换乘/跨城公交的起点城市。可选值：城市名称/citycode。
            kwargs:
                cityd:跨城公交规划时的终点城市，可选（ 跨城必填 ）。跨城公交规划必填参数。可选值：城市名称/citycode。
                extensions:返回结果详略，可选，默认base。可选值：base(default)/all。base:返回基本信息；all：返回全部信息。
                strategy:公交换乘策略，可选。可选值：0：最快捷模式；1：最经济模式；2：最少换乘模式；3：最少步行模式；5：不乘地铁模式。
                nightFlag:是否计算夜班车，可选。可选值：0：不计算夜班车；1：计算夜班车。
                date:出发日期，可选根据出发时间和日期，筛选可乘坐的公交路线，格式示例：date=2014-3-19。在无需设置预计出发时间时，请不要在请求之中携带此参数。
                bus_time:出发时间，可选。根据出发时间和日期，筛选可乘坐的公交路线，格式示例：time=22:34。在无需设置预计出发时间时，请不要在请求之中携带此参数。
                output:返回数据格式类型，可选，默认JSON格式。可选值：JSON，XML。
        Returns:返回获得的json格式数据或错误信息
        """

        self.city = city
        self.destination = destination
        self.origin = origin

        if 'bus_time' in kwargs:
            self.bus_time = kwargs['bus_time']
        if 'cityd' in kwargs:
            self.cityd = kwargs['cityd']
        else:
            self.cityd = ''
        if 'date' in kwargs:
            self.date = kwargs['date']
        if 'extensions' in kwargs:
            self.extensions = kwargs['extensions']
        if 'nightFlag' in kwargs:
            self.nightFlag = kwargs['nightFlag']
        if 'output' in kwargs:
            self.output = kwargs['output']
        if 'strategy' in kwargs:
            self.strategy = kwargs['strategy']
        else:
            self.strategy = 10

        # 传入参数
        parameters = {'key': self.APIkey,
                      'origin': self.origin,
                      'destination': self.destination,
                      'city': self.city,
                      'cityd': self.cityd,
                      }

        if self.bus_time is not None:
            parameters.update(bus_time=self.bus_time)
        if self.cityd is not None:
            parameters.update(cityd=self.cityd)
        if self.date is not None:
            parameters.update(date=self.date)
        if self.extensions is not None:
            parameters.update(nightflag=self.nightFlag)
        if self.output is not None:
            parameters.update(output=self.output)
        if self.strategy is not None:
            parameters.update(strategy=self.strategy)

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/direction/transit/integrated?parameters",
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
                                  context='Function name:{0} - Bus route Planning data successful get.'.format(
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

    def parse_bus_route_planning(self, json_decode: dict, batch: bool = False
                                 ) -> list:
        """
        函数：解析公交路径规划数据。\n
        Args:
            json_decode:get_bus_route_planning()方法从网络中获取到的数据
            batch:是否为多值查询
        """

        # TODO:未来版本将返回数据从list升级为dict
        self.json_decode = json_decode
        self.batch = batch

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

                    geographic_coding = GeographicCoding()
                    # 起始位置数据
                    origin = self.json_decode['route']['origin']
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - origin:{1}'.format(function_name,
                                                                                          origin)
                                          )

                    inverse_start_json_decode = geographic_coding.get_inverse_geographic_coding(
                        location=origin,
                        radius=100,
                        roadLevel=1,
                        extensions='base')
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - inverse_start_json_decode get successfully.'.format(
                                              function_name)
                                          )

                    start_bus_station_information = geographic_coding.parse_inverse_geographic_coding(
                        inverse_json_decode=inverse_start_json_decode, flag_batch=self.batch)
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - start_bus_station_information:{1}'.format(
                                              function_name,
                                              start_bus_station_information)
                                          )

                    # 终点位置数据
                    destination = self.json_decode['route']['destination']
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - destination:{1}'.format(function_name,
                                                                                               destination)
                                          )

                    inverse_end_json_decode = geographic_coding.get_inverse_geographic_coding(
                        location=destination,
                        radius=100,
                        roadLevel=1,
                        extensions='base')
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - inverse_end_json_decode get successfully.'.format(
                                              function_name)
                                          )

                    terminal_bus_station_information = geographic_coding.parse_inverse_geographic_coding(
                        inverse_json_decode=inverse_end_json_decode, flag_batch=self.batch)
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - terminal_bus_station_information:{1}'.format(
                                              function_name,
                                              terminal_bus_station_information)
                                          )

                    distance = int(self.json_decode['route']['distance']) / 1000
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - distance:{1}'.format(function_name,
                                                                                            distance)
                                          )

                    taxi_cost = self.json_decode['route']['taxi_cost']
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - taxi_cost:{1}'.format(function_name,
                                                                                             taxi_cost)
                                          )

                    resultContext.append("您好，从{0}到{1}的公交路程规划如下所示：".format(start_bus_station_information,
                                                                          terminal_bus_station_information))
                    resultContext.append("此次路线规划的起点到终点的距离为{0:.2f}公里".format(distance))
                    resultContext.append("若您采用打车方案，打车费用预计为{0}元".format(taxi_cost))

                    # 换乘方案
                    transits = self.json_decode['route']['transits']
                    len_transits = self.json_decode["count"]
                    resultContext.append("已为您智能生成如下{0}种换乘方案。".format(len_transits))
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - transits length:{1}'.format(function_name,
                                                                                                   len_transits)
                                          )

                    # 详细内容
                    for item, transit in enumerate(transits):
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - item:{1}'.format(function_name,
                                                                                            item)
                                              )
                        transit_cost = 0
                        if transit['cost']:
                            transit_cost = float(transit['cost'])
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - transit_cost:{1}'.format(function_name,
                                                                                                    transit_cost)
                                              )
                        transit_duration = str(datetime.timedelta(seconds=int(transit['duration']))).split(":")
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - transit_duration:{1}'.format(function_name,
                                                                                                        destination)
                                              )
                        transit_walking_distance = transit['walking_distance']
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - transit_walking_distance:{1}'.format(
                                                  function_name,
                                                  transit_walking_distance)
                                              )
                        transit_nightflag = transit['nightflag']  # 夜间乘车标志
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - transit_nightflag:{1}'.format(function_name,
                                                                                                         transit_nightflag)
                                              )

                        resultContext.append("=========================================")

                        # 方案换乘花费
                        resultContext.append("方案{0}的换乘价格为{1:.0f}元".format(item + 1, transit_cost))

                        # 方案换乘时间
                        if transit_duration[1] == '0':  # 在60秒以内
                            resultContext.append("此换乘方案预期时间为{0}秒".format(transit_duration[2]))
                        elif transit_duration[0] == '0':  # 在一小时以内
                            resultContext.append(
                                "此公交乘坐方案预计花费的时间为{0}分{1}秒".format(transit_duration[1], transit_duration[2]))
                        else:
                            if transit_duration[1] == '0':
                                resultContext.append(
                                    "此换乘方案预期时间为{0}时{1}秒".format(transit_duration[0], transit_duration[2]))
                            else:
                                resultContext.append(
                                    "此换乘方案预期时间为{0}时{1}分{2}秒".format(transit_duration[0], transit_duration[1],
                                                                    transit_duration[2]))
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=6,
                                              context='Function name:{0} - transit successfully executed'.format(
                                                  function_name)
                                              )

                        # 此方案总步行距离
                        resultContext.append("方案{0}的总步行距离为{1}米".format(item + 1, transit_walking_distance))

                        # 换乘路段列表
                        segments = transit['segments']
                        len_segments = len(segments)
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - segments length:{1}'.format(function_name,
                                                                                                       len_segments)
                                              )

                        resultContext.append("此方案需要{0}次中转".format(len_segments - 1))

                        for segment in segments:
                            context = self.print_bus_segments(segment)
                            resultContext.extend(context)
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
            context = "公交导航查询失败，换个词进行搜索吧"
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

            context = "步行导航查询失败，换个词进行搜索吧"
            resultContext.append(context)
            return resultContext

    def print_bus_segments(self, segment: dict
                           ) -> list:
        """
        函数：打印公交路线信息
        Args:
            segment:换乘路段列表中的具体换乘方案
        """

        # TODO:未来版本将返回数据从list升级为dict
        self.segment = segment

        resultContext = []

        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # taxi字段，占位符
        if self.segment['taxi']:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - taxi data:{1}'.format(function_name,
                                                                                     self.segment['taxi'])
                                  )

        # 此路段步行导航信息
        if self.segment['walking']:
            resultContext.append("==============================")
            resultContext.append("请步行走到离您将要乘坐的公交站或地铁口")
            walking = self.segment['walking']
            # 步行距离长度，步行持续时间
            walking_distance = walking['distance']
            walking_duration = walking['duration']
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - walking_distance:{1}'.format(function_name,
                                                                                            walking_distance)
                                  )
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - walking duration:{1}'.format(function_name,
                                                                                            walking_duration)
                                  )
            # 路线规划
            resultContext.append("步行距离长度{0}米，预计行走{1}秒".format(walking_distance, walking_duration))
            steps = walking['steps']
            len_steps = len(steps)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - steps length:{1}'.format(function_name,
                                                                                        len_steps)
                                  )

            # 具体步骤
            for sub_item, step in enumerate(steps):
                instruction = step['instruction']
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=1,
                                      context='Function name:{0} - instruction:{1}'.format(function_name,
                                                                                           instruction)
                                      )
                resultContext.append("第{0}步：{1}".format(sub_item + 1, instruction))
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=1,
                                      context='Function name:{0} - step action:{1}'.format(function_name,
                                                                                           step['assistant_action'])
                                      )

                # 步行到达终点
                if step['assistant_action']:
                    assistant_action = step['assistant_action']
                    resultContext.append("步行已到达目的地：{0}".format(assistant_action))
                    resultContext.append("步行导航结束")

        if self.segment['bus']:  # 此路段公交导航信息
            resultContext.append("================================")
            buslines = self.segment['bus']['buslines']
            bus_entrance = self.segment['entrance']
            bus_exit = self.segment['exit']
            # 公交路线
            for busline in buslines:
                context = self.parse_buslines(busline, bus_entrance, bus_exit)
                resultContext.extend(context)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - buslines data successfully get'.format(function_name)
                                  )

        if self.segment['railway']['via_stops']:  # 此路段乘坐火车的信息
            resultContext.append("=============================")
            railway = self.segment['railway']
            context = self.parse_railway_lines(railway)
            resultContext.extend(context)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - railway data successfully get'.format(function_name,
                                                                                                     railway)
                                  )
        return resultContext

    def parse_buslines(self, busline: dict,
                       bus_entrance=None,
                       bus_exit=None
                       ) -> list:
        """
        函数：解析公交数据
        Args:
            busline:此路段公交导航信息列表
            bus_entrance:地铁入口，只在地铁路段有值
            bus_exit:地铁出口，只在地铁路段有值
        """

        self.busLine = busline
        self.bus_entrance = bus_entrance
        self.bus_exit = bus_exit

        # 输出结果
        resultContext = []

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 公交路线的名称，此段起乘站信息，此段下车站信息，公交路线名称，公交类型，公交行驶距离，公交预计行驶时间，
        # 首班车时间，末班车时间，此段途经公交站数，此段途经公交站点列表
        if self.bus_exit is None:
            self.bus_exit = {}
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - bus exit:{0}'.format(function_name,
                                                                                    self.bus_exit)
                                  )

        if self.bus_entrance is None:
            self.bus_entrance = {}
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - bus entrance:{0}'.format(function_name,
                                                                                        self.bus_entrance)
                                  )

        name = self.busLine['name']
        departure_stop = self.busLine['departure_stop']['name']
        arrival_stop = self.busLine['arrival_stop']['name']
        busline_type = self.busLine['type']
        busline_distance = int(self.busLine['distance'])
        busline_duration = str(datetime.timedelta(seconds=int(self.busLine['duration']))).split(":")
        start_time = self.busLine['start_time']
        end_time = self.busLine['end_time']
        via_num = self.busLine['via_num']
        via_stops = self.busLine['via_stops']

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - name:{0}'.format(function_name,
                                                                            name)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - departure stop:{0}'.format(function_name,
                                                                                      departure_stop)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - arrival stop:{0}'.format(function_name,
                                                                                    arrival_stop)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - busline type:{0}'.format(function_name,
                                                                                    busline_type)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - busline distance:{0}'.format(function_name,
                                                                                        busline_distance)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - bus duration:{0}'.format(function_name,
                                                                                    busline_duration)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - start time:{0}'.format(function_name,
                                                                                  start_time)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - end time:{0}'.format(function_name,
                                                                                end_time)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - via num:{0}'.format(function_name,
                                                                               via_num)
                              )

        # 地铁线路路线
        if busline_type == '地铁线路':
            resultContext.append("您将要乘坐的地铁路线为{0}".format(name))
            resultContext.append(
                "该地铁路线的发车时间为{0}时{1}分，末班车时间为{2}时{3}分，请提前规划好您的时间，以免错过末班车。".format(start_time[0:2], start_time[2:4],
                                                                                end_time[0:2], end_time[2:4]))
            resultContext.append("您在该段地铁乘坐路线长度的预计为{0}公里，".format(busline_distance / 1000))
            # TODO:
            # Need to combine

            # 公交乘坐时间
            if busline_duration[1] == '0':  # 在60秒以内
                resultContext.append("预计乘坐{0}秒".format(busline_duration[2]))
            elif busline_duration[0] == '0':  # 在一小时以内
                resultContext.append("预计乘坐{0}分{1}秒".format(busline_duration[1], busline_duration[2]))
            else:
                if busline_duration[1] == '0':
                    resultContext.append("预计乘坐{0}时{1}秒".format(busline_duration[0], busline_duration[2]))
                else:
                    resultContext.append("预计乘坐{0}{0}时{1}分{2}秒".format(busline_duration[0], busline_duration[1],
                                                                      busline_duration[2]))

            resultContext.append("从起点站{0}出发，终点站{1}下车".format(departure_stop, arrival_stop))
            resultContext.append("乘坐路段经过{0}个地铁站".format(via_num))

            # 路线详情
            # 起点站
            if self.bus_entrance:
                resultContext.append("起点站：{0} —— {1}".format(departure_stop, self.bus_entrance['name']))
            else:
                resultContext.append("起点站：{0}".format(departure_stop))

            for item, via_stop in enumerate(via_stops):
                resultContext.append("途径站{0}：{1}".format(item + 1, via_stop['name']))

            # 终点站
            if self.bus_exit:
                resultContext.append("终点站：{0} —— {1}".format(arrival_stop, self.bus_exit['name']))
            else:
                resultContext.append("终点站：{0}".format(arrival_stop))
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - subway data successfully print'.format(function_name)
                                  )

        # 普通公交路线
        elif busline_type == '普通公交线路':
            resultContext.append("您将要乘坐的公交路线为{0}".format(name))
            if start_time:
                resultContext.append(
                    "该公交路线的发车时间为{0}时{1}分，末班车时间为{2}时{3}分，请提前规划好您的行程，以免错过末班车".format(start_time[0:2], start_time[2:4],
                                                                                   end_time[0:2], end_time[2:4]))
            else:
                resultContext.append("该路公交暂无运营时间信息，请注意留意当地路牌指示")
            resultContext.append("您在该段公交乘坐路线长度的预计为{0:.2f}公里，".format(busline_distance / 1000))
            # TODO:Need to combine

            # 公交乘坐时间
            if busline_duration[1] == '0':  # 在60秒以内
                resultContext.append("预计乘坐{0}秒".format(busline_duration[2]))
            elif busline_duration[0] == '0':  # 在一小时以内
                resultContext.append("预计乘坐{0}分{1}秒".format(busline_duration[1], busline_duration[2]))
            else:
                if busline_duration[1] == '0':
                    resultContext.append("预计乘坐{0}时{1}秒".format(busline_duration[0], busline_duration[2]))
                else:
                    resultContext.append("预计乘坐{0}时{1}分{2}秒".format(busline_duration[0], busline_duration[1],
                                                                   busline_duration[2]))

            resultContext.append("从起点站{0}出发".format(departure_stop))
            resultContext.append("乘坐路段经过{0}个公交站".format(via_num))
            for item, via_stop in enumerate(via_stops):
                resultContext.append("途径站{0}：{1}".format(item + 1, via_stop['name']))
            resultContext.append("终点站{0}下车".format(arrival_stop))
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - bus data successfully print'.format(function_name)
                                  )

        return resultContext

    def parse_railway_lines(self, railway: dict
                            ) -> list:
        """
        函数：解析火车路径规划数据
        Args:
            railway:乘坐火车的信息列表
        """

        # TODO:未来版本将返回数据从list升级为dict
        self.railway = railway

        # 输出结果
        resultContext = []

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        railway_time = str(datetime.timedelta(seconds=int(self.railway['time']))).split(":")
        name = self.railway['name']
        trip = self.railway['trip']
        distance = int(self.railway['distance']) / 1000
        railway_type = self.railway['type']
        departure_stop = self.railway['departure_stop']
        arrival_stop = self.railway['arrival_stop']
        via_stops = self.railway['via_stop']
        spaces = self.railway['spaces']

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - railway time:{0}'.format(function_name,
                                                                                    railway_time)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - name:{0}'.format(function_name,
                                                                            name)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - trip:{0}'.format(function_name,
                                                                            trip)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - distance:{0}'.format(function_name,
                                                                                distance)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - railway type:{0}'.format(function_name,
                                                                                    railway_type)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - departure stop:{0}'.format(function_name,
                                                                                      departure_stop)
                              )
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - arrival stop:{0}'.format(function_name,
                                                                                    arrival_stop)
                              )

        # 动车信息
        if railway_type == "D字头的动车火车":
            resultContext.append("您将要乘坐的动车路线为{0}".format(name))
            resultContext.append("动车车次为{0}".format(trip))
            resultContext.append("您将在该动车上预计乘坐{0}小时，该动车预计运行{0}公里".format(railway_time, distance))

            # 价格情况
            resultContext.append("您乘坐的该班次动车一等座票{0}元，二等座票{1}元，无座票{2}元".format(spaces[0]['cost'], spaces[1]['cost'],
                                                                             spaces[2]['cost']))

            # 路线详情
            # 起始站信息
            start = departure_stop['start']
            departure_name = departure_stop['name']
            departure_time = departure_stop['time']

            # 终点站信息
            end = arrival_stop['end']
            arrival_name = arrival_stop['name']
            arrival_time = arrival_stop['time']

            if start:
                resultContext.append("您将从起点站{0}站出发，发车时间是{0}时{1}分，请您合理安排您的行程".format(departure_name, departure_time[0:2],
                                                                                    departure_time[2:4]))
            else:
                resultContext.append("您将从途径站{0}站出发，发车时间是{0}时{1}分，请您合理安排您的行程".format(departure_name, departure_time[0:2],
                                                                                    departure_time[2:4]))

            # 途径站信息
            if via_stops:
                for item, via_stop in enumerate(via_stops):
                    via_stop_name = via_stop['name']
                    via_stop_time = via_stop['time']
                    via_stop_wait = via_stop['wait']
                    resultContext.append("途径站{0}：{1}。进站时间：{2}，停靠时间{3}分钟".format(item + 1, via_stop_name, via_stop_time,
                                                                                via_stop_wait))

            # 终点站信息
            if end:
                resultContext.append(
                    "您将在{0}时{1}分到达动车的终点站{2}站".format(arrival_time[0:2], arrival_time[2:4], arrival_name))
            else:
                resultContext.append(
                    "您将在{0}时{1}分到达本次旅程的终点站{2}站".format(arrival_time[0:2], arrival_time[2:4], arrival_name))

            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - railway data successfully print:{0}'.format(
                                      function_name)
                                  )

        return resultContext

    def get_drive_route_planning(self, origin: str,
                                 destination: str,
                                 **kwargs
                                 ) -> dict:
        """
        函数：获取驾车路径规划数据。\n
        Args:
            origin:出发点，必填。经度在前，纬度在后，经度和纬度用","分割，经纬度小数点后不得超过6位。格式为x1,y1|x2,y2|x3,y3。由于在实际使用过程中，存在定位飘点的情况。为了解决此类问题，允许传入多个起
                    点用于计算车头角度。最多允许传入3个坐标对，每对坐标之间距离必须超过2m。 虽然对每对坐标之间长度没有上限，但是如果超过4米会有概率性出现不准确的情况。使用三个点来判断距离和角度的有效性，如果两者都有
                    效，使用第一个点和最后一个点计算的角度设置抓路的角度，规划路径时以最后一个坐标对进行规划。
            destination:目的地，必填。经度在前，纬度在后，经度和纬度用","分割，经纬度小数点后不得超过6位。
            kwargs:
                extensions:返回结果控制，必填，默认base。可选值：base/all。base:返回基本信息；all：返回全部信息。
                originId:出发点poiId，选填。当起点为POI时，建议填充此值。
                destinationId:目的地poiId，选填。当终点为POI时，建议填充此值。
                originType:起点的poi类别，选填。当用户知道起点POI的类别时候，建议填充此值。
                destinationType:终点的poi类别，选填。当用户知道终点POI的类别时候，建议填充此值。
                strategy:驾车选择策略，选填，默认10。返回结果会躲避拥堵，路程较短，尽量缩短时间，与高德地图的默认策略也就是不进行任何勾选一致。
                        下方10~20的策略，会返回多条路径规划结果。下方策略 0~9的策略，仅会返回一条路径规划结果。
                        下方策略返回多条路径规划结果
                            10，返回结果会躲避拥堵，路程较短，尽量缩短时间，与高德地图的默认策略也就是不进行任何勾选一致
                            11，返回三个结果包含：时间最短；距离最短；躲避拥堵 （由于有更优秀的算法，建议用10代替）
                            12，返回的结果考虑路况，尽量躲避拥堵而规划路径，与高德地图的“躲避拥堵”策略一致
                            13，返回的结果不走高速，与高德地图“不走高速”策略一致
                            14，返回的结果尽可能规划收费较低甚至免费的路径，与高德地图“避免收费”策略一致
                            15，返回的结果考虑路况，尽量躲避拥堵而规划路径，并且不走高速，与高德地图的“躲避拥堵&不走高速”策略一致
                            16，返回的结果尽量不走高速，并且尽量规划收费较低甚至免费的路径结果，与高德地图的“避免收费&不走高速”策略一致
                            17，返回路径规划结果会尽量的躲避拥堵，并且规划收费较低甚至免费的路径结果，与高德地图的“躲避拥堵&避免收费”策略一致
                            18，返回的结果尽量躲避拥堵，规划收费较低甚至免费的路径结果，并且尽量不走高速路，与高德地图的“避免拥堵&避免收费&不走高速”策略一致
                            19，返回的结果会优先选择高速路，与高德地图的“高速优先”策略一致
                            20，返回的结果会优先考虑高速路，并且会考虑路况躲避拥堵，与高德地图的“躲避拥堵&高速优先”策略一致
                        下方策略仅返回一条路径规划结果
                            0，速度优先，不考虑当时路况，此路线不一定距离最短
                            1，费用优先，不走收费路段，且耗时最少的路线
                            2，距离优先，不考虑路况，仅走距离最短的路线，但是可能存在穿越小路/小区的情况
                            3，速度优先，不走快速路，例如京通快速路（因为策略迭代，建议使用13）
                            4，躲避拥堵，但是可能会存在绕路的情况，耗时可能较长
                            5，多策略（同时使用速度优先、费用优先、距离优先三个策略计算路径）。
                        其中必须说明，就算使用三个策略算路，会根据路况不固定的返回一到三条路径规划信息。
                            6，速度优先，不走高速，但是不排除走其余收费路段
                            7，费用优先，不走高速且避免所有收费路段
                            8，躲避拥堵和收费，可能存在走高速的情况，并且考虑路况不走拥堵路线，但有可能存在绕路和时间较长
                            9，躲避拥堵和收费，不走高速
                waypoints:途经点，选填。经度和纬度用","分割，经度在前，纬度在后，小数点后不超过6位，坐标点之间用";"分隔最大数目：16个坐标点。如果输入多个途径点，则按照用户输入的顺序进行路径规划。
                avoidPolygons:避让区域，选填。区域避让，支持32个避让区域，每个区域最多可有16个顶点经度和纬度用","分割，经度在前，纬度在后，小数点后不超过6位，坐标点之间用";"分隔，区域之间用"|"分隔。如果是四边形则有四个坐标点，如果是五边形则有五个坐标点；同时传入避让区域及避让道路，仅支持避让道路；避让区域不能超过81平方公里，否则避让区域会失效。
                avoidRoad:避让道路名，选填。只支持一条避让道路。
                province:用汉字填入车牌省份缩写，用于判断是否限行，选填。例如：京
                number:填入除省份及标点之外，车牌的字母和数字（需大写），选填。用于判断限行相关，选填。例如:NH1N11，支持6位传统车牌和7位新能源车牌。
                carType:车辆类型，选填，默认普通汽车。0：普通汽车(默认值)；1：纯电动车；2：插电混动车。
                ferry:在路径规划中，是否使用轮渡，选填，默认使用渡轮。0:使用渡轮(默认) ，1:不使用渡轮。
                roadAggregation:是否返回路径聚合信息，选填，默认false。false:不返回路径聚合信息，true:返回路径聚合信息，在steps上层增加roads做聚合
                noSteps:是否返回steps字段内容，选填，默认0。当取值为0时，steps字段内容正常返回；当取值为1时，steps字段内容为空。
                output:返回数据格式类型，选填，默认JSON格式。可选值：JSON，XML。
        Returns:返回获得的json格式数据或错误信息
        """

        self.destination = destination
        self.origin = origin

        if 'avoidPolygons' in kwargs:
            self.avoidPolygons = kwargs['avoidPolygons']
        if 'avoidRoad' in kwargs:
            self.avoidRoad = kwargs['avoidRoad']
        if 'carType' in kwargs:
            self.carType = kwargs['carType']
        if 'destinationId' in kwargs:
            self.destinationId = kwargs['destinationId']
        if 'destinationType' in kwargs:
            self.destinationType = kwargs['destinationType']
        if 'extensions' in kwargs:
            self.extensions = kwargs['extensions']
        if 'ferry' in kwargs:
            self.ferry = kwargs['ferry']
        if 'noSteps' in kwargs:
            self.noSteps = kwargs['noSteps']
        if 'number' in kwargs:
            self.number = kwargs['number']
        if 'originId' in kwargs:
            self.originId = kwargs['originId']
        if 'originType' in kwargs:
            self.originType = kwargs['originType']
        if 'output' in kwargs:
            self.output = kwargs['output']
        if 'province' in kwargs:
            self.province = kwargs['province']
        if 'roadAggregation' in kwargs:
            self.roadAggregation = kwargs['roadAggregation']
        if 'strategy' in kwargs:
            self.strategy = kwargs['strategy']
        else:
            self.strategy = 10
        if 'waypoints' in kwargs:
            self.waypoints = kwargs['waypoints']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': self.APIkey,
                      'origin': self.origin,
                      'destination': self.destination,
                      }

        if self.avoidPolygons is not None:
            parameters.update(avoidpolygons=self.avoidPolygons)
        if self.avoidRoad is not None:
            parameters.update(avoidroad=self.avoidRoad)
        if self.carType is not None:
            parameters.update(cartype=self.carType)
        if self.destinationId is not None:
            parameters.update(destinationid=self.destinationId)
        if self.destinationType is not None:
            parameters.update(destinationtype=self.destinationType)
        if self.extensions is not None:
            parameters.update(extensions=self.extensions)
        if self.ferry is not None:
            parameters.update(ferry=self.ferry)
        if self.noSteps is not None:
            parameters.update(nosteps=self.noSteps)
        if self.number is not None:
            parameters.update(number=self.number)
        if self.originId is not None:
            parameters.update(originid=self.originId)
        if self.originType is not None:
            parameters.update(origintype=self.originType)
        if self.output is not None:
            parameters.update(output=self.output)
        if self.province is not None:
            parameters.update(province=self.province)
        if self.roadAggregation is not None:
            parameters.update(roadaggregation=self.roadAggregation)
        if self.strategy is not None:
            parameters.update(strategy=self.strategy)
        if self.waypoints is not None:
            parameters.update(waypoints=self.waypoints)

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/direction/driving?parameters",
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
                                  context='Function name:{0} - Drive route data successful get.'.format(
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

    def parse_drive_route_planning(self, json_decode: dict
                                   ) -> list:
        """
        函数：解析驾驶路径规划数据。\n
        Args:
            json_decode:get_drive_route_planning()方法从网络中获取的数据
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
                if self.json_decode['infocode'] == "10000":
                    # 请求数据成功的状态码
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=6,
                                          context='Function name:{0} - infocode:{1}'.format(function_name,
                                                                                            self.json_decode[
                                                                                                'infocode'])
                                          )
                    # 驾车路径规划方案数目
                    drive_count = self.json_decode["count"]
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - drive count:{1}'.format(function_name,
                                                                                               drive_count)
                                          )
                    resultContext.append("您选择的是驾驶规划，已为您智能生成如下{0}种出行方案".format(drive_count))
                    resultContext.append("=========================================================")
                    paths = self.json_decode['route']['paths']
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=6,
                                          context='Function name:{0} - paths data successfully parsed.'.format(
                                              function_name)
                                          )

                    for item, path in enumerate(paths):
                        strategy = path['strategy']
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - strategy:{1}'.format(function_name,
                                                                                                strategy)
                                              )
                        resultContext.append("方案{0}是{1}的方案".format(item + 1, strategy))
                        resultContext.append("出行规划如下所示：")

                        # 步数
                        steps = path['steps']
                        len_steps = len(steps)
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - steps length:{1}'.format(function_name,
                                                                                                    len_steps)
                                              )
                        resultContext.append("出行方案{0}共{1}步".format(item + 1, len_steps))

                        # 路径规划收费情况
                        tolls = path['tolls']
                        toll_distance = path['toll_distance']
                        traffic_lights = path['traffic_lights']
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - tolls:{1}'.format(function_name,
                                                                                             tolls)
                                              )
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - toll_distance:{1}'.format(function_name,
                                                                                                     toll_distance)
                                              )
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - traffic_lights:{1}'.format(function_name,
                                                                                                      traffic_lights)
                                              )

                        # 不计费路段
                        if tolls == "0":
                            resultContext.append("此次路线规划已使用免费无高速方案")
                        else:
                            resultContext.append("此次路线规划已使用途径高速方案，预计收费{0}元，收费路段长度为{1:.1f}公里".format(
                                tolls, int(toll_distance) / 1000))

                        # 路径红绿灯个数情况
                        resultContext.append("此次导航中会经过{0}个红绿灯".format(traffic_lights))

                        # 详细路线内容
                        for sub_item, step in enumerate(steps):
                            information = step['instruction']
                            # only for debugging
                            writeLog.write_to_log(file_name=log_filename,
                                                  log_level=1,
                                                  context='Function name:{0} - instruction:{1}'.format(function_name,
                                                                                                       information)
                                                  )
                            resultContext.append("第{0}步：{1}".format(sub_item + 1, information))
                        resultContext.append("导航结束")
                        resultContext.append("=========================================================")
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=6,
                                          context='Function name:{0} - drive data successfully print.'.format(
                                              function_name)
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

            # 异常信息
            resultContext.append(errorInfo)
            context = "驾驶导航查询失败，换个词进行搜索吧"
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

            # 异常信息
            context = "驾驶导航查询失败，换个词进行搜索吧"
            resultContext.append(context)
            return resultContext

    def get_ride_route_planning(self, origin: str,
                                destination: str
                                ) -> dict:
        """
        函数：获取骑行路径规划数据。\n
        Args:
            origin:出发点经纬度，必填。填入规则：X,Y，采用","分隔，例如“ 117.500244, 40.417801 ”，小数点后不得超过6位
            destination:目的地经纬度，必填。填入规则：X,Y，采用","分隔，例如“ 117.500244, 40.417801 ”，小数点后不得超过6位
        Returns:返回获得的json格式数据或错误信息
        """

        self.destination = destination
        self.origin = origin

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': self.APIkey,
                      'origin': self.origin,
                      'destination': self.destination
                      }

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v4/direction/bicycling?parameters",
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
                                  context='Function name:{0} - Ride route data successful get.'.format(
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

    def parse_ride_route_planning(self, json_decode: dict
                                  ) -> list:
        """
        函数：解析骑行路径规划数据。\n
        Args:
            json_decode:get_ride_route_planning()方法从网络中获取的数据
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
            if 'errcode' not in self.json_decode:
                if self.json_decode['status'] == '0':
                    # 官方文档异常
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - status:{1}'.format(function_name,
                                                                                          self.json_decode['status'])
                                          )
                    raise OfficialException

                elif self.json_decode['status'] == '2':
                    # 自定义异常
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - status:{1}'.format(function_name,
                                                                                          self.json_decode['status'])
                                          )
                    raise CustomExpection

            elif self.json_decode['errcode'] == 0:  # 请求数据成功的状态码
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=6,
                                      context='Function name:{0} - errcode:{1},not error'.format(function_name,
                                                                                                 self.json_decode[
                                                                                                     'errcode'])
                                      )
                # 骑行方案列表信息
                paths = self.json_decode['data']['paths']
                len_paths = len(paths)
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=1,
                                      context='Function name:{0} - paths length:{1}'.format(function_name,
                                                                                            len_paths)
                                      )
                resultContext.append("已为您智能生成{0}种骑行方案".format(len_paths))

                for path in paths:
                    steps = path['steps']
                    len_steps = len(steps)
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=1,
                                          context='Function name:{0} - steps length:{1}'.format(function_name,
                                                                                                len_steps)
                                          )
                    resultContext.append("本次路径规划共分为{0}步".format(len_steps))

                    for sub_item, step in enumerate(steps):
                        instruction = step['instruction']
                        # only for debugging
                        writeLog.write_to_log(file_name=log_filename,
                                              log_level=1,
                                              context='Function name:{0} - instruction:{1}'.format(
                                                  function_name,
                                                  instruction)
                                              )
                        resultContext.append("第{0}步：{1}".format(sub_item + 1, instruction))
                    resultContext.append("骑行导航结束")
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
            # 异常信息
            resultContext.append(errorInfo)
            context = "骑行导航查询失败，换个词进行搜索吧"
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

            # 异常信息
            context = "骑行导航查询失败，换个词进行搜索吧"
            resultContext.append(context)
            return resultContext
