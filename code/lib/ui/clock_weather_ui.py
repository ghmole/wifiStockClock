# 导入工具类
import gc

class ClockWeatherUI():
    __log    = None
    __color  = None
    __screen = None
    
    def __init__(self, log, color, screen):
        self.__log = log
        self.__color = color
        self.__screen = screen
        
        
    __last_today_weather = ''
    __last_now_warn = ''
    __last_now_warn_color = ''
    __last_now_aqi = ''
    __last_now_weather = ''
    __last_now_temp = ''
    __last_now_wind_level = ''
    __last_now_nongli= ''
    __last_temps = ['', '', '']
    
    __last_later_weathers = []
    __last_later_temps = []
    
    __last_hour = -1
    
    
    
    
    
    '初始化界面'
    def init(self):
        gc.collect()
        
        self.__screen.fill(self.__color.BLACK)
        
        self.__last_today_weather = ''
        self.__last_now_warn = ''
        self.__last_now_warn_color = ''
        self.__last_now_aqi = ''
        self.__last_now_weather = ''
        self.__last_now_temp = ''
        self.__last_now_wind_level = ''
        self.__last_now_nongli = ''
        self.__last_temps = ['', '', '']
        
        self.__last_later_weathers = []
        self.__last_later_temps = []
        
        self.__last_hour = -1
    
    '刷新界面信息'
    def refresh(self, datetime, weather_bean, weather_warn, calendar_bean):
        gc.collect()
        
        # 今日天气
        if (self.__last_today_weather != weather_bean.today_weather):
            self.__screen.print_str("            ", 5, 5, color = self.__color.BLACK, backcolor = self.__color.BLACK, size = 2) # 清屏        
            
            # 最多显示6个字
            self.__screen.print_chinese(weather_bean.today_weather[:6], 5, 5, color = self.__color.WHITE, backcolor = self.__color.BLACK, size = 2)
            self.__last_today_weather = weather_bean.today_weather

        # 天气预警
        if (weather_warn[0] != ''):
            warn_color_str = weather_warn[1]
            warn_color = self.__color.BLACK
            warn_content = weather_warn[0]
            warn_content_color = self.__color.WHITE

            if (self.__last_now_warn_color != warn_color_str or self.__last_now_warn != warn_content):
                self.__last_now_warn_color = warn_color_str
                self.__last_now_warn = warn_content
                
                if (warn_color_str == "蓝"):
                    warn_color = self.__color.BLUE
                elif (warn_color_str == "黄"):
                    warn_color = (240,202,0)
                elif (warn_color_str == "橙"):
                    warn_color = self.__color.ORANGE
                else:
                    warn_color = (193,18,28)
                    
                if (warn_content == "雷暴大风" or warn_content == "雷雨大风"):
                    warn_content = "雷风"
                elif (warn_content == '沙尘暴'):
                    warn_content = "沙尘"
                elif (warn_content == '道路积冰'):
                    warn_content = "积冰"
                elif (warn_content == '道路积雪'):
                    warn_content = "积雪"
                elif (warn_content == '道路冰雪'):
                    warn_content = "冰雪"
                elif (warn_content == '森林草原火险' or warn_content == '森林火险' or warn_content == '草原火险'):
                    warn_content = "火险"
                elif (warn_content == '地质灾害气象风险' or warn_content == '地质灾害'):
                    warn_content = "地质"
                elif (warn_content == '强季风'):
                    warn_content = "季风"

                self.__screen.print_chinese(warn_content, 158, 5, color = warn_content_color, backcolor = warn_color, size = 2)

        else:
            self.__screen.print_str("    ", 158, 5, color = self.__color.BLACK, backcolor = self.__color.BLACK, size = 2)
        
        # 空气指数
        if (self.__last_now_aqi != weather_bean.now_aqi):
            now_aqi = int(weather_bean.now_aqi)
            index = 0
            if 0 <= now_aqi < 50: #优
                index = 0
            elif 50 <= now_aqi < 100:#良
                index = 1
            elif 100 <= now_aqi < 150:#轻度
                index = 2
            elif 150 <= now_aqi < 200:#中度
                index = 3
            elif 200 <= now_aqi < 300:#重度
                index = 4
            elif 300 <= now_aqi < 500:#严重
                index = 5
            aqi_chn=['优','良','轻','中','重','严']
            aqi_color = [self.__color.AQI_YOU, self.__color.AQI_LIANG, self.__color.AQI_QINGDU, self.__color.AQI_ZHONGDU, self.__color.AQI_ZDU, self.__color.AQI_YANZHONG]
            
            self.__screen.print_chinese(aqi_chn[index], 211, 5, color = self.__color.WHITE, backcolor = aqi_color[index], size = 2)
            
            self.__last_now_aqi = weather_bean.now_aqi
        
        color_word = (200, 200, 200)
        # 实时天气
        if (self.__last_now_weather != weather_bean.now_weather):
            self.__screen.print_str("          ", 5, 35, color = self.__color.BLACK, backcolor = self.__color.BLACK, size = 1) # 清屏
            self.__screen.print_chinese(weather_bean.now_weather[:5], 5, 35, color = color_word, backcolor = self.__color.BLACK, size = 1)
 
            self.__last_now_weather = weather_bean.now_weather
            
        # 风力
        if (self.__last_now_wind_level != weather_bean.now_wind_level):
            x = 90
            self.__screen.clear(x - 5, 35, 52, 16, self.__color.BLACK)
            #self.__screen.draw_rect(x - 5, 35, 52, 16, self.__color.BLACK, 0, self.__color.BLACK)
            now_wind_level = weather_bean.now_wind_level
            now_wind_level = now_wind_level.split("级")[0]
            
            if (now_wind_level == '0'):
                self.__screen.print_chinese('无风', x + 5, 35, color = color_word, backcolor = self.__color.BLACK, size = 1)
            else:
                if (int(now_wind_level) >= 10):
                    x2 = x - 4
                    self.__screen.print_str(now_wind_level, x2, 35, color = color_word, backcolor = self.__color.BLACK, size = 1)
                    x2 += len(now_wind_level) * 8 + 2
                    self.__screen.print_chinese('级风', x2, 35, color = color_word, backcolor = self.__color.BLACK, size = 1)

                else:
                    x2 = x + 1
                    self.__screen.print_str(now_wind_level, x2, 35, color = color_word, backcolor = self.__color.BLACK, size = 1)
                    x2 += len(now_wind_level) * 8 + 2
                    self.__screen.print_chinese('级风', x2, 35, color = color_word, backcolor = self.__color.BLACK, size = 1)

            self.__last_now_wind_level = weather_bean.now_wind_level
            
        # 农历
        now_nongli = calendar_bean.l_month_cn + calendar_bean.l_day_cn
        if (self.__last_now_nongli != now_nongli):
            x = 147
            
            self.__screen.clear(143, 35, 95, 16, self.__color.BLACK)
            #self.__screen.draw_rect(143, 35, 95, 16, self.__color.BLACK, 0, self.__color.BLACK)
            
            color_term = (50, 205, 50)
            color_festival = (0, 191, 255)
            
            # 非 节气和节日
            if (calendar_bean.is_term == False and calendar_bean.is_festival  == False):
                t = now_nongli
                
                x2 = x + 8
                if (len(t) == 4):
                    x2 += 16
                self.__screen.print_chinese(t, x2, 35, color = color_word, backcolor = self.__color.BLACK, size = 1)
            
            # 只是节气
            elif (calendar_bean.is_term == True and calendar_bean.is_festival  == False):
                t = calendar_bean.term
                
                x2 = x + 8
                x2 += 16 * 3
                self.__screen.print_chinese(t, x2, 35, color = color_term, backcolor = self.__color.BLACK, size = 1)
            
            # 只是节日，且只有一个节日
            elif (calendar_bean.is_term == False and calendar_bean.is_festival  == True and len(calendar_bean.festival_list) == 1):
                t = calendar_bean.festival_list[0]
                
                x2 = x + 8
                x2 += 16 * 2
                
                if (len(t) == 2):
                    x2 += 16
                self.__screen.print_chinese(t, x2, 35, color = color_festival, backcolor = self.__color.BLACK, size = 1)
            
            # 有节气和节日 或 没有节气，但有多个节日
            else:
                if (calendar_bean.is_term == True):
                    t1 = calendar_bean.term
                    t2 = calendar_bean.festival_list[0]
                    
                    chn_num = len(t1) + len(t2)
                    
                    x2 = x - 4
                    if (len(t1 + t2) == 4):
                        x2 += 16
                    
                    self.__screen.print_chinese(t1, x2, 35, color = color_term, backcolor = self.__color.BLACK, size = 1)
                    
                    x2 += 16 * 2
                    self.__screen.print_str('|', x2, 35, color = color_word, backcolor = self.__color.BLACK, size = 1)
                    
                    x2 += 12
                    self.__screen.print_chinese(t2, x2, 35, color = color_festival, backcolor = self.__color.BLACK, size = 1)
                else:
                    t1 = calendar_bean.festival_list[1]
                    t2 = calendar_bean.festival_list[0]
                    
                    x2 = x - 4
                    
                    chn_num = len(t1) + len(t2)                    
                    if (chn_num == 6):
                        if (t1[2:3] == '节'):
                            t1 = t1[0:2]
                            
                            self.__screen.print_chinese(t1, x2, 35, color = color_festival, backcolor = self.__color.BLACK, size = 1)
                            
                            x2 += 16 * 2
                            self.__screen.print_str('|', x2, 35, color = color_word, backcolor = self.__color.BLACK, size = 1)
                            
                            x2 += 12
                            self.__screen.print_chinese(t2, x2, 35, color = color_festival, backcolor = self.__color.BLACK, size = 1)

                        else:
                            t2 = t2[0:2]
                            
                            self.__screen.print_chinese(t1, x2, 35, color = color_festival, backcolor = self.__color.BLACK, size = 1)
                            
                            x2 += 16 * 3
                            self.__screen.print_str('|', x2, 35, color = color_word, backcolor = self.__color.BLACK, size = 1)
                            
                            x2 += 12
                            self.__screen.print_chinese(t2, x2, 35, color = color_festival, backcolor = self.__color.BLACK, size = 1)
                            
                    elif (chn_num == 5):
                        self.__screen.print_chinese(t1, x2, 35, color = color_festival, backcolor = self.__color.BLACK, size = 1)
                        
                        x2 += 16 * len(t1)
                        self.__screen.print_str('|', x2, 35, color = color_word, backcolor = self.__color.BLACK, size = 1)
                        
                        x2 += 12
                        self.__screen.print_chinese(t2, x2, 35, color = color_festival, backcolor = self.__color.BLACK, size = 1)
                        
                    else:
                        x2 += 16
                    
                        self.__screen.print_chinese(t1, x2, 35, color = color_festival, backcolor = self.__color.BLACK, size = 1)
                        
                        x2 += 16 * len(t1)
                        self.__screen.print_str('|', x2, 35, color = color_word, backcolor = self.__color.BLACK, size = 1)
                        
                        x2 += 12
                        self.__screen.print_chinese(t2, x2, 35, color = color_festival, backcolor = self.__color.BLACK, size = 1)
                    

            self.__last_now_nongli = now_nongli
        
        # 时间
        second = datetime[6]
        minute = datetime[5]
        hour = datetime[4]
        
        x = 15
        y = 67
        if hour > 9:
            self.__screen.print_str(str(hour), x, y, color = self.__color.ORANGE, backcolor = None, size=4)
        else:
            self.__screen.print_str('0'+str(hour), x, y, color = self.__color.ORANGE, backcolor = None, size=4)
        
        if (second % 2 == 0):
            self.__screen.print_str(':', x + 48, y - 4, color = (200, 200, 200), backcolor = None, size=4)
        else:
            self.__screen.print_str(' ', x + 48, y - 4, color = (200, 200, 200), backcolor = None, size=4)

        if minute > 9:
            self.__screen.print_str(str(minute), x + 72, y, color = self.__color.YELLOW, backcolor = None, size=4)
        else:
            self.__screen.print_str('0'+str(minute), x + 72, y, color = self.__color.YELLOW, backcolor = None, size=4)
            
        # 日期
        month = datetime[1]
        day = datetime[2]
        week = datetime[3]
 
        x = 156
        y = y + 20
        color = self.__color.WHITE
        if (month < 10):
            month_str = '0' + str(month)
        else:
            month_str = str(month)
        if (day < 10):
            day_str = '0' + str(day)
        else:
            day_str = str(day)
            
        self.__screen.print_str(month_str, x, y, color, backcolor = None, size=2)
        self.__screen.print_str('-', x + 27, y, color, backcolor = None, size=2)
        self.__screen.print_str(day_str, x + 42, y, color, backcolor = None, size=2)
        
        week_list = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        self.__screen.print_str(week_list[week], 178, y - 15, color, backcolor = None, size=1)
        
        #week_list = ['一','二','三','四','五','六','日']
        #self.__screen.print_chinese(week_list[week], 181, y - 15, (200, 200, 200), backcolor = self.__color.BLACK, size = 1)
        
        # 未来N个小时的温度（最多24小时）
        x_begin = 37
        y_begin = 131
        y_end = 145
        base_height = 2
        width = 168
        n = 24

        if (self.__last_later_temps != weather_bean.later_temps or self.__last_later_weathers != weather_bean.later_weathers):
            # 清除之前绘制的图像
            self.__screen.clear(x_begin, y_begin, width, y_end - y_begin + base_height, self.__color.BLACK)
            #self.__screen.draw_rect(x_begin, y_begin, width, y_end - y_begin + base_height, self.__color.BLACK, 0, self.__color.BLACK)
 
            # 虚线
            if (weather_bean.later_temps_y[2] != weather_bean.later_temps[24]): # 第25小时是最高温度的话，就不画了
                for k in range(n):
                    i = n - 1 - k
                    if (weather_bean.later_temps[i] == weather_bean.later_temps_y[2]):
                        for j in range(int(width * (k + 1) / n)):
                            x4 = x_begin + int(width * i / n) + j
                            if (2 <= j % 7 <= 5):
                                self.__screen.draw_line(x4, y_begin, x4 + 1, y_begin, (128,128,128))
                            else:
                                self.__screen.draw_line(x4, y_begin, x4 + 1, y_begin, self.__color.BLACK)
                        
                        break
            
            # 最高温度
            self.__screen.print_str('   ', x_begin + width, y_begin - 8, (128,128,128), backcolor = None, size = 1)
            if (weather_bean.later_temps_y[2] <= -10):
                self.__screen.print_str(str(weather_bean.later_temps_y[2]), x_begin + width + 8, y_begin - 8, (128,128,128), backcolor = None, size = 1)
            elif (-10 < weather_bean.later_temps_y[2] < 0 or 10 <= weather_bean.later_temps_y[2]):
                self.__screen.print_str(str(weather_bean.later_temps_y[2]), x_begin + width + 8, y_begin - 8, (128,128,128), backcolor = None, size = 1)
            else:
                self.__screen.print_str(str(weather_bean.later_temps_y[2]), x_begin + width + 8, y_begin - 8, (128,128,128), backcolor = None, size = 1)
            
            # 最低温度
            self.__screen.print_str('   ', x_begin + width , y_end + base_height - 8, (128,128,128), backcolor = None, size = 1)
            if (weather_bean.later_temps_y[0] <= -10):
                self.__screen.print_str(str(weather_bean.later_temps_y[0]), x_begin + width + 8, y_end + base_height - 8, (128,128,128), backcolor = None, size = 1)
            elif (-10 < weather_bean.later_temps_y[0] < 0 or 10 <= weather_bean.later_temps_y[0]):
                self.__screen.print_str(str(weather_bean.later_temps_y[0]), x_begin + width + 8, y_end + base_height - 8, (128,128,128), backcolor = None, size = 1)
            else:
                self.__screen.print_str(str(weather_bean.later_temps_y[0]), x_begin + width + 8, y_end + base_height - 8, (128,128,128), backcolor = None, size = 1)
            
            # 实时温度
            self.__screen.clear(x_begin - 32, y_begin - 8, 28, y_end - y_begin + base_height + 16, self.__color.BLACK)
            #self.__screen.draw_rect(x_begin - 32, y_begin - 8, 28, y_end - y_begin + base_height + 16, self.__color.BLACK, 0, self.__color.BLACK)
            now_temp_y = round(y_end - (y_end - y_begin) * 1.0 / (weather_bean.later_temps_y[2] - weather_bean.later_temps_y[0]) * (weather_bean.later_temps[0] - weather_bean.later_temps_y[0])) - 8
            if (weather_bean.later_temps[0] <= -10):
                self.__screen.print_str(str(weather_bean.later_temps[0]), x_begin - 32, now_temp_y, (128,128,128), backcolor = None, size = 1)
            elif (-10 < weather_bean.later_temps[0] < 0 or 10 <= weather_bean.later_temps[0]):
                self.__screen.print_str(str(weather_bean.later_temps[0]), x_begin - 24, now_temp_y, (128,128,128), backcolor = None, size = 1)
            else:
                self.__screen.print_str(str(weather_bean.later_temps[0]), x_begin - 16, now_temp_y, (128,128,128), backcolor = None, size = 1)
            # self.__screen.draw_line(x_begin - 4 , now_temp_y + 8, x_begin - 2, now_temp_y + 8, (183,183,183))
            
            for i in range(n):
                later_weather = weather_bean.later_weathers[i]
                
                color_weather = color
                    
                if (later_weather == "晴"):
                    color_weather = self.__color.WEATHER_QING
                elif (later_weather == "阴"):
                    color_weather = self.__color.WEATHER_YIN
                elif (later_weather == "多云"):
                    color_weather = self.__color.WEATHER_DUOYUN
                elif (later_weather == "阵雨"):
                    color_weather = self.__color.WEATHER_ZHENYU
                elif (later_weather == "雷阵雨"):
                    color_weather = self.__color.WEATHER_LEIZHENYU
                elif (later_weather == "小雨"):
                    color_weather = self.__color.WEATHER_XIAOYU
                elif (later_weather == "中雨"):
                    color_weather = self.__color.WEATHER_ZHONGYU
                elif (later_weather == "大雨"):
                    color_weather = self.__color.WEATHER_DAYU
                elif (later_weather == "暴雨"):
                    color_weather = self.__color.WEATHER_DAYU
                    
                elif (later_weather == "小雪"):
                    color_weather = self.__color.WEATHER_XIAOXUE
                elif (later_weather == "中雪"):
                    color_weather = self.__color.WEATHER_ZHONGXUE
                elif (later_weather == "大雪"):
                    color_weather = self.__color.WEATHER_DAXUE
                elif (later_weather == "暴雪"):
                    color_weather = self.__color.WEATHER_BAOXUE
                elif (later_weather == "大雾" or later_weather == "雾"):
                    color_weather = self.__color.WEATHER_WU
                elif (later_weather == "雨夹雪"):
                    color_weather = self.__color.WEATHER_XIAOYU
                else:
                    pass
                
                x = x_begin + int(width * i / n)
                y = round(y_end - (y_end - y_begin) * 1.0 / (weather_bean.later_temps_y[2] - weather_bean.later_temps_y[0]) * (weather_bean.later_temps[i] - weather_bean.later_temps_y[0]))
                #self.__screen.draw_line(x, y, x, y, self.__color.WHITE)
                
                # 斜线
                x2 = x_begin + int(width * (i + 1) / n) - 2
                y2 = round(y_end - (y_end - y_begin) * 1.0 / (weather_bean.later_temps_y[2] - weather_bean.later_temps_y[0]) * (weather_bean.later_temps[i + 1] - weather_bean.later_temps_y[0]))
                # self.__screen.draw_line(x, y, x2, y2, color_weather)
                
                # 填充
                for j in range(int(width / n) - 1):
                    x3 = x + j
                    y3 = round(y - (y - y2) * 1.0 * j / (int(width / n) - 1))
                    
                    if (later_weather == "雨夹雪"):
                        self.__screen.draw_line(x3, y3, x3, y3 + int((y_end + base_height - y3) / 2), color_weather)
                        self.__screen.draw_line(x3, y3 + int((y_end + base_height - y3) / 2) + 1, x3, y_end + base_height, self.__color.WEATHER_XIAOXUE)
                    else:
                        self.__screen.draw_line(x3, y3, x3, y_end + base_height, color_weather)
              

            if (self.__last_later_temps == []):
                self.__last_later_temps = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0]

            for i in range(n + 1):
                self.__last_later_temps[i] = weather_bean.later_temps[i]
                
            if (self.__last_later_weathers == []):
                self.__last_later_weathers = ['','','','','','','','','','','','','','','','','','','','','','','','']

            for i in range(n):
                self.__last_later_weathers[i] = weather_bean.later_weathers[i]
        
        
        if (self.__last_hour != hour):
            # 清除之前绘制的图像
            self.__screen.clear(x_begin - 3, y_end + base_height + 1, width + 6, 5, self.__color.BLACK)
            #self.__screen.draw_rect(x_begin - 3, y_end + base_height + 1, width + 6, 5, self.__color.BLACK, 0, self.__color.BLACK)

            # 12/24点分隔符                    
            if (hour == 0):
                x_start = x_begin - 1 + int(width * 1.0 * 12 / 24)
            elif (hour == 12):
                x_start = x_begin - 1 
            else:
                if (hour < 12):
                    x_start = x_begin - 1 + int(width * 1.0 * (12 - hour) / 24)
                else:
                    x_start = x_begin - 1 + int(width * 1.0 * (24 - hour) / 24)
            
            if (hour > 12):
                self.__screen.draw_line(x_start, y_end + base_height + 1, x_start, y_end + base_height + 5, self.__color.BLUE)
            else:
                self.__screen.draw_line(x_start, y_end + base_height + 1, x_start, y_end + base_height + 5, (183,183,183))
            
            x_start += int(width * 1.0 * 12 / 24)
            
            if (hour > 12):
                self.__screen.draw_line(x_start, y_end + base_height + 1, x_start, y_end + base_height + 5, (183,183,183))
            else:
                self.__screen.draw_line(x_start, y_end + base_height + 1, x_start, y_end + base_height + 5, self.__color.BLUE)
                
                
            # 日落日出
            self.__screen.clear(0, y_end + base_height + 8, 240, 16, self.__color.BLACK)
            #self.__screen.draw_rect(0, y_end + base_height + 8, 240, 16, self.__color.BLACK, 0, self.__color.BLACK)
            
            sunriseHour = int(weather_bean.sunriseTime.split(':')[0])
            if (hour <= sunriseHour):
                x_start = x_begin - 1 + int(width * 1.0 * (sunriseHour - hour) / 24)
            else:
                x_start = x_begin - 1 + int(width * 1.0 * (24 - hour + sunriseHour) / 24)
            for i in range(7):
                self.__screen.draw_line(x_start + i + 1, y_end + base_height + 5, x_start + i + 1, y_end + base_height + 2 + abs(3 - i), (128,128,128))  
            
            self.__screen.print_str(weather_bean.sunriseTime, x_start - 16, y_end + base_height + 7, (128,128,128), backcolor = None, size = 1)
            
            
            
            sunsetHour = int(weather_bean.sunsetTime.split(':')[0])
            if (hour <= sunsetHour):
                x_start = x_begin - 1 + int(width * 1.0 * (sunsetHour - hour) / 24)
            else:
                x_start = x_begin - 1 + int(width * 1.0 * (24 - hour + sunsetHour) / 24)
            for i in range(7):
                self.__screen.draw_line(x_start + i + 1, y_end + base_height + 4 - abs(3 - i), x_start + i + 1, y_end + base_height + 1, (128,128,128))  
            
            self.__screen.print_str(weather_bean.sunsetTime, x_start - 16, y_end + base_height + 7, (128,128,128), backcolor = None, size = 1)
            
            
            self.__last_hour = hour
            
                    
        '未来三天天气'
        x = 15
        y = 178
        color = (255, 255, 255)
        color2 = (200, 200, 200)
        
        #self.__screen.picture(x + 10, y, self.__get_weather_picture(weather_bean.today_weather))
        self.__screen.picture(x + 10, y, self.__get_weather_picture(weather_bean.now_weather))
        # self.__screen.print_str(weather_bean.today_month + '.' + weather_bean.today_day, x + 10, y - 21, color, backcolor = None, size = 1)
        temp_str = weather_bean.today_temp_l + '~' + weather_bean.today_temp_h
        if (self.__last_temps[0] != temp_str):
            self.__screen.clear(x, y + 45, 70, 16, self.__color.BLACK)
            #self.__screen.draw_rect(x, y + 45, 70, 16, self.__color.BLACK, 0, self.__color.BLACK)
            self.__screen.print_str(temp_str, x + 10 + self.__get_temp_x(weather_bean.today_temp_l, weather_bean.today_temp_h), y + 45, color2, backcolor = None, size = 1)
            
            self.__last_temps[0] = temp_str
        
        
        self.__screen.picture(x + 10 + 75 * 1, y, self.__get_weather_picture(weather_bean.tommorow_weather))
        # self.__screen.print_str(weather_bean.tommorow_month + '.' + weather_bean.tommorow_day, x + 10 + 75 * 1, y - 21, color, backcolor = None, size = 1)
        temp_str = weather_bean.tommorow_temp_l + '~' + weather_bean.tommorow_temp_h
        if (self.__last_temps[1] != temp_str):
            self.__screen.clear(x + 70, y + 45, 70, 16, self.__color.BLACK)
            #self.__screen.draw_rect(x + 70, y + 45, 70, 16, self.__color.BLACK, 0, self.__color.BLACK)
            self.__screen.print_str(temp_str, x + 10 + 75 * 1 + self.__get_temp_x(weather_bean.tommorow_temp_l, weather_bean.tommorow_temp_h), y + 45, color2, backcolor = None, size = 1)
            
            self.__last_temps[1] = temp_str
        
        self.__screen.picture(x + 10 + 75 * 2, y, self.__get_weather_picture(weather_bean.houtian_weather))
        # self.__screen.print_str(weather_bean.houtian_month + '.' + weather_bean.houtian_day, x + 10 + 75 * 2, y - 21, color, backcolor = None, size = 1)
        temp_str = weather_bean.houtian_temp_l + '~' + weather_bean.houtian_temp_h
        if (self.__last_temps[2] != temp_str):
            self.__screen.clear(x + 70 * 2, y + 45, 70, 16, self.__color.BLACK)
            #self.__screen.draw_rect(x + 70 * 2, y + 45, 70, 16, self.__color.BLACK, 0, self.__color.BLACK)
            self.__screen.print_str(temp_str, x + 10 + 75 * 2 + self.__get_temp_x(weather_bean.houtian_temp_l, weather_bean.houtian_temp_h), y + 45, color2, backcolor = None, size = 1)
            
            self.__last_temps[2] = temp_str
            
    
    def __get_temp_x(self, temp_l, temp_h):
       return 15 - int((len(temp_l + '~' + temp_h) * 6) / 2)
    
    
    def __get_weather_picture(self, weather):
        weather += '转'
        weather = weather.split('转')[0]
        
        picture = "/data/picture/default/weather/"
        filename = ''
        
        if (weather == "晴"):
            filename = 'qing'
            
        elif (weather == "阴"):
            filename = 'yin'
            
        elif (weather == "多云"):
            filename = 'duoyun'
            
        elif (weather == "阵雨"):
            filename = 'zhenyu'
            
        elif (weather == "雷阵雨"):
            filename = 'leizhenyu'
            
        elif (weather == "小雨"):
            filename = 'xiaoyu'
            
        elif (weather == "中雨"):
            filename = 'zhongyu'
            
        elif (weather == "大雨"):
            filename = 'dayu'
            
        elif (weather == "暴雨"):
            filename = 'baoyu'
            
        elif (weather == "小雪"):
            filename = 'xiaoxue'
            
        elif (weather == "中雪"):
            filename = 'zhongxue'
            
        elif (weather == "大雪"):
            filename = 'daxue'
            
        elif (weather == "暴雪"):
            filename = 'daxue'
            
        elif (weather == "雨加雪" or weather == "雨夹雪"):
            filename = 'yujiaxue'
            
        elif (weather == '大雾' or weather == '雾'):
            filename = 'wu'
        
        elif (weather == '雾霾' or weather == '霾'):
            filename = 'mai'
            
        else:
            filename = 'no'
            
        return picture + filename + '.jpg'




















