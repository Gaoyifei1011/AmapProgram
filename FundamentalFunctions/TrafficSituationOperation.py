import inspect

# from math import cos, sin, atan2, sqrt, radians, degrees
# from AmapFunctions.GeographicCoding import GeographicCoding
from AmapFunctions.TrafficSituationByBaiduMap import TrafficSituationByBaiduMap
from logrecord.WriteLog import WriteLog


class TrafficSituationOperation:
    """
    Class:交通信息执具体操作
    """
    def __init__(self):
        self.city = None
        self.roadName = None
        self.position = None
        self.bounds = None
        self.geographicLocations = None
        self.geographicPositionBottomLeft = None
        self.geographicPositionTopRight = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    def check_real_road_information(self, roadName: str
                                    ) -> int:
        """
        函数：检测用户提供的道路名称是否符合规范要求
        Args:
            roadName: 用户输入的道路名称
        Returns:
            检测类型识别码
        """

        self.roadName = roadName

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        checkedResult = self.roadName is None or self.roadName == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - traffic real road check result:{1}'.format(function_name,
                                                                                                      checkedResult)
                              )

        if checkedResult:
            return 2
        # TODO:
        # 使用python正则表达式验证用户名格式
        # 此处检测格式错误返回false
        else:
            return True

    # 这里有一些异常发生，将在未来的某一个版本进行修复
    # There are some exceptions occurring here that will be fixed in a future release
    # def checkRectanglePositionInformation(self, position: str):
    #     """
    #     函数：检测用户提供的地理位置是否符合规范要求
    #     Args:
    #         position: 用户输入的地理位置
    #     Returns:
    #         检测类型识别码
    #     """
    #
    #     self.position = position
    #
    #     if self.position is None or self.position == '':
    #         return 2
    #     # TODO:
    #     # 使用python正则表达式验证用户名格式
    #     # 此处检测格式错误返回false
    #     else:
    #         return True

    def check_rectangle_road_information(self, bounds: str
                                         ) -> int:
        """
        函数：检测用户提供的矩形区域的位置是否符合规范要求
        Args:
            bounds: 矩形区域的地理位置
        Returns:
            检测类型识别码
        """

        self.bounds = bounds

        if self.bounds is None or self.bounds == '':
            return 2
        # TODO:
        # 使用python正则表达式bounds格式是否正确
        # 此处检测格式错误返回false
        else:
            return True

    def get_traffic_situation_real_road_information(self, city: str,
                                                    roadName: str
                                                    ) -> list:
        """
        函数：获取输入的道路名称对应的具体路况信息
        Args:
            city:城市名称
            roadName:道路名称
        Returns:
            返回输入的道路名称对应的具体路况信息
        """

        # TODO:未来版本将返回数据从str升级为dict
        self.city = city
        self.roadName = roadName

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        trafficSituation = TrafficSituationByBaiduMap()
        # 获取到的交通态势原信息（未解析）
        resultTrafficRealRoadInformation = trafficSituation.get_traffic_situation_by_road(city=self.city,
                                                                                          road_name=roadName)
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - resultTrafficRealRoadInformation:{1}'.format(function_name,
                                                                                                        resultTrafficRealRoadInformation)
                              )

        # 对获取的数据进行解析
        resultTrafficRealRoadDetailInformation = trafficSituation.parse_traffic_situation(
            resultTrafficRealRoadInformation)
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - resultTrafficRealRoadDetailInformation:{1}'.format(
                                  function_name,
                                  resultTrafficRealRoadDetailInformation)
                              )

        return resultTrafficRealRoadDetailInformation

    # def getCenterGeographicPosition(self, geographicLocations: list):
    #     """
    #     函数：获取多边形地理坐标的中心点
    #     Args:
    #         geographicLocations:用户输入的多个地理位置
    #     Returns:
    #         中心点对应的地理位置
    #     """
    #
    #     self.geographicLocations = geographicLocations
    #
    #     x = 0
    #     y = 0
    #     z = 0
    #     length = len(self.geographicLocations)
    #
    #     for lon, lat in self.geographicLocations:
    #         lon = radians(float(lon))
    #         lat = radians(float(lat))
    #         x += cos(lat) * cos(lon)
    #         y += cos(lat) * sin(lon)
    #         z += sin(lat)
    #
    #     x = float(x / length)
    #     y = float(y / length)
    #     z = float(z / length)
    #
    #     return degrees(atan2(y, x)), degrees(atan2(z, sqrt(x * x + y * y)))
    #
    # def getGeographicCodingPosition(self, position: str
    #                                 ) -> str:
    #     """
    #     函数：获取中文名称地点对应的地理位置信息（高德地图）
    #     Args:
    #         position: 中文位置名称
    #     Returns: 高德地图对应地点地理位置信息
    #     """
    #
    #     self.position = position
    #
    #     geographicCoding = GeographicCoding()
    #     positionJsonDecode = geographicCoding.get_geographic_coding(address=self.position,
    #                                                                 city='')
    #     parsePositionInformation = geographicCoding.parse_geographic_coding(positionJsonDecode)
    #
    #     # 地理位置编码
    #     if 'error_context' not in parsePositionInformation:
    #         resultPositionGeographicCoding = parsePositionInformation['geographic_position']
    #         return resultPositionGeographicCoding
    #
    #     else:
    #         return "1"

    # 这里有一些异常发生，将在未来的某一个版本进行修复
    # There are some exceptions occurring here that will be fixed in a future release
    # def getTrafficSituationRectangleRoadInformation(self, geographicPositionBottomLeft: str,
    #                                                 geographicPositionTopRight: str,
    #                                                 roadGrade: int
    #                                                 ) -> list:
    #     """
    #     函数：获取输入的矩形区域的地理位置对应的具体路况信息
    #     Args:
    #         geographicPositionBottomLeft:矩形区域的左下角地理位置
    #         geographicPositionTopRight:矩形区域的右上角地理位置
    #         roadGrade:道路等级
    #     Returns:
    #         返回输入的矩形区域的地理位置对应的具体路况信息
    #     """
    #
    #     self.geographicPositionBottomLeft = geographicPositionBottomLeft
    #     self.geographicPositionTopRight = geographicPositionTopRight
    #     self.roadGrade = roadGrade
    #
    #     geographicPositionList = [self.geographicPositionBottomLeft, self.geographicPositionTopRight]
    #     reversedGeographicPositionList = []
    #
    #     comparingPositionPositionBottomLeft = self.geographicPositionBottomLeft.split(',')
    #     comparingPositionPositionTopRight = self.geographicPositionTopRight.split(',')
    #
    #     if eval(comparingPositionPositionBottomLeft[0]) > eval(comparingPositionPositionTopRight[0]):
    #         geographicPositionList = list(reversed(geographicPositionList))
    #
    #     for item in geographicPositionList:
    #         reverseList = item.split(',')
    #         reversedList = list(reversed(reverseList))
    #         reversedGeographicPositionList.append(','.join(reversedList))
    #
    #     autonaviBounds = ';'.join(reversedGeographicPositionList)
    #     # autonaviBounds = "39.912078,116.464303;39.918276,116.475442"
    #
    #     # 使用百度地图API进行矩形区域查询
    #     trafficSituation = TrafficSituationByBaiduMap()
    #     # 获取到的交通态势原信息（未解析）
    #     resultTrafficRectangleRoadInformation = trafficSituation.get_traffic_situation_by_rectangle(
    #         bounds=autonaviBounds, road_grade=self.roadGrade, coord_type_input="gcj02")
    #     resultTrafficRectangleRoadDetailInformation = trafficSituation.parse_traffic_situation(
    #         resultTrafficRectangleRoadInformation)
    #     return resultTrafficRectangleRoadDetailInformation
