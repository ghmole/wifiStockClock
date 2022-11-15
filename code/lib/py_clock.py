#导入相关模块
import  gc 
from machine import Pin, WDT, reset
from time import sleep_ms,ticks_ms
import os
from micropython import mem_info#, stack_use

gc.collect()

# UI类
from lib.ui.clock_weather_ui import ClockWeatherUI              # 天气时间UI
from lib.ui.clock_stock_ui import ClockStockUI                  # 股票UI
gc.collect() 

# 业务类
from lib.service.time_service import TimeService                   # 时间
from lib.service.weather_baidu_service import WeatherBaiduService  # 天气
#from lib.service.upgrade_service import UpgradeService            # 更新
from lib.service.calendar_service import CalendarService           # 日历
from lib.service.stockservice import  StockService                 # 股票


from lib.bean.calendar_bean import CalendarBean
from lib.bean.weather_bean import WeatherBean
from lib.bean.stock_bean import * # 股票数据模板
gc.collect()


class PyClock:
    # 系统方法  
    #__gc_collect = None
    
    # 常用类 
    __log   = None  # 日志
    __color = None  # 颜色
    
    # 设备类 
    __screen = None  # 屏幕
    __wifi   = None  # Wifi
    __led    = None  # Led灯
    __key    = None  # 按键
    
    # 业务类 
    __time_service    = None  # 时间
    __weather_service = None  # 天气
    __stock_service = None    # 股票
    __bluetooth_service = None# 蓝牙
    
    #  UI类  
    __clock_weather_ui        = None  # 天气时间UI
    #__clock_weather_win_xp_ui = None  # winxp 天气时间UI
    __clock_stock_ui = None           # 股票 UI
    
    # 数据容器
    __weatherWarn  = WeatherBean() #None # 获取 天气预警
    __weatherBean  = WeatherBean()  #None  # 获取 天气数据
    __calendarBean = CalendarBean()
    __stock_bean   = None
    
    # 看门狗 
    __wdt        = None   # 看门狗
    __is_use_wdt = True  # 是否启用看门狗
 
    
    __ui_num = 2    # UI的数量
    __ui_index = -1 # 当前UI的序号
    __is_switch_new_ui = True # 是否 切换了新界面
    
    __fail_num_list = [0, 0] # 获取数据连续失败的次数。分别记录天气和预警的连续失败次数。
    
    # 股票
    __stock_list=['sh000001','sz399001','sz399006']

    __max_stock_num = 12
    __stock_num = 3
    __stock_page = 1
    __stock_update_index = 0
    
    
    __last_refresh_ui_second = 61   # 上次 刷新界面的秒数
    __last_get_data_minute = 61     # 上次 获取数据的分钟数
    __last_change_ui_time = 0       # 上次 切换UI的时间
    #__last_get_upgrade_minite = 61  # 上次 获取更新的分钟数
    __last_get_upgrade_hour = 25    # 上次 获取更新的小时数
    
    
    '构造方法，初始化数据'
    def __init__(self,
                 log, color,
                 screen, wifi, led, bluetooth_service):
        gc.collect()
        
        self.__log   = log
        self.__color = color
        
        self.__screen = screen
        self.__wifi   = wifi
        self.__led    = led
        
        self.__time_service     = TimeService(log)
        self.__weather_service  = WeatherBaiduService(log)
        self.__calendar_service = CalendarService(log)
        self.__stock_service = StockService(log)
        self.__bluetooth_service = bluetooth_service 
        
        self.__clock_weather_ui = ClockWeatherUI(log, color, screen)
        self.__clock_stock_ui = ClockStockUI(log, color, screen)
        
        self.__stock_bean = StockBean(log)
        # 3 个指数
        self.__stock_bean.add_stock_data(StockData(0))
        self.__stock_bean.add_stock_data(StockData(1))
        self.__stock_bean.add_stock_data(StockData(2))
        gc.collect()
        # 关闭 LED灯
        self.__led.turn_off()
        
        # 配置 按键
        Pin(9, Pin.IN, Pin.PULL_UP).irq(self.__key_handler, Pin.IRQ_FALLING) # 定义中断的回调函数

        # 配置 WiFi,当没有wifilist.cfg时
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
            f = open('/data/config/stocklist.cfg', 'r')
            
            # 读一行
            stockcode = f.readline()
            cnt=3
            while (stockcode):
                # 测试
                #print(stockcode.replace('\n',''),stockcode.encode('gbk'))
                # 删除换行
                stockcode=stockcode.replace('\r','').replace('\n','')
                #stockcode=stockcode.replace('\n','')
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
            self.__log.info('read_stock_list():  stock_list len=' + str(len(self.__stock_list)))
            self.__log.info('read_stock_list():  stock_num=' + str(self.__stock_num))
            self.__log.info('read_stock_list():  stock_page=' + str(self.__stock_page))
            #self.__log.info('read_stock_list(): list=' + str(self.__stock_list))
            
    def write_stock_list(self):
        #self.__log.info('pyClock.write_stock_list():  stock_list len=' + str(len(self.__stock_list)))
        f = open('/data/config/stocklist.cfg', 'wt')
        # 逐个写入股票代码，3个指数不写入
        for i in range(3,len(self.__stock_list)):
            stockcode=self.__stock_list[i]

            f.write(stockcode)
            # print(i, len(stocklist))
            # 写入换行
            if i!=len(self.__stock_list)-1:
                f.write('\n')
        f.close()
        
     # 初始化股票代码
    def init_stock_bean(self):
        for index,stockcode in enumerate(self.__stock_list):
            if self.__stock_service.query_stock(stockcode):
                sleep_ms(10)
                d=self.__stock_service.get_stock_data()
            
                self.__stock_bean.update_stock_data(index,d)
            
        
        gc.collect()
      
    # 按键的回调函数
    def __key_handler(self, key):
        sleep_ms(10) # 消除按键抖动
        
        command = '' # 按键的最终命令
 
        # 短按一次：切换界面
        if (key.value() == 0): # 确认按键被按下
            command = 'change_next_ui'
            
        # 长按
        start_time = ticks_ms()
        while (key.value() == 0):
            now_time = ticks_ms()
            
            # 长按6秒：重置Wifi和城市信息
            if now_time - start_time > 6 * 1000:
                command = 'reset'
                break
        
        if (command == 'change_next_ui'):
            self.change_next_ui()
            sleep_ms(20)
            gc.collect()
            
        elif (command == 'reset'):
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
                
            reset() # 重启   
    
    
    #切换下一个UI
    def change_next_ui(self):
        self.__log.info("PyClock.change_next_ui")
      
        self.__ui_index += 1
        self.__ui_index %= self.__ui_num
    
        self.__is_switch_new_ui = True
        self.__last_change_ui_time = ticks_ms()
        gc.collect()
 
        
    '喂看门狗'
    def __feed_wdt(self):
        #self.__log.info("PyClock.__feed_wdt")
        
        if (self.__is_use_wdt):
            self.__wdt.feed()
            
    '开始运行'
    def run(self):
        #self.__log.info(__file__ +".run")
        
        # 连接WiFi
        self.__wifi.multi_wifi_connect()
        self.__feed_wdt()
 
        # 更新时间
        self.__time_service.update_ntp_time() # 更新机器的时间为网络时间
        self.__feed_wdt()
        
        # 读股票列表
        self.read_stock_list()
 
        # 初始化股票数据
        #self.init_stock_bean()
        #self.__stock_bean.check_bean_data()
        gc.collect()
                                
        while True:
            try:
                gc.collect()
                
                if (self.__is_switch_new_ui):
                    if (self.__ui_index == -1):
                        self.__ui_index = self.__get_init_ui_index()                            
                    
                    self.__log.info('ui_index:'+  str(self.__ui_index))
                    # 界面初始化（获取数据之前）
                    if (self.__ui_index == 0):
                        #self.__screen.picture(0, 0, "/data/picture/winxp/desktop.jpg")
                        sleep_ms(100)
                    elif (self.__ui_index == 1):
                        pass
                    
                gc.collect()

                # 获取机器的时间
                datetime = self.__time_service.get_datetime()
                
                 
                # 调试用
                #datetime2 = [0,0,0,0,0,0,0,0]
                #for i in range(len(datetime)):
                #    datetime2[i] = datetime[i]
                #
                #datetime2[0] = 2022
                #datetime2[1] = 9
                #datetime2[2] = 10
                #datetime = datetime2
                 
                # 秒
                second = datetime[6]
                
                # 获取数据
                # winxp+weatherclock UI: 每10分钟获取一次 天气数据和预警信息
                if (self.__ui_index == 1 ):
                    hour = datetime[4]
                    minute = datetime[5]
                    gc.collect()
                    # 当__last_get_data_minute == 61（第一次运行）初始化天气
                    if (self.__last_get_data_minute == 61 or ((minute % 10 == 0 or (hour == 0 and minute == 3)) and self.__last_get_data_minute != minute)):  # 
                        self.__wifi.multi_wifi_connect()
                        self.__log.info(mem_info())
                        #self.__log.info('PyClock.update_weather()  :'+str(hour)+','+str(minute)+\
                        #                ','+str(second)+','+str(self.__last_refresh_ui_second))

                        self.__weatherWarn  = self.__weather_service.get_weather_warn(self, datetime) # 获取 天气预警
                        gc.collect()
                        self.__weatherBean  = self.__weather_service.get_weather_bean(self, datetime) # 获取 天气数据
                        gc.collect()
                        self.__calendarBean = self.__calendar_service.get_date_info(datetime)         # 获取 日历数据
                        gc.collect()  
                        self.__last_get_data_minute = minute
                    
                    gc.collect()
                    
                    # 开机后检测一次，之后每小时的25分检测一次更新; 并更新时间
                    if (self.__last_get_upgrade_hour == 25 or (minute % 25 == 0  and self.__last_get_upgrade_hour != hour)):
                        self.__wifi.multi_wifi_connect()
                        self.__feed_wdt()
                        
                        # 更新机器的时间为网络时间
                        if (self.__last_get_upgrade_hour != 25):
                            self.__time_service.update_ntp_time()
                            self.__feed_wdt()
                        
                        self.__last_get_upgrade_hour = hour
                     
 

                    
                elif (self.__ui_index == 0):        # stock ui
                    minute = datetime[5]
                    #self.__log.info('PyClock.get_stock_data() check second:',second, self.__last_refresh_ui_second)
                    if (self.__last_get_data_minute == 61):
                        # 初始化股票数据
                        self.init_stock_bean()
                        #self.__stock_bean.check_bean_data()
 
                        self.__last_get_data_minute = minute
                        
                    if second!=self.__last_refresh_ui_second:
                        #self.__log.info('PyClock.get_stock_data() second=',second)
                        current_stock_index=int((second+4)/5) % 12
                        #self.__log.info('PyClock.get_stock_data() current_stock_index=',current_stock_index,\
                        #                '   stock_update_index=',self.__stock_update_index)
                        
                        if current_stock_index < len(self.__stock_list) \
                           and second % 5 ==0 and self.__stock_update_index==current_stock_index:
                            
                            current_stock_code = self.__stock_list[current_stock_index]
                            #self.__log.info('PyClock.query_stock() code=:'+ current_stock_code)
                            if self.__stock_service.query_stock(current_stock_code):
                                sleep_ms(10) 
                                stockdata=self.__stock_service.get_stock_data()
                                sleep_ms(10) 
                                #self.__log.info('PyClock update stock_bean  index='+ str(current_stock_index ))
                                self.__stock_bean.update_stock_data(current_stock_index,stockdata)
                                
                                self.__stock_update_index= (self.__stock_update_index+1) % self.__stock_num
                                #self.__log.info('PyClock update stock_bean  updat_index='+str(self.__stock_update_index ))
                            #self.__stock_bean.check_bean_data()
 
                            self.__feed_wdt()
                        
                gc.collect()      
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
                            #self.__log.info('PyClock.run weather_ui init')
                        self.__is_switch_new_ui = False
                    gc.collect()
                    # 刷新界面
                    if (self.__ui_index == 0):
                        self.__clock_stock_ui.refresh(datetime, self.__stock_bean)

                    elif (self.__ui_index == 1):
                        
                        self.__log.info( mem_info())
                        #self.__log.info('stack use' + str(stack_use()))
                        if self.__weatherBean is None:
                            self.__weatherBean  = self.__weather_service.get_weather_bean(self, datetime) # 获取 天气数据
                        
                        if self.__weatherWarn is None:
                            self.__weatherWarn  = self.__weather_service.get_weather_warn(self, datetime) # 获取 天气预警
                            
                        if self.__calendarBean is None:
                            self.__calendarBean = self.__calendar_service.get_date_info(datetime)         # 获取 日历数据

                            
                        #self.__log.info('PyClock.run update_weather_ui')
                        if self.__weatherBean is not None and \
                           self.__weatherWarn is not None and \
                           self.__calendarBean is not None:
                            self.__clock_weather_ui.refresh(datetime, self.__weatherBean, \
                                                            self.__weatherWarn, self.__calendarBean)

                        else:
                            self.__log.info('invalid data, could not update weatehre_ui')
                        self.__feed_wdt()
                        gc.collect()
                    else:
                        pass
                        gc.collect()
                    
                    # 记录用户选择的UI，下次启动时自动选择显示该UI
                    if (self.__last_change_ui_time != 0):
                        # 切换界面后，如果一分钟没有再切换，就记录当前UI的序号
                        if (  ticks_ms() - self.__last_change_ui_time >= 60 * 1000):
                            self.__update_init_ui_index(self.__ui_index)
                            self.__last_change_ui_time = 0
               
               
                    self.__last_refresh_ui_second = second
                
                gc.collect()
                
                # 处理蓝牙消息
                if self.__bluetooth_service is not None:
                    BLE_MSG=self.__bluetooth_service.get_msg()
                    if BLE_MSG is not "":
                        self.__feed_wdt()
                        self.process_ble_msg(BLE_MSG)
                        self.__bluetooth_service.set_msg("")
                gc.collect()
                
                self.__feed_wdt()
            except BaseException as e:
                gc.collect()
                self.__log.error("PyClock.run error : " + __file__ + ', ' + repr(e))
                
                if e.errno==12:
                    self.__log.error("No enough memory!")
                gc.collect()
                self.__screen.picture(0, 0, "/data/picture/winxp/error.jpg")
                sleep_ms(2000)
                
                reset()
                # raise
 
            sleep_ms(200)
    
        
        
    '处理蓝牙消息'    
    def process_ble_msg(self,ble_msg):
        try:
            if 'stock' in ble_msg:
                stockcode=ble_msg.split(':')[1]
                if 'add' in ble_msg:
                    if self.__stock_num < self.__max_stock_num:
                        self.__stock_list.append(stockcode)                 
                        self.__stock_bean.add_stock_data(StockData(self.__stock_num))
                        self.__stock_num += 1
                        self.write_stock_list()
#                         self.__log.info('PyClock.process_ble_msg(): add stock code '+stockcode) 

                elif 'del' in ble_msg or 'remove' in ble_msg:
                    if self.__stock_num >0:
                        if stockcode in self.__stock_list:
                            for codeindex, code in enumerate(self.__stock_list):
                                if code==stockcode:
                                    break
                            if codeindex >=3 and codeindex < len(self.__stock_list):
                                del self.__stock_list[codeindex]
                                self.__stock_bean.del_stock_data(codeindex)
                                self.__stock_num -= 1
                                self.write_stock_list()
#                                 self.__log.info('PyClock.process_ble_msg(): del stock code '+stockcode) 
                            elif codeindex<3:
                                self.__log.info('can not delete stock index')
                else:
                    pass
#                 self.__log.info('bluetooth command stock'+stockcode)
                
            elif 'wifi' in ble_msg:
                ssid = ble_msg.split(':')[1].split(',')[0]
                
                if 'add' in ble_msg:
                    passwd = ble_msg.split(':')[1].split(',')[1]
                    self.__wifi.add_wifi_info(ssid,passwd)
#                     self.__log.info('bluetooth add wifi:'+ ssid +','+ passwd)
                    
                elif 'del' in ble_msg or 'remove' in ble_msg:
                    self.__wifi.del_wifi_info(ssid)
#                     self.__log.info('bluetooth del wifi:'+ ssid)
                    
                else:
                    pass
#                 self.__log.info('bluetooth command wifi '+ ssid)
                
            elif 'city' in ble_msg:
                if 'add' in ble_msg:
                    pass
                elif 'del' in ble_msg or 'remove' in ble_msg:
                    pass
                else:
                    pass
#                 self.__log.info('bluetooth command city') 
            else:
                pass
        except BaseException as e:
            self.__log.error("PyClock.process_ble_msg(): " + __file__ + ', ' + repr(e))

        gc.collect()    
            
            
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
            if (self.__fail_num_list[i] >= 60):
                self.__log.error("PyClock.__fail_num_list["+str(i)+"] = " + str(self.__fail_num_list[i]))
                reset()
     
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
        #self.__log.info("PyClock.__update_init_ui_index")
        
        try:
            with open("/data/config/ui_index.txt", "w") as f:
                f.write(str(index))
        except BaseException as e:
            self.__log.error("PyClock.__update_init_ui_index  error : " + str(repr(e)))
            








