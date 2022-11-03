'''
Class：PyClock天气时钟
Data：2022.7
Author：nxnqh
'''

import gc

# 主类
from lib.py_clock import PyClock

# 常用类
from lib.common.log import Log      # 日志
from lib.common.color import Color  # 颜色

# 设备类
gc.collect()
from lib.device.screen import Screen  # 屏幕
#from lib.device.wifi import Wifi      # Wifi
from lib.device.multiwifi import MultiWifi
from lib.device.led import Led        # Led灯

# 业务类
gc.collect()
from lib.service.time_service import TimeService                   # 时间
from lib.service.weather_baidu_service import WeatherBaiduService  # 天气
#from lib.service.upgrade_service import UpgradeService            # 更新
from lib.service.calendar_service import CalendarService           # 日历
from lib.service.stockservice import  StockService                 # 股票 
# UI类
gc.collect()
from lib.ui.clock_weather_ui import ClockWeatherUI              # 天气时间UI
#from lib.ui.clock_weather_win_xp_ui import ClockWeatherWinXpUI  # winxp 天气时间UI
from lib.ui.clock_stock_ui import ClockStockUI                  # 股票UI


gc.collect()

log   = Log()
color = Color()

screen = Screen(log)
#wifi   = Wifi(log, color, screen)
wifi   = MultiWifi(log, color, screen)
led    = Led(log)

time_service     = TimeService(log)
weather_service  = WeatherBaiduService(log)
calendar_service = CalendarService(log)
stock_service = StockService(log)

clock_weather_ui        = ClockWeatherUI(log, color, screen)
#clock_weather_win_xp_ui = ClockWeatherWinXpUI(log, color, screen)
clock_stock_ui = ClockStockUI(log, color, screen)


gc.collect()

# 运行设备
PyClock(
    log, color,
    screen, wifi, led,
    time_service, weather_service, calendar_service, stock_service,
    clock_weather_ui, clock_stock_ui
).run() 











