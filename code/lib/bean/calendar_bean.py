class CalendarBean():
    is_today = False # 是否是今天
    animal = '' # 生肖
    astro = ''  # 星座
    
    year = ''  # 阳历 年
    month = '' # 阳历 月
    day = ''   # 阳历 日
    
    week = 0    # 星期 1-7
    week_cn = ''# 星期（中文）
    
    is_leap = False # 农历 是否是闰月
    l_year = ''  # 农历 年
    l_month = '' # 农历 月
    l_day = ''   # 农历 日
    
    l_month_cn = '' # 农历 月（中文）
    l_day_cn = ''   # 农历 日（中文）
    
    is_term = False # 是否是节气
    term = '' # 节气
    
    is_festival = False # 是否是节日
    festival_list = []  # 节日（可能一天有多个节日）
    
    adjust = 0  # 是否有假期调整。0：没有调整；1：变成放假；-1：变成加班
    






