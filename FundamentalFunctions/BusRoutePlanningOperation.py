import inspect

from AmapFunctions.GeographicCoding import GeographicCoding
from AmapFunctions.RoutePlanning import RoutePlanning
from logrecord.WriteLog import WriteLog


class BusRoutePlanningOperation:
    """
    Class:公交路径查询规划操作
    """
    def __init__(self):
        self.busDepartureAddress = None
        self.busDestinationAddress = None
        self.busDepartureCity = None
        self.busDestinationCity = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    def check_bus_departure_information(self, busDepartureAddress: str
                                        ) -> int:
        """
        函数：检测用户提供的公交路径出发点是否符合规范要求
        Args:
            busDepartureAddress: 用户输入的出发点
        Returns:
            检测类型识别码
        """

        self.busDepartureAddress = busDepartureAddress

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 检查结果
        checkedResult = self.busDepartureAddress is None or self.busDepartureAddress == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - bus departure address check result:{1}'.format(function_name,
                                                                                                          checkedResult)
                              )

        if checkedResult:
            return 2
        # TODO:
        # 使用python正则表达式验证提供的公交路径出发点是否符合规范要求
        # 此处检测格式错误返回false
        else:
            return True

    def check_bus_destination_information(self, busDestinationAddress: str
                                          ) -> int:
        """
        函数：检测用户提供的公交路径终点是否符合规范要求
        Args:
            busDestinationAddress: 用户输入的终点
        Returns:
            检测类型识别码
        """

        self.busDestinationAddress = busDestinationAddress

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 检查结果
        checkedResult = self.busDestinationAddress is None or self.busDestinationAddress == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - bus destination address check result:{1}'.format(
                                  function_name,
                                  checkedResult)
                              )

        if checkedResult:
            return 2
        # TODO:
        # 检测用户提供的公交路径出发点是否符合规范要求
        # 此处检测格式错误返回false
        else:
            return True

    def get_bus_route_planning_information(self, busDepartureAddress: str,
                                           busDestinationAddress: str,
                                           busDepartureCity: str = '',
                                           busDestinationCity: str = ''
                                           ) -> list:
        """
        函数：获取公交路径规划的具体信息
        Args:
            busDepartureAddress: 用户输入的出发点
            busDestinationAddress: 用户输入的终点
            busDepartureCity: 用户输入的出发点对应的城市
            busDestinationCity: 用户输入的终点对应的城市
        Returns:
            返回获取的步行路径规划对应的具体信息
        """

        # TODO:未来版本将返回数据从list升级为dict

        self.busDepartureAddress = busDepartureAddress
        self.busDestinationAddress = busDestinationAddress
        # 在以后的版本中添加
        self.busDepartureCity = busDepartureCity
        self.busDestinationCity = busDestinationCity

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 公交路径规划
        geographicCoding = GeographicCoding()
        # 获取起点终点对应的初始编码信息
        # TODO:优化city参数
        busDepartureJsonDecode = geographicCoding.get_geographic_coding(address=self.busDepartureAddress,
                                                                        city='')
        busDestinationJsonDecode = geographicCoding.get_geographic_coding(address=self.busDestinationAddress,
                                                                          city='')

        parseBusDepartureInformation = geographicCoding.parse_geographic_coding(busDepartureJsonDecode)
        parseBusDestinationInformation = geographicCoding.parse_geographic_coding(busDestinationJsonDecode)

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - bus departure information:{1}'.format(function_name,
                                                                                                 parseBusDepartureInformation)
                              )

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - bus destination information:{1}'.format(function_name,
                                                                                                   parseBusDestinationInformation)
                              )

        # 起点位置编码
        if 'error_context' not in parseBusDepartureInformation:
            resultDepartureGeographicCoding = parseBusDepartureInformation['geographic_position']
        else:
            return [parseBusDepartureInformation['error_context']]

        # 终点位置编码
        if 'error_context' not in parseBusDestinationInformation:
            resultDestinationGeographicCoding = parseBusDestinationInformation['geographic_position']
        else:
            return [parseBusDestinationInformation['error_context']]

        # 起点对应的城市
        resultDepartureCity = parseBusDepartureInformation['geographic_city']

        routePlanning = RoutePlanning()
        busRoutePlanning = routePlanning.get_bus_route_planning(origin=resultDepartureGeographicCoding,
                                                                destination=resultDestinationGeographicCoding,
                                                                city=resultDepartureCity
                                                                )

        # 输出路径规划信息
        resultBusRoutePlanning = routePlanning.parse_bus_route_planning(busRoutePlanning)
        promptInformation = "从{0}到{1}的步行导航信息如下所示".format(self.busDepartureAddress, self.busDestinationAddress)
        resultBusRoutePlanning.insert(0, promptInformation)
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - result bus route planning:{1}'.format(function_name,
                                                                                                 resultBusRoutePlanning)
                              )

        return resultBusRoutePlanning
