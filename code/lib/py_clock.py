#导入相关模块
from machine import Pin, WDT, reset
import time, gc, machine
import os 
from lib.bean.stock_bean import * # 股票数据模板


class PyClock:
    ''' 系统方法 '''
    __gc_collect = None
    
    ''' 常用类 '''
    __log   = None  # 日志
    __color = None  # 颜色
    
    ''' 设备类 '''
    __screen = None  # 屏幕
    __wifi   = None  # Wifi
    __led    = None  # Led灯
    __key    = None  # 按键
    
    ''' 业务类 '''
    __time_service    = None  # 时间
    __weather_service = None  # 天气
    __stock_service = None    #股票
    
    ''' UI类 '''
    __clock_weather_ui        = None  # 天气时间UI
    #__clock_weather_win_xp_ui = None  # winxp 天气时间UI
    __clock_stock_ui = None           # 股票 UI
    
    ''' 看门狗 '''
    __wdt        = None   # 看门狗
    __is_use_wdt = True  # 是否启用看门狗
 
    
    __ui_num = 2    # UI的数量
    __ui_index = -1 # 当前UI的序号
    __is_switch_new_ui = True # 是否 切换了新界面
    
    __fail_num_list = [0, 0] # 获取数据连续失败的次数。分别记录天气和预警的连续失败次数。
    
    __stock_list=['sh000001','sz399001','sz399006']
    __stock_bean=None
    __max_stock_num = 12
    __stock_num = 3
    __stock_page = 1
    __stock_update_index = 0
    
    
    __last_refresh_ui_second = 61   # 上次 刷新界面的秒数
    __last_get_data_minute = 61     # 上次 获取数据的分钟数
    __last_change_ui_time = 0       # 上次 切换UI的时间
    __last_get_upgrade_minite = 61  # 上次 获取更新的分钟数
    __last_get_upgrade_hour = 25    # 上次 获取更新的小时数
    
    
    '构造方法，初始化数据'
    def __init__(self,
                 log, color,
                 screen, wifi, led, 
                 time_service, weather_service, calendar_service, stock_service,
                 clock_weather_ui, clock_stock_ui):
        gc.collect()
        
        self.__log   = log
        self.__color = color
        
        self.__screen = screen
        self.__wifi   = wifi
        self.__led    = led
        
        self.__time_service     = time_service
        self.__weather_service  = weather_service
        self.__calendar_service = calendar_service
        self.__stock_service = stock_service
        
        self.__clock_weather_ui        = clock_weather_ui
        self.__clock_stock_ui = clock_stock_ui
        
        self.__stock_bean = StockBean(log)
        # 3 个指数
        self.__stock_bean.add_stock_data(StockData(0))
        self.__stock_bean.add_stock_data(StockData(1))
        self.__stock_bean.add_stock_data(StockData(2))
        
        # 关闭 LED灯
        self.__led.turn_off()
        
        # 配置 按键
        Pin(9, Pin.IN, Pin.PULL_UP).irq(self.__key_handler, Pin.IRQ_FALLING) # 定义中断的回调函数

        # 配置 WiFi
        self.__wifi.config()
        
        # 配置 看门狗
        if (self.__is_use_wdt):
            self.__wdt = WDT(timeout = 60 * 1000) # 看门狗超时时间：60秒
        
        gc.collect()
    
    # 读股票代码
    def read_stock_list(self):
        
        # 股票代码文件是否存在
        if 'stocklist.cfg' in os.listdir('/data/config'): 
            # 读文件，注意文件编码
            f = open('/data/config/stocklist.cfg', 'r',encoding='gbk')
            
            # 读一行
            stockcode = f.readline()
            cnt=3
            while (stockcode):
                # 测试
                #print(stockcode.replace('\n',''),stockcode.encode('gbk'))
                # 删除换行
                stockcode=stockcode.replace('\r','')
                stockcode=stockcode.replace('\n','')
                # 如果不在列表里面，则添加
                if not stockcode in self.__stock_list:
                    self.__stock_list.append(stockcode)
                    self.__stock_bean.add_stock_data(StockData(cnt))
                # 读下一行   
                stockcode = f.readline()
                cnt+=1
            f.close()
            self.__stock_num = len(self.__stock_list)
            self.__stock_page = int((self.__stock_num+2)/3)
            self.__log.info('read_stock_list():  stock_list len=', len(self.__stock_list))
            self.__log.info('read_stock_list():  stock_num=',self.__stock_num)
            self.__log.info('read_stock_list():  stock_page=',self.__stock_page)
            self.__log.info('read_stock_list(): list=' , self.__stock_list)
             
     # 初始化股票代码
    def init_stock_bean(self):
        for index,stockcode in enumerate(self.__stock_list):
            if self.__stock_service.query_stock(stockcode):
                time.sleep_ms(10)
                d=self.__stock_service.get_stock_data()
            
                self.__stock_bean.update_stock_data(index,d)
            gc.collect()
            time.sleep_ms(10)
            self.__feed_wdt()
      
    # 按键的回调函数
    def __key_handler(self, key):
        time.sleep_ms(10) # 消除按键抖动
        
        commond = '' # 按键的最终命令
 
        # 短按一次：切换界面
        if (key.value() == 0): # 确认按键被按下
            commond = 'change_next_ui'
            
        # 长按
        start_time = time.ticks_ms()
        while (key.value() == 0):
            now_time = time.ticks_ms()
            
            # 长按6秒：重置Wifi和城市信息
            if now_time - start_time > 6 * 1000:
                commond = 'reset'
                break
                

        
        if (commond == 'change_next_ui'):
            self.change_next_ui()
        elif (commond == 'reset'):
            # 打开 Led灯
            self.__led.turn_on() 
            
            try:
                self.__log.info('Remove wifi.cfg')
                os.remove('/data/config/wifilist.cfg')  
            except:
                self.__log.error(__file__+', no wifi.cfg')
                 
            try:
                self.__log.info('Remove city.cfg')
                os.remove('/data/config/city.cfg')
            except:
                self.__log.error(__file__+', no city.cfg')
                
            machine.reset() # 重启   
    
    
    '切换下一个UI'
    def change_next_ui(self):
        self.__log.info("PyClock.change_next_ui")
        
      
        self.__ui_index += 1
        self.__ui_index %= self.__ui_num
    
        self.__is_switch_new_ui = True
        self.__last_change_ui_time = time.ticks_ms()
    
 
        
    '喂看门狗'
    def __feed_wdt(self):
        #self.__log.info("PyClock.__feed_wdt")
        
        if (self.__is_use_wdt):
            self.__wdt.feed()
            
    '开始运行'
    def run(self):
        self.__log.info("PyClock.run")
        
        # 连接WiFi
        self.__wifi.multi_wifi_connect()
        self.__feed_wdt()
 
        # 更新时间
        self.__time_service.update_ntp_time() # 更新机器的时间为网络时间
        self.__feed_wdt()
        
        # 读股票列表
        self.read_stock_list()
        
        # 初始化股票数据
        self.init_stock_bean()
        self.__stock_bean.check_bean_data()
        
        while True:
            try:
                gc.collect()
                
                if (self.__is_switch_new_ui):
                    if (self.__ui_index == -1):
                        self.__ui_index = self.__get_init_ui_index()                            
                    
                    self.__log.info('ui_index:', self.__ui_index)
                    # 界面初始化（获取数据之前）
                    if (self.__ui_index == 0):
                        self.__screen.picture(0, 0, "/data/picture/winxp/desktop.jpg")
                        time.sleep_ms(400)
                    elif (self.__ui_index == 1):
                        pass
 

                # 获取机器的时间
                datetime = self.__time_service.get_datetime()
                
                '''
                # 调试用
                datetime2 = [0,0,0,0,0,0,0,0]
                for i in range(len(datetime)):
                    datetime2[i] = datetime[i]
                
                datetime2[0] = 2022
                datetime2[1] = 9
                datetime2[2] = 10
                datetime = datetime2
                '''
                # 秒
                second = datetime[6]
                
                # 获取数据
                # winxp+weatherclock UI: 每10分钟获取一次 天气数据和预警信息
                if (self.__ui_index == 0 or self.__ui_index == 1):
                    hour = datetime[4]
                    minute = datetime[5]
 
                    if (self.__last_get_data_minute == 61 or ((minute % 10 == 0 or (hour == 0 and minute == 3)) and self.__last_get_data_minute != minute)):  # 
                        self.__wifi.multi_wifi_connect()
                        
                        weatherWarn  = self.__weather_service.get_weather_warn(self, datetime) # 获取 天气预警
                        weatherBean  = self.__weather_service.get_weather_bean(self, datetime) # 获取 天气数据
                        calendarBean = self.__calendar_service.get_date_info(datetime)         # 获取 日历数据
                  
                        self.__last_get_data_minute = minute
                    
                    # 开机后检测一次，之后每小时的25分检测一次更新; 并更新时间
                    if (self.__last_get_upgrade_hour == 25 or (minute % 25 == 0  and self.__last_get_upgrade_hour != hour)):
                        self.__wifi.multi_wifi_connect()
                        
                        # 更新机器的时间为网络时间
                        if (self.__last_get_upgrade_hour != 25):
                            self.__time_service.update_ntp_time()
                            self.__feed_wdt()
                        
                        self.__last_get_upgrade_hour = hour
                        
                elif (self.__ui_index == 2):        # stock ui
                    #self.__log.info('PyClock.get_stock_data()')
                    if second!=self.__last_refresh_ui_second:
                        #self.__log.info('PyClock.get_stock_data() second=',second)
                        current_stock_index=int((second+4)/5) % 12
                        #self.__log.info('PyClock.get_stock_data() current_stock_index=',current_stock_index,\
                        #                '   stock_update_index=',self.__stock_update_index)
                        
                        if current_stock_index < len(self.__stock_list) \
                           and second % 5 ==0 and self.__stock_update_index==current_stock_index:
                            
                            current_stock_code = self.__stock_list[current_stock_index]
                            self.__log.info('PyClock.query_stock() code=:', current_stock_code)
                            if self.__stock_service.query_stock(current_stock_code):
                                time.sleep_ms(300) 
                                stockdata=self.__stock_service.get_stock_data()
                                time.sleep_ms(20) 
                                self.__log.info('PyClock update stock_bean  index=', current_stock_index )
                                self.__stock_bean.update_stock_data(current_stock_index,stockdata)
                                
                                self.__stock_update_index= (self.__stock_update_index+1) % self.__stock_num
                                self.__log.info('PyClock update stock_bean  updat_index=', self.__stock_update_index )
                            self.__stock_bean.check_bean_data()
                        
                      
                # 刷新UI数据
                
                if (self.__last_refresh_ui_second != second): # 每秒刷新一次
                    
                    # 检测数据的状态
                    self.__check_data_status()
                    
                    # 界面初始化（获取数据之后）
                    if (self.__is_switch_new_ui):
                        if (self.__ui_index == 0):
                            self.__clock_stock_ui.init()
                        elif (self.__ui_index == 1):
                            self.__clock_weather_ui.init()
                       
                            
                        self.__is_switch_new_ui = False
                    
                    # 刷新界面
                    if (self.__ui_index == 0):
                        self.__clock_stock_ui.refresh(datetime, self.__stock_bean)
                    elif (self.__ui_index == 1):
                        self.__clock_weather_ui.refresh(datetime, weatherBean, weatherWarn, calendarBean)
                    else:
                        pass
                    
                    
                    # 记录用户选择的UI，下次启动时自动选择显示该UI
                    if (self.__last_change_ui_time != 0):
                        # 切换界面后，如果一分钟没有再切换，就记录当前UI的序号
                        if (  time.ticks_ms() - self.__last_change_ui_time >= 60 * 1000):
                            self.__update_init_ui_index(self.__ui_index)
                            self.__last_change_ui_time = 0
               
               
                    self.__last_refresh_ui_second = second
                    
                self.__feed_wdt()
            except BaseException as e:
                gc.collect()
                self.__log.error("PyClock.run error : " + __file__ + ', ' + repr(e))
                
                self.__screen.picture(0, 0, "/data/picture/winxp/error.jpg")
                time.sleep_ms(2000)
                
                machine.reset()
                # raise
 
            time.sleep_ms(200)
    
        
        
        
        
            
    '记录获取数据 成功或失败'
    def update_data_status(self, index, is_success):
        self.__log.info("PyClock.update_status")
        
        # 更新连续失败次数
        if (is_success == True):
            self.__fail_num_list[index] = 0
        else:
            self.__fail_num_list[index] += 1
    
    '检测数据的状态'
    def __check_data_status(self):
        '''
        # 调试用，如果数据获取有失败的，控制台显示连续错误的次数
        is_data_fail = False
        for i in range( len(self.__fail_num_list) ):
            if (self.__fail_num_list[i] > 0):
                is_data_fail = True
                break
        if (is_data_fail):
            self.__log.error("PyClock.__fail_num_list = " + str(self.__fail_num_list[0]) + "," + str(self.__fail_num_list[1]) )
        '''
        
        # 连续获取数据失败超过次数，重启设备
        for i in range( len(self.__fail_num_list) ):
            if (self.__fail_num_list[i] >= 4): 
                machine.reset()
     
    '获取 初始显示的UI编号'
    def __get_init_ui_index(self):
        self.__log.info("PyClock.__get_init_ui_index")
        
        index = 0
        
        try:
            with open("/data/config/ui_index.txt") as f:
                lines = f.readlines()
                
            for line in lines:
                index = int(line)
                break
        except BaseException as e:
            self.__log.error("PyClock.__get_init_ui_index  error : " + str(repr(e)))
            
            index = 0
            
        return index
        
         
    '更新 初始显示的UI编号'
    def __update_init_ui_index(self, index):
        self.__log.info("PyClock.__update_init_ui_index")
        
        try:
            with open("/data/config/ui_index.txt", "w") as f:
                f.write(str(index))
        except BaseException as e:
            self.__log.error("PyClock.__update_init_ui_index  error : " + str(repr(e)))
            








