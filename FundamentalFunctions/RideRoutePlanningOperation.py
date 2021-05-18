import inspect

from AmapFunctions.GeographicCoding import GeographicCoding
from AmapFunctions.RoutePlanning import RoutePlanning
from logrecord.WriteLog import WriteLog


class RideRoutePlanningOperation:
    """
    Class:骑行路径规划操作
    """
    def __init__(self):
        self.rideDepartureAddress = None
        self.rideDestinationAddress = None
        self.rideDepartureCity = None
        self.rideDestinationCity = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    def check_ride_departure_information(self, rideDepartureAddress: str,
                                         ) -> int:
        """
        函数：检测用户提供的骑行路径出发点是否符合规范要求
        Args:
            rideDepartureAddress: 用户输入的出发点
        Returns:
            检测类型识别码
        """

        self.rideDepartureAddress = rideDepartureAddress

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        checkedResult = self.rideDepartureAddress is None or self.rideDepartureAddress == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - ride departure address information :{1}'.format(
                                  function_name,
                                  checkedResult)
                              )

        if checkedResult:
            return 2
        # TODO:
        # 使用python正则表达式验证用户名格式
        # 此处检测格式错误返回false
        else:
            return True

    def check_ride_destination_information(self, rideDestinationAddress: str
                                           ) -> int:
        """
        函数：检测用户提供的骑行路径终点是否符合规范要求
        Args:
            rideDestinationAddress: 用户输入的终点
        Returns:
            检测类型识别码
        """

        self.rideDestinationAddress = rideDestinationAddress

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 检测结果
        checkedResult = self.rideDestinationAddress is None or self.rideDestinationAddress == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - ride destination address information :{1}'.format(
                                  function_name,
                                  checkedResult)
                              )

        if checkedResult:
            return 2
        # TODO:
        # 检测用户提供的骑行路径出发点是否符合规范要求
        # 此处检测格式错误返回false
        else:
            return True

    def get_ride_route_planning_information(self, rideDepartureAddress: str,
                                            rideDestinationAddress: str,
                                            rideDepartureCity: str = '',
                                            rideDestinationCity: str = ''
                                            ) -> list:
        """
        函数：获取骑行路径规划的具体信息
        Args:
            rideDepartureAddress: 用户输入的出发点
            rideDestinationAddress: 用户输入的终点
            rideDepartureCity: 用户输入的出发点对应的城市
            rideDestinationCity: 用户输入的终点对应的城市
        Returns:
            返回获取的骑行路径规划对应的具体信息
        """

        # TODO:未来版本将返回数据从list升级为dict
        self.rideDepartureAddress = rideDepartureAddress
        self.rideDestinationAddress = rideDestinationAddress
        # 在以后的版本中添加
        self.rideDepartureCity = rideDepartureCity
        self.rideDestinationCity = rideDestinationCity

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 骑行路径规划
        geographicCoding = GeographicCoding()
        # 获取起点终点对应的初始编码信息
        # TODO:优化city参数
        rideDepartureJsonDecode = geographicCoding.get_geographic_coding(address=self.rideDepartureAddress,
                                                                         city='')
        rideDestinationJsonDecode = geographicCoding.get_geographic_coding(address=self.rideDestinationAddress,
                                                                           city='')

        parseRideDepartureInformation = geographicCoding.parse_geographic_coding(rideDepartureJsonDecode)
        parseRideDestinationInformation = geographicCoding.parse_geographic_coding(rideDestinationJsonDecode)

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - ride departure information:{1}'.format(function_name,
                                                                                                  parseRideDepartureInformation)
                              )

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - ride destination information:{1}'.format(function_name,
                                                                                                    parseRideDestinationInformation)
                              )

        # 起点终点位置编码
        if 'error_context' not in parseRideDepartureInformation:
            resultDepartureGeographicCoding = parseRideDepartureInformation['geographic_position']
        else:
            return [parseRideDepartureInformation['error_context']]
        if 'error_context' not in parseRideDestinationInformation:
            resultDestinationGeographicCoding = parseRideDestinationInformation['geographic_position']
        else:
            return [parseRideDestinationInformation['error_context']]

        routePlanning = RoutePlanning()
        rideRoutePlanning = routePlanning.get_ride_route_planning(origin=resultDepartureGeographicCoding,
                                                                  destination=resultDestinationGeographicCoding)
        # only for debugging
        # print("详细信息")
        # print(walkingRoutePlanning)

        # 输出路径规划信息
        resultRideRoutePlanning = routePlanning.parse_ride_route_planning(rideRoutePlanning)
        promptInformation = "从{0}到{1}的骑行导航信息如下所示".format(self.rideDepartureAddress, self.rideDestinationAddress)
        resultRideRoutePlanning.insert(0, promptInformation)
        return resultRideRoutePlanning
