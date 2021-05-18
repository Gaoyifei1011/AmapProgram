from typing import Any

from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QMessageBox


class SelfMessageBox:
    """
    Class:自定义QMessageBox（修改）
    """
    def __init__(self):
        super(SelfMessageBox, self).__init__()

    def selfDefineFont(self, fontName: str = "微软雅黑 Light",
                       fontSize: int = 12
                       ) -> QFont():
        """
        函数：自定义字体样式
        Args:
            fontName: 字体名称
            fontSize: 字体大小
        Returns:
            font: 需要的字体类型
        """

        self.fontName = fontName
        self.fontSize = fontSize

        font = QFont()
        # 设置字体类型
        font.setFamily(self.fontName)
        # 设置字体大小
        font.setPointSize(self.fontSize)
        return font

    def messageLevel(self, level: int
                     ) -> 'QMessageBox.Icon':
        """
        函数：对话框消息等级
        Args:
            level: 消息等级
        Returns:
            QMessageBox对应的消息等级
        """

        self.level = level

        if self.level == 1:
            return QMessageBox.Information
        elif self.level == 2:
            return QMessageBox.Question
        elif self.level == 3:
            return QMessageBox.Warning
        elif self.level == 4:
            return QMessageBox.Critical
        elif self.level == 5:
            return QMessageBox.About

    def initUI(self, MainWindow,
               **parameters: [str, Any]
               ) -> None:
        """
        函数：窗口界面初始化
        Args:
            MainWindow:主窗口界面实例
            **parameters:消息框对应的其他参数
        """

        self.MainWindow = MainWindow
        self.parameters = parameters

        if self.parameters['level'] and self.parameters['title'] and self.parameters['information']:
            self.messageBox = QMessageBox(self.parameters['level'], self.parameters['title'], self.parameters['information'])
        if self.parameters['icon']:
            self.messageBox.setWindowIcon(QIcon(self.parameters['icon']))
        if self.parameters['font']:
            self.messageBox.setFont(self.parameters['font'])
        self.messageBox.addButton(self.MainWindow.tr("确定"), QMessageBox.YesRole)
        self.messageBox.exec_()
