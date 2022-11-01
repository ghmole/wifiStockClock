import network,time
from lib.common.log import Log
from machine import Pin,Timer
from tftlcd import LCD15



#WIFI连接函数
def WIFI_Connect():

    WIFI_LED=Pin(2, Pin.OUT) #初始化WIFI指示灯

    wlan = network.WLAN(network.STA_IF) #STA模式
    wlan.active(True)                   #激活接口
    start_time=time.time()              #记录时间做超时判断

    if not wlan.isconnected():
        print('connecting to network...')
        wlan.connect('TP-LINK', '') #输入WIFI账号密码

        while not wlan.isconnected():

            #LED闪烁提示
            WIFI_LED.value(1)
            time.sleep_ms(300)
            WIFI_LED.value(0)
            time.sleep_ms(300)

            #超时判断,15秒没连接成功判定为超时
            if time.time()-start_time > 15 :
                print('WIFI Connected Timeout!')
                wlan.active(False) #反激活WiFi
                break

    if wlan.isconnected():
        #LED点亮
        WIFI_LED.value(1)

        #串口打印信息
        print('network information:', wlan.ifconfig())

        #显示IP信息
        d.printStr('IP/Subnet/GW:',10,10,color=BLUE,size=2)
        d.printStr(wlan.ifconfig()[0],10,50,color=WHITE,size=2)
        d.printStr(wlan.ifconfig()[1],10,80,color=WHITE,size=2)
        d.printStr(wlan.ifconfig()[2],10,110,color=WHITE,size=2)
        
        return True

    else:
        return False



from lib.service.stockservice import StockData,StockService

if __name__=='__main__':
    #定义常用颜色
    RED = (255,0,0)
    GREEN = (0,255,0)
    BLUE = (0,0,255)
    BLACK = (0,0,0)
    WHITE = (255,255,255)

    ########################
    # 构建1.5寸LCD对象并初始化
    ########################
    d = LCD15(portrait=1) #默认方向竖屏

    #填充白色
    d.fill(BLACK)
    WIFI_Connect()
    gc.collect()
    d=StockData()
    log = Log()
    ss=StockService(log)
    ss.query_stock('sh000001')
    d=ss.get_stock_data()
    
    
    print('stock_name: %s\n' % d.stock_name)
    print('stock_code: %s\n' % d.stock_code)
    print('last_price: %s\n' % d.last_price)
    print('pre_close: %s\n' % d.pre_close)
    print('open_price: %s\n' % d.open_price)
    print('low_price: %s\n' % (d.diff_price))
    print('high_price: %s\n' % (d.diff_percent))
