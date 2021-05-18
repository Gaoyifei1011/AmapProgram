class OfficialException(BaseException):
    def __init__(self) -> None:
        self.error_info = None

    def get_error_info(self, error_info: dict) -> tuple[str, str, str]:
        """
        函数：返回错误信息
        Args:
            error_info:获得的json格式数据文档
        Returns:
            errcode:info返回值
            errorInfo:状态描述
            solution:问题排查策略
        """
        self.error_info = error_info

        infocode = error_info['infocode']
        if infocode == '100001':
            errcode = 'INVALID_USER_KEY'
            errorInfo = 'key不正确或过期'
            solution = '开发者发起请求时，传入的key不正确或者过期。'
            # 写入日志文件
        elif infocode == '10002':
            # 写入日志文件
            errcode = 'SERVICE_NOT_AVAILABLE'
            errorInfo = '没有权限使用相应的服务或者请求接口的路径拼写错误。'
            solution = '1.开发者没有权限使用相应的服务，例如：开发者申请了WEB定位功能的key，却使用该key访问逆地理编码功能时，就会返回该错误。反之亦然。\n2.开发者请求接口的路径拼写错误。例如：正确的https://restapi.amap.com/v3/ip在程序中被拼装写了https://restapi.amap.com/vv3/ip"。'
        elif infocode == '10003':
            errcode = 'DAILY_QUERY_OVER_LIMIT'
            errorInfo = '访问已超出日访问量'
            solution = '开发者的日访问量超限，被系统自动封停，第二天0:00会自动解封。'
        elif infocode == '10004':
            errcode = 'ACCESS_TOO_FREQUENT'
            errorInfo = '单位时间内访问过于频繁'
            solution = '开发者的单位时间内（1分钟）访问量超限，被系统自动封停，下一分钟自动解封。'
        elif infocode == '10005':
            errcode = 'INVALID_USER_IP'
            errorInfo = 'IP白名单出错，发送请求的服务器IP不在IP白名单内。'
            solution = '开发者在LBS官网控制台设置的IP白名单不正确。白名单中未添加对应服务器的出口IP。可到"控制台>配置"  中设定IP白名单。'
        elif infocode == '10006':
            errcode = 'INVALID_USER_DOMAIN'
            errorInfo = '绑定域名无效'
            solution = '开发者绑定的域名无效，需要在官网控制台重新设置。'
        elif infocode == '10007':
            errcode = 'INVALID_USER_SIGNATURE'
            errorInfo = '数字签名未通过验证'
            solution = '开发者签名未通过开发者在key控制台中，开启了“数字签名”功能，但没有按照指定算法生成“数字签名”。'
        elif infocode == '10008':
            errcode = 'INVALID_USER_SCODE'
            errorInfo = 'MD5安全码未通过验证'
            solution = '需要开发者判定key绑定的SHA1,package是否与sdk包里的一致。'
        elif infocode == '10009':
            errcode = 'USERKEY_PLAT_NOMATCH'
            errorInfo = '请求key与绑定平台不符'
            solution = '请求中使用的key与绑定平台不符，例如：开发者申请的是js api的key，却用来调web服务接口。'
        elif infocode == '10010':
            errcode = 'IP_QUERY_OVER_LIMIT'
            errorInfo = 'IP访问超限'
            solution = '未设定IP白名单的开发者使用key发起请求，从单个IP向服务器发送的请求次数超出限制，被系统自动封停。'
        elif infocode == '10011':
            errcode = 'NOT_SUPPORT_HTTPS'
            errorInfo = '服务不支持https请求'
            solution = '服务不支持https请求，请联系提供商。'
        elif infocode == '10012':
            errcode = 'INSUFFICIENT_PRIVILEGES'
            errorInfo = '权限不足，服务请求被拒绝'
            solution = '由于不具备请求该服务的权限，所以服务被拒绝。'
        elif infocode == '10013':
            errcode = 'USER_KEY_RECYCLED'
            errorInfo = 'Key被删除'
            solution = '开发者删除了key，key被删除后无法正常使用。'
        elif infocode == '10014':
            errcode = 'QPS_HAS_EXCEEDED_THE_LIMIT'
            errorInfo = '云图服务QPS超限'
            solution = 'QPS超出限制，超出部分的请求被拒绝。限流阈值内的请求依旧会正常返回。'
        elif infocode == '10015':
            errcode = 'GATEWAY_TIMEOUT'
            errorInfo = '受单机QPS限流限制'
            solution = '受单机QPS限流限制时出现该问题，建议降低请求的QPS。'
        elif infocode == '10016':
            errcode = 'SERVER_IS_BUSY'
            errorInfo = '服务器负载过高'
            solution = '服务器负载过高，请稍后再试。'
        elif infocode == '10017':
            errcode = 'RESOURCE_UNAVAILABLE'
            errorInfo = '所请求的资源不可用'
            solution = '所请求的资源不可用。'
        elif infocode == '10019':
            errcode = 'CQPS_HAS_EXCEEDED_THE_LIMIT'
            errorInfo = '使用的某个服务总QPS超限'
            solution = 'QPS超出限制，超出部分的请求被拒绝。限流阈值内的请求依旧会正常返回。'
        elif infocode == '10020':
            errcode = 'CKQPS_HAS_EXCEEDED_THE_LIMIT'
            errorInfo = '某个Key使用某个服务接口QPS超出限制'
            solution = 'QPS超出限制，超出部分的请求被拒绝。限流阈值内的请求依旧会正常返回。'
        elif infocode == '10021':
            errcode = 'CUQPS_HAS_EXCEEDED_THE_LIMIT '
            errorInfo = '账号使用某个服务接口QPS超出限制'
            solution = 'QPS超出限制，超出部分的请求被拒绝。限流阈值内的请求依旧会正常返回。'
        elif infocode == '10026':
            errcode = 'INVALID_REQUEST'
            errorInfo = '账号处于被封禁状态'
            solution = '由于违规行为账号被封禁不可用，如有异议请登录控制台提交工单进行申诉。'
        elif infocode == '10029':
            errcode = 'ABROAD_DAILY_QUERY_OVER_LIMIT'
            errorInfo = '某个Key的QPS超出限制'
            solution = 'QPS超出限制，超出部分的请求被拒绝。限流阈值内的请求依旧会正常返回。'
        elif infocode == '10044':
            errcode = 'USER_DAILY_QUERY_OVER_LIMIT'
            errorInfo = '账号维度日调用量超出限制'
            solution = '账号维度日调用量超出限制，超出部分的请求被拒绝。限流阈值内的请求依旧会正常返回。'
        elif infocode == '10045':
            errcode = 'USER_ABROAD_DAILY_QUERY_OVER_LIMIT'
            errorInfo = '账号维度海外服务日调用量超出限制'
            solution = '账号维度海外服务接口日调用量超出限制，超出部分的请求被拒绝。限流阈值内的请求依旧会正常返回。'
        elif infocode == '20000':
            errcode = 'INVALID_PARAMS'
            errorInfo = '请求参数非法'
            solution = '请求参数的值没有按照规范要求填写。例如，某参数值域范围为[1,3],开发者误填了’4’。'
        elif infocode == '20001':
            errcode = 'MISSING_REQUIRED_PARAMS'
            errorInfo = '缺少必填参数'
            solution = '缺少接口中要求的必填参数。'
        elif infocode == '20002':
            errcode = 'ILLEGAL_REQUEST'
            errorInfo = '请求协议非法'
            solution = '请求协议非法。比如某接口仅支持get请求，结果用了POST方式'
        elif infocode == '20003':
            errcode = 'UNKNOWN_ERROR'
            errorInfo = '其他未知错误'
            solution = '其他未知错误'
        elif infocode == '20011':
            errcode = 'INSUFFICIENT_ABROAD_PRIVILEGES'
            errorInfo = '查询坐标或规划点（包括起点、终点、途经点）在海外，但没有海外地图权限'
            solution = '使用逆地理编码接口、输入提示接口、周边搜索接口、路径规划接口时可能出现该问题，规划点（包括起点、终点、途经点）不在中国陆地范围内。'
        elif infocode == '20012':
            errcode = 'ILLEGAL_CONTENT'
            errorInfo = '查询信息存在非法内容'
            solution = '使用搜索接口时可能出现该问题，通常是由于查询内容非法导致。'
        elif infocode == '20800':
            errcode = 'OUT_OF_SERVICE'
            errorInfo = '规划点（包括起点、终点、途经点）不在中国陆地范围内'
            solution = '使用路径规划服务接口时可能出现该问题，规划点（包括起点、终点、途经点）不在中国陆地范围内。'
        elif infocode == '20801':
            errcode = 'NO_ROADS_NEARBY'
            errorInfo = '划点（起点、终点、途经点）附近搜不到路'
            solution = '使用路径规划服务接口时可能出现该问题，划点（起点、终点、途经点）附近搜不到路。'
        elif infocode == '20802':
            errcode = 'ROUTE_FAIL'
            errorInfo = '路线计算失败，通常是由于道路连通关系导致'
            solution = '使用路径规划服务接口时可能出现该问题，路线计算失败，通常是由于道路连通关系导致。'
        elif infocode == '20803':
            errcode = 'OVER_DIRECTION_RANGE'
            errorInfo = '起点终点距离过长'
            solution = '使用路径规划服务接口时可能出现该问题，路线计算失败，通常是由于道路起点和终点距离过长导致。'
        elif infocode == '30001' or '30002' or '30003' or '32000' or '32001' or '32002' or '32003' or '32200' or '32201' or '32202' or '32203':
            errcode = 'ENGINE_RESPONSE_DATA_ERROR'
            errorInfo = '服务响应失败'
            solution = '出现3开头的错误码，建议先检查传入参数是否正确。'
        elif infocode == '40000':
            errcode = 'QUOTA_PLAN_RUN_OUT'
            errorInfo = '余额耗尽'
            solution = '所购买服务的余额耗尽，无法继续使用服务'
        elif infocode == '40001':
            errcode = 'GEOFENCE_MAX_COUNT_REACHED'
            errorInfo = '围栏个数达到上限'
            solution = 'Key可创建的地理围栏的数量，已达上限。'
        elif infocode == '40002':
            errcode = 'SERVICE_EXPIRED'
            errorInfo = '购买服务到期'
            solution = '所购买的服务期限已到，无法继续使用。'
        elif infocode == '40003':
            errcode = 'ABROAD_QUOTA_PLAN_RUN_OUT'
            errorInfo = '海外服务余额耗尽'
            solution = '所购买服务的海外余额耗尽，无法继续使用服务'
        else:
            errcode = 'UNKNOWN_ERROR'
            errorInfo = '其他未知错误'
            solution = '其他未知错误'
        return errcode, errorInfo, solution
