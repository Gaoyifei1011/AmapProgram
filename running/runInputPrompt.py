from AmapFunctions.InputPrompt import *

if __name__ == '__main__':

    datatype_dict = {'1': 'all', '2': 'poi', '3': 'bus', '4': 'busline', '': 'all'}

    keywords = input("请输入您要搜索的关键字：")
    input_type = input("请输入您要查询POI类型（可选）：")
    location = input("请输入您要查询的经纬度值（可选）：")
    city = input("请输入您要查询的城市（可选）：")
    data_type = input("请输入您要获取的数据类型，默认、1或2为全部，3为公交站点，4为公交线路：")

    inputprompt = InputPrompt()
    # 空值，默认为全部
    if datatype_dict[data_type] == '':
        # print("1")
        # print(datatype_dict[data_type])
        result_input_prompt = inputprompt.get_input_prompt(keywords=keywords,
                                                           input_type=input_type,
                                                           location=location,
                                                           city=city,
                                                           datatype=datatype_dict[data_type])
        inputprompt.parse_input_prompt(result_input_prompt, datatype_dict[data_type])
    else:
        # print("2")
        # print(datatype_dict[data_type])
        result_input_prompt = inputprompt.get_input_prompt(keywords=keywords,
                                                           input_type=input_type,
                                                           location=location,
                                                           city=city,
                                                           datatype=datatype_dict[data_type])
        inputprompt.parse_input_prompt(result_input_prompt, datatype_dict[data_type])
