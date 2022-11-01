# 导入工具类
import gc

class ClockWeatherWinXpUI():
    __log    = None
    __color  = None
    __screen = None
    
    def __init__(self, log, color, screen):
        self.__log = log
        self.__color = color
        self.__screen = screen
    
    __base_path = '/data/picture/winxp/'
    
    __last_hour = -1
    __last_minute = -1
    __last_second = -1
    __last_year = -1
    __last_month = -1
    __last_day = -1
    __last_week = -1
    
    __last_today_weather = ''
    __last_today_temp = ''
    __last_today_aqi = ''
    __last_tommorow_weather = ''
    __last_tommorow_temp = ''
    __last_tommorow_aqi = ''
    __last_now_warn = ''
    __last_now_warn_color = ''
    __last_now_aqi = ''
    __last_now_weather = ''
    __last_now_temp = ''
    __last_now_wind_level = ''
    
    __last_later_weathers = []
    
    '初始化界面'
    def init(self):
        gc.collect()
        
        self.__last_hour = -1
        self.__last_minute = -1
        self.__last_second = -1
        self.__last_year = -1
        self.__last_month = -1
        self.__last_day = -1
        self.__last_week = -1
        
        self.__last_today_weather = ''
        self.__last_today_temp = ''
        self.__last_today_aqi = ''
        self.__last_tommorow_weather = ''
        self.__last_tommorow_temp = ''
        self.__last_tommorow_aqi = ''
        self.__last_now_warn = ''
        self.__last_now_warn_color = ''
        self.__last_now_aqi = ''
        self.__last_now_weather = ''
        self.__last_now_temp = ''
        self.__last_now_wind_level = ''
        
        self.__last_later_weathers = []
        
        self.__screen.picture(49, 0, self.__base_path + "webpage.jpg")
        self.__screen.picture(63, 53, self.__base_path + "time_panel.jpg")
        self.__screen.picture(63, 90, self.__base_path + "weather_panel.jpg")
 
    
    '刷新界面信息'
    def refresh(self, datetime, weather_bean, weather_warn):
        gc.collect()
        
        '时间'
        filepath = self.__base_path + "time/"
        
        x = 74
        y = 57
        
        second = datetime[6]
        minute = datetime[5]
        hour = datetime[4]
        
        # 时
        if (self.__last_hour != hour): 
            if hour > 9:
                hour_str = str(hour)
                
                self.__screen.picture(x, y, filepath + hour_str[0:1] + ".jpg")
                self.__screen.picture(x + 13, y, filepath + hour_str[1:2] + ".jpg")
            else:
                self.__screen.picture(x, y, filepath + "0.jpg")
                self.__screen.picture(x + 13, y, filepath + str(hour) + ".jpg")
                
            self.__last_hour = hour

        # 时与分之间的冒号
        if (second % 2 == 0):
            self.__screen.picture(x + 28, y - 2, filepath + "mh.jpg")
        else:
            self.__screen.picture(x + 28, y, filepath + "blank.jpg")
        
        # 分
        x += 38
        if (self.__last_minute != minute):
            if minute > 9:
                minute_str = str(minute)
                self.__screen.picture(x, y, filepath + minute_str[0:1] + ".jpg")
                self.__screen.picture(x + 13, y, filepath + minute_str[1:2] + ".jpg")
            else:
                self.__screen.picture(x, y, filepath + "0.jpg")
                self.__screen.picture(x + 13, y, filepath + str(minute) + ".jpg")
            
            self.__last_minute = minute

        '日期'
        x = 152
        y = 68
        
        year = datetime[0]
        month = datetime[1]
        day = datetime[2]
        week = datetime[3]
        
        # 年
        if (self.__last_year != year):
            year_str = str(year)
            self.__screen.picture(x, y, filepath + "s_" + year_str[0:1] + ".jpg")
            self.__screen.picture(x + 7, y, filepath + "s_" + year_str[1:2] + ".jpg")
            self.__screen.picture(x + 13, y, filepath + "s_" + year_str[2:3] + ".jpg")
            self.__screen.picture(x + 19, y, filepath + "s_" + year_str[3:4] + ".jpg")
            
            self.__screen.picture(x + 26, y, filepath + "s_h.jpg")
            
            self.__last_year = year
        
        # 月
        x += 31
        if (self.__last_month != month):
            if month > 9:
                if (month == 10):
                    self.__screen.picture(x, y, filepath + "s_1.jpg")
                    self.__screen.picture(x + 7, y, filepath + "s_0.jpg")
                elif (month == 11):
                    self.__screen.picture(x, y, filepath + "s_1.jpg")
                    self.__screen.picture(x + 7, y, filepath + "s_1.jpg")
                else:
                    self.__screen.picture(x, y, filepath + "s_1.jpg")
                    self.__screen.picture(x + 7, y, filepath + "s_2.jpg")
            else:
                self.__screen.picture(x, y, filepath + "s_0.jpg")
                self.__screen.picture(x + 7, y, filepath + "s_" + str(month) + ".jpg")
            
            self.__screen.picture(x + 14, y, filepath + "s_h.jpg")
            
            self.__last_month = month
            
        # 日    
        x += 19
        if (self.__last_day != day):
            if day > 9:
                day_str = str(day)
                self.__screen.picture(x, y, filepath + "s_" + day_str[0:1] + ".jpg")
                self.__screen.picture(x + 7, y, filepath + "s_" + day_str[1:2] + ".jpg")
            else:
                self.__screen.picture(x, y, filepath + "s_0.jpg")
                self.__screen.picture(x + 7, y, filepath + "s_" + str(day) + ".jpg")
                
            self.__last_day = day

        # 星期
        x = 172
        y = 57
        
        if (self.__last_week != week):
            week_list = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
            self.__screen.picture(x, y, filepath + week_list[week] + ".jpg")
            
            self.__last_week = week
        
        
        
        '天气预警'
        x = 63
        y = 91
        if (weather_warn[0] != ''):
            warn = weather_warn[0]
            warn_color = weather_warn[1]
            
            if (self.__last_now_warn_color != warn_color or self.__last_now_warn != warn):
                self.__screen.picture(x, y, self.__get_char_picture(warn_color, 'warn_'))
                
                x = 83
                warn_t = warn + warn_color + '色预警'
                for i in range(len(warn_t)):
                    self.__screen.picture(x, y, self.__get_char_picture(warn_t[i], '2_'))
                    x += 11
                
                self.__last_now_warn_color = warn_color
                self.__last_now_warn = warn
        else:
            self.__last_now_warn_color = ''
            self.__last_now_warn = ''
            
            self.__screen.picture(x, y, self.__base_path + "weather/warn_blank.jpg")
        
        '天气'
        # 实时天气的图片 和 实时天气
        now_weather = weather_bean.now_weather
        if (self.__last_now_weather != now_weather):
            # 实时天气的图片
            x = 72
            y = 115
            self.__screen.picture(x, y, self.__get_weather_picture(datetime, now_weather))
            
            # 实时天气
            x = 108
            y = 132
            if (len(now_weather) < 3):
                x = 113
            
            self.__screen.picture(106, y, self.__get_char_picture('blank_1', '0_'))
            for i in range(len(now_weather)):
                gc.collect()
                
                self.__screen.picture(x, y, self.__get_char_picture(now_weather[i], '0_'))
                x += 12
                
            self.__last_now_weather = now_weather
        
        # 实时温度
        x = 113
        y = 116
        
        now_temp = weather_bean.now_temp
        if (len(now_temp) == 3):
            x -= 8
        
        if (self.__last_now_temp != now_temp):
            self.__screen.picture(106, y, self.__get_char_picture('blank_0', '0_'))
            for i in range(len(now_temp)):
                gc.collect()
                
                self.__screen.picture(x, y, self.__get_char_picture(now_temp[i], '0_'))
                x += 8
            self.__screen.picture(x + 2, y, self.__get_char_picture('℃', '0_'))

            self.__last_now_temp = now_temp
        
            
        # 今日温度
        y = 153
        
        today_temp_l = weather_bean.today_temp_l
        today_temp_h = weather_bean.today_temp_h
        today_temp = today_temp_l + '~' + today_temp_h + '℃'
        
        x = 108 - int(((len(today_temp) - 1) * 8 + 10)/ 2)
        
        if (self.__last_today_temp != today_temp):
            self.__screen.picture(73, y, self.__get_char_picture('blank_0', '1_'))
            for i in range(len(today_temp)):
                gc.collect()
                
                self.__screen.picture(x, y, self.__get_char_picture(today_temp[i], '1_'))
                x += 8

            self.__last_today_temp = today_temp
            
        # 今日天气
        y = 166
        
        today_weather = weather_bean.today_weather
        x = 108 - int(len(today_weather) * 10 / 2)
        
        if (self.__last_today_weather != today_weather):

            self.__screen.picture(73, y, self.__get_char_picture('blank_1', '1_'))
            for i in range(len(today_weather)):
                gc.collect()
                
                self.__screen.picture(x, y, self.__get_char_picture(today_weather[i], '1_'))
                x += 10

            self.__last_today_weather = today_weather
        
        # 实时空气指数
        x = 101
        y = 179
        
        now_aqi = self.__get_aqi_chn(weather_bean.now_aqi)
        if (self.__last_now_aqi != now_aqi):
            for i in range(len(now_aqi)):
                gc.collect()
                
                self.__screen.picture(x, y, self.__get_char_picture(now_aqi[i], 'aqi_'))
                x += 15

            self.__last_now_aqi = now_aqi
        
        
        # 明日天气的图片 和 明日天气信息
        tommorow_weather = weather_bean.tommorow_weather
        if (self.__last_tommorow_weather != tommorow_weather):
            # 明日天气的图片
            x = 177
            y = 115
        
            self.__screen.picture(x, y, self.__get_weather_picture(datetime, tommorow_weather))
            
            # 明日天气
            y = 166
            
            tommorow_weather = weather_bean.tommorow_weather
            x = 192 - int(len(tommorow_weather) * 10 / 2)

            self.__screen.picture(156, y, self.__get_char_picture('blank_1', '1_'))
            for i in range(len(tommorow_weather)):
                gc.collect()
                
                self.__screen.picture(x, y, self.__get_char_picture(tommorow_weather[i], '1_'))
                x += 10
                
            self.__last_tommorow_weather = tommorow_weather
        
        # 明日温度
        y = 153
        
        tommorow_temp_l = weather_bean.tommorow_temp_l
        tommorow_temp_h = weather_bean.tommorow_temp_h
        tommorow_temp = tommorow_temp_l + '~' + tommorow_temp_h + '℃'
        
        x = 191 - int(((len(tommorow_temp) - 1) * 8 + 10)/ 2)
        if (self.__last_tommorow_temp != tommorow_temp):
            self.__screen.picture(156, y, self.__get_char_picture('blank_0', '1_'))
            for i in range(len(tommorow_temp)):
                gc.collect()
                
                self.__screen.picture(x, y, self.__get_char_picture(tommorow_temp[i], '1_'))
                x += 8

            self.__last_tommorow_temp = tommorow_temp
            
        # 明日空气指数
        x = 185
        y = 179
        
        tommorow_aqi = self.__get_aqi_chn(weather_bean.tommorow_aqi)
        if (self.__last_tommorow_aqi != tommorow_aqi):
            for i in range(len(tommorow_aqi)):
                gc.collect()
                
                self.__screen.picture(x, y, self.__get_char_picture(tommorow_aqi[i], 'aqi_'))
                x += 15

            self.__last_tommorow_aqi = tommorow_aqi
        

    
    def __get_weather_picture(self, datetime, weather):
        weather += '转'
        weather = weather.split('转')[0]
        
        picture = self.__base_path + "weather/"
        filename = ''
        
        hour = datetime[4]
        is_night = True # 是否是夜间
        if (8 <= hour < 20):
            is_night = False
        else:
            is_night = True
            

        if (weather == "晴"):
            filename = 'qing'
            
            if (is_night):
                filename += '_night'
                
        elif (weather == "阴"):
            filename = 'yin'
            
        elif (weather == "多云"):
            filename = 'duoyun'
            
            if (is_night):
                filename += '_night'
        
        elif (weather == "大雾" or weather == "雾"):
            filename = 'wu'
            
        elif (weather == "雾霾" or weather == "霾"):
            filename = 'mai'
            
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
        else:
            filename += 'no'
        
        return picture + filename + '.jpg'
    
    '空气指数转换'
    def __get_aqi_chn(self, aqi):
        aqi = int(aqi)
        index = 0
        if 0 <= aqi < 50: #优
            index = 0
        elif 50 <= aqi < 100:#良
            index = 1
        elif 100 <= aqi < 150:#轻度
            index = 2
        elif 150 <= aqi < 200:#中度
            index = 3
        elif 200 <= aqi < 300:#重度
            index = 4
        elif 300 <= aqi < 500:#严重
            index = 5
        
        aqi_chn=['优','良','轻','中','重','严']
        
        return aqi_chn[index]
    
    '获取单个字符对应的图片文件'
    def __get_char_picture(self, char, prefix):
        picture = self.__base_path + "weather/" + prefix
        
        if ('0' <= char <= '9'):
            picture += char + '.jpg'
        elif (char == '℃'):
            picture += 'c.jpg'
        elif (char == '-'):
            picture += '-.jpg'
        elif (char == '~'):
            picture += '~.jpg'
        elif (char == 'blank_0' or char == 'blank_1'):
            picture += char + '.jpg'
        else:
            cn_string = '晴阴风多云雷阵雨加雪雾霾霜冻沙尘小中大暴转到优良轻重严蓝黄橙红色预警高温寒潮冰雹灾道路积电森林草原火险地质害气象强季夹'
            py_list = ['qing','yin','feng','duo','yun','lei','zhen','yu','jia','xue','wu','mai','shuang',
                       'dong','sha','chen','xiao','zhong','da','bao','zhuan','dao', 'you', 'liang', 'qing',
                       'zhong2', 'yan', 'lan', 'huang', 'cheng', 'hong', 'se', 'yu2', 'jing', 'gao', 'wen',
                       'han', 'chao', 'bing', 'bao2', 'zai', 'dao', 'lu', 'ji', 'dian', 'sen', 'lin', 'cao',
                       'yuan', 'huo', 'xian','di','zhi','hai','qi','xiang','qiang','ji2','jia2']
            
            for i in range(len(cn_string)):
                if (char == cn_string[i]):
                    picture += py_list[i] + '.jpg'
                    break
                
        # print(picture)
        return picture    
            










