class WeatherBean(object):
    # 实时
    now_weather = "晴"   # 天气
    now_temp = "0"       # 温度
    now_humi = "100"     # 湿度
    now_wind = ""        # 风向
    now_wind_level = "0" # 风力
    now_aqi = "优"       # 空气指数
    now_warnings = []    # 预警
    
    later_weathers = ['晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴', '晴'] # 把未来24小时分成N个时段，每个时段的天气
    later_temps = [0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0,0,0,0, 0] # 未来24小时温度
    later_temps_y = [0,0,0] # 温度图的三个分段：最低温度、中间温度、最高温度
    
    sunriseTime = "" # 日出时间
    sunsetTime = ""  # 日落时间
    
    now_nongli = "" # 农历
    
    # 今日
    today_weather = "晴" # 天气
    today_temp_h = "0 "  # 最高温度
    today_temp_l = "0 "  # 最低温度
    today_month = "1"    # 月份
    today_day = "1"      # 日期
    
    # 明天
    tommorow_weather = "晴" # 天气
    tommorow_temp_h = "0"   # 最高温度
    tommorow_temp_l = "0 "  # 最低温度
    tommorow_aqi = "优"     # 空气指数
    tommorow_month = "1"    # 月份
    tommorow_day = "1"      # 日期
    
    # 后天
    houtian_weather = "晴" # 天气
    houtian_temp_h = "0"   # 最高温度
    houtian_temp_l = "0"   # 最低温度
    houtian_month = "1"    # 月份
    houtian_day = "1"      # 日期

    






