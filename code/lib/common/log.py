
class Log():
    __is_show_info = True # 是否显示 正常的系统日志
    __is_show_error = True # 是否显示 错误日志
    
    '控制台输出日志'
    def info(self, *msg):
        if self.__is_show_info:
            print("Info: " , str(msg))
    
    '控制台输出异常日志'
    def error(self, *msg):
        if self.__is_show_error:
            print("Error: " , str(msg))

        
        
    