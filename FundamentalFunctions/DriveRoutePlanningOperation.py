import inspect

from AmapFunctions.GeographicCoding import GeographicCoding
from AmapFunctions.RoutePlanning import RoutePlanning
from logrecord.WriteLog import WriteLog


class DriveRoutePlanningOperation:
    """
    Class:驾驶路径规划操作
    """
    def __init__(self):
        self.driveDepartureAddress = None
        self.driveDestinationAddress = None
        self.driveDepartureCity = None
        self.driveDestinationCity = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    def check_drive_departure_information(self, driveDepartureAddress: str,
                                          ) -> int:
        """
        函数：检测用户提供的驾驶路径出发点是否符合规范要求
        Args:
            driveDepartureAddress: 用户输入的出发点
        Returns:
            检测类型识别码
        """

        self.driveDepartureAddress = driveDepartureAddress

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 检查结果
        checkedResult = self.driveDepartureAddress is None or self.driveDepartureAddress == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - drive departure address check result:{1}'.format(
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

    def check_drive_destination_information(self, driveDestinationAddress: str
                                            ) -> int:
        """
        函数：检测用户提供的步行路径终点是否符合规范要求
        Args:
            driveDestinationAddress: 用户输入的终点
        Returns:
            检测类型识别码
        """

        self.driveDestinationAddress = driveDestinationAddress

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 检查结果
        checkedResult = self.driveDestinationAddress is None or self.driveDestinationAddress == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - drive destination address check result:{1}'.format(
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

    def get_drive_route_planning_information(self, driveDepartureAddress: str,
                                             driveDestinationAddress: str,
                                             driveDepartureCity: str = '',
                                             driveDestinationCity: str = ''
                                             ) -> list:
        """
        函数：获取驾驶路径规划的具体信息
        Args:
            driveDepartureAddress: 用户输入的出发点
            driveDestinationAddress: 用户输入的终点
            driveDepartureCity: 用户输入的出发点对应的城市
            driveDestinationCity: 用户输入的终点对应的城市
        Returns:
            返回获取的驾驶路径规划对应的具体信息
        """

        # TODO:未来版本将返回数据从list升级为dict
        self.driveDepartureAddress = driveDepartureAddress
        self.driveDestinationAddress = driveDestinationAddress
        # 在以后的版本中添加
        self.driveDepartureCity = driveDepartureCity
        self.driveDestinationCity = driveDestinationCity

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 驾驶路径规划
        geographicCoding = GeographicCoding()
        # 获取起点终点对应的初始编码信息
        # TODO:优化city参数
        driveDepartureJsonDecode = geographicCoding.get_geographic_coding(address=self.driveDepartureAddress,
                                                                          city='')
        driveDestinationJsonDecode = geographicCoding.get_geographic_coding(address=self.driveDestinationAddress,
                                                                            city='')

        parseDriveDepartureInformation = geographicCoding.parse_geographic_coding(driveDepartureJsonDecode)
        parseDriveDestinationInformation = geographicCoding.parse_geographic_coding(driveDestinationJsonDecode)

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - drive departure information:{1}'.format(function_name,
                                                                                                   parseDriveDepartureInformation)
                              )

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - drive destination information:{1}'.format(function_name,
                                                                                                     parseDriveDestinationInformation)
                              )

        # 起点位置编码
        if 'error_context' not in parseDriveDepartureInformation:
            resultDepartureGeographicCoding = parseDriveDepartureInformation['geographic_position']
        else:
            return [parseDriveDepartureInformation['error_context']]

        # 终点位置编码
        if 'error_context' not in parseDriveDestinationInformation:
            resultDestinationGeographicCoding = parseDriveDestinationInformation['geographic_position']
        else:
            return [parseDriveDestinationInformation['error_context']]

        # TODO: 未来将strategy和extensions放入设置选项中
        routePlanning = RoutePlanning()
        driveRoutePlanning = routePlanning.get_drive_route_planning(origin=resultDepartureGeographicCoding,
                                                                    destination=resultDestinationGeographicCoding,
                                                                    strategy=10,
                                                                    extensions='base')

        # 获取内容
        resultDriveRoutePlanning = routePlanning.parse_drive_route_planning(driveRoutePlanning)
        promptInformation = "从{0}到{1}的驾驶导航信息如下所示".format(self.driveDepartureAddress, self.driveDestinationAddress)
        resultDriveRoutePlanning.insert(0, promptInformation)
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - result drive route planning:{1}'.format(function_name,
                                                                                                   resultDriveRoutePlanning)
                              )

        return resultDriveRoutePlanning
