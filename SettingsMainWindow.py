import sys

from PyQt5 import QtWidgets

from Window.SettingsUI import Ui_SettingsUI


# from LoginMainWindow import LoginMainWindow
# from MainWindow import MainWindow


class SettingsMainWindow(QtWidgets.QMainWindow, Ui_SettingsUI):
    """
    函数：设置窗口界面函数LoginMainWindow
    """

    def __init__(self, parent=None):
        """
        函数：设置窗口界面组件初始化
        Args:
            parent:arent作为构造函数的最后一个参数被传入，但通常情况下不必显示去指定parent对象。因为当调用局管理器时，部局管理器会自动处理这种parent-child关系。
        """

        # 对继承自父类的属性进行初始化
        super(SettingsMainWindow, self).__init__()
        self.setupUi(self)

        # 侧边栏选择条目触发器
        self.itemListWidget.itemClicked.connect(self.item_list_widget_clicked)

        # 个人中心退出按钮事件触发器
        self.logoutButton.clicked.connect(self.logout_button_clicked)

    # 侧边栏选择条目事件处理01
    def item_list_widget_clicked(self):
        # 获取当前列表部件中所有选中项的一个列表
        selectedItems = self.itemListWidget.selectedItems()
        # 设置当前列表部件选中项为None
        selectItem = None
        # # 清除选中的项
        # self.itemListWidget.clearSelection()
        # 获取当前选中项的名称
        for item in selectedItems:
            selectItem = item.text().lstrip()
        if selectItem == "个人中心":
            self.itemListWidget.setCurrentRow(0)
            self.stackedWidget.setCurrentIndex(0)
        elif selectItem == "静态地图":
            self.itemListWidget.setCurrentRow(1)
            self.stackedWidget.setCurrentIndex(1)
        elif selectItem == "天气类型":
            self.itemListWidget.setCurrentRow(2)
            self.stackedWidget.setCurrentIndex(2)
        elif selectItem == "详细说明":
            self.itemListWidget.setCurrentRow(3)
            self.stackedWidget.setCurrentIndex(3)
        elif selectItem == "参考及引用":
            self.itemListWidget.setCurrentRow(4)
            self.stackedWidget.setCurrentIndex(4)

    # 个人中心退出按钮事件触发器
    def logout_button_clicked(self):
        #
        # self.loginMainWindow = LoginMainWindow()
        # self.mainWindow = MainWindow()
        # # 设置窗口关闭
        # self.close()
        # # 主窗口关闭
        # self.mainWindow.close()
        # # 打开登录窗口
        # time.sleep(0.5)
        # self.loginMainWindow.show()
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    loginWindow = SettingsMainWindow()
    loginWindow.show()
    sys.exit(app.exec_())
