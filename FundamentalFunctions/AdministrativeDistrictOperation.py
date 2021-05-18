import inspect

from AmapFunctions.AdministrativeDistrictEnquiry import AdministrativeDistrictEnquiry
from logrecord.WriteLog import WriteLog


class AdministrativeDistrictOperation:
    """
    Class:行政区域查询操作
    """
    def __init__(self):
        self.district = None
        self.subdistrict = None

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        log_filename = writeLog.create_filename(class_name=class_name)
        writeLog.write_to_log(file_name=log_filename, log_level=1, context='Class name:{0} start'.format(class_name))

    def get_sub_district(self, district: str
                         ) -> list:
        """
        函数：获取选择的行政区域对应的下级行政区域
        Args:
            district:根行政区域
        Returns:
            返回获取到根行政区域对应的具体信息
        """

        # TODO:未来版本将返回数据从list升级为dict
        self.district = district

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        administrativeDistrictEnquiry = AdministrativeDistrictEnquiry()

        # 北京市对应的行政区域
        if self.district == '北京市':
            resultAdministrativeDistrictEnquiry = administrativeDistrictEnquiry.get_administrative_district(
                keywords='北京城区',
                sub_district=1)
            resultAdministrativeList = administrativeDistrictEnquiry.get_sub_administrative_district(
                resultAdministrativeDistrictEnquiry)

            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - resultAdministrativeDistrictEnquiry:{1}'.format(
                                      function_name,
                                      resultAdministrativeDistrictEnquiry)
                                  )
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - resultAdministrativeList:{1}'.format(function_name,
                                                                                                    resultAdministrativeList)
                                  )

        # 上海市对应的行政区域
        elif self.district == '上海市':
            resultAdministrativeDistrictEnquiry = administrativeDistrictEnquiry.get_administrative_district(
                keywords='上海城区',
                sub_district=1)
            resultAdministrativeList = administrativeDistrictEnquiry.get_sub_administrative_district(
                resultAdministrativeDistrictEnquiry)

            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - resultAdministrativeDistrictEnquiry:{1}'.format(
                                      function_name,
                                      resultAdministrativeDistrictEnquiry)
                                  )
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - resultAdministrativeList:{1}'.format(function_name,
                                                                                                    resultAdministrativeList)
                                  )

        # 天津市对应的行政区域
        elif self.district == '天津市':
            resultAdministrativeDistrictEnquiry = administrativeDistrictEnquiry.get_administrative_district(
                keywords='天津城区',
                sub_district=1)
            resultAdministrativeList = administrativeDistrictEnquiry.get_sub_administrative_district(
                resultAdministrativeDistrictEnquiry)

            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - resultAdministrativeDistrictEnquiry:{1}'.format(
                                      function_name,
                                      resultAdministrativeDistrictEnquiry)
                                  )
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - resultAdministrativeList:{1}'.format(function_name,
                                                                                                    resultAdministrativeList)
                                  )

        # 重庆市对应的行政区域
        elif self.district == '重庆市':
            resultAdministrativeList = []
            resultAdministrativeDistrictEnquiry = administrativeDistrictEnquiry.get_administrative_district(
                keywords='重庆城区',
                sub_district=1)
            resultAdministrativeList.extend(administrativeDistrictEnquiry.get_sub_administrative_district(
                resultAdministrativeDistrictEnquiry))
            resultAdministrativeDistrictEnquiry = administrativeDistrictEnquiry.get_administrative_district(
                keywords='重庆郊县',
                sub_district=1)
            resultAdministrativeList.extend(administrativeDistrictEnquiry.get_sub_administrative_district(
                resultAdministrativeDistrictEnquiry))

            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - resultAdministrativeDistrictEnquiry:{1}'.format(
                                      function_name,
                                      resultAdministrativeDistrictEnquiry)
                                  )
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - resultAdministrativeList:{1}'.format(function_name,
                                                                                                    resultAdministrativeList)
                                  )

        # 普通地区对应的行政区域
        else:
            resultAdministrativeDistrictEnquiry = administrativeDistrictEnquiry.get_administrative_district(
                keywords=self.district,
                sub_district=1)
            resultAdministrativeList = administrativeDistrictEnquiry.get_sub_administrative_district(
                resultAdministrativeDistrictEnquiry)

            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - resultAdministrativeDistrictEnquiry:{1}'.format(
                                      function_name,
                                      resultAdministrativeDistrictEnquiry)
                                  )
            # only for debugging
            writeLog.write_to_log(file_name=log_filename,
                                  log_level=1,
                                  context='Function name:{0} - resultAdministrativeList:{1}'.format(function_name,
                                                                                                    resultAdministrativeList)
                                  )

        return resultAdministrativeList

    def get_all_district_information(self, district: str,
                                     subdistrict: int
                                     )->list:
        """
        函数：获取选择的行政区域对应的下级行政区域
        Args:
            district:根行政区域
            subdistrict:下级行政区级数
        Returns:
            返回获取到根行政区域对应的具体信息
        """

        # TODO:未来版本将返回数据从list升级为dict
        self.district = district
        self.subdistrict = subdistrict

        # 写入日志
        writeLog = WriteLog()
        class_name = self.__class__.__name__
        function_name = inspect.stack()[0][3]
        log_filename = writeLog.create_filename(class_name=class_name)

        # 获取内容
        administrativeDistrictEnquiry = AdministrativeDistrictEnquiry()
        resultAdministrativeDistrictEnquiry = administrativeDistrictEnquiry.get_administrative_district(
            keywords=self.district,
            sub_district=subdistrict)
        resultAdministrativeList = administrativeDistrictEnquiry.parse_administrative_district(
            resultAdministrativeDistrictEnquiry, self.subdistrict)

        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - resultAdministrativeDistrictEnquiry:{1}'.format(
                                  function_name,
                                  resultAdministrativeDistrictEnquiry)
                              )
        # only for debugging
        writeLog.write_to_log(file_name=log_filename,
                              log_level=1,
                              context='Function name:{0} - resultAdministrativeList:{1}'.format(function_name,
                                                                                                resultAdministrativeList)
                              )

        return resultAdministrativeList
