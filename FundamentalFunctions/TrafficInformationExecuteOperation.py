import inspect
import os
import time

import xlrd  # 读取excel文件
import xlwt  # 写入excel文件
from xlutils.copy import copy
from xlwt import XFStyle

from logrecord.WriteLog import WriteLog


class TrafficInformationWriteOperation:
    """
    Class:交通信息执行操作
    """

    def __init__(self, RoadNameList):
        self.file_path = None
        self.font_style = None
        self.name = None
        self.height = None
        self.bold = None
        self.path = None
        self.sheet_name = None
        self.value = None
        self.cityName = None
        self.resultInformation = None
        self.path = None
        self.RoadNameList = RoadNameList
        self.sheet_init()

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    def sheet_init(self) -> None:
        """
        函数：单元表格初始化
        """

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

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

        # 数据目录
        data_directory = '\\'.join([temp_directory, 'Data'])
        # 目录不存在，创建
        if not os.path.exists(data_directory):
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - directory successfully created'.format(function_name)
                                  )
            os.mkdir(data_directory)

        # 文件绝对路径
        list_filename = [data_directory, 'TrafficInformation.XLS']
        self.file_path = '\\'.join(list_filename)

        # 字体样式
        self.font_style = self.set_style('微软雅黑 Light', 12 * 20, False)

        # 文件不存在，创建并初始化excel表格文件
        if not os.path.exists(self.file_path):
            book = xlwt.Workbook(encoding='utf-8')
            # cell_overwrite_ok=True表示一个单元格可以被多次覆盖写入
            # 标题行
            row_head = [['日期', '时间', '状态码', '响应信息', '道路名称', '路况语义化描述', '路况整体评价', '路况整体评价的语义化描述',
                         '路段拥堵语义化描述', '路段拥堵评价', '平均通行速度', '拥堵距离', '较10分钟前拥堵趋势'
                         ]]
            # 初始化单元格
            for city in self.RoadNameList:
                book.add_sheet(city)
            book.save(self.file_path)
            time.sleep(3)
            # 初始化单元格每一个标题
            for city in self.RoadNameList:
                self.write_excel_xls_append(self.file_path, city, row_head)

    # 设置字体样式
    def set_style(self, name: str,
                  height: int,
                  bold: bool = False
                  ) -> XFStyle:
        """
        函数：设置字体的表格样式
        Args:
            name: 字体的名称
            height: 字体的大小
            bold: 表格的字体是否为粗体
        Returns: 表格的字体格式对象
        """

        self.name = name
        self.height = height
        self.bold = bold

        style = xlwt.XFStyle()
        font = xlwt.Font()
        font.name = self.name
        font.bold = self.bold
        font.color_index = 4
        font.height = self.height

        global rows_num

        style.font = font
        return style

    def write_excel_xls(self, path: str,
                        sheet_name: str,
                        value: list
                        ) -> None:
        """
        函数：向excel中写入数据
        Args:
            path: 文件路径
            sheet_name: 表格名称
            value: 要写入的内容
        """

        self.path = path
        self.sheet_name = sheet_name
        self.value = value

        index = len(self.value)  # 获取需要写入数据的行数
        workbook = xlwt.Workbook()  # 新建一个工作簿
        sheet = workbook.add_sheet(self.sheet_name, cell_overwrite_ok=True)  # 在工作簿中新建一个表格
        for i in range(0, index):
            for j in range(0, len(self.value[i])):
                sheet.write(i, j, self.value[i][j])  # 像表格中写入数据（对应的行和列）
        workbook.save(self.path)  # 保存工作簿

    def write_excel_xls_append(self, path: str,
                               sheet_name: str,
                               value: list
                               ) -> None:
        """
        函数：向excel中追加写入数据
        Args:
            path: 文件路径
            sheet_name: 表格名称
            value: 要写入的内容
        """
        self.path = path
        self.sheet_name = sheet_name
        self.value = value

        index = len(self.value)  # 获取需要写入数据的行数
        workbook = xlrd.open_workbook(self.path)  # 打开工作簿
        # sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(self.sheet_name)  # 获取工作簿中所有表格中的的sheet_name表格
        rows_old = worksheet.nrows  # 获取表格中已存在的数据的行数
        new_workbook = copy(workbook)  # 将xlrd对象拷贝转化为xlwt对象
        new_worksheet = new_workbook.get_sheet(self.sheet_name)  # 获取转化后工作簿中的sheet_name表格
        for i in range(0, index):
            for j in range(0, len(self.value[i])):
                new_worksheet.write(i + rows_old, j, self.value[i][j])  # 追加写入数据，注意是从i+rows_old行开始写入
        new_workbook.save(self.path)  # 保存工作簿

    def write_to_excel(self, cityName: str,
                       resultInformation: dict
                       ) -> None:
        """
        将获取到的数据写入excel文件中
        Args:
            cityName: 城市名称，对应sheet_name
            resultInformation: 获取到的数据
        """

        self.cityName = cityName
        self.resultInformation = resultInformation

        # 写入表格的内容
        writeList = []

        # 写入数据
        # 1.获取当前系统的日期
        local_date = time.strftime("%Y-%m-%d", time.localtime())
        writeList.append(local_date)
        # 2.获取当前系统的时间
        local_time = time.strftime("%H:%M:%S", time.localtime())
        writeList.append(local_time)
        # 3.状态码
        if 'status' in resultInformation:
            status = resultInformation['status']
            writeList.append(status)
        # 4.响应信息
        if 'message' in resultInformation:
            message = resultInformation['message']
            writeList.append(message)
        # 5.道路名称
        if 'road_traffic' in resultInformation:
            road_traffic = resultInformation['road_traffic'][0]
            if 'road_name' in road_traffic:
                road_name = road_traffic['road_name']
                writeList.append(road_name)
        # 6.路况语义化描述
        if 'description' in resultInformation:
            description = resultInformation['description']
            writeList.append(description)
        if 'evaluation' in resultInformation:
            evaluation = resultInformation['evaluation']
            # 7.路况整体评价
            if 'status' in evaluation:
                status = evaluation['status']
                writeList.append(status)
            # 8.路况整体评价的语义化描述
            if 'status_desc' in evaluation:
                status_desc = evaluation['status_desc']
                writeList.append(status_desc)
        if 'road_traffic' in resultInformation:
            road_traffic = resultInformation['road_traffic'][0]
            if 'congestion_sections' in road_traffic:
                congestion_sections = road_traffic['congestion_sections'][0]
                # 9.路段拥堵语义化描述
                if 'section_desc' in congestion_sections:
                    section_desc = congestion_sections['section_desc']
                    writeList.append(section_desc)
                # 10.路段拥堵评价
                if 'status' in congestion_sections:
                    status = congestion_sections['status']
                    writeList.append(status)
                # 11.平均通行速度
                if 'speed' in congestion_sections:
                    speed = congestion_sections['speed']
                    writeList.append(speed)
                # 12.拥堵距离
                if 'congestion_distance' in congestion_sections:
                    congestion_distance = congestion_sections['congestion_distance']
                    writeList.append(congestion_distance)
                # 13.较10分钟前拥堵趋势
                if 'congestion_trend' in congestion_sections:
                    congestion_trend = congestion_sections['congestion_trend']
                    writeList.append(congestion_trend)

        self.write_excel_xls_append(self.file_path, cityName, [writeList])


