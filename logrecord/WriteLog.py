import os
import time
from pathlib import Path

from loguru import logger


class WriteLog:
    def __init__(self):
        self.class_name = None
        self.file_name = None
        self.log_level = None
        self.context = None

    def create_filename(self, class_name: str
                        ) -> str:
        """
        函数：创建日志记录文件
        Args:
            class_name: 日志记录被调用所属的类的名称
        Returns:

        """
        self.class_name = class_name

        # TODO:优化代码，递归创建目录
        # 项目目录
        project_dir = os.getenv('LOCALAPPDATA')
        project_dir_name = '\\'.join([project_dir, 'AmapProgram'])
        # 若当前的目录是文件，删除
        if os.path.isfile(project_dir_name):
            os.remove(project_dir_name)
        # 若当前目录不存在，创建
        if not os.path.exists(project_dir_name):
            os.mkdir(project_dir_name)

        # 日志总目录
        log_dir = [project_dir_name, 'Log']
        log_dir_name = '\\'.join(log_dir)
        # 若当前的目录是文件，删除
        if os.path.isfile(log_dir_name):
            os.remove(log_dir_name)
        # 若当前目录不存在，创建
        if not os.path.exists(log_dir_name):
            os.mkdir(log_dir_name)

        # 各个功能对应的目录
        class_dir = [log_dir_name, class_name]
        class_dir_name = '\\'.join(class_dir)
        # 若当前的目录是文件，删除
        if os.path.isfile(class_dir_name):
            os.remove(class_dir_name)
        # 若当前目录不存在，创建
        if not os.path.exists(class_dir_name):
            os.mkdir(class_dir_name)

        # 文件名称
        time_now = time.strftime("%Y-%m-%d", time.localtime())
        time_file = time_now + '.log'
        file_list = [class_dir_name, time_file]
        file_name = '\\'.join(file_list)
        if not os.path.exists(file_name):
            Path(file_name).touch()
        return file_name

    def write_to_log(self, file_name: str,
                     log_level: int,
                     context: str = ''
                     ) -> None:

        self.file_name = file_name
        self.log_level = log_level
        self.context = context

        logger.remove(handler_id=None)
        logger.add(file_name, encoding='utf-8')
        if log_level == 0:
            logger.debug(context)
        elif log_level == 1:
            logger.info(context)
        elif log_level == 2:
            logger.warning(context)
        elif log_level == 3:
            logger.error(context)
        elif log_level == 4:
            logger.critical(context)
        elif log_level == 5:
            logger.exception(context)
        elif log_level == 6:
            logger.success(context)
