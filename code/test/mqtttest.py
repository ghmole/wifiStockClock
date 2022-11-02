'''
实验名称：MQTT通信
版本：v1.0
日期：2022.5
作者：01Studio
说明：编程实现MQTT通信，实现订阅（接收）数据。
MQTT助手：http://www.tongxinmao.com/txm/webmqtt.php#collapseOne
'''
import network,time
from lib.service.mqttrobust import MQTTClient #导入MQTT板块
from machine import Pin,Timer
from tftlcd import LCD15

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


#设置MQTT回调函数,有信息时候执行
def MQTT_callback(topic, msg):
    print('topic: {}'.format(topic))
    print('msg: {}'.format(msg))

#接收数据任务
def MQTT_Rev(tim):
    client.check_msg()
    print('check mqtt')

#执行WIFI连接函数并判断是否已经连接成功
if WIFI_Connect():

    SERVER = 'mq.tongxinmao.com'
    PORT = 18830
    CLIENT_ID = 'pyClockXuke'   # 客户端ID
    TOPIC = '/public/pyXuke/1' # TOPIC名称

    client = MQTTClient(CLIENT_ID, SERVER, PORT) #建立客户端对象
    client.set_callback(MQTT_callback)  #配置回调函数
    client.connect()
    client.subscribe(TOPIC) #订阅主题

    #开启RTOS定时器，编号为-1,周期300ms，执行socket通信接收任务
    tim = Timer(-1)
    tim.init(period=300, mode=Timer.PERIODIC,callback=MQTT_Rev)
