import inspect

from AmapFunctions.WeatherInformation import WeatherInformation
from logrecord.WriteLog import WriteLog


class WeatherOperation:
    """
    Class:天气信息操作
    """
    def __init__(self):
        self.city = None
        self.weatherInformation = None
        self.weatherType = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    def check_weather_information(self, city: str) -> int:
        """
        函数：检测用户提供的天气信息是否符合规范要求
        Args:
            city:用户输入的城市
        Returns:
            检测类型识别码
        """
        self.city = city

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 检测结果
        checkedResult = self.city is None or self.city == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - weather check result:{1}'.format(function_name,
                                                                                            checkedResult)
                              )

        if checkedResult:
            return 2
        # TODO:
        # 使用python正则表达式验证用户名格式
        # 此处检测格式错误返回false
        else:
            return True

    def get_weather_information(self, city: str,
                                weatherType: str
                                ) -> list:
        """
        函数：获取输入城市对应的天气信息
        Args:
            city:城市名称
            weatherType:查询的天气类型
        Returns:
            返回获取到输入城市对应的天气具体信息
        """

        # TODO:未来版本将返回数据从str升级为dict
        self.city = city
        self.weatherType = weatherType

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        weatherInformation = WeatherInformation()
        # 获取的天气原信息（未解析）
        resultWeatherInformation = weatherInformation.get_weather_information(self.city, extensions=self.weatherType)

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - resultWeatherInformation:{1}'.format(function_name,
                                                                                                resultWeatherInformation)
                              )
        # 解析后的天气信息
        resultWeatherDetailInformation = weatherInformation.parse_weather_information(resultWeatherInformation,
                                                                                      self.weatherType)
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - resultWeatherDetailInformation:{1}'.format(function_name,
                                                                                                      resultWeatherDetailInformation)
                              )

        return resultWeatherDetailInformation
