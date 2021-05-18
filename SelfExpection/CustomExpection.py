#_*_coding=UTF-8_*_
class CustomExpection(Exception):
    def __init__(self)->None:
        super(CustomExpection,self).__init__()
        self.error_info = None

    def get_error_info(self, error_info: dict) -> tuple[str, str, str]:
        """
        函数：返回自定义异常的错误信息
        Args:
            error_info:自定义异常的内容
        Returns:
            info:自定义异常信息
            detail_information:具体的异常信息内容
            error_prompt:异常发生的提示
        """
        self.error_info = error_info
        info = error_info['info']
        detail_information = error_info['detail_information']
        error_prompt = error_info['error_prompt']

        return info, detail_information, error_prompt
