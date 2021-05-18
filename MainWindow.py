import urllib.request

from PIL import Image
from PIL.ImageQt import ImageQt
from PyQt5 import QtWidgets, QtGui, QtChart
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsPixmapItem, QGraphicsScene

from FundamentalFunctions.AdministrativeDistrictOperation import AdministrativeDistrictOperation
from FundamentalFunctions.BusRoutePlanningOperation import BusRoutePlanningOperation
from FundamentalFunctions.DriveRoutePlanningOperation import DriveRoutePlanningOperation
from FundamentalFunctions.GetTrafficData import GetTrafficData
from FundamentalFunctions.IPLocationOperation import IPLocationOperation
from FundamentalFunctions.RideRoutePlanningOperation import RideRoutePlanningOperation
from FundamentalFunctions.StaticMapsOperation import StaticMapsOperation
from FundamentalFunctions.TrafficInformationExecuteOperation import TrafficInformationReadOperation
from FundamentalFunctions.TrafficSituationOperation import TrafficSituationOperation
from FundamentalFunctions.WalkingRoutePlanningOperation import WalkingRoutePlanningOperation
from FundamentalFunctions.WeatherOperation import WeatherOperation
from Resources.Icon.Icon import *
from SettingsMainWindow import SettingsMainWindow
from Window.MainUI import Ui_AmapMainUI
from Window.MessageBoxUI import SelfMessageBox
from logrecord.WriteLog import WriteLog


