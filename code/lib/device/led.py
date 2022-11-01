# 导入相关模块
from machine import Pin

class Led:
    __log = None
    
    def __init__(self, log):
        self.__log = log
    
    '开启Led灯'
    def turn_on(self):
        self.__log.info('Led.turn_on')
        
        led = Pin(2, Pin.OUT)
        led.value(1) 
    
    '关闭Led灯'
    def turn_off(self):
        self.__log.info('Led.turn_off')
        
        led = Pin(2, Pin.OUT)
        led.value(0) 