import inspect
import os.path
from typing import Any

from PyQt5 import QtWidgets

from FundamentalFunctions.AccountOperation import AccountOperation
from MainWindow import MainWindow
from Window.MessageBoxUI import SelfMessageBox
from Window.loginUI import Ui_AmapLoginUI
from logrecord.WriteLog import WriteLog
from Resources.Icon.Icon import *


class LoginMainWindow(QtWidgets.QMainWindow, Ui_AmapLoginUI):
    """
    函数：主窗口界面函数LoginMainWindow
    """

    def __init__(self, parent=None):
        """
        函数：登录窗口界面组件初始化
        Args:
            parent:arent作为构造函数的最后一个参数被传入，但通常情况下不必显示去指定parent对象。因为当调用局管理器时，部局管理器会自动处理这种parent-child关系。
        """

        # 对继承自父类的属性进行初始化
        super(LoginMainWindow, self).__init__()
        self.setupUi(self)

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

        # 用户账号名称和密码初始化
        self.userNameText = None
        self.passwordText = None

        # 用户账号密码输入框内容变化监听器
        self.userNameLineEdit.textChanged[str].connect(self.userNameLineEditTextChanged)
        self.passwordLineEdit.textChanged[str].connect(self.passwordLineEditTextChanged)

        # 用户账号密码输入框按下回车键（Enter）监听器
        self.userNameLineEdit.returnPressed.connect(
            lambda: self.loginEventHandler(self.userNameText, self.passwordText))
        self.passwordLineEdit.returnPressed.connect(
            lambda: self.loginEventHandler(self.userNameText, self.passwordText))
        # 登录按钮点击触发器
        self.loginInButton.clicked.connect(lambda: self.loginEventHandler(self.userNameText, self.passwordText))

    def userNameLineEditTextChanged(self, text: Any
                                    ) -> None:
        """
        函数：事件监听器：检测userNameLineEdit窗口文字发生变化时做出相应的操作
        Args:
            text: 从userNameLineEdit中即时获取用户的输入文本
        """
        self.userNameText = text

    def passwordLineEditTextChanged(self, text):
        """
        函数：事件监听器：检测passwordLineEdit窗口文字发生变化时做出相应的操作
        Args:
            text: 从passwordLineEdit中即时获取用户的输入文本
        """
        self.passwordText = text

    def loginEventHandler(self, userNameText: str,
                          passwordText: str
                          ) -> None:
        """
        函数：事件处理器：检测用户的登录操作
        Args:
            userNameText:用户的登录内容
            passwordText:用户的密码内容
        """

        self.userNameText = userNameText
        self.passwordText = passwordText

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 用户操作实例化
        accountOperation = AccountOperation()
        # 检测用户登录账号和密码内容的格式
        userNameCheckedResult = accountOperation.check_user_name(self.userNameText)
        passwordCheckedResult = accountOperation.check_password(self.passwordText)

        if userNameCheckedResult == 2:
            # 账号输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="账号输入提示",
                                  information="请您输入账号后再登录",
                                  icon=":/About.png"
                                  )

        elif userNameCheckedResult == 0:
            # 账号输入框中账号格式不正确
            # 账号输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(3)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="账号输入提示",
                                  information="您输入的账号格式不正确",
                                  icon=":/Warning.png"
                                  )

        elif passwordCheckedResult == 2:
            # 密码输入框内容为空
            selfMessageBox = SelfMessageBox()
            font = selfMessageBox.selfDefineFont()
            level = selfMessageBox.messageLevel(1)
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="密码输入提示",
                                  information="请您输入密码后再登录",
                                  icon=":/About.png"
                                  )

        elif passwordCheckedResult == 0:
            # 密码输入框中账号格式不正确
            # 账号输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义消息等级
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(3)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="密码输入提示",
                                  information="您输入的密码格式不正确",
                                  icon=":/Warning.png"
                                  )

        elif userNameCheckedResult and passwordCheckedResult:
            # 用户账号密码格式正确，尝试登录
            # 用户信息存储根目录（目录不存在则创建）

            # TODO:优化路径创建，采用递归方式创建
            # 文件保存路径
            local_appdata_directory = os.getenv('LOCALAPPDATA')

            # 根目录
            temp_directory = '\\'.join([local_appdata_directory, 'AmapProgram'])
            # 目录不存在，创建
            if not os.path.exists(temp_directory):
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=6,
                                      context='Function name:{0} - directory successfully created'.format(function_name)
                                      )
                os.mkdir(temp_directory)

            # 账户数据目录
            account_directory = '\\'.join([temp_directory, 'Account'])
            # 目录不存在，创建
            if not os.path.exists(account_directory):
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=6,
                                      context='Function name:{0} - directory successfully created'.format(function_name)
                                      )
                accountOperation.create_directory(account_directory)

            userInformationDirectory = os.path.join(account_directory, 'UserInformation')
            accountOperation.create_directory(userInformationDirectory)

            # 用户信息文件（文件不存在则创建）
            userInformationFile = os.path.join(userInformationDirectory, 'userinformation')
            accountOperation.create_file(userInformationFile)

            # 进行登录操作
            checkResult = accountOperation.login(userInformationFile, self.userNameText, self.passwordText)
            if checkResult:
                self.hide()  # 隐藏登录界面
                self.mainWindow = MainWindow()
                self.mainWindow.show()
            else:
                # 登录失败，弹出对话框
                selfMessageBox = SelfMessageBox()
                font = selfMessageBox.selfDefineFont()
                level = selfMessageBox.messageLevel(3)
                selfMessageBox.initUI(self, font=font,
                                      level=level,
                                      title="账号输入信息",
                                      information="您输入的账号或密码有误",
                                      icon=":/Warning.png"
                                      )