class MainWindow(QtWidgets.QMainWindow, Ui_AmapMainUI):
    """
    函数：主窗口界面函数MainWindow

    """

    def __init__(self, parent=None):
        """
        函数：主窗口界面组件初始化
        Args:
            parent:arent作为构造函数的最后一个参数被传入，但通常情况下不必显示去指定parent对象。因为当调用局管理器时，部局管理器会自动处理这种parent-child关系。
        """

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

        # 对继承自父类的属性进行初始化
        super(MainWindow, self).__init__()
        self.setupUi(self)

        # 侧边栏选择条目触发器
        self.basicFunctionListWidget.itemClicked.connect(self.basic_function_list_widget_clicked)
        self.searchServiceListWidget.itemClicked.connect(self.search_service_list_widget_clicked)
        self.advancedFunctionListWidget.itemClicked.connect(self.advanced_function_list_widget_clicked)
        self.otherOptionsListWidget.itemClicked.connect(self.other_options_list_widget_clicked)

        # 步行路径规划查询页面
        self.walkingDepartureAddress = None
        self.walkingDestinationAddress = None
        # 步行路径出发点输入框内容变化监听器，步行路径终点输入框内容变化监听器
        self.walkingDepartureLineEdit.textChanged[str].connect(self.walking_departure_line_edit_text_changed)
        self.walkingDestinationLineEdit.textChanged[str].connect(self.walking_destination_line_edit_text_changed)
        # 步行路径出发点回车键（Enter）监听器，步行路径终点回车键（Enter）监听器
        self.walkingDepartureLineEdit.returnPressed.connect(
            lambda: self.get_walking_route_planning_event_handler(self.walkingDepartureAddress,
                                                                  self.walkingDestinationAddress))
        self.walkingDestinationLineEdit.returnPressed.connect(
            lambda: self.get_walking_route_planning_event_handler(self.walkingDepartureAddress,
                                                                  self.walkingDestinationAddress))
        # 步行路径规划查询按钮点击触发器
        self.walkingSearchButton.clicked.connect(
            lambda: self.get_walking_route_planning_event_handler(self.walkingDepartureAddress,
                                                                  self.walkingDestinationAddress))

        # 公交路径规划查询页面
        self.busDepartureAddress = None
        self.busDestinationAddress = None
        # 公交路径出发点输入框内容变化监听器，公交路径终点输入框内容变化监听器
        self.busDepartureLineEdit.textChanged[str].connect(self.bus_departure_line_edit_text_changed)
        self.busDestinationLineEdit.textChanged[str].connect(self.bus_destination_line_edit_text_changed)
        # 公交路径出发点回车键（Enter）监听器，公交路径终点回车键（Enter）监听器
        self.busDepartureLineEdit.returnPressed.connect(
            lambda: self.get_bus_route_planning_event_handler(self.busDepartureAddress,
                                                              self.busDestinationAddress))
        self.busDestinationLineEdit.returnPressed.connect(
            lambda: self.get_bus_route_planning_event_handler(self.busDepartureAddress,
                                                              self.busDestinationAddress))
        # 公交路径规划查询按钮点击触发器
        self.busSearchButton.clicked.connect(
            lambda: self.get_bus_route_planning_event_handler(self.busDepartureAddress,
                                                              self.busDestinationAddress))

        # 驾驶路径规划查询页面
        self.driveDepartureAddress = None
        self.driveDestinationAddress = None
        # 驾驶路径出发点输入框内容变化监听器，驾驶路径终点输入框内容变化监听器
        self.driveDepartureLineEdit.textChanged[str].connect(self.drive_departure_line_edit_text_changed)
        self.driveDestinationLineEdit.textChanged[str].connect(self.drive_destination_line_edit_text_changed)
        # 驾驶路径出发点回车键（Enter）监听器，驾驶路径终点回车键（Enter）监听器
        self.driveDepartureLineEdit.returnPressed.connect(
            lambda: self.get_drive_route_planning_event_handler(self.driveDepartureAddress,
                                                                self.driveDestinationAddress))
        self.driveDestinationLineEdit.returnPressed.connect(
            lambda: self.get_drive_route_planning_event_handler(self.driveDepartureAddress,
                                                                self.driveDestinationAddress))
        # 驾驶路径规划查询按钮点击触发器
        self.driveSearchButton.clicked.connect(
            lambda: self.get_drive_route_planning_event_handler(self.driveDepartureAddress,
                                                                self.driveDestinationAddress))

        # 骑行路径规划查询页面
        self.rideDepartureAddress = None
        self.rideDestinationAddress = None
        # 骑行路径出发点输入框内容变化监听器，骑行路径终点输入框内容变化监听器
        self.rideDepartureLineEdit.textChanged[str].connect(self.ride_departure_line_edit_text_changed)
        self.rideDestinationLineEdit.textChanged[str].connect(self.ride_destination_line_edit_text_changed)
        # 骑行路径出发点回车键（Enter）监听器，骑行路径终点回车键（Enter）监听器
        self.rideDepartureLineEdit.returnPressed.connect(
            lambda: self.get_ride_route_planning_event_handler(self.rideDepartureAddress,
                                                               self.rideDestinationAddress))
        self.rideDestinationLineEdit.returnPressed.connect(
            lambda: self.get_ride_route_planning_event_handler(self.rideDepartureAddress,
                                                               self.rideDestinationAddress))
        # 骑行路径规划查询按钮点击触发器
        self.rideSearchButton.clicked.connect(
            lambda: self.get_ride_route_planning_event_handler(self.rideDepartureAddress,
                                                               self.rideDestinationAddress))

        # 静态地图查询页面
        self.staticMapsPosition = None
        # 静态地图地点查询框内容变化监听器
        self.staticMapsSearchLineEdit.textChanged[str].connect(self.static_maps_search_line_edit_text_changed)
        # 静态地图地点查询框回车键（Enter）监听器
        self.staticMapsSearchLineEdit.returnPressed.connect(
            lambda: self.get_static_maps_event_handler(self.staticMapsPosition)
        )
        # 静态地图查询按钮点击触发器
        self.staticMapsSearchButton.clicked.connect(
            lambda: self.get_static_maps_event_handler(self.staticMapsPosition)
        )

        # IP地址查询界面
        self.ip = None
        # IP信息输入框内容变化监听器
        self.IPLocationLineEdit.textChanged[str].connect(self.ip_location_line_edit_text_changed)
        # IP信息输入框回车键（Enter）监听器
        self.IPLocationLineEdit.returnPressed.connect(lambda: self.get_ip_location_event_handler(self.ip))
        # IP信息查询按钮点击触发器
        self.IPLocationSearchButton.clicked.connect(lambda: self.get_ip_location_event_handler(self.ip))
        # 获取当前网络IP地址按钮点击触发器
        self.IPLocationGetLocalNetWorkButton.clicked.connect(self.get_ip_location_from_host)

        # 行政区域查询页面
        self.administrativeInformation = None
        # 省份列表
        provinceList = ['请选择省份',
                        '北京市', '天津市', '河北省', '山西省', '内蒙古自治区',
                        '辽宁省', '吉林省', '黑龙江省',
                        '上海市', '江苏省', '浙江省', '安徽省', '福建省 ', '江西省', '山东省',
                        '河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区', '海南省',
                        '重庆市', '四川省', '贵州省', '云南省', '西藏自治区',
                        '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区',
                        '台湾省', '香港特别行政区', '澳门特别行政区']
        # 市区列表
        cityList = ['请选择城市']
        # 县城列表
        countyList = ['请选择区/县']

        # 省份列表初始化
        for province in provinceList:
            self.provinceComboBox.addItem(province)
        # 市区列表初始化
        self.cityComboBox.setEnabled(False)
        for city in cityList:
            self.cityComboBox.addItem(city)
        # 县城列表初始化
        self.countyComboBox.setEnabled(False)
        for county in countyList:
            self.countyComboBox.addItem(county)

        # 省份下拉选择框条目变化事件监听器
        self.provinceComboBox.currentIndexChanged.connect(self.province_index_changed_event_handler)
        # 市区下拉选择框条目变化事件监听器
        self.cityComboBox.currentIndexChanged.connect(self.city_index_changed_event_handler)
        # 行政区域查询按钮点击触发器
        self.administrativeSearchButton.clicked.connect(self.administrative_search_button_event_handler)

        # 天气查询界面
        self.city = None
        # 天气信息查询输入框内容变化监听器
        self.weatherSearchLineEdit.textChanged[str].connect(self.weather_search_line_edit_changed)
        # 天气信息查询输入框回车键（Enter）监听器
        self.weatherSearchLineEdit.returnPressed.connect(lambda: self.get_weather_information_event_handler(self.city))
        # 天气信息查询按钮点击触发器
        self.weatherSearchButton.clicked.connect(lambda: self.get_weather_information_event_handler(self.city))

        # 交通态势界面
        # 省份列表
        trafficProvinceList = ['请选择省份',
                               '北京市', '天津市', '河北省', '山西省', '内蒙古自治区',
                               '辽宁省', '吉林省', '黑龙江省',
                               '上海市', '江苏省', '浙江省', '安徽省', '福建省 ', '江西省', '山东省',
                               '河南省', '湖北省', '湖南省', '广东省', '广西壮族自治区', '海南省',
                               '重庆市', '四川省', '贵州省', '云南省', '西藏自治区',
                               '陕西省', '甘肃省', '青海省', '宁夏回族自治区', '新疆维吾尔自治区']
        # 市区列表
        trafficCityList = ['请选择城市']
        # 交通态势查询方式下拉选择框条目变化事件监听器
        self.trafficRoadRealSituationComboBox.currentIndexChanged.connect(
            self.traffic_situation_index_changed_event_handler)
        # 省份列表初始化
        for province in trafficProvinceList:
            self.trafficRealRoadProvinceComboBox.addItem(province)
        # 市区列表初始化
        self.trafficRealRoadCityComboBox.setEnabled(False)
        for city in trafficCityList:
            self.trafficRealRoadCityComboBox.addItem(city)
        # 交通态势省份下拉选择框条目变化事件监听器
        self.trafficRealRoadProvinceComboBox.currentIndexChanged.connect(
            self.traffic_province_index_changed_event_handler)

        # 交通态势（道路实时路况）
        self.roadName = None
        # 交通态势（道路实时路况）输入框内容变化监听器
        self.trafficSituationRealRoadSearchRoadName.textChanged.connect(self.traffic_situation_real_road_text_changed)
        # 交通态势（道路实时路况）输入框回车键（Enter）监听器
        self.trafficSituationRealRoadSearchRoadName.returnPressed.connect(
            lambda: self.get_traffic_real_road_event_handler(self.roadName))
        # 交通态势（道路实时路况）信息查询按钮点击触发器
        self.trafficRealRoadSearchButton.clicked.connect(
            lambda: self.get_traffic_real_road_event_handler(self.roadName))

        # 交通态势分析系统界面
        RoadNameList = {"太原市": ["迎泽大街", "建设南路", "建设北路", "太榆路", "滨河东路", "滨河西路", "并州北路", "并州南路", "南内环街",
                                "五一路", "府东街", "长风街", "平阳路", "南中环街", "东中环路", "北中环街", "西中环路"],
                        "大同市": ["魏都大道", "御河西路", "御河东路", "云中路", "文兴路", "同煤快线", "北都街", "南环路", "迎宾街"],
                        "阳泉市": ["桃北东街", "桃北中街", "泉中路", "南大街", "东环路"],
                        "长治市": ["英雄南路", "英雄中路", "英雄北路", "太行东街", "太行西街"],
                        "晋城市": ["泽州路", "泽州南路", "中原东街", "中原西街", "凤台东街", "凤台西街"],
                        "朔州市": ["民福东街", "民福西街", "张辽南路", "张辽北路", "开发南路", "开发北路", "文远路"],
                        "忻州市": ["和平东街", "和平西街", "七一南路", "七一北路", "慕山南路", "慕山北路", "雁门西大道", "建设南路", "建设北路"],
                        "吕梁市": ["龙凤南大街", "龙凤北大街", "北川河西路", "滨河北西路", "滨河北中路", "滨河北东路", "吕梁大道"],
                        "晋中市": ["汇通北路", "汇通路", "汇通南路", "龙湖大街", "迎宾街", "顺城街", "中都路", "新建路", "定阳路", "锦纶路", "蕴华街"],
                        "临汾市": ["滨河西路", "滨河路", "鼓楼南大街", "鼓楼北大街"],
                        "运城市": ["解放南路", "解放北路", "中银南路", "中银北路", "机场路", "工农东街", "人民北路", "学苑路"]
                        }

        # 这里有一些异常发生，将在未来的某一个版本进行修复
        # There are some exceptions occurring here that will be fixed in a future release
        # # 交通态势（矩形区域实时路况）
        # self.positionBottomLeft = None
        # self.positionTopRight = None
        # # 交通态势（矩形区域实时路况）输入框（矩形区域左下角）内容变化监听器
        # self.trafficRectangleRoadSearchPositionLineEdit1.textChanged.connect(
        #     self.trafficRectangleBottomLeftRoadTextChanged)
        # # 交通态势（矩形区域实时路况）输入框（矩形区域右上角）内容变化监听器
        # self.trafficRectangleRoadSearchPositionLineEdit2.textChanged.connect(
        #     self.trafficRectangleTopRightRoadTextChanged)
        # # 交通态势（矩形区域实时路况）输入框（矩形区域左下角）回车键（Enter）监听器
        # self.trafficRectangleRoadSearchPositionLineEdit1.returnPressed.connect(
        #     lambda: self.getTrafficPolygonRoadEventHandler(self.positionBottomLeft, self.positionTopRight))
        # # 交通态势（矩形区域实时路况）输入框（矩形区域左下角）回车键（Enter）监听器
        # self.trafficRectangleRoadSearchPositionLineEdit2.returnPressed.connect(
        #     lambda: self.getTrafficPolygonRoadEventHandler(self.positionBottomLeft, self.positionTopRight))
        # # 交通态势（矩形区域实时路况）查询按钮点击触发器
        # self.trafficRectangleRoadLevelSearchButton.clicked.connect(
        #     lambda: self.getTrafficPolygonRoadEventHandler(self.positionBottomLeft, self.positionTopRight))

        # 交通信息分析系统信息开始获取
        self.flagStart = False
        self.trafficSituationAnalysisSystemStartButton.clicked.connect(
            lambda: self.analysis_system_start_event_handler(RoadNameList))
        # 交通信息分析系统信息停止获取
        self.trafficSituationAnalysisSystemStopButton.clicked.connect(self.analysis_system_stop_event_handler)
        # 交通信息分析系统信息面板查看
        self.trafficSituationAnalysisSystemViewButton.clicked.connect(self.analysis_system_view_event_handler)

    # 侧边栏选择条目事件处理01
    def basic_function_list_widget_clicked(self):
        # 获取当前列表部件中所有选中项的一个列表
        selectedItems = self.basicFunctionListWidget.selectedItems()
        # 设置当前列表部件选中项为None
        selectItem = None
        # 清除选中的项
        self.searchServiceListWidget.clearSelection()
        self.advancedFunctionListWidget.clearSelection()
        # 获取当前选中项的名称
        for item in selectedItems:
            selectItem = item.text()
        if selectItem == "路径规划":
            self.amapProgramStackedWidget.setCurrentIndex(0)
        elif selectItem == "静态地图":
            self.amapProgramStackedWidget.setCurrentIndex(2)

    # 侧边栏选择条目事件处理02
    def search_service_list_widget_clicked(self):
        # 获取当前列表部件中所有选中项的一个列表
        selectedItems = self.searchServiceListWidget.selectedItems()
        # 设置当前列表部件选中项为None
        selectItem = None
        # 清除选中的项
        self.basicFunctionListWidget.clearSelection()
        self.advancedFunctionListWidget.clearSelection()
        # 获取当前选中项的名称
        for item in selectedItems:
            selectItem = item.text()
        if selectItem == "IP地址查询":
            self.amapProgramStackedWidget.setCurrentIndex(1)
        elif selectItem == "行政区域查询":
            self.amapProgramStackedWidget.setCurrentIndex(3)
        elif selectItem == "天气查询":
            self.amapProgramStackedWidget.setCurrentIndex(4)

    # 侧边栏选择条目事件处理03
    def advanced_function_list_widget_clicked(self):
        # 获取当前列表部件中所有选中项的一个列表
        selectedItems = self.advancedFunctionListWidget.selectedItems()
        # 设置当前列表部件选中项为None
        selectItem = None
        # 清除选中的项
        self.basicFunctionListWidget.clearSelection()
        self.searchServiceListWidget.clearSelection()
        # 获取当前选中项的名称
        for item in selectedItems:
            selectItem = item.text()
        if selectItem == "交通态势":
            self.amapProgramStackedWidget.setCurrentIndex(5)
        elif selectItem == "交通态势分析系统":
            self.amapProgramStackedWidget.setCurrentIndex(6)

    # 侧边栏选择条目事件处理04
    def other_options_list_widget_clicked(self):
        # 获取当前列表部件中所有选中项的一个列表
        selectedItems = self.otherOptionsListWidget.selectedItems()
        # 设置当前列表部件选中项为None
        selectItem = None
        # 获取当前选中项的名称
        for item in selectedItems:
            selectItem = item.text()
        if selectItem == "设置":
            self.settingsMainWindow = SettingsMainWindow()
            # 新建的窗口始终位于当前屏幕的最前面
            self.settingsMainWindow.setWindowFlags(Qt.WindowStaysOnTopHint)
            # 阻塞父类窗口不能点击
            self.settingsMainWindow.setWindowModality(Qt.ApplicationModal)
            self.settingsMainWindow.show()
            # 点击打开条目后清除选中的项
            self.otherOptionsListWidget.clearSelection()

        elif selectItem == "关于":
            self.settingsMainWindow = SettingsMainWindow()
            self.settingsMainWindow.itemListWidget.setCurrentRow(3)
            self.settingsMainWindow.stackedWidget.setCurrentIndex(3)
            # 新建的窗口始终位于当前屏幕的最前面
            self.settingsMainWindow.setWindowFlags(Qt.WindowStaysOnTopHint)
            # 阻塞父类窗口不能点击
            self.settingsMainWindow.setWindowModality(Qt.ApplicationModal)
            self.settingsMainWindow.show()
            # 点击打开条目后清除选中的项
            self.otherOptionsListWidget.clearSelection()

    # 文本输入框内容变化事件处理器
    # 步行路径规划起点输入框内容变化事件处理器
    def walking_departure_line_edit_text_changed(self, text):
        self.text = text
        self.walkingDepartureAddress = self.text

    # 步行路径规划终点输入框内容变化事件处理器
    def walking_destination_line_edit_text_changed(self, text):
        self.text = text
        self.walkingDestinationAddress = self.text

    # 公交路径规划起点输入框内容变化事件处理器
    def bus_departure_line_edit_text_changed(self, text):
        self.text = text
        self.busDepartureAddress = self.text

    # 公交路径规划终点输入框内容变化事件处理器
    def bus_destination_line_edit_text_changed(self, text):
        self.text = text
        self.busDestinationAddress = self.text

    # 驾驶路径规划起点输入框内容变化事件处理器
    def drive_departure_line_edit_text_changed(self, text):
        self.text = text
        self.driveDepartureAddress = self.text

    # 驾驶路径规划终点输入框内容变化事件处理器
    def drive_destination_line_edit_text_changed(self, text):
        self.text = text
        self.driveDestinationAddress = self.text

    # 骑行路径规划起点输入框内容变化事件处理器
    def ride_departure_line_edit_text_changed(self, text):
        self.text = text
        self.rideDepartureAddress = self.text

    # 驾驶路径规划终点输入框内容变化事件处理器
    def ride_destination_line_edit_text_changed(self, text):
        self.text = text
        self.rideDestinationAddress = self.text

    def static_maps_search_line_edit_text_changed(self, text):
        self.text = text
        self.staticMapsPosition = self.text

    # IP地址查询输入框内容变化事件处理器
    def ip_location_line_edit_text_changed(self, text):
        self.text = text
        self.ip = self.text

    # 天气查询输入框内容变化事件处理器
    def weather_search_line_edit_changed(self, text):
        self.text = text
        self.city = self.text

    # 交通态势（道路实时路况）输入框内容变化事件处理器
    def traffic_situation_real_road_text_changed(self, text):
        self.text = text
        self.roadName = self.text

    # 这里有一些异常发生，将在未来的某一个版本进行修复
    # There are some exceptions occurring here that will be fixed in a future release
    # # 交通态势（矩形区域实时路况）输入框（矩形区域左上角）内容变化监听器
    # def trafficRectangleBottomLeftRoadTextChanged(self, text):
    #     self.text = text
    #     self.positionBottomLeft = self.text
    #
    # # 交通态势（矩形区域实时路况）输入框（矩形区域右上角）内容变化监听器
    # def trafficRectangleTopRightRoadTextChanged(self, text):
    #     self.text = text
    #     self.positionTopRight = self.text

    # 步行路径规划查询按钮事件处理器
    def get_walking_route_planning_event_handler(self, walkingDepartureAddress, walkingDestinationAddress):
        self.walkingDepartureAddress = walkingDepartureAddress
        self.walkingDestinationAddress = walkingDestinationAddress

        # 步行路径规划实例化
        walkingRoutePlanningOperation = WalkingRoutePlanningOperation()
        walkingDepartureCheckedResult = walkingRoutePlanningOperation.check_walking_departure_information(
            self.walkingDepartureAddress)
        walkingDestinationCheckedResult = walkingRoutePlanningOperation.check_walking_destination_information(
            self.walkingDestinationAddress)

        if walkingDepartureCheckedResult == 2:
            # 步行路径规划起点输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="步行路径规划输入提示",
                                  information="请您输入出发点后再查询",
                                  icon=":/About.png"
                                  )

        elif walkingDestinationCheckedResult == 2:
            # 步行路径规划终点输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="步行路径规划输入提示",
                                  information="请您输入终点后再查询",
                                  icon=":/About.png"
                                  )

        elif walkingDepartureCheckedResult and walkingDestinationCheckedResult:
            # 步行路径规划起点和终点输入框内容有信息
            walkingInformationList = walkingRoutePlanningOperation.get_walking_route_planning_information(
                self.walkingDepartureAddress,
                self.walkingDestinationAddress
            )
            # 在GUI窗口上显示获得的信息
            walkingInformation = '\n'.join(walkingInformationList)
            self.walkingResultTextEdit.setText(walkingInformation)

    # 公交路径规划查询按钮事件处理器
    def get_bus_route_planning_event_handler(self, busDepartureAddress, busDestinationAddress):
        self.busDepartureAddress = busDepartureAddress
        self.busDestinationAddress = busDestinationAddress

        # 公交路径规划实例化
        busRoutePlanningOperation = BusRoutePlanningOperation()
        busDepartureCheckedResult = busRoutePlanningOperation.check_bus_departure_information(
            self.busDepartureAddress)
        busDestinationCheckedResult = busRoutePlanningOperation.check_bus_destination_information(
            self.busDestinationAddress)

        if busDepartureCheckedResult == 2:
            # 公交路径规划起点输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="公交路径规划输入提示",
                                  information="请您输入出发点后再查询",
                                  icon=":/About.png"
                                  )

        elif busDestinationCheckedResult == 2:
            # 公交路径规划终点输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="公交路径规划输入提示",
                                  information="请您输入终点后再查询",
                                  icon=":/About.png"
                                  )

        elif busDepartureCheckedResult and busDestinationCheckedResult:
            # 步行路径规划起点和终点输入框内容有信息
            busInformationList = busRoutePlanningOperation.get_bus_route_planning_information(
                self.busDepartureAddress,
                self.busDestinationAddress
            )
            # 在GUI窗口上显示获得的信息
            busInformation = '\n'.join(busInformationList)
            self.busResultTextEdit.setText(busInformation)

    # 驾驶路径规划查询按钮事件处理器
    def get_drive_route_planning_event_handler(self, driveDepartureAddress, driveDestinationAddress):
        self.driveDepartureAddress = driveDepartureAddress
        self.driveDestinationAddress = driveDestinationAddress

        # 驾驶路径规划实例化
        driveRoutePlanningOperation = DriveRoutePlanningOperation()
        driveDepartureCheckedResult = driveRoutePlanningOperation.check_drive_departure_information(
            self.driveDepartureAddress)
        driveDestinationCheckedResult = driveRoutePlanningOperation.check_drive_destination_information(
            self.driveDestinationAddress)

        if driveDepartureCheckedResult == 2:
            # 驾驶路径规划起点输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="驾驶路径规划输入提示",
                                  information="请您输入出发点后再查询",
                                  icon=":/About.png"
                                  )

        elif driveDestinationCheckedResult == 2:
            # 驾驶路径规划终点输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="驾驶路径规划输入提示",
                                  information="请您输入终点后再查询",
                                  icon=":/About.png"
                                  )

        elif driveDepartureCheckedResult and driveDestinationCheckedResult:
            # 步行路径规划起点和终点输入框内容有信息
            driveInformationList = driveRoutePlanningOperation.get_drive_route_planning_information(
                self.driveDepartureAddress,
                self.driveDestinationAddress
            )
            # 在GUI窗口上显示获得的信息
            driveInformation = '\n'.join(driveInformationList)
            self.driveResultTextEdit.setText(driveInformation)

    # 骑行路径规划查询按钮事件处理器
    def get_ride_route_planning_event_handler(self, rideDepartureAddress, rideDestinationAddress):
        self.rideDepartureAddress = rideDepartureAddress
        self.rideDestinationAddress = rideDestinationAddress

        # 骑行路径规划实例化
        rideRoutePlanningOperation = RideRoutePlanningOperation()
        rideDepartureCheckedResult = rideRoutePlanningOperation.check_ride_departure_information(
            self.rideDepartureAddress)
        rideDestinationCheckedResult = rideRoutePlanningOperation.check_ride_destination_information(
            self.rideDestinationAddress)

        if rideDepartureCheckedResult == 2:
            # 骑行路径规划起点输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="骑行路径规划输入提示",
                                  information="请您输入出发点后再查询",
                                  icon=":/About.png"
                                  )

        elif rideDestinationCheckedResult == 2:
            # 骑行路径规划终点输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="骑行路径规划输入提示",
                                  information="请您输入终点后再查询",
                                  icon=":/About.png"
                                  )

        elif rideDepartureCheckedResult and rideDestinationCheckedResult:
            # 骑行路径规划起点和终点输入框内容有信息
            rideInformationList = rideRoutePlanningOperation.get_ride_route_planning_information(
                self.rideDepartureAddress,
                self.rideDestinationAddress
            )
            rideInformation = '\n'.join(rideInformationList)
            self.rideResultTextEdit.setText(rideInformation)

    # 静态地图查询按钮事件处理器
    def get_static_maps_event_handler(self, staticMapsPosition):
        self.staticMapsPosition = staticMapsPosition

        # 静态地图实例化
        staticMapsOperation = StaticMapsOperation()
        staticMapsCheckedResult = staticMapsOperation.check_static_maps_information(self.staticMapsPosition)

        if staticMapsCheckedResult == 2:
            # 静态地图地点输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="静态地图输入提示",
                                  information="请您输入地点后再查询",
                                  icon=":/About.png"
                                  )

        else:
            # 静态地图实例初始化
            staticMapsInformation = staticMapsOperation.get_static_maps(staticMapsPosition=self.staticMapsPosition,
                                                                        zoom=15,
                                                                        size='351*236',
                                                                        scale=2,
                                                                        traffic=0
                                                                        )

            if staticMapsInformation == "1":
                # 静态地图查询内容存在错误
                # 消息框初始化（自定义消息框）
                selfMessageBox = SelfMessageBox()
                # 自定义字体
                font = selfMessageBox.selfDefineFont()
                # 自定义消息等级
                level = selfMessageBox.messageLevel(4)
                # 消息框界面初始化
                selfMessageBox.initUI(self, font=font,
                                      level=level,
                                      title="静态地图查询提示",
                                      information="获取地图图片失败",
                                      icon=":/Error.png"
                                      )

            elif staticMapsInformation == "2":
                # 静态地图查询内容存在错误
                # 消息框初始化（自定义消息框）
                selfMessageBox = SelfMessageBox()
                # 自定义字体
                font = selfMessageBox.selfDefineFont()
                # 自定义消息等级
                level = selfMessageBox.messageLevel(4)
                # 消息框界面初始化
                selfMessageBox.initUI(self, font=font,
                                      level=level,
                                      title="静态地图查询提示",
                                      information="图片保存失败，请检查您的网络链接或是否有保存文件的权限",
                                      icon=":/Error.png"
                                      )

            elif staticMapsInformation == "3":
                # 地理位置信息查询失败
                # 消息框初始化（自定义消息框）
                selfMessageBox = SelfMessageBox()
                # 自定义字体
                font = selfMessageBox.selfDefineFont()
                # 自定义消息等级
                level = selfMessageBox.messageLevel(4)
                # 消息框界面初始化
                selfMessageBox.initUI(self, font=font,
                                      level=level,
                                      title="静态地图查询提示",
                                      information="您提供的地点信息查询失败，换个词进行搜索吧",
                                      icon=":/Error.png"
                                      )

            else:
                # 显示图片
                img = Image.open(staticMapsInformation)
                frame = ImageQt(img)
                pixmap = QPixmap.fromImage(frame)
                self.item = QGraphicsPixmapItem(pixmap)
                self.scene = QGraphicsScene()
                self.scene.addItem(self.item)
                self.staticMapsPhotoView.setScene(self.scene)

    # IP地址查询按钮事件处理器
    def get_ip_location_event_handler(self, ip):
        self.ip = ip

        # IP地址实例初始化
        ipLocationOperation = IPLocationOperation()
        IPFormatCheckResult = ipLocationOperation.check_ip_formation(self.ip)

        if IPFormatCheckResult == 1:
            IPInformation = ipLocationOperation.get_ip_information(self.ip)
            if 'error_context' in IPInformation:
                self.IPLocationResultTextEdit.setText(IPInformation['error_context'])

            else:
                # 在GUI窗口上显示获得的信息
                ipInformation = '\n'.join(IPInformation.values())
                self.IPLocationResultTextEdit.setText(ipInformation)

        elif IPFormatCheckResult == 2:
            selfMessageBox = SelfMessageBox()
            font = selfMessageBox.selfDefineFont()
            level = selfMessageBox.messageLevel(1)
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="IP输入提示",
                                  information="您输入的IP地址内容为空",
                                  icon=":/About.png"
                                  )

        else:
            selfMessageBox = SelfMessageBox()
            font = selfMessageBox.selfDefineFont()
            level = selfMessageBox.messageLevel(3)
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="IP输入提示",
                                  information="您输入的IP地址格式有误",
                                  icon=":/Warning.png"
                                  )

    def get_ip_location_from_host(self):
        # 获取本机IP
        ip = urllib.request.urlopen('http://ip.42.pl/raw').read()
        ip = str(ip).strip('b')

        # IP地址实例初始化
        ipLocationOperation = IPLocationOperation()
        IPInformation = ipLocationOperation.get_ip_information(eval(ip))
        if 'error_context' in IPInformation:
            self.IPLocationResultTextEdit.setText(IPInformation['error_context'])

        else:
            # 在GUI窗口上显示获得的信息
            ipInformation = '\n'.join(IPInformation.values())
            self.IPLocationResultTextEdit.setText(ipInformation)

    # 省份下拉选择框条目变化事件处理器
    def province_index_changed_event_handler(self):
        administrativeDistrictOperation = AdministrativeDistrictOperation()
        # 未选择省份
        if self.provinceComboBox.currentIndex() == 0:
            self.cityComboBox.setEnabled(False)
            self.cityComboBox.setCurrentIndex(0)

        else:
            # 选择省份
            indexText = self.provinceComboBox.currentText()
            administrativeList = administrativeDistrictOperation.get_sub_district(indexText)
            administrativeListLength = len(administrativeList)
            # 市区列表为空
            if administrativeListLength == 0:
                self.cityComboBox.setEnabled(False)

            # 市区列表不为空
            elif administrativeListLength > 0:
                self.cityComboBox.clear()
                self.cityComboBox.addItem("请选择城市")
                self.cityComboBox.addItems(administrativeList)
                self.cityComboBox.setEnabled(True)

    # 市区下拉选择框条目变化事件处理器
    def city_index_changed_event_handler(self):
        # 直筒子市
        no_county_or_district_city = ['东莞市', '中山市', '儋州市', '嘉峪关市']
        MunicipalityCity = ['北京市', '上海市', '天津市', '重庆市']
        administrativeDistrictOperation = AdministrativeDistrictOperation()
        # 未选择城市
        if self.cityComboBox.currentIndex() == 0:
            self.countyComboBox.setEnabled(False)
            self.countyComboBox.setCurrentIndex(0)

        # 已选择城市
        else:
            indexText = self.cityComboBox.currentText()
            # 直筒子市，不显示区县行政区域
            if indexText in no_county_or_district_city:
                self.countyComboBox.clear()
                self.countyComboBox.setEnabled(False)

            # 直辖市，不显示区县行政区域
            elif self.provinceComboBox.currentText() in MunicipalityCity:
                self.countyComboBox.clear()
                self.countyComboBox.setEnabled(False)

            # 不是直筒子市，显示行政区域
            else:
                administrativeList = administrativeDistrictOperation.get_sub_district(indexText)
                administrativeListLength = len(administrativeList)
                # 县/区列表为空
                if administrativeListLength == 0:
                    self.countyComboBox.setEnabled(False)

                # 县/区列表不为空
                elif administrativeListLength > 0:
                    self.countyComboBox.clear()
                    self.countyComboBox.addItem("请选择区/县")
                    self.countyComboBox.addItems(administrativeList)
                    self.countyComboBox.setEnabled(True)

    # 行政区域查询按钮点击事件处理器
    def administrative_search_button_event_handler(self):
        # 省份/城市/县/区名称
        provinceIndexText = self.provinceComboBox.currentText()
        cityIndexText = self.cityComboBox.currentText()
        countyIndexText = self.countyComboBox.currentText()

        # 下subdistrict级行政区域
        subdistrict = self.subDistrictNumComboBox.currentIndex()
        resultDistrict = ''

        if countyIndexText != "请选择区/县":
            resultDistrict = countyIndexText
        elif cityIndexText != "请选择城市":
            resultDistrict = cityIndexText
        elif provinceIndexText != "请选择省份":
            resultDistrict = provinceIndexText

        if resultDistrict == '':
            # 行政区域查询选择框未选择
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="行政区域查询提示",
                                  information="请您选择省份、城市、区/县后再查询",
                                  icon=":/About.png"
                                  )

        else:
            administrativeDistrictOperation = AdministrativeDistrictOperation()
            administrativeDistrictList = administrativeDistrictOperation.get_all_district_information(resultDistrict,
                                                                                                      subdistrict)
            administrativeDistrictInformation = '\n'.join(administrativeDistrictList)
            self.administrativeResultTextEdit.setText(administrativeDistrictInformation)

    # 天气查询按钮事件处理器
    def get_weather_information_event_handler(self, city):
        self.city = city
        weatherOperation = WeatherOperation()
        weatherFormatCheckResult = weatherOperation.check_weather_information(self.city)

        if weatherFormatCheckResult == 1:
            # 天气查询实例初始化
            weatherInformationList = weatherOperation.get_weather_information(city=self.city, weatherType='base')
            weatherInformation = '\n'.join(weatherInformationList)
            self.weatherResultTextEdit.setText(weatherInformation)

        elif weatherFormatCheckResult == 2:
            # 天气信息输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="天气输入提示",
                                  information="请您输入城市后再查询",
                                  icon=":/About.png"
                                  )

    def traffic_situation_index_changed_event_handler(self):
        # 获取当前页面索引
        trafficSituationPage = self.trafficRoadRealSituationComboBox.currentIndex()
        if trafficSituationPage == 0:
            self.trafficSituationStackedWidget.setCurrentIndex(0)
        elif trafficSituationPage == 1:
            self.trafficSituationStackedWidget.setCurrentIndex(1)
        elif trafficSituationPage == 2:
            self.trafficSituationStackedWidget.setCurrentIndex(2)
        elif trafficSituationPage == 3:
            self.trafficSituationStackedWidget.setCurrentIndex(3)

    # 交通态势省份下拉选择框条目变化事件处理器
    def traffic_province_index_changed_event_handler(self):
        administrativeDistrictOperation = AdministrativeDistrictOperation()

        # 未选择省份
        if self.trafficRealRoadProvinceComboBox.currentIndex() == 0:
            self.trafficRealRoadCityComboBox.setEnabled(False)
            self.trafficRealRoadCityComboBox.setCurrentIndex(0)

        else:
            # 选择省份
            indexText = self.trafficRealRoadProvinceComboBox.currentText()
            administrativeList = administrativeDistrictOperation.get_sub_district(indexText)
            administrativeListLength = len(administrativeList)
            # 市区列表为空
            if administrativeListLength == 0:
                self.trafficRealRoadCityComboBox.setEnabled(False)

            # 市区列表不为空
            elif administrativeListLength > 0:
                self.trafficRealRoadCityComboBox.clear()
                self.trafficRealRoadCityComboBox.addItem("请选择城市")
                self.trafficRealRoadCityComboBox.addItems(administrativeList)
                self.trafficRealRoadCityComboBox.setEnabled(True)

    def get_traffic_real_road_event_handler(self, roadName):
        self.roadName = roadName

        # 交通信息实例初始化
        trafficSituationOperation = TrafficSituationOperation()
        trafficSituationRealRoadCheckResult = trafficSituationOperation.check_real_road_information(self.roadName)

        if trafficSituationRealRoadCheckResult == 2:
            # 交通态势（道路实时路况）信息输入框内容为空
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="交通态势查询提示",
                                  information="请您输入道路名称后再查询",
                                  icon=":/About.png"
                                  )

        elif self.trafficRealRoadCityComboBox.currentIndex() == 0:
            # 交通态势（道路实时路况）下拉选择框未选择城市进行查询
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="交通态势查询提示",
                                  information="请您选择城市后再查询",
                                  icon=":/About.png"
                                  )

        else:
            # 获取选中的城市
            city = self.trafficRealRoadCityComboBox.currentText()

            # 获取交通态势（实时路况）图片信息
            position = str(city) + str(self.roadName)
            staticMapsOperation = StaticMapsOperation()
            staticMapsInformation = staticMapsOperation.get_static_maps(staticMapsPosition=position,
                                                                        zoom=11,
                                                                        size='224*193',
                                                                        scale=2,
                                                                        traffic=1
                                                                        )

            if staticMapsInformation not in ["1", "2", "3"]:
                # 显示图片
                img = Image.open(staticMapsInformation)
                frame = ImageQt(img)
                pixmap = QPixmap.fromImage(frame)
                self.item = QGraphicsPixmapItem(pixmap)
                self.scene = QGraphicsScene()
                self.scene.addItem(self.item)
                self.trafficRealReadRoadPhotoView.setScene(self.scene)

            # 获取描述信息
            if self.trafficRealRoadProvinceComboBox.currentText() == '北京市':
                city = '北京市'
            elif self.trafficRealRoadProvinceComboBox.currentText() == '上海市':
                city = '上海市'
            elif self.trafficRealRoadProvinceComboBox.currentText() == '天津市':
                city = '天津市'
            elif self.trafficRealRoadProvinceComboBox.currentText() == '重庆市':
                city = '重庆市'

            # 显示道路路况实时信息
            trafficSituationRealRoadList = trafficSituationOperation.get_traffic_situation_real_road_information(city,
                                                                                                                 self.roadName)
            trafficSituationRealRoadInformation = '\n'.join(trafficSituationRealRoadList)
            self.trafficSituationRealRoadTextEdit.setText(trafficSituationRealRoadInformation)

    # 设置按钮

    # 这里有一些异常发生，将在未来的某一个版本进行修复
    # There are some exceptions occurring here that will be fixed in a future release
    # def getTrafficPolygonRoadEventHandler(self, positionBottomLeft, positionTopRight):
    #     self.positionBottomLeft = positionBottomLeft
    #     self.positionTopRight = positionTopRight
    #
    #     roadLevelIndex = self.trafficRectangleRoadLevelComboBox.currentIndex()
    #
    #     # 交通态势初始化
    #     trafficSituationOperation = TrafficSituationOperation()
    #     positionBottomLeftCheckedResult = trafficSituationOperation.checkRectanglePositionInformation(
    #         self.positionBottomLeft)
    #     positionTopRightCheckedResult = trafficSituationOperation.checkRectanglePositionInformation(
    #         self.positionTopRight)
    #     if positionBottomLeftCheckedResult == 2:
    #         # 交通态势（矩形区域实时路况）信息输入框（左下角区域）内容为空
    #         # 消息框初始化（自定义消息框）
    #         selfMessageBox = SelfMessageBox()
    #         # 自定义字体
    #         font = selfMessageBox.selfDefineFont()
    #         # 自定义消息等级
    #         level = selfMessageBox.messageLevel(1)
    #         # 消息框界面初始化
    #         selfMessageBox.initUI(self, font=font,
    #                               level=level,
    #                               title="交通态势查询提示",
    #                               information="请您输入具体位置信息后再查询",
    #                               icon=":/About.png"
    #                               )
    #
    #     elif positionTopRightCheckedResult == 2:
    #         # 交通态势（矩形区域实时路况）信息输入框（右上角区域）内容为空
    #         # 消息框初始化（自定义消息框）
    #         selfMessageBox = SelfMessageBox()
    #         # 自定义字体
    #         font = selfMessageBox.selfDefineFont()
    #         # 自定义消息等级
    #         level = selfMessageBox.messageLevel(1)
    #         # 消息框界面初始化
    #         selfMessageBox.initUI(self, font=font,
    #                               level=level,
    #                               title="交通态势查询提示",
    #                               information="请您输入具体位置信息后再查询",
    #                               icon=":/About.png"
    #                               )
    #
    #     elif positionBottomLeftCheckedResult and positionTopRightCheckedResult:
    #         # 中文地理位置名称转换为高德地图地理位置名称
    #         geographicPositionBottomLeft = trafficSituationOperation.getGeographicCodingPosition(
    #             self.positionBottomLeft)
    #         geographicPositionTopRight = trafficSituationOperation.getGeographicCodingPosition(self.positionTopRight)
    #
    #         if geographicPositionBottomLeft == "1" or geographicPositionTopRight == "1":
    #             # 步行路径规划起点输入框内容为空
    #             # 消息框初始化（自定义消息框）
    #             selfMessageBox = SelfMessageBox()
    #             # 自定义字体
    #             font = selfMessageBox.selfDefineFont()
    #             # 自定义消息等级
    #             level = selfMessageBox.messageLevel(1)
    #             # 消息框界面初始化
    #             selfMessageBox.initUI(self, font=font,
    #                                   level=level,
    #                                   title="交通态势查询提示",
    #                                   information="您提供的地点信息查询失败，换个词进行搜索吧",
    #                                   icon=":/About.png"
    #                                   )
    #         else:
    #             # 计算中心点
    #             # 数据处理
    #             # 将高德地图字符串格式数据转换成计算格式的数据
    #             BottomLeft = geographicPositionBottomLeft.split(',')
    #             TopRight = geographicPositionTopRight.split(',')
    #             # 矩形区域左下角坐标元素
    #             BottomLeftList = []
    #             # 矩形区域右上角坐标元素
    #             TopRightList = []
    #             # 将字符串数据转换成float浮点数格式数据
    #             for item in BottomLeft:
    #                 item = float(item)
    #                 BottomLeftList.append(item)
    #             for item in TopRight:
    #                 item = float(item)
    #                 TopRightList.append(item)
    #             # 将列表数据转换成元组数据，以进行计算
    #             BottomLeftList = tuple(BottomLeftList)
    #             TopRightList = tuple(TopRightList)
    #             geographicPositionList = [BottomLeftList, TopRightList]
    #             # 获取中心点
    #             geographicPositionCenter = trafficSituationOperation.getCenterGeographicPosition(geographicPositionList)
    #             # 将中心点的元组数据转换成字符串数据，并保留小数点后六位
    #             geographicPositionCenterList = []
    #             for item in geographicPositionCenter:
    #                 item = '{:.6f}'.format(item)
    #                 geographicPositionCenterList.append(item)
    #             geographicPositionCenter = ','.join(geographicPositionCenterList)
    #
    #             # 获取描述信息
    #             trafficSituationRectangleRoadList = trafficSituationOperation.getTrafficSituationRectangleRoadInformation(
    #                 geographicPositionBottomLeft, geographicPositionTopRight, roadLevelIndex)
    #             trafficSituationRectangleInformation = ''
    #             for item in trafficSituationRectangleRoadList:
    #                 trafficSituationRectangleInformation = trafficSituationRectangleInformation + item + '\n'
    #             self.trafficRectangleRoadTextEdit.setText(trafficSituationRectangleInformation)
    #
    #             # 获取中心点对应的图片信息
    #             staticMapsOperation = StaticMapsOperation()
    #             staticMapsInformation = staticMapsOperation.getStaticMapsbyLocation(
    #                 staticMapsPosition=geographicPositionCenter,
    #                 zoom=12,
    #                 size='224*193',
    #                 scale=2,
    #                 traffic=1
    #             )
    #
    #             # 显示图片
    #             if staticMapsInformation not in ["1", "2", "3"]:
    #                 img = Image.open(staticMapsInformation)
    #                 frame = ImageQt(img)
    #                 pixmap = QPixmap.fromImage(frame)
    #                 self.item = QGraphicsPixmapItem(pixmap)
    #                 self.scene = QGraphicsScene()
    #                 self.scene.addItem(self.item)
    #                 self.trafficRectangleReadRoadPhotoView.setScene(self.scene)

    # 交通信息分析系统信息开始获取按钮事件处理器
    def analysis_system_start_event_handler(self, RoadNameList):
        self.RoadNameList = RoadNameList

        # 按钮已经按下，不要再重复按键
        if self.flagStart:
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="交通态势系统提示",
                                  information="程序已经在运行中",
                                  icon=":/About.png"
                                  )

        else:
            # 设置按钮按下状态
            self.flagStart = True
            # 获取当前显示的内容
            currentContext = self.trafficSituationAnalysisSystemTextEdit.toPlainText()
            currentContextList = currentContext.split("===================")
            # 清空显示的内容
            self.trafficSituationAnalysisSystemTextEdit.clear()
            # 内容为空，直接显示结果
            if currentContext == '':
                self.trafficSituationAnalysisSystemTextEdit.setText("数据采集情况\n程序在后台获取数据中\n")
            # 之前存在数据
            elif currentContextList[0]:
                currentContextList[0] = "数据采集情况\n程序在后台获取数据中\n"
                currentContext = '==================='.join(currentContextList)
                self.trafficSituationAnalysisSystemTextEdit.setText(currentContext)
            else:
                self.trafficSituationAnalysisSystemTextEdit.setText(
                    "数据采集情况\n程序在后台获取数据中\n===================\n{0}".format(currentContext))
            self.thread = GetTrafficData(self.RoadNameList)
            self.thread.signal.connect(self.callback)  # 连接回调函数，接收结果
            self.thread.start()

    def analysis_system_stop_event_handler(self):
        if self.flagStart:
            self.thread.stop()
            # 获取当前显示的内容
            currentContext = self.trafficSituationAnalysisSystemTextEdit.toPlainText()
            currentContextList = currentContext.split("===================")
            # 清空显示的内容
            self.trafficSituationAnalysisSystemTextEdit.clear()
            # 内容为空，直接显示结果
            if currentContext == '':
                self.trafficSituationAnalysisSystemTextEdit.setText("数据采集情况\n数据获取完成\n")
            # 之前存在数据
            elif currentContextList[0]:
                currentContextList[0] = "数据采集情况\n数据获取完成\n"
                currentContext = '==================='.join(currentContextList)
                self.trafficSituationAnalysisSystemTextEdit.setText(currentContext)
            else:
                self.trafficSituationAnalysisSystemTextEdit.setText(
                    "数据采集情况\n数据获取完成\n===================\n{0}".format(currentContext))
            # 取消按钮按下状态
            self.flagStart = False

        else:
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="交通态势系统提示",
                                  information="程序尚未运行",
                                  icon=":/About.png"
                                  )

    # 回调函数
    def callback(self, msg):
        self.msg = msg

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Traffic Data batch Operation Successfully get'
                              )
        # 文件中输出回调信息
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context=self.msg
                              )

    # 交通态势信息查看事件处理器
    def analysis_system_view_event_handler(self):
        # 获取下拉框选择的城市信息
        currentCity = self.trafficSituationAnalysisSystemCityComboBox.currentText()

        if currentCity == '请选择城市':
            # 消息框初始化（自定义消息框）
            selfMessageBox = SelfMessageBox()
            # 自定义字体
            font = selfMessageBox.selfDefineFont()
            # 自定义消息等级
            level = selfMessageBox.messageLevel(1)
            # 消息框界面初始化
            selfMessageBox.initUI(self, font=font,
                                  level=level,
                                  title="交通态势系统提示",
                                  information="请选择具体的城市再查询",
                                  icon=":/About.png"
                                  )

        else:
            # 读取Excel具体内容
            trafficInformationReadOperation = TrafficInformationReadOperation()
            # 读取excel具体信息
            result = trafficInformationReadOperation.read_excel_xls(currentCity)

            wholeDataLength = int(result['wholeDataLength'])
            effectiveDataLength = int(result['effectiveDataLength'])
            percentContext = result['percentContext']

            # 数据颜色填充
            data = {"拥堵": (effectiveDataLength, QtGui.QColor("#FFFF7F"), QtGui.QColor("#E74856")),
                    "畅通": (wholeDataLength - effectiveDataLength, QtGui.QColor("#7FBF7F"), QtGui.QColor("#0078D4"))
                    }

            series = QtChart.QPieSeries()
            series.setPieSize(0.7)

            # 设置字体样式
            font = QtGui.QFont()
            font.setFamily("微软雅黑 Light")
            font.setPointSize(14)

            for name, (value, color, borderColor) in data.items():
                sliceItem = series.append(name, value)
                sliceItem.setBorderColor(borderColor)
                sliceItem.setLabel("{0}情况".format(name))
                sliceItem.setLabelFont(font)
                sliceItem.setLabelVisible(True)
                sliceItem.setBrush(color)

            # 创建图表
            chart = QtChart.QChart()
            chart.setBackgroundVisible(False)
            chart.addSeries(series)
            # 设置标题
            chart.setFont(font)
            chart.setTitle("山西省{0}的道路通行情况通行数据统计".format(currentCity))
            chart.setTitleFont(font)
            # 设置标签
            chart.legend().setAlignment(QtCore.Qt.AlignBottom)
            chart.legend().setFont(font)

            self.trafficSituationAnalysisSystemPhoto.setChart(chart)

            # 设置文字模块
            currentContext = self.trafficSituationAnalysisSystemTextEdit.toPlainText()
            currentContextList = currentContext.split("===================")
            currentContextListLength = len(currentContextList)
            # 清空之前的内容
            self.trafficSituationAnalysisSystemTextEdit.clear()
            # 内容为空，直接显示结果
            if currentContext == '':
                self.trafficSituationAnalysisSystemTextEdit.setText("道路通行分析\n{0}".format(percentContext))
            # 之前存在数据
            elif currentContextListLength > 1:
                currentContextList[1] = "道路通行分析\n" + percentContext
                currentContext = '==================='.join(currentContextList)
                self.trafficSituationAnalysisSystemTextEdit.setText(currentContext)
            # 内容不为空，同时打印前面的内容（追加显示）
            else:
                self.trafficSituationAnalysisSystemTextEdit.append(
                    "{0}===================\n{1}".format(currentContext, percentContext))
