from machine import Timer
from time import sleep_ms
import bluetooth,gc
from lib.common.log import Log
gc.collect()

class BluetoothService():
    __conn_handle=None
    __BLE_MSG = ""
    __log = None
    def __init__(self, name, log):
        self.__log=log
        self.timer1 = Timer(0)
        self.name = name
        self.ble = bluetooth.BLE()
        self.ble.active(True)
        self.ble.config(gap_name=name)
        self.disconnected()
        self.ble.irq(self.ble_irq)
        self.register()
        self.advertiser()

    def connected(self):
        self.timer1.deinit()

    def disconnected(self):        
        self.timer1.init(period=5000, mode=Timer.PERIODIC, callback=lambda t: self.__log.info('bt wait connect'+str(t)))

    def ble_irq(self, event, data):
        
        if event == 1: #_IRQ_CENTRAL_CONNECT 手机链接了此设备
            self.__conn_handle, addr_type, addr = data
            self.connected()
        elif event == 2: #_IRQ_CENTRAL_DISCONNECT 手机断开此设备
            self.advertiser()
            self.disconnected()
            self.__conn_handle=None
        elif event == 3: #_IRQ_GATTS_WRITE 手机发送了数据 
            buffer = self.ble.gatts_read(self.rx)
            self.__BLE_MSG = buffer.decode('UTF-8').strip()
            
    def register(self):        
        service_uuid = '6E400001-B5A3-F393-E0A9-E50E24DCCA9E'
        reader_uuid = '6E400002-B5A3-F393-E0A9-E50E24DCCA9E'
        sender_uuid = '6E400003-B5A3-F393-E0A9-E50E24DCCA9E'

        services = (
            (
                bluetooth.UUID(service_uuid), 
                (
                    (bluetooth.UUID(sender_uuid), bluetooth.FLAG_NOTIFY), 
                    (bluetooth.UUID(reader_uuid), bluetooth.FLAG_WRITE),
                )
            ), 
        )

        ((self.tx, self.rx,), ) = self.ble.gatts_register_services(services)

    def send(self, data):
        self.ble.gatts_notify(self.__conn_handle, self.tx, data + '\n')

    def advertiser(self):
        name = bytes(self.name, 'UTF-8')
        adv_data = bytearray('\x02\x01\x02') + bytearray((len(name) + 1, 0x09)) + name
        self.ble.gap_advertise(100, adv_data)
        self.__log.info(adv_data)
        self.__log.info("\r\n")

    def set_msg(self, msg):
        self.__BLE_MSG=msg
    
    def get_msg(self):
        return self.__BLE_MSG
 
# if __name__ == "__main__":
#     log=Log()
#     ble = BluetoothService("pyClockBLE",log)
# 
#  
# 
#     while True:
#         if ble.get_msg() == 'read':
#             log.info(ble.get_msg())
#             ble.set_msg("")
#  
#             ble.send('LED is state.')
#         elif ble.get_msg() == 'off':
#             log.info('led will off')
#             ble.set_msg("")
#         elif ble.get_msg() == 'on':
#             log.info('led will on')
#             ble.set_msg("")
#         
#         sleep_ms(1000)



