import inspect

from AmapFunctions.GeographicCoding import GeographicCoding
from AmapFunctions.RoutePlanning import RoutePlanning
from logrecord.WriteLog import WriteLog


class WalkingRoutePlanningOperation:
    """
    Class：步行路径规划操作
    """
    def __init__(self):
        self.walkingDepartureAddress = None
        self.walkingDestinationAddress = None
        self.walkingDepartureCity = None
        self.walkingDestinationCity = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    def check_walking_departure_information(self, walkingDepartureAddress: str,
                                            ) -> int:
        """
        函数：检测用户提供的步行路径出发点是否符合规范要求
        Args:
            walkingDepartureAddress: 用户输入的出发点
        Returns:
            检测类型识别码
        """

        self.walkingDepartureAddress = walkingDepartureAddress

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 检测结果
        checkedResult = self.walkingDepartureAddress is None or self.walkingDepartureAddress == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - walking departure address check result:{1}'.format(
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

    def check_walking_destination_information(self, walkingDestinationAddress: str
                                              ) -> int:
        """
        函数：检测用户提供的步行路径终点是否符合规范要求
        Args:
            walkingDestinationAddress: 用户输入的终点
        Returns:
            检测类型识别码
        """

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        self.walkingDestinationAddress = walkingDestinationAddress

        # 检测结果
        checkedResult = self.walkingDestinationAddress is None or self.walkingDestinationAddress == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - walking destination address check result:{1}'.format(
                                  function_name,
                                  checkedResult)
                              )

        if checkedResult:
            return 2
        # TODO:
        # 检测用户提供的步行路径出发点是否符合规范要求
        # 此处检测格式错误返回false
        else:
            return True

    def get_walking_route_planning_information(self, walkingDepartureAddress: str,
                                               walkingDestinationAddress: str,
                                               walkingDepartureCity: str = '',
                                               walkingDestinationCity: str = ''
                                               ) -> list:
        """
        函数：获取步行路径规划的具体信息
        Args:
            walkingDepartureAddress: 用户输入的出发点
            walkingDestinationAddress: 用户输入的终点
            walkingDepartureCity: 用户输入的出发点对应的城市
            walkingDestinationCity: 用户输入的终点对应的城市
        Returns:
            返回获取的步行路径规划对应的具体信息
        """

        # TODO:未来版本将返回数据从str升级为dict
        self.walkingDepartureAddress = walkingDepartureAddress
        self.walkingDestinationAddress = walkingDestinationAddress
        # 在以后的版本中添加
        self.walkingDepartureCity = walkingDepartureCity
        self.walkingDestinationCity = walkingDestinationCity

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 步行路径规划
        geographicCoding = GeographicCoding()
        # 获取起点终点对应的初始编码信息
        # TODO:优化city参数
        walkingDepartureJsonDecode = geographicCoding.get_geographic_coding(address=self.walkingDepartureAddress,
                                                                            city='')
        walkingDestinationJsonDecode = geographicCoding.get_geographic_coding(address=self.walkingDestinationAddress,
                                                                              city='')

        parseWalkingDepartureInformation = geographicCoding.parse_geographic_coding(walkingDepartureJsonDecode)
        parseWalkingDestinationInformation = geographicCoding.parse_geographic_coding(walkingDestinationJsonDecode)

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - walking departure information:{1}'.format(function_name,
                                                                                                     parseWalkingDepartureInformation)
                              )

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - walking destination information:{1}'.format(function_name,
                                                                                                       parseWalkingDestinationInformation)
                              )

        # 起点位置编码
        if 'error_context' not in parseWalkingDepartureInformation:
            resultDepartureGeographicCoding = parseWalkingDepartureInformation['geographic_position']
        else:
            return [parseWalkingDepartureInformation['error_context']]

        # 终点位置编码
        if 'error_context' not in parseWalkingDestinationInformation:
            resultDestinationGeographicCoding = parseWalkingDestinationInformation['geographic_position']
        else:
            return [parseWalkingDestinationInformation['error_context']]

        routePlanning = RoutePlanning()
        walkingRoutePlanning = routePlanning.get_walking_route_planning(origin=resultDepartureGeographicCoding,
                                                                        destination=resultDestinationGeographicCoding)

        # 解析路径规划信息
        resultWalkingRoutePlanning = routePlanning.parse_walking_route_planning(walkingRoutePlanning)
        promptInformation = "从{0}到{1}的步行导航信息如下所示".format(self.walkingDepartureAddress, self.walkingDestinationAddress)
        resultWalkingRoutePlanning.insert(0, promptInformation)
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - result walking route planning:{1}'.format(function_name,
                                                                                                     resultWalkingRoutePlanning)
                              )

        return resultWalkingRoutePlanning
