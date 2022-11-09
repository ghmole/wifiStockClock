# 导入相关模块
import  re,json
from libs.urllib import urequest
import gc

# 导入工具类
from lib.bean.weather_bean import * # 天气数据模板
gc.collect()


class WeatherBaiduService:
    __log = None
    
    __last_success_weather_warn = ['', '']
    __last_success_weather = None
    
    def __init__(self, log):
        self.__log = log
    
    '获取天气预警' 
    def get_weather_warn(self, pyClock, datetime):
        weatherWarn = ['', '']
        
        city_data = self.__get_city_code_and_py() # 获取城市代码和拼英

        is_find_warn_model = False # 是否找到天气预警模块。大多时候天气正常，有预警模块，但是找不到预警信息。
        for i in range(7): # 失败重试最多重试的次数
            gc.collect() # 内存回收
            
            text = ''
            myURL = None
            
            try:
                #self.__log.info("mem = " + str(gc.mem_free()))
                myURL = urequest.urlopen("https://www.qweather.com/severe-weather/" + city_data[1] + "-" + city_data[0] + ".html")
                self.__log.info("Weather URL: " + "https://www.qweather.com/severe-weather/" + city_data[1] + "-" + city_data[0] + ".html") #https://www.qweather.com/severe-weather/beijing-101010100.html
                
                for j in range(3):
                    text = myURL.read(6000 + i * 100).decode('UTF-8')

                    if (j == 2 and text.count('class="cont"') > 0):
                        is_find_warn_model = True
                        
                        warn = self.__match_index('(发布.*?|更新.*?)色', '预警', text, 0, False)
                        
                        self.__log.info("weather warn : " + str(warn[2:-1]) + " color : " + str( warn[-1:]))
                        myURL.close()
                        
                        text = ''
                        gc.collect() # 内存回收
                        
                        weatherWarn = ['', '']
                        if (warn.count('感冒') > 0):
                            weatherWarn = ['', '']
                        else:
                            weatherWarn = [warn[2:-1], warn[-1:]]
                        self.__last_success_weather_warn = weatherWarn
                        
                        pyClock.update_data_status(0, True)
                        return weatherWarn
                    elif (j == 2 and text.count('暂无预警') > 0):
                        self.__log.info("get_weather_warn: 暂无预警")

                        is_find_warn_model = True
                        break
                    
                    text = ''
                    warn = ''
                    gc.collect() # 内存回收
                
                if (is_find_warn_model):
                    break
                
                text = ''
                warn = ''
                myURL.close()
                gc.collect() 
                
            except NotImplementedError as e:
                self.__log.error("城市拼音错误")
                gc.collect()
                
            except BaseException as e:
                self.__log.error("Can not get weather warn! try : " + str(i + 1) + " error : "+ repr(e))
                try:
                    myURL.close()
                except:
                    pass
                
                text = ''
                myURL = None
                gc.collect() # 内存回收
        
        try:
            myURL.close()
        except:
            pass
        text = ''
        warn = ''
        myURL = None
        gc.collect() # 内存回收
        
        if (is_find_warn_model == False):
            pyClock.update_data_status(0, False)
        else:
            pyClock.update_data_status(0, True)
            self.__last_success_weather_warn = ['', '']
            
        return self.__last_success_weather_warn
    
    '获取天气数据' 
    def get_weather_bean(self, pyClock, datetime):
        weatherBean = None
        
        city = self.__get_city() # 获取城市名称
        self.__log.info("city = " + str(city))

        for i in range(10): # 失败重试最多重试的次数
            gc.collect() # 内存回收
            
            weatherBean = WeatherBean()

            text = ''
            myURL = None
            try:
                self.__log.info("mem = " + str(gc.mem_free()))
                #weather_url="https://weathernew.pae.baidu.com/weathernew/pc?query=" + city + "天气&srcid=4982"
                #self.__log.info("URL:"+ weather_url)
                myURL = urequest.urlopen("https://weathernew.pae.baidu.com/weathernew/pc?query=" + city + "天气&srcid=4982")
                #self.__log.info('after urlopen') 
                #self.__log.info('Weather URL: ' + 'https://weathernew.pae.baidu.com/weathernew/pc?query=' + city + '天气&srcid=4982')
                #https://www.qweather.com/weather/beijing-101010100.html
              
                for j in range(7):
                    if (j == 0):
                        text = myURL.read(8300 + i * 100).decode('UTF-8')
                    else:
                        text = myURL.read(9300 + i * 100).decode('UTF-8')
                    
                    if (j == 0):
                        # 实时天气
                        weatherBean.now_weather = self.__match_index('"weather":"', '"', text)
                        self.__log.info("weatherBean.now_weather = " + str(weatherBean.now_weather))
                        
                        # 实时温度
                        weatherBean.now_temp = self.__match_index('"temperature":"', '"', text)
                        self.__log.info("weatherBean.now_temp = " + str(weatherBean.now_temp))
                        
                        # 实时湿度
                        weatherBean.now_humi = (self.__match_index('"humidity":"', '"', text) + '.0').split('.')[0]
                        self.__log.info("weatherBean.now_humi = " + str(weatherBean.now_humi))
                        
                        # 日出时间
                        weatherBean.sunriseTime = (self.__match_index('"sunriseTime":"', '"', text) + '.0').split('.')[0]
                        self.__log.info("weatherBean.sunriseTime = " + str(weatherBean.sunriseTime))
                        
                        # 日落时间
                        weatherBean.sunsetTime = (self.__match_index('"sunsetTime":"', '"', text) + '.0').split('.')[0]
                        self.__log.info("weatherBean.sunsetTime = " + str(weatherBean.sunsetTime))
                        
                        # 实时风向、风力
                        weatherBean.now_wind = self.__match_index('"wind_direction":"', '"', text)
                        self.__log.info("weatherBean.now_wind = " + str(weatherBean.now_wind))
                        
                        weatherBean.now_wind_level = self.__match_index('"wind_power":"', '"', text)
                        self.__log.info("weatherBean.now_wind_level = " + str(weatherBean.now_wind_level))
                        
                        # 实时空气质量指数
                        weatherBean.now_aqi = self.__match_index('","ps_pm25":"', '"', text)
                        self.__log.info("weatherBean.now_aqi = " + str(weatherBean.now_aqi))
                        
                        
                        # 今天天气
                        weather_day = self.__match_index('"weather_day":"', '"', text)
                        weather_night = self.__match_index('"weather_night":"', '"', text)
                        
                        if (weather_day == weather_night):
                            weatherBean.today_weather = weather_day
                        else:
                            weatherBean.today_weather = weather_day + "转" + weather_night

                        self.__log.info("weatherBean.today_weather = " + str(weatherBean.today_weather))
                        
                        # 今天温度
                        temperature_night = self.__match_index('"temperature_night":"', '"', text)
                        temperature_day = self.__match_index('"temperature_day":"', '"', text)
                        
                        if (int(temperature_night) <= int(temperature_day)):
                            weatherBean.today_temp_l = temperature_night
                            weatherBean.today_temp_h = temperature_day
                        else:
                            weatherBean.today_temp_l = temperature_day
                            weatherBean.today_temp_h = temperature_night
                        
                        self.__log.info("weatherBean.today_temp_l = " + str(weatherBean.today_temp_l))
                        self.__log.info("weatherBean.today_temp_h = " + str(weatherBean.today_temp_h))
                        
                        # 今日日期
                        date = self.__match_index('"listTitle":"', '"', text, 0)
                        weatherBean.today_month = date.split('-')[1]
                        weatherBean.today_day = date.split('-')[2]
                        
                        self.__log.info("weatherBean.today_month = " + str(weatherBean.today_month))
                        self.__log.info("weatherBean.today_day = " + str(weatherBean.today_day))
                        
                        
                        # 明天天气
                        weather_day = self.__match_index('"weather_day":"', '"', text, 2)
                        weather_night = self.__match_index('"weather_night":"', '"', text, 2)
                        
                        if (weather_day == weather_night):
                            weatherBean.tommorow_weather = weather_day
                        else:
                            weatherBean.tommorow_weather = weather_day + "转" + weather_night

                        self.__log.info("weatherBean.tommorow_weather = " + str(weatherBean.tommorow_weather))
                        
                        # 明天温度
                        temperature_night = self.__match_index('"temperature_night":"', '"', text, 1)
                        temperature_day = self.__match_index('"temperature_day":"', '"', text, 1)
                        
                        if (int(temperature_night) <= int(temperature_day)):
                            weatherBean.tommorow_temp_l = temperature_night
                            weatherBean.tommorow_temp_h = temperature_day
                        else:
                            weatherBean.tommorow_temp_l = temperature_day
                            weatherBean.tommorow_temp_h = temperature_night
                        
                        self.__log.info("weatherBean.tommorow_temp_l = " + str(weatherBean.tommorow_temp_l))
                        self.__log.info("weatherBean.tommorow_temp_h = " + str(weatherBean.tommorow_temp_h))
        
                        # 明天空气质量指数
                        tommorow_aqi = self.__match_index('"listAqiVal":"', '"', text, 1)
                        weatherBean.tommorow_aqi = tommorow_aqi
                        
                        self.__log.info("weatherBean.tommorow_aqi = " + str(weatherBean.tommorow_aqi))

                        # 明天日期
                        date = self.__match_index('"listTitle":"', '"', text, 1)
                        weatherBean.tommorow_month = date.split('-')[1]
                        weatherBean.tommorow_day = date.split('-')[2]
                        
                        self.__log.info("weatherBean.tommorow_month = " + str(weatherBean.tommorow_month))
                        self.__log.info("weatherBean.tommorow_day = " + str(weatherBean.tommorow_day))
                            
                        # 后天天气
                        weather_day = self.__match_index('"weather_day":"', '"', text, 3)
                        weather_night = self.__match_index('"weather_night":"', '"', text, 3)
                        
                        if (weather_day == weather_night):
                            weatherBean.houtian_weather = weather_day
                        else:
                            weatherBean.houtian_weather = weather_day + "转" + weather_night

                        self.__log.info("weatherBean.houtian_weather = " + str(weatherBean.houtian_weather))
                        
                        # 后天温度
                        temperature_night = self.__match_index('"temperature_night":"', '"', text, 2)
                        temperature_day = self.__match_index('"temperature_day":"', '"', text, 2)
                        
                        if (int(temperature_night) <= int(temperature_day)):
                            weatherBean.houtian_temp_l = temperature_night
                            weatherBean.houtian_temp_h = temperature_day
                        else:
                            weatherBean.houtian_temp_l = temperature_day
                            weatherBean.houtian_temp_h = temperature_night
                        
                        self.__log.info("weatherBean.houtian_temp_l = " + str(weatherBean.houtian_temp_l))
                        self.__log.info("weatherBean.houtian_temp_h = " + str(weatherBean.houtian_temp_h))
                        
                        # 后天日期
                        date = self.__match_index('"listTitle":"', '"', text, 2)
                        weatherBean.houtian_month = date.split('-')[1]
                        weatherBean.houtian_day = date.split('-')[2]
                        
                        self.__log.info("weatherBean.houtian_month = " + str(weatherBean.houtian_month))
                        self.__log.info("weatherBean.houtian_day = " + str(weatherBean.houtian_day))
                        
                    elif (j == 6):
                        # 从现在起，24小时各小时的天气、温度
                        result = self.__match_index('"temperaturePointArr":\[', '"middleTemperature"', text, is_decode = False)
                        for k in range(24):
                            # 天气
                            weatherBean.later_weathers[k] = self.__match_index(',"\d+","', '","temperature"\]', result, k)
                            self.__log.info("weatherBean.later_weathers[" + str(k) + "] = " + str(weatherBean.later_weathers[k]))
                            
                            # 温度
                            t = str(self.__match_index('\[', '","temperature"\]', result, k, is_decode = False))
                            weatherBean.later_temps[k] = int(self.__match_index(',"', '","', t))
                            self.__log.info("weatherBean.later_temps[" + str(k) + "] = " + str(weatherBean.later_temps[k]))
                        
                        # 第一个小时，换成实时的 天气 和 温度
                        weatherBean.later_weathers[0] = weatherBean.now_weather 
                        weatherBean.later_temps[0] = int(weatherBean.now_temp)
                        
                        # 第二十五个小时的温度
                        is_get_25h_temp = False
                        try:
                            t = str(self.__match_index('\[', '","temperature"\]', result, 24, is_decode = False))
                            weatherBean.later_temps[24] = int(self.__match_index(',"', '","', t))
                            self.__log.info("weatherBean.later_temps[" + str(24) + "] = " + str(weatherBean.later_temps[24]))
                            
                            is_get_25h_temp = True
                        except:
                            self.__log.error("weatherBean.later_temps[24] 获取失败")
                            weatherBean.later_temps[24] = weatherBean.later_temps[23] 
                        
                        # 温度分段
                        weatherBean.later_temps_y[0] = weatherBean.later_temps[0]
                        weatherBean.later_temps_y[2] = weatherBean.later_temps[0]
                        
                        for k in range(25):
                            if (weatherBean.later_temps[k] < weatherBean.later_temps_y[0]):
                                weatherBean.later_temps_y[0] = weatherBean.later_temps[k]
                            if (weatherBean.later_temps[k] > weatherBean.later_temps_y[2]):
                                weatherBean.later_temps_y[2] = weatherBean.later_temps[k]
                        
                        # 如果25小时的温度获取失败，则手动简单预测一下
                        if (is_get_25h_temp == False):
                            weatherBean.later_temps[24] = weatherBean.later_temps[23]
                            if (weatherBean.later_temps[23] == weatherBean.later_temps[22]):
                                pass
                            elif (weatherBean.later_temps[23] < weatherBean.later_temps[22]):
                                if (weatherBean.later_temps[22] == weatherBean.later_temps[21]):
                                    pass
                                else:
                                    weatherBean.later_temps[24] -= 1
                            else:
                                if (weatherBean.later_temps[22] == weatherBean.later_temps[21]):
                                    pass
                                else:
                                    weatherBean.later_temps[24] += 1
                            
                            if (weatherBean.later_temps[24] > weatherBean.later_temps_y[2]):
                                weatherBean.later_temps[24] = weatherBean.later_temps_y[2]
                            elif (weatherBean.later_temps[24] < weatherBean.later_temps_y[0]):
                                weatherBean.later_temps[24] = weatherBean.later_temps_y[0]
                    
                    text = ''
                    gc.collect() #内存回收
                  
                self.__last_success_weather = weatherBean
                
                text = ''
                try:
                    myURL.close()
                except:
                    pass
                myURL = None
                gc.collect() #内存回收
                
                pyClock.update_data_status(1, True)
                return weatherBean
                    
            except BaseException as e:
                self.__log.error("Can not get weather! try : " + str(i + 1) + " "+ repr(e))
                
                try:
                    myURL.close()
                except:
                    pass
   
                text = ''
                myURL = None
                gc.collect() #内存回收
        
        self.__log.error("use __last_success_weather")

        try:
            myURL.close()
        except:
            pass
        text = ''
        myURL = None
        gc.collect() #内存回收
                
        pyClock.update_data_status(1, False)
        return self.__last_success_weather
        
    '获取城市名称'
    def __get_city(self):
        city = ''
        
        # 获取城市名称
        f = open('/data/config/city.cfg', 'r')
        info = json.loads(f.read())
        #self.__log.info('info='+ str(info))
        f.close()
        
        city = info['CITY'] 
        #self.__log.info('city ='+  str(city))
        return str(city)

    '把unicode字符转化正常字符' 
    def __decode(self, text):
        return eval('u"%s"' % text)

    '查找text中 第index个满足匹配的结果'
    def __match_index(self, begin, end, text, index = 0, is_decode = True):
        pattern = ''
        if (index > 0):
            for i in range(index):
                pattern += begin + '.*?'
        pattern += begin + '(.*?)' + end
        
        if is_decode:
            return self.__decode( re.search(pattern, text).group(1) )
        else:
            return re.search(pattern, text).group(1)

    '获取城市代码和拼英'
    def __get_city_code_and_py(self):
        # 获取城市编码
        f = open('/data/config/city.cfg', 'r')
        info = json.loads(f.read())
        f.close()
        
        return [str(info['CITY_CODE']), str(info['CITY_PY'])]















