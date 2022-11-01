'''
实验名称：股票（主界面）
版本：v1.0
日期：2022.4
作者：CaptainJackey
说明：天气时钟信息
'''

#导入相关模块
 
import math
from machine import RTC
import network,time,gc,random
# 股票列表
#from libs import stocklist
from lib.device.multiwifi import MultiWifi
from libs.urllib import urequest
import tftlcd
import gc,json

########################
# 构建1.5寸LCD对象并初始化
########################
gc.collect()
d = tftlcd.LCD15(1)


# d = tftlcd.LCD15(portrait=1)

#定义常用颜色
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
YELLOW = (255,255,0)
DEEPGREEN = (1,179,105)

#空气质量颜色
BROWN=(101, 72, 91)
CYAN=(139, 230, 255)
LIGHTBLUE=(57, 143, 254)
YOU = (156,202,127) #优
LIANG = (249,218,101) #良 
QINGDU = (242,159,57) #轻度
ZHONGDU = (219,85,94) #中度
ZDU = (186,55,121) #重度
YANZHONG = (136,11,32) #严重
 

def datetime_display(datetime):
     
       
    #时间显示
    second = datetime[6]
    minute = datetime[5]
    hour = datetime[4]

    
    if hour > 9:
        d.printStr(str(hour), 160, 5, GREEN, size=1)
    else:
        d.printStr('0'+str(hour), 160, 5, GREEN, size=1)
    
    d.printStr(':', 180, 5, WHITE, size=1)
    
    if minute > 9:
        d.printStr(str(minute), 190, 5, YELLOW, size=1)
    else:
        d.printStr('0'+str(minute), 190, 5, YELLOW, size=1)
        
    d.printStr(':', 210, 5, WHITE, size=1)
    
    if second > 9:
        d.printStr(str(second), 220, 5, RED, size=1)
    else:
        d.printStr('0'+str(second), 220, 5, RED, size=1)
        
        
def background():#画出表盘
    
    #ZHONGDU=None
    d.drawRect(5,32,230,66,YOU,border=5,fillcolor=None)
    d.drawRect(5,102,230,66,YOU,border=5,fillcolor=None)
    d.drawRect(5,172,230,66,CYAN,border=5,fillcolor=None)
    colors=[BROWN,CYAN,LIGHTBLUE,YOU ,LIANG ,QINGDU,ZHONGDU,ZDU,YANZHONG]
#     for i in range(len(colors)):
#         c=colors[i]
#         print(c)
#         d.drawLine(i*15,34, i*15, 94, c)
    d.printStr('stock', 90, 1, CYAN, size=2)
        

#显示图片
def UI_Display(datetime):
    global UI_Change
    #print(UI_Change)
    if UI_Change: #首次画表盘
        
        UI_Change = 0        
        d.fill(BLACK) #清屏
        background()        

    
    datetime_display(datetime)
    
   
def get_rand():
    r=(random.random()-0.5)*100
    return r

def get_diff():
    r=get_rand()
    s=str('%04.2f' % r)
    print(len(s),s)
    if r<0:
        if len(s)<6:
            s=' '*(6-len(s))+s 
    else:
        if len(s)<5:
            s=' '*(5-len(s))+'+'+s
        else:
            s='+'+s
     
    return s
    
def get_perc():
    r=get_rand()
    s=str('%04.2f' % r)
    
    if r<0:
        if len(s)<6:
            s= ' '*(6-len(s))+s 
    else:
        if len(s)<5:
            s=' '*(5-len(s))+'+'+s
        else:
            s='+'+s
     
    return s+'%'


UI_Change = 1 
###########################
if __name__=='__main__':
#     print(dir(d))
    rtc = RTC()
    
    datetime=rtc.datetime()
    print(datetime)
    
    #print(UI_Change)
    UI_Display(datetime)
    datetime_display(datetime)
    #print(datetime[6]%30)
    d.printStr('000001', 10, 36, color=WHITE, backcolor=YANZHONG,size=3)
    d.printStr(get_diff(), 155, 40, color=RED, backcolor=YANZHONG,size=2)
    d.printStr(get_perc(), 170, 72, color=GREEN, backcolor=YANZHONG,size=1)
    lastdatetime=datetime
    cnt=1;
    while True:
        gc.collect()
        datetime=rtc.datetime()
        if lastdatetime[6]!=datetime[6]:
            
            UI_Display(datetime)
            stt='%06d' % cnt
            cnt+=1
            lastdatetime=datetime
             
            d.printStr(stt, 10, 36, color=WHITE, backcolor=None,size=3)
            r=get_rand()
            if r>=0:
                cl=RED
            else:
                cl=GREEN
            d.printStr(get_diff(), 155, 40, color=cl, backcolor=None,size=2)
            d.printStr(get_perc(), 170, 72, color=cl, backcolor=None,size=1)
            
            
            d.printStr(stt, 10, 106, color=WHITE, backcolor=YANZHONG,size=3)
            print(gc.mem_free())
            
            gc.collect()
            print(gc.mem_free())
            print('-'*40)
            if cnt>10:
                break
            
        time.sleep_ms(20)
        if datetime[6]%30==0:
            print('get stock')
