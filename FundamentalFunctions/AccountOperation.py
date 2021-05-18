import inspect
import os
import pathlib

from logrecord.WriteLog import WriteLog


class AccountOperation:
    """
    Class:账户登录操作
    """

    def __init__(self):
        self.directory = None
        self.file = None
        self.passwordText = None
        self.userInformationFile = None
        self.userNameText = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    def check_user_name(self, userNameText: str
                        ) -> int:
        """
        函数：检测用户提供的账号是否符合规范要求
        Args:
            userNameText: 用户输入账号
        Returns:
            检测类型识别码
        """

        self.userNameText = userNameText

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 检查结果
        checkedResult = self.userNameText is None or self.userNameText == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - user name login result:{1}'.format(function_name,
                                                                                                 checkedResult)
                              )

        if checkedResult:
            return 2
        # TODO:
        # 使用python正则表达式验证用户名格式
        # 此处检测格式错误返回false
        else:
            return True

    def check_password(self, passwordText: str
                       ) -> int:
        """
        函数：检测用户提供的账号是否符合规范要求
        Args:
            passwordText: 用户输入的密码
        Returns:
            检测类型识别码
        """

        self.passwordText = passwordText

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 检查结果
        checkedResult = self.passwordText is None or self.passwordText == ''

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - password login result:{1}'.format(function_name,
                                                                                                 checkedResult)
                              )

        if checkedResult:
            return 2
        # TODO:
        # 使用python正则表达式验证密码格式
        # 此处检测格式错误返回false
        else:
            return True

    def create_directory(self, directory: str
                         ) -> None:
        """
        函数：创建记录用户账号及密码的目录
        Args:
            directory: 系统指定的目录
        """

        self.directory = directory

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        try:
            # 指定的目录不存在，创建
            if os.path.exists(self.directory):
                if os.path.isfile(self.directory):
                    os.remove(self.directory)
                    os.mkdir(self.directory)

        except FileNotFoundError:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - The system could not find the specified path.'.format(
                                      function_name)
                                  )

        except Exception:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - Unknown Error.'.format(
                                      function_name)
                                  )

    def create_file(self, file: str
                    ) -> None:
        """
        函数：创建记录用户账号及密码的文件
        Args:
            file: 系统指定的文件
        """

        self.file = file

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        try:
            # 指定的目录不存在，创建
            if os.path.exists(self.file):
                if os.path.isdir(self.file):
                    os.removedirs(self.file)
                    pathlib.Path(self.file).touch()
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - File {0} successfully created.'.format(
                                      self.file)
                                  )

        except FileNotFoundError:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - File does not exist.'.format(
                                      function_name)
                                  )

        except LookupError:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - Error specifying encoding.'.format(
                                      function_name)
                                  )

        except UnicodeDecodeError:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - Decoding error while reading file.'.format(
                                      function_name)
                                  )

        except Exception:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - Unknown Error.'.format(
                                      function_name)
                                  )

    def login(self, userInformationFile: str,
              userNameText: str,
              passwordText: str
              ) -> bool:
        """
        函数：进行账户登录，验证登录的账号及密码是否正确
        Args:
            userInformationFile: 记录用户账号及密码的文件
            userNameText: 用户输入的账号
            passwordText: 用户输入的密码
        Returns:
            检测账号和密码是否正确的识别码
        """

        self.userInformationFile = userInformationFile
        self.userNameText = userNameText
        self.passwordText = passwordText

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        flag = False
        with open(self.userInformationFile, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip("\n")
                userName, password = line.split(',')
                if self.userNameText == userName and self.passwordText == password:
                    flag = True
                    break

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=6,
                              context='Function name:{0} - login checked result "{1}".'.format(
                                  function_name, flag)
                              )

        return flag
