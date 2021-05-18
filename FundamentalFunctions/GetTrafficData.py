import inspect
import time

from PyQt5.QtCore import QThread, pyqtSignal
from apscheduler.schedulers.blocking import BlockingScheduler

from AmapFunctions.TrafficSituationByBaiduMap import TrafficSituationByBaiduMap
from FundamentalFunctions.TrafficInformationExecuteOperation import TrafficInformationWriteOperation
from logrecord.WriteLog import WriteLog


class GetTrafficData(QThread):
    """
    Class:批量获取交通数据（新线程）
    """
    # 定义信号
    signal = pyqtSignal(str)

    def __init__(self, RoadNameList, parent=None):
        super(GetTrafficData, self).__init__()
        self.trafficSituationByBaiduMap = TrafficSituationByBaiduMap()
        self.flag = 1  # 自定义开关变量
        # 初始化创建excel数据表
        self.RoadNameList = RoadNameList
        self.trafficInformationSavingOperation = TrafficInformationWriteOperation(self.RoadNameList)

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    def __del__(self):
        self.wait()

    def run(self) -> None:
        """
        进行多线程任务操作，主要的逻辑操作,返回结果
        """

        self.flag = 1

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 定时运行
        scheduler = BlockingScheduler()
        # 每天定时在6-23点执行
        scheduler.add_job(func=self.job, trigger='cron', month='*', day='*', hour='6-23', minute='0')
        scheduler.start()
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - Successfully Start'.format(
                                  function_name)
                              )

    def job(self) -> None:
        """
        函数：程序具体运行内容
        """

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - Data get Time:{1}'.format(
                                  function_name,
                                  time.asctime(time.localtime(time.time())))
                              )

        for road in self.RoadNameList:
            if self.flag == 1:
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=1,
                                      context='Function name:{0} - Successfully Executed'.format(
                                          function_name)
                                      )

                # 依次遍历每一个城市
                # 城市名称
                cityName = road
                roadName = self.RoadNameList[cityName]
                for item in roadName:
                    if self.flag == 1:
                        # 获取实时路况信息
                        resultInformation = self.trafficSituationByBaiduMap.get_traffic_situation_by_road(
                            road_name=item, city=cityName)
                        # 将获取的路况信息保存到excel数据库文件中
                        self.trafficInformationSavingOperation.write_to_excel(cityName, resultInformation)
                        time.sleep(3)
                    else:
                        self.flag = 0

            else:
                self.signal.emit("successfully Saved")

    # 重写程序停止运行
    def stop(self) -> None:
        self.flag = 0
