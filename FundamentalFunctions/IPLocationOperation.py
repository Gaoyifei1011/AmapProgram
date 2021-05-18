import inspect
import re

from AmapFunctions.IPLocation import IPLocation
from logrecord.WriteLog import WriteLog


class IPLocationOperation:
    """
    Class:IP地址查询操作
    """
    def __init__(self):
        self.ip = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    def check_ip_formation(self, ip: str
                           ) -> int:
        """
        函数：检测用户提供的IP格式是否符合规范要求
        Args:
            ip: 用户输入的IP地址
        Returns:
            检测类型识别码
        """

        self.ip = ip

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        checkedResult = self.ip is None or self.ip == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - ip check result 1 :{1}'.format(function_name,
                                                                                          checkedResult)
                              )

        # 用户输入的IP地址为空
        if checkedResult:
            return 2
        # 匹配 0.0.0.0-255.255.255.255的表达式书写方法
        pattern = re.compile(r'(([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])\.){3}([1-9]?\d|1\d\d|2[0-4]\d|25[0-5])')
        IPCheckResult = bool(pattern.match(self.ip))
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - ip check result 2:{1}'.format(function_name,
                                                                                         IPCheckResult)
                              )

        return IPCheckResult

    def get_ip_information(self, ip: str
                           ) -> dict:
        """
        函数：获取IP地址对应的具体信息
        Args:
            ip:IP地址
        Returns:
            返回获取到IP地址对应的具体信息
        """

        self.ip = ip

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        ipLocation = IPLocation()
        # 获取的IP原信息（未解析）
        resultIPLocation = ipLocation.get_ip_location(self.ip, input_type=4)
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - resultIPLocation:{1}'.format(function_name,
                                                                                        resultIPLocation)
                              )

        # 解析后的IP地址信息
        resultIPDetailInformation = ipLocation.parse_ip_location(resultIPLocation)
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - resultIPDetailInformation:{1}'.format(function_name,
                                                                                                 resultIPDetailInformation)
                              )

        return resultIPDetailInformation
