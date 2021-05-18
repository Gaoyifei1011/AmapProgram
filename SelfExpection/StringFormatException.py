import inspect

from logrecord.WriteLog import WriteLog


class StringFormatException(BaseException):
    """this is user's Exception for check the length of name """

    def __init__(self):
        pass

    def error_reason(self):
        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - request_information:{1}'.format(function_name,
                                                                                           '您输入的数据格式异常')
                              )
