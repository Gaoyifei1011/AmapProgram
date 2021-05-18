# -*- coding:utf-8 -*-
# 导入的库
import inspect
import json
import os
import re
import urllib.request
from http.client import IncompleteRead, RemoteDisconnected
from urllib.error import HTTPError, URLError

import requests

from SelfExpection.CustomExpection import CustomExpection
from SelfExpection.StringFormatException import StringFormatException
from logrecord.WriteLog import WriteLog


class StaticMaps:
    """
    Class:静态地图
    静态地图服务通过返回一张地图图片响应HTTP请求，使用户能够将高德地图以图片形式嵌入自己的网页中。用户可以指定请求的地图位置、图片大小、以及在地图上添加覆盖物，如标签、标注、折线、多边形。
    """

    def __init__(self):
        self.location = None
        self.zoom = None
        self.scale = None
        self.size = None
        self.markers = None
        self.labels = None
        self.traffic = None
        self.paths = None
        self.check_result = None
        self.url = None
        self.filename = None
        self.fillColor = None
        self.fill_transparency = None
        self.num_retries = None
        self.color = None
        self.color = None
        self.label = None
        self.content = None
        self.font = None
        self.bold = None
        self.fontSize = None
        self.fontColor = None
        self.background = None
        self.rgbColor = None
        self.transparency = None
        self.weight = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    # 获取高德地图数据API的钥匙
    APIkey = '<请自己输入自己申请的API Key>'
    fileItem = 1

    def check_static_maps_url(self, location: str,
                              zoom: int,
                              **kwargs
                              ) -> bool:

        """
        函数：检测静态地图数据
        Args:
            location:地图中心点，部分条件必填。中心点坐标。规则：经度和纬度用","分隔 经纬度小数点后不得超过6位。
            zoom:地图级别，必填。地图缩放级别:[1,17]
            **kwargs:
                size:地图大小，必填，默认400*400。图片宽度*图片高度。最大值为1024*1024
                scale:普通/高清，可选，默认1。1:返回普通图；2:调用高清图，图片高度和宽度都增加一倍，zoom也增加一倍（当zoom为最大值时，zoom不再改变）。
                traffic:交通路况标识，可选，默认0。底图是否展现实时路况。 可选值： 0，不展现；1，展现。
                markers:标注，可选。使用规则见markers详细说明，标注最大数10个
                labels:标签，可选。使用规则见labels详细说明，标签最大数10个
                paths:折线，可选。使用规则见paths详细说明，折线和多边形最大数4个
            注：如果有标注/标签/折线等覆盖物，则中心点（location）和地图级别（zoom）可选填。当请求中无location值时，地图区域以包含请求中所有的标注/标签/折线的几何中心为中心点；如请求中无zoom，地图区域以包含请求中所有的标注/标签/折线为准，系统计算出zoom值。
        Returns:返回数据的检测格式是否符合要求
        """

        self.location = location
        self.zoom = zoom

        if 'markers' in kwargs:
            self.markers = kwargs['markers']
        if 'labels' in kwargs:
            self.labels = kwargs['labels']
        if 'paths' in kwargs:
            self.paths = kwargs['paths']
        if 'scale' in kwargs:
            self.scale = kwargs['scale']
        if 'size' in kwargs:
            self.size = kwargs['size']
        if 'traffic' in kwargs:
            self.traffic = kwargs['traffic']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': self.APIkey,
                      'location': self.location,
                      'zoom': self.zoom
                      }

        if self.markers is not None:
            parameters.update(markers=self.markers)
        if self.labels is not None:
            parameters.update(labels=self.labels)
        if self.paths is not None:
            parameters.update(paths=self.paths)
        if self.size is not None:
            parameters.update(size=self.size)
        if self.scale is not None:
            parameters.update(scale=self.scale)
        if self.traffic is not None:
            parameters.update(traffic=self.traffic)

        # 获取数据
        try:
            request_information = requests.get("https://restapi.amap.com/v3/staticmap?parameters",
                                               params=parameters)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - request_information:{1}'.format(function_name,
                                                                                               request_information)
                                  )
            request_information.close()  # 关闭访问
            request_information.raise_for_status()  # 如果响应状态码不是 200，就主动抛出异常
            json.loads(request_information.text)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - Json data error.'.format(
                                      function_name)
                                  )
            raise CustomExpection

        except requests.RequestException as e:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,
                                                                                        e.__class__.__name__)
                                  )
            exit(0)

        except json.decoder.JSONDecodeError as e:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,
                                                                                        e.__class__.__name__)
                                  )
            return True

        except CustomExpection as e:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,

                                                                                        e.__class__.__name__)
                                  )
            return False

        except Exception as e:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=5,
                                  context='Function name:{0} - {1} has occured.'.format(function_name,
                                                                                        e.__class__.__name__)
                                  )
            return False

    def get_static_maps_url(self, location: str,
                            zoom: int,
                            check_result: bool,
                            size: str = '400*400',
                            scale: int = 1,
                            traffic: int = 0,
                            **kwargs
                            ) -> str:

        """
        函数：获取静态地图数据
        Args:
            location:地图中心点，部分条件必填。中心点坐标。规则：经度和纬度用","分隔 经纬度小数点后不得超过6位。
            zoom:地图级别，必填。地图缩放级别:[1,17]
            check_result:数据的检测格式符合要求标志
            size:地图大小，必填，默认400*400。图片宽度*图片高度。最大值为1024*1024
            scale:普通/高清，可选，默认1。1:返回普通图；2:调用高清图，图片高度和宽度都增加一倍，zoom也增加一倍（当zoom为最大值时，zoom不再改变）。
            kwargs:
                markers:标注，可选。使用规则见markers详细说明，标注最大数10个
                labels:标签，可选。使用规则见labels详细说明，标签最大数10个
                paths:折线，可选。使用规则见paths详细说明，折线和多边形最大数4个
            traffic:交通路况标识，可选，默认0。底图是否展现实时路况。 可选值： 0，不展现；1，展现。
            注：如果有标注/标签/折线等覆盖物，则中心点（location）和地图级别（zoom）可选填。当请求中无location值时，地图区域以包含请求中所有的标注/标签/折线的几何中心为中心点；如请求中无zoom，地图区域以包含请求中所有的标注/标签/折线为准，系统计算出zoom值。
        Returns:返回获得的json格式数据或错误信息
        """

        # TODO:未来版本将返回数据从str升级为dict
        self.location = location
        self.zoom = zoom
        self.check_result = check_result
        self.size = size
        self.scale = scale
        self.traffic = traffic

        if 'markers' in kwargs:
            self.markers = kwargs['markers']
        if 'labels' in kwargs:
            self.labels = kwargs['labels']
        if 'paths' in kwargs:
            self.paths = kwargs['paths']
        if 'scale' in kwargs:
            self.scale = kwargs['scale']
        if 'size' in kwargs:
            self.size = kwargs['size']
        if 'traffic' in kwargs:
            self.traffic = kwargs['traffic']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 传入参数
        parameters = {'key': self.APIkey,
                      'location': self.location,
                      'zoom': self.zoom,
                      }

        if self.markers is not None:
            parameters.update(markers=self.markers)
        if self.labels is not None:
            parameters.update(labels=self.labels)
        if self.paths is not None:
            parameters.update(paths=self.paths)
        if self.size is not None:
            parameters.update(size=self.size)
        if self.scale is not None:
            parameters.update(scale=self.scale)
        if self.traffic is not None:
            parameters.update(traffic=self.traffic)

        # 获取数据
        if check_result:
            request_information = requests.get("https://restapi.amap.com/v3/staticmap?parameters",
                                               params=parameters)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - request successfully'.format(function_name)
                                  )
            request_information.close()  # 关闭访问
            return request_information.url
        else:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - request failed'.format(function_name)
                                  )
            return 'Error'

    def parse_static_maps_url(self, url: str
                              ) -> str:
        """
        函数：解析图片网页链接
        Args:
            url:网页图片链接
        """

        # TODO:未来版本将返回数据从str升级为dict
        self.url = url

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # TODO:优化代码，递归创建目录
        # 图片保存的位置
        local_appdata_directory = os.getenv('LOCALAPPDATA')
        temp_directory = '\\'.join([local_appdata_directory, 'AmapProgram'])
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - windows temp directory:{1}'.format(function_name,
                                                                                              temp_directory)
                              )

        # 目录不存在，创建
        if not os.path.exists(temp_directory):
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - directory successfully created'.format(function_name)
                                  )
            os.mkdir(temp_directory)

        # Photo目录文件夹
        list_photo = [temp_directory, 'StaticMaps']
        photo_directory = '\\'.join(list_photo)
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - photo directory:{1}'.format(function_name,
                                                                                       temp_directory)
                              )

        # 目录不存在，创建
        if not os.path.exists(photo_directory):
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - directory successfully created'.format(function_name)
                                  )
            os.mkdir(photo_directory)

        # 文件绝对路径
        list_filename = [photo_directory, 'StaticMap{0}.png'.format(StaticMaps.fileItem)]
        filename = '\\'.join(list_filename)
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - file name:{1}'.format(function_name,
                                                                                 filename)
                              )

        # 保存图片
        savePhotoResult = self.save_photo(self.url, filename=filename)
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=6,
                              context='Function name:{0} - photo successfully saved in local directory.'.format(
                                  function_name)
                              )

        if savePhotoResult:
            # 图片保存成功，返回图片保存的文件位置信息
            return filename
        else:
            return "Error"

    def save_photo(self, url: str,
                   filename: str,
                   num_retries: int = 3
                   ) -> bool:
        """
        函数：将网页url对应的图片保存到本地目录下
        Args:
            url:网页图片连接
            filename:保存到本地图片的位置
            num_retries:重连次数
        """

        self.url = url
        self.filename = filename
        self.num_retries = num_retries

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        img_src = self.url

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - img_src:{1}'.format(function_name,
                                                                               img_src)
                              )
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - file name:{1}'.format(function_name,
                                                                                 self.filename)
                              )

        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) \
                AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/35.0.1916.114 Safari/537.36',
            'Cookie': 'AspxAutoDetectCookieSupport=1'
        }
        # Request类可以使用给定的header访问URL
        result = urllib.request.Request(url=img_src, headers=header)

        try:
            response = urllib.request.urlopen(result, timeout=15)  # 得到访问的网址
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=6,
                                  context='Function name:{0} - response successfully'.format(function_name)
                                  )

            # 保存图片文件
            with open(self.filename, 'wb') as file:
                content = response.read()  # 获得图片
                file.write(content)  # 保存图片
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=6,
                                      context='Function name:{0} - picture saved successfully'.format(function_name)
                                      )
                return True

        except HTTPError as e:  # HTTP响应异常处理
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - error reason:{1}'.format(function_name,
                                                                                        e.reason)
                                  )
            return False

        except URLError as e:  # 一定要放到HTTPError之后，因为它包含了前者
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - error reason:{1}'.format(function_name,
                                                                                        e.reason)
                                  )
            return False

        except IncompleteRead or RemoteDisconnected:
            if self.num_retries == 0:  # 重连机制
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=1,
                                      context='Function name:{0} - retries time:{1}'.format(function_name,
                                                                                            self.num_retries)
                                      )
                return False

            else:
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=1,
                                      context='Function name:{0} - retries time:{1}'.format(function_name,
                                                                                            self.num_retries)
                                      )
                self.save_photo(self.url, self.filename, self.num_retries - 1)

    def user_define_markers(self, location: str,
                            size: str = 'small',
                            color: str = '0xFC6054',
                            **kwargs,
                            ) -> str:
        """
        函数：自定义标注
        Args:
            location:地理位置坐标
            size:自定义标注的大小，可选值： small,mid,large，默认为small
            color:自定义标注的颜色，选值范围：[0x000000, 0xffffff]，默认为0xFC6054
            kwargs:
                label:[0-9]、[A-Z]、[单个中文字] 当size为small时，图片不展现标注名。
        Returns:返回格式化后的单个marker字符串
        """

        self.size = size
        self.color = color
        self.location = location

        if 'label' in kwargs:
            self.label = kwargs['label']
        else:
            self.label = ''

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        try:
            # 检测字符格式正误
            if not self.is_rgb_color(self.color):
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - exception:StringFormatException'.format(
                                          function_name)
                                      )
                raise StringFormatException

            if not self.is_label(self.label):
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - exception:StringFormatException'.format(
                                          function_name)
                                      )
                raise StringFormatException

            list_location = self.location.split(";")
            for item in list_location:
                if not self.is_location(item):
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=3,
                                          context='Function name:{0} - exception:StringFormatException'.format(
                                              function_name)
                                          )
                    raise StringFormatException

            # 字符串合并
            # 合并markerStyle
            list_markers = [self.size, self.color, self.label]
            temp_markers = ','.join(list_markers)
            # 合并marker字符串
            list_temp = [temp_markers, self.location]
            result_markers = ":".join(list_temp)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - markers:{1}'.format(function_name,
                                                                                   result_markers)
                                  )
            return result_markers

        except StringFormatException as e:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - error reason:{1}'.format(function_name,
                                                                                        e.error_reason())
                                  )

    def user_define_labels(self, content: str,
                           location: str,
                           **kwargs
                           ) -> str:
        """
        函数：自定义标签
        Args:
            content:标签内容，字符最大数目为15
            location:地理位置坐标
            kwargs:
                font:0：微软雅黑；1：宋体；2：Times New Roman;3：Helvetica
                bold:0：非粗体；1：粗体
                fontSize:字体大小，可选值[1,72]
                font_color:字体颜色，取值范围：[0x000000, 0xffffff]，默认为0xFFFFFF
                background:背景色，取值范围：[0x000000, 0xffffff]，默认为0x5288d8
        Returns:返回格式化后的单个label字符串
        """

        self.content = content
        self.location = location

        if 'background' in kwargs:
            self.background = kwargs['background']
        if 'bold' in kwargs:
            self.bold = kwargs['bold']
        if 'font' in kwargs:
            self.font = kwargs['font']
        if 'fontColor' in kwargs:
            self.fontColor = kwargs['fontColor']
        if 'fontSize' in kwargs:
            self.fontSize = kwargs['fontSize']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        try:
            # 检测字符串格式
            # 检测字体
            if self.font not in [0, 1, 2, 3]:
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - exception:StringFormatException'.format(
                                          function_name)
                                      )
                raise StringFormatException

            # 检测文字粗体
            if self.bold not in [0, 1]:
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - exception:StringFormatException'.format(
                                          function_name)
                                      )
                raise StringFormatException

            # 检测文字字体大小
            if self.fontSize not in list(range(1, 73)):
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - exception:StringFormatException'.format(
                                          function_name)
                                      )
                raise StringFormatException

            # 检测字体颜色格式
            if not self.is_rgb_color(self.fontColor):
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - exception:StringFormatException'.format(
                                          function_name)
                                      )
                raise StringFormatException

            # 检测背景颜色格式
            if not self.is_rgb_color(self.background):
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - exception:StringFormatException'.format(
                                          function_name)
                                      )
                raise StringFormatException

            list_location = self.location.split(";")
            for item in list_location:
                if not self.is_location(item):
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=3,
                                          context='Function name:{0} - exception:StringFormatException'.format(
                                              function_name)
                                          )
                    raise StringFormatException

            # 字符串合并
            # 合并labelStyle
            list_labels = [self.content, self.font, self.bold, self.fontSize, self.fontColor, self.background]
            temp_labels = ','.join('%s' % item for item in list_labels)
            # 合并
            list_temp = [temp_labels, self.location]
            result_labels = ':'.join(list_temp)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - labels:{1}'.format(function_name,
                                                                                  result_labels)
                                  )
            return result_labels

        except StringFormatException as e:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - error reason:{1}'.format(function_name,
                                                                                        e.error_reason())
                                  )

    def user_define_paths(self, location: str,
                          **kwargs
                          ) -> str:
        """
        函数：自定义路线
        Args:
            location:地理位置坐标
            kwargs:
                weight: 线条粗细，可选值： [2,15]，默认5
                color:折线颜色。 选值范围：[0x000000, 0xffffff]
                transparency:透明度。可选值[0,1]，小数后最多2位，0表示完全透明，1表示完全不透明。默认1
                fillcolor:多边形的填充颜色，此值不为空时折线封闭成多边形。取值规则同color
                fill_transparency:填充面透明度。可选值[0,1]，小数后最多2位，0表示完全透明，1表示完全不透明。默认0.5
        Returns:返回格式化后的单个path字符串
        """

        self.location = location

        if 'widget' in kwargs:
            self.weight = kwargs['widget']
        if 'color' in kwargs:
            self.color = kwargs['color']
        if 'transparency' in kwargs:
            self.transparency = kwargs['transparency']
        if 'fillColor' in kwargs:
            self.fillColor = kwargs['fillColor']
        if 'fill_transparency' in kwargs:
            self.fill_transparency = kwargs['fill_transparency']

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        try:
            # 检测字符串格式
            if self.weight not in list(range(2, 16)):
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - exception:StringFormatException'.format(
                                          function_name)
                                      )
                raise StringFormatException

            if 0 > self.transparency > 1 and len(str(self.transparency).split(".")) != 2:
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - exception:StringFormatException'.format(
                                          function_name)
                                      )
                raise StringFormatException

            if not self.is_rgb_color(self.color):
                # only for debugging
                writeLog.write_to_log(file_name=log_filename,
                                      log_level=3,
                                      context='Function name:{0} - exception:StringFormatException'.format(
                                          function_name)
                                      )
                raise StringFormatException

            if 0 > self.fill_transparency > 1 and len(str(self.fill_transparency).split(".")) != 2:
                raise StringFormatException

            if self.fillColor != '':
                if not self.is_rgb_color(self.fillColor):
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=3,
                                          context='Function name:{0} - exception:StringFormatException'.format(
                                              function_name)
                                          )
                    raise StringFormatException

            list_location = self.location.split(";")

            for item in list_location:
                if not self.is_location(item):
                    # only for debugging
                    writeLog.write_to_log(file_name=log_filename,
                                          log_level=3,
                                          context='Function name:{0} - exception:StringFormatException'.format(
                                              function_name)
                                          )
                    raise StringFormatException

            # 字符串合并
            # 合并labelStyle
            list_paths = [self.weight, self.color, self.transparency, self.fillColor, self.fill_transparency]
            temp_paths = ','.join('%s' % item for item in list_paths)
            # 合并
            list_temp = [temp_paths, self.location]
            result_paths = ':'.join(list_temp)
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - paths:{1}'.format(function_name,
                                                                                 result_paths)
                                  )
            return result_paths

        except StringFormatException as e:
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=3,
                                  context='Function name:{0} - error reason:{1}'.format(function_name,
                                                                                        e.error_reason())
                                  )

    def is_rgb_color(self, rgbColor: str
                     ) -> bool:
        """
        函数：判断是否符合rgb格式字符串
        Args:
            rgbColor: rgb颜色值
        Returns:返回判断值
        """

        self.rgbColor = rgbColor

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 检测字符串是否符合rgb格式字符串
        rgbString = re.compile(r'0x[a-fA-F0-9]{6}$')
        result = bool(rgbString.match(self.rgbColor))
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=6,
                              context='Function name:{0} - rgb color string checked result:{1}'.format(function_name,
                                                                                                       result)
                              )
        return result

    def is_label(self, label: str
                 ) -> bool:
        """
        函数：判断是否符合label字符串
        Args:
            label: label字符串
        Returns:返回判断值
        """

        self.label = label

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        labelString = re.compile(r'[0-9A-Z\u4e00-\u9fa5]$')  # 检测字符串是否符合[0-9]、[A-Z]、[单个中文字]格式

        result = bool(labelString.match(self.label))
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=6,
                              context='Function name:{0} - label string checked result:{1}'.format(function_name,
                                                                                                   result)
                              )
        return result

    def is_location(self, location: str
                    ) -> bool:
        """
        函数：判断是否符合经纬度值格式
        Args:
            location: 经纬度值
        Returns:返回判断值
        """
        self.location = location

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        locationString = re.compile(r'\d{1,3}.\d{5,6},\d{1,3}.\d{5,6}$')
        result = bool(locationString.match(location))
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=6,
                              context='Function name:{0} - location string checked result:{1}'.format(function_name,
                                                                                                      result)
                              )
        return bool(locationString.match(location))
