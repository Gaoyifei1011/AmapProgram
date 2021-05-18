import inspect

from AmapFunctions.GeographicCoding import GeographicCoding
from AmapFunctions.StaticMaps import StaticMaps
from logrecord.WriteLog import WriteLog


class StaticMapsOperation:
    """
    Class:静态地图查询操作
    """
    def __init__(self):
        self.staticMapsPosition = None
        self.zoom = None
        self.size = None
        self.scale = None
        self.traffic = None
        self.context = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    def check_static_maps_information(self, staticMapsPosition: str
                                      ) -> int:

        """
        函数：检测用户提供的静态地图地点是否符合规范要求
        Args:
            staticMapsPosition: 用户输入的地理位置
        Returns:
            检测类型识别码
        """

        # TODO:未来版本将返回数据从list升级为dict
        self.staticMapsPosition = staticMapsPosition

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 检测结果
        checkedResult = self.staticMapsPosition is None or self.staticMapsPosition == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - static maps position check result:{1}'.format(function_name,
                                                                                                         checkedResult)
                              )

        if checkedResult:
            return 2
        else:
            return True

    def get_static_maps(self, staticMapsPosition: str,
                        zoom: int,
                        size: str,
                        scale: int,
                        traffic: int
                        ) -> str:
        """
        函数：获取静态地图
        Args:
            staticMapsPosition:地理位置
            zoom:缩放级别
            size:图片尺寸大小
            scale:是否为高清图
            traffic:是否包含交通状况
        """

        # TODO:未来版本将返回数据从list升级为dict
        self.staticMapsPosition = staticMapsPosition
        self.zoom = zoom
        self.size = size
        self.scale = scale
        self.traffic = traffic

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 获取地理位置信息的地理编码
        geographicCoding = GeographicCoding()
        # 获取地理位置信息对应的初始编码信息
        # TODO:优化City参数
        staticMapsJsonDecode = geographicCoding.get_geographic_coding(address=self.staticMapsPosition,
                                                                      city='')

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - staticMapsJsonDecode:{1}'.format(function_name,
                                                                                            staticMapsJsonDecode)
                              )

        parseStaticMapsInformation = geographicCoding.parse_geographic_coding(staticMapsJsonDecode)

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - parseStaticMapsInformation:{1}'.format(function_name,
                                                                                                  parseStaticMapsInformation)
                              )

        # 地理位置编码
        if 'error_context' not in parseStaticMapsInformation:
            resultStaticMapsGeographicCoding = parseStaticMapsInformation['geographic_position']
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - resultStaticMapsGeographicCoding:{1}'.format(
                                      function_name,
                                      resultStaticMapsGeographicCoding)
                                  )

        else:
            return "3"

        staticMaps = StaticMaps()

        markers = staticMaps.user_define_markers(location=resultStaticMapsGeographicCoding,
                                                 size='large',
                                                 color='0x0085FF',
                                                 label=""
                                                 )

        labels = staticMaps.user_define_labels(content=self.staticMapsPosition,
                                               font=0,
                                               font_size=20,
                                               font_color='0xFFFFFF',
                                               background='0x0000FF',
                                               location=resultStaticMapsGeographicCoding
                                               )

        # TODO:
        # 将这些选项放入设置中
        check_result = staticMaps.check_static_maps_url(location=resultStaticMapsGeographicCoding,
                                                        zoom=self.zoom,
                                                        size=self.size,
                                                        scale=self.scale,
                                                        markers=markers,
                                                        labels=labels,
                                                        traffic=self.traffic
                                                        )

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - static maps check result:{1}'.format(function_name,
                                                                                                check_result)
                              )

        # 获取静态地图数据
        result_static_maps = staticMaps.get_static_maps_url(location=resultStaticMapsGeographicCoding,
                                                            zoom=self.zoom,
                                                            size=self.size,
                                                            scale=self.scale,
                                                            markers=markers,
                                                            labels=labels,
                                                            check_result=check_result,
                                                            traffic=self.traffic
                                                            )

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - result_static_maps:{1}'.format(function_name,
                                                                                          result_static_maps)
                              )

        if result_static_maps == 'Error':
            return "1"  # '获取地图图片失败'
        else:
            result_Photo = staticMaps.parse_static_maps_url(result_static_maps)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - result Photo:{1}'.format(function_name,
                                                                                        result_Photo)
                                  )

            if result_Photo == 'Error':
                return "2"  # '图片保存失败，请检查您的网络链接或是否有保存文件的权限'
            else:
                return result_Photo

    def get_static_maps_by_location(self, staticMapsPosition: str,
                                    zoom: int,
                                    size: str,
                                    scale: int,
                                    traffic: int,
                                    context: str = 'Unknown',
                                    ) -> str:
        """
        函数：获取静态地图（通过地理位置）
        Args:
            staticMapsPosition:地理位置坐标
            zoom:缩放级别
            size:图片尺寸大小
            scale:是否为高清图
            traffic:是否包含交通状况
            context:查询的地理位置名称
        """

        # TODO:未来版本将返回数据从list升级为dict
        self.staticMapsPosition = staticMapsPosition
        self.zoom = zoom
        self.size = size
        self.scale = scale
        self.traffic = traffic
        self.context = context

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        staticMaps = StaticMaps()

        markers = staticMaps.user_define_markers(location=self.staticMapsPosition,
                                                 size='large',
                                                 color='0x0085FF',
                                                 )

        # TODO:
        # 将这些选项放入设置中
        check_result = staticMaps.check_static_maps_url(location=self.staticMapsPosition,
                                                        zoom=self.zoom,
                                                        size=self.size,
                                                        scale=self.scale,
                                                        markers=markers,
                                                        traffic=self.traffic
                                                        )

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - static maps check result:{1}'.format(function_name,
                                                                                                check_result)
                              )

        result_static_maps = staticMaps.get_static_maps_url(location=self.staticMapsPosition,
                                                            zoom=self.zoom,
                                                            size=self.size,
                                                            scale=self.scale,
                                                            markers=markers,
                                                            check_result=check_result,
                                                            traffic=self.traffic
                                                            )

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - result_static_maps:{1}'.format(function_name,
                                                                                          result_static_maps)
                              )

        if result_static_maps == 'Error':
            return "1"  # '获取地图图片失败'
        else:
            # 获取静态地图数据
            result_Photo = staticMaps.parse_static_maps_url(result_static_maps)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - result Photo:{1}'.format(function_name,
                                                                                        result_Photo)
                                  )

            if result_Photo == 'Error':
                return "2"  # '图片保存失败，请检查您的网络链接或是否有保存文件的权限'
            else:
                return result_Photo
