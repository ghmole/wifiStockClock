# 导入相关模块
import network,time
from machine import RTC
import ntptime



class TimeService:
    __log = None
    
    def __init__(self, log):
        self.__log = log
    
    __rtc = RTC()
    
    '更新网络时间'          
    def update_ntp_time(self):
        self.__log.info("TimeService.get_ntp_time(self)")
        
        ntptime.NTP_DELTA = 3155644800 
        ntptime.host = 'ntp1.aliyun.com'
    
        for i in range(10): # 最多尝试获取10次
            
            try:
                ntptime.settime() # 获取网络时间
                self.__log.info("ntp time(BeiJing): " + str(self.__rtc.datetime()) )
                return True

            except:
                self.__log.error("Can not get time! try : " + str(i + 1))
            
            time.sleep_ms(300)

    '获取机器的日期时间，格式：(2022, 7, 13, 2, 18, 23, 24, 140)'
    def get_datetime(self):
        return self.__rtc.datetime()
    
    
    
    
    