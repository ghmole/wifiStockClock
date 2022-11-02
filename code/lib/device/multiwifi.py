'''
实验名称：顺序连接多个无线路由器
版本：v1.0
日期：2022.10
作者：许可
说明：编程实现连接路由器，将IP地址等相关信息通过LCD显示（只支持2.4G网络）。
'''
# 导入相关模块
import network,time,json,os,gc
from libs import ap


class MultiWifi:
    __log    = None
    __color  = None
    __screen = None
    
    def __init__(self, log, color, screen):
        self.__log = log
        self.__color = color
        self.__screen = screen
    
    '配置Wifi的参数'
    def config(self):
        self.__log.info("MultiWifi.config")
        
        # 如没有配置过，启动AP配网模式
        while 'wifilist.cfg' not in os.listdir('/data/config/'):
            self.__log.info("MultiWifi startAP")
            ap.startAP()
            
    #WIFI连接函数
    def wifi_connect(self,ssid,passwd):
        self.__log.info("Wifi.connect")
         

        wlan = network.WLAN(network.STA_IF) #STA模式
        wlan.active(False)
        time.sleep_ms(10)
        wlan.active(True)                   #激活接口
        start_time=time.time()              #记录时间做超时判断

        if not wlan.isconnected():
            self.__log.info('MultiWifi connecting to network ' + ssid)
            
            filepath = "/data/picture/winxp/"
            
            # 显示XP开机界面的背景
            self.__screen.picture(0, 0, filepath + "winxp.jpg")
            
            wlan.connect(ssid, passwd) #输入WIFI账号密码
            #显示IP信息
            #lcd.printStr('connecting AP:',10,50,color=(255,255,255),size=2)
            #lcd.printStr(ssid, 10, 110, color=(255,255,255), size=2)
            index=1
            while not wlan.isconnected():
 
                # 显示XP开机界面的滚动条
                x = 74
                if (index == 1 or index == 2 or index == 3):
                    self.__screen.picture(x, 187, filepath + "progressbar/" + str(index) + ".jpg")
                elif (4 <= index <= 15):
                    self.__screen.picture(x + 6 * (index - 3), 187, filepath + "progressbar/" + "3.jpg")
                    self.__screen.draw_rect(x + 6 * (index - 4), 187, 6, 7, self.__color.BLACK, 0, self.__color.BLACK)
                elif (index == 16):
                    self.__screen.picture(x + 6 * (index - 3), 187, filepath + "progressbar/" + "4.jpg")
                    self.__screen.draw_rect(x + 6 * (index - 4), 187, 6, 7, self.__color.BLACK, 0, self.__color.BLACK)
                elif (index == 17):
                    self.__screen.picture(x + 6 * (index - 3), 187, filepath + "progressbar/" + "5.jpg")
                    self.__screen.draw_rect(x + 6 * (index - 4), 187, 6, 7, self.__color.BLACK, 0, self.__color.BLACK)
                else:
                    self.__screen.draw_rect(x + 6 * (18 - 4), 187, 6, 7, self.__color.BLACK, 0, self.__color.BLACK)
                    
                time.sleep_ms(40)
                
                index += 1
                index %= 18

                #超时判断,15秒没连接成功判定为超时
                if time.time()-start_time > 15 :
                    self.__log.info('MultiWifi  Connected Timeout!')
                    self.__screen.fill(self.__color.BLACK)
                    self.__screen.print_str('WIFI Connected Timeout!', 10, 50, self.__color.RED, self.__color.BLACK, size=1)
                    self.__screen.print_str(ssid, 10, 120, self.__color.RED, self.__color.BLACK, size=1)
                    
                    self.__log.info('WIFI Connect (' + ssid + ') Timeout!')
                    wlan.active(False) #反使能WiFi
                    break

        if wlan.isconnected():
             
            #串口打印信息
            self.__log.info('network information:'+ str(wlan.ifconfig()))
            
         

    def multi_wifi_connect(self):
        self.__log.info("Multi.multi_wifi_connect")   
        #执行WIFI连接函数
        f = open('/data/config/wifilist.cfg', 'r') #获取账号密码
        info = json.loads(f.read())
        f.close()

    #     print(info)
        wlan = network.WLAN(network.STA_IF) #STA模式
        self.__screen.picture(5,5,"/data/picture/wifi_slash.jpg")
        if not wlan.isconnected():
            for data in info:
                self.__log.info(data)   
                wificonfig=json.loads(data)
    #             print(wificonfig)
    #             wdt.feed() #喂狗
                self.wifi_connect(wificonfig['ssid'],wificonfig['password'])
                
                if wlan.isconnected():
                    self.__log.info(wificonfig['ssid']+' connected.')
                    gc.collect()
                    return True
        else:
    #         print(dir(wlan))
            self.__screen.picture(5,5,"/data/picture/wifi.jpg")
            self.__log.info('connected AP:'+wlan.config('essid'))
            #显示IP信息
            #self.__screen.print_str('connected AP:',10,50,color=(255,255,255),backcolor=None,size=2)
            #self.__screen.print_str(wlan.config('essid'),30,80,color=(255,255,255),backcolor=None,size=2)
            #串口打印信息
            self.__log.info('network information: '  )
            self.__log.info(str(wlan.ifconfig()))
        gc.collect()

if __name__=='__main__':
    from lib.common.log import Log      # 日志
    from lib.common.color import Color  # 颜色

    from lib.device.screen import Screen  # 屏幕
    
    gc.collect()

    log   = Log()
    color = Color()
 
    screen = Screen(log)
    multiwifi=MultiWifi(log, color, screen)
    
    multiwifi.config()
    log.info("before Multi.multi_wifi_connect")   
    multiwifi.multi_wifi_connect()