class TrafficInformationReadOperation:
    def __init__(self):
        self.path = None

    def read_excel_xls(self, sheet_name: str
                       ) -> dict:
        """
        函数：读取excel文件内容
        Args:
            sheet_name: 表格名称
        Returns:
            返回获取的状态信息
        """

        # 文件保存路径
        local_appdata_directory = os.getenv('LOCALAPPDATA')
        # 根目录
        temp_directory = '\\'.join([local_appdata_directory, 'AmapProgram'])
        # 数据目录
        data_directory = '\\'.join([temp_directory, 'Data'])
        # 文件绝对路径
        list_filename = [data_directory, 'TrafficInformation.XLS']
        self.path = '\\'.join(list_filename)

        # 输出结果
        resultDict = {}

        workbook = xlrd.open_workbook(self.path)  # 打开工作簿
        # sheets = workbook.sheet_names()  # 获取工作簿中的所有表格
        worksheet = workbook.sheet_by_name(sheet_name)  # 获取工作簿中所有表格中的的sheet_name表格

        wholeDataLength = 0
        effectiveDataLength = 0
        # 统计获取的数据个数
        for i in range(1, worksheet.nrows):
            if worksheet.cell_value(i, 6):
                wholeDataLength = wholeDataLength + 1

        # 统计有效值数据个数
        for i in range(1, worksheet.nrows):
            if worksheet.cell_value(i, 9) != '':
                effectiveDataLength = effectiveDataLength + 1

        # 道路通行状况语言描述
        percent = float(effectiveDataLength / wholeDataLength * 100)

        resultDict.update(effectiveDataLength=effectiveDataLength)
        resultDict.update(wholeDataLength=wholeDataLength)
        resultDict.update(percent=percent)

        if 0 <= percent < 10:
            resultDict.update(percentContext="该城市道路拥堵占比{0:.2f}%，基本上没有拥堵路段，请继续保持".format(percent))
        elif 10 <= percent < 30:
            resultDict.update(percentContext="该城市道路拥堵占比{0:.2f}%，有较少路段经常发生拥堵，请继续保持".format(percent))
        elif 30 <= percent < 50:
            resultDict.update(percentContext="该城市道路拥堵占比{0:.2f}%，有部分路段经常发生拥堵，建议您绕行这部分路段".format(percent))
        elif 50 <= percent < 75:
            resultDict.update(percentContext="该城市道路拥堵占比{0:.2f}%，有大部分路段经常发生拥堵，建议您合理安排出行计划，避开拥堵路段".format(percent))
        elif 75 <= percent < 100:
            resultDict.update(percentContext="该城市道路拥堵占比{0:.2f}%，经常发生拥堵，建议您采取其他方式或乘坐公共交通出行，以免耽误您的出行计划".format(percent))

        return resultDict
