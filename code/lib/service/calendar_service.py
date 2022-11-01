import time
from math import ceil

from lib.bean.calendar_bean import CalendarBean


'''
2020-2040的 公历、节日、节气
'''
class CalendarService:
    __log = None
    
    def __init__(self, log):
        self.__log = log
        
    # 农历2020-2040的润大小信息
    __lunar_info = [
            0x07954,0x06aa0,0x0ad50,0x05b52,0x04b60,0x0a6e6,0x0a4e0,0x0d260,0x0ea65,0x0d530, # 2020-2029
            0x05aa0,0x076a3,0x096d0,0x04afb,0x04ad0,0x0a4d0,0x1d0b6,0x0d250,0x0d520,0x0dd45,  # 2030-2039
            0x0b5a0
    ]
 
    # 公历每个月份的天数普通表
    __solar_month = [31,28,31,30,31,30,31,31,30,31,30,31]
 
    # 天干速查表
    __gan = ["甲","乙","丙","丁","戊","己","庚","辛","壬","癸"]
 
    # 地支速查表
    __zhi = ["子","丑","寅","卯","辰","巳","午","未","申","酉","戌","亥"]
 
    # 生肖
    __animals = ["鼠","牛","虎","兔","龙","蛇","马","羊","猴","鸡","狗","猪"]
 
    # 24节气速查表
    __solar_term = ["小寒","大寒","立春","雨水","惊蛰","春分","清明","谷雨","立夏","小满","芒种","夏至","小暑","大暑","立秋","处暑","白露","秋分","寒露","霜降","立冬","小雪","大雪","冬至"]
 
    # 2020-2040各年的24节气日期速查表
    __s_term_info = [
              '977837f0e37f14998082b0787b0721','7f07e7f0e47f531b0723b0b6fb0721','7f0e37f1487f595b0b0bb0b6fb0722',
              '7f0e397bd097c35b0b6fc9210c8dc2','977837f0e37f14998082b0787b06bd','7f07e7f0e47f531b0723b0b6fb0721',
              '7f0e27f1487f531b0b0bb0b6fb0722','7f0e397bd097c35b0b6fc920fb0722','977837f0e37f14998082b0787b06bd',
              '7f07e7f0e47f531b0723b0b6fb0721','7f0e27f1487f531b0b0bb0b6fb0722','7f0e397bd097c35b0b6fc920fb0722',
              '977837f0e37f14998082b0787b06bd','7f07e7f0e47f531b0723b0b6fb0721','7f0e27f1487f531b0b0bb0b6fb0722',
              '7f0e397bd07f595b0b0bc920fb0722','977837f0e37f14998082b0787b06bd','7f07e7f0e47f531b0723b0b6fb0721',
              '7f0e27f1487f531b0b0bb0b6fb0722','7f0e397bd07f595b0b0bc920fb0722','977837f0e37f14998082b0787b06bd'
    ]
     
    # 节假日（除夕除外，需动态计算）
    __festivals = {
        "t0101": "t,春节",
        "t0115": "t,元宵节",
        "t0202": "t,龙抬头",
        "t0505": "t,端午节",
        "t0707": "t,七夕节",
        "t0715": "t,中元节",
        "t0815": "t,中秋节",
        "t0909": "t,重阳节",
        "t1208": "t,腊八节",
        "t1223": "t,北小年",
        "t1224": "t,南小年",
        
        "0308": "i,妇女节",
        "0401": "i,愚人节",
        "0501": "i,劳动节",
        
        "0101": "h,元旦",
        "0312": "h,植树节",
        "0504": "h,青年节",
        "0601": "h,儿童节",
        "0701": "h,建党节",
        "0801": "h,建军节",
        "0910": "h,教师节",
        "1001": "h,国庆节",
        
        "1224": "c,平安夜",
        "1225": "c,圣诞节",
        
        "0214": "a,情人节",
        
        # 前2位代表月份，第3位是第几个星期，第4位是星期几
        "extra": { 
            "0527": "i,母亲节",
            "0637": "a,父亲节",
            "1144": "a,感恩节"
        }
    }
    
    # 数字 转 中文
    __n_str1 = ['日','一','二','三','四','五','六','七','八','九','十']

    # 日期 转 农历称呼
    __n_str2 = ['初','十','廿','卅']

    # 月份 转 农历称呼
    __n_str3 = ['正','二','三','四','五','六','七','八','九','十','冬','腊']

    # 农历year年一整年的总天数    eg: count = self.l_year_days(1987)   # count=384
    def l_year_days(self, year):
        sum = 348
        i = 0x8000
        while (i > 0x8):
            if (self.__lunar_info[year - 2020] & i):
                sum += 1
            i >>= 1
            
        return sum + self.leap_days(year)

    # 返回农历year年闰月是哪个月；若y年没有闰月 则返回0   eg: leapMonth = self.leap_month(1987)  # leapMonth=6
    def leap_month(self, year):
        return self.__lunar_info[year - 2020] & 0xf
    
    
    # 返回农历year年闰月的天数 若该年没有闰月则返回0  eg: leapMonthDay = self.leap_days(1987) #  leapMonthDay=29
    def leap_days(self, year):
        if (self.leap_month(year)):
            if (self.__lunar_info[year - 2020] & 0x10000):
                return 30
            else:
                return 29
        return 0
      
    # 返回农历year年month月（非闰月）的总天数。month为闰月时，计算天数使用leap_days方法
    # eg: MonthDay = self.month_days(1987,9) #  MonthDay=29
    def month_days(self, l_year, l_month):
        if (l_month > 12 or l_month < 1):
            return -1
        if (self.__lunar_info[l_year - 2020] & (0x10000 >> l_month)):
            return 30
        else:
            return 29

    # 返回公历year年month月的天数  eg: SolarDays = self.solar_days(1987,9) #  SolarDays=30
    def solar_days(self, year, month):
        if (month > 12 or month < 1):
            return -1
        
        ms = month - 1
        if(ms == 1):
            if ((year % 4 == 0) and (year % 100 != 0)) or (year % 400 == 0):
                return 29
            else:
                return 28
        else:
            return self.__solar_month[ms]
        
    # 农历年份转换为干支纪年   eg: GanZhiYear = self.to_gan_zhi_year(1987)  # GanZhiYear=丁卯
    def to_gan_zhi_year(self, l_year):
        gan_key = (l_year - 3) % 10
        zhi_key = (l_year - 3) % 12
        
        if (gan_key == 0): # 如果余数为0则为最后一个天干
            gan_key = 10
        if (zhi_key == 0): # 如果余数为0则为最后一个地支
            zhi_key = 12
        
        return self.__gan[gan_key - 1] + self.__zhi[zhi_key - 1]

    # 公历月、日判断所属星座
    def to_astro(self, c_month,c_day):
        s = "魔羯水瓶双鱼白羊金牛双子巨蟹狮子处女天秤天蝎射手魔羯"
        arr = [20,19,21,21,21,22,23,23,23,23,22,22]
        
        index = c_month * 2
        if (c_day < arr[c_month - 1]):
            index -= 2
            
        return s[index : index + 2] + "座"

    # 传入offset偏移量返回干支
    def to_gan_zhi(self, offset):
        return self.__gan[offset % 10] + self.__zhi[offset % 12]

    # 传入公历year年获得该年第n个节气的公历日期
    # n: 二十四节气中的第几个节气(1~24)，从n=1(小寒)算起 eg: _24 = self.get_term(1987,3) # _24=4;意即1987年2月4日立春
    def get_term(self, year, n):
        if(year < 2020 or year > 2040):
            return -1
        if(n < 1 or n > 24):
            return -1

        _table = self.__s_term_info[year - 2020]
        _info = [
            str(int('0x'+_table[0 : 5], 16)),
            str(int('0x'+_table[5 : 10], 16)),
            str(int('0x'+_table[10 : 15], 16)),
            str(int('0x'+_table[15 : 20], 16)),
            str(int('0x'+_table[20 : 25], 16)),
            str(int('0x'+_table[25 : 30], 16))
        ]
        _calday = [
            _info[0][0 : 1],
            _info[0][1 : 3],
            _info[0][3 : 4],
            _info[0][4 : 6],
            
            _info[1][0 : 1],
            _info[1][1 : 3],
            _info[1][3 : 4],
            _info[1][4 : 6],
            
            _info[2][0 : 1],
            _info[2][1 : 3],
            _info[2][3 : 4],
            _info[2][4 : 6],
            
            _info[3][0 : 1],
            _info[3][1 : 3],
            _info[3][3 : 4],
            _info[3][4 : 6],
            
            _info[4][0 : 1],
            _info[4][1 : 3],
            _info[4][3 : 4],
            _info[4][4 : 6],
            
            _info[5][0 : 1],
            _info[5][1 : 3],
            _info[5][3 : 4],
            _info[5][4 : 6]
        ]
        
        return int(_calday[n - 1])
 
    # 传入农历数字月份返回汉语通俗表示法  eg: cnMonth = self.toChinaMonth(12) #  cnMonth='腊月'
    def to_china_month(self, month):
        if(month > 12 or month < 1):
            return -1
        
        return self.__n_str3[month - 1] + '月'
    
    # 传入农历日期数字返回汉字表示法  eg: cnDay = self.toChinaDay(21) # cnMonth='廿一'
    def to_china_day(self, day):
        s = ''
        if (day == 10):
            s = '初十'
        elif (day == 20):
            s = '二十'
        elif (day == 30):
            s = '三十'
        else:
            s = self.__n_str2[int(day / 10)]
            s += self.__n_str1[day % 10]
            
        return s

    # 年份转生肖[!仅能大致转换] => 精确划分生肖分界线是“立春”  eg: animal = self.getAnimal(1987)  # animal='兔'
    def get_animal(self, year):
        return self.__animals[(year - 4) % 12]
    
    # 填充零 
    def zero_pad(self, num): 
        if (num) < 10:
            return "0" + str(num)
        return str(num)
    
    # 获取 当日的节日信息列表
    def get_festivals(self, year, month, day, week, l_year, l_month, l_day):
        f_extra = self.zero_pad(month) + str(ceil(day / 7)) + str(week)
        f_traditional = "t" + self.zero_pad(l_month) + self.zero_pad(l_day)
        f_normal = self.zero_pad(month) + self.zero_pad(day);
        
        arr_holidays = []
        
        # 除夕单独处理
        if (l_month == 12 and l_day == self.month_days(l_year, l_month)):
            arr_holidays.append("t,除夕")
        
        # 节日：某月第几周的星级几
        if (f_extra in self.__festivals["extra"]):
            f = self.__festivals["extra"][f_extra]
            arr_holidays.append(f)
        
        # 阳历的节日
        if (f_normal in self.__festivals):  
            f = self.__festivals[f_normal]
            arr_holidays.append(f)
        
        # 农历的节日
        if (f_traditional in self.__festivals):  
            f = self.__festivals[f_traditional]
            arr_holidays.append(f)
        
        # 节日排序
        arr_holidays.sort(key = lambda x: x[0], reverse = True)
        
        # 去掉分类和起始年份
        for i in range(len(arr_holidays)):
            arr_holidays[i] = arr_holidays[i].split(',')[1]
        
        #for h in (arr_holidays):
        #    print(h)

        return arr_holidays
    
    # 获取 传入阳历日期的 农历、节日、节气信息
    # ps: 懒得写计算日期间隔的算法，暂用time计算，所以暂时只支持2000/1/1 - 2034/1/9的日期。emmm...小电视估计也用不到那时候...
    def __get_date_info(self, y, m, d):
        if (y < 2020 or y > 2040):
            return -1

        i = 0
        leap=0
        temp=0
 
        # offset = (UTC(现在) - UTC(1900,1,31)) / 86400        
        offset = - 35 + int(time.mktime((y, m, d, 0, 0, 0, 0, 0)) / 86400)
        # print(offset)
        
        i = 2000
        while (i < 2040 and offset > 0):
            temp    = self.l_year_days(i)
            offset -= temp
            
            i += 1

        if (offset < 0):
            offset += temp
            i -= 1
        
        
        # 是否今天
        is_today = False
        if (int(time.localtime()[0]) == y and int(time.localtime()[1]) == m and int(time.localtime()[2]) == d):
            is_today = True
        
        # 星期
        nWeek = int(time.localtime(time.mktime((y, m, d, 0, 0, 0, 0, 0)))[6]) + 1
        cWeek = self.__n_str1[nWeek]
        
        # 数字表示周几，顺应周一开始的惯例
        if (nWeek == 0):
            nWeek = 7
            
        # 农历年
        year   = i
        leap   = self.leap_month(i) # 闰哪个月
        is_leap = False
        
        # 效验闰月
        i = 1
        while (i < 13 and offset > 0):
            # 闰月
            if (leap > 0 and i == leap + 1 and is_leap == False):
                i -= 1
                is_leap = True
                temp = self.leap_days(year) # 计算农历闰月天数
            
            else:
                temp = self.month_days(year, i); # 计算农历普通月天数
            
            # 解除闰月
            if (is_leap == True and i == leap + 1):
                is_leap = False
                
            offset -= temp
            i += 1
            
        # 闰月导致数组下标重叠取反
        if (offset == 0 and leap > 0 and i == leap + 1):
            if(is_leap):
                is_leap = False
            else:
                is_leap = True
                i -= 1
            
        if (offset < 0):
            offset += temp
            i -= 1
 
        # 农历月
        month      = i
        # 农历日
        day        = offset + 1

        # 当月的两个节气
        first_node  = self.get_term(y, (m * 2 - 1)) # 返回当月「节」为几日开始
        second_node = self.get_term(y, (m * 2)) # 返回当月「节」为几日开始

        # 传入的日期的节气与否
        is_term = False
        term   = None
        if(first_node == d):
            is_term  = True
            term    = self.__solar_term[m * 2 - 2]
        
        if(second_node == d):
            is_term  = True
            term    = self.__solar_term[m * 2 - 1]
        
        # 该日期所属的星座
        astro       = self.to_astro(m, d)
        
        # 该日期的节日信息
        is_festival = False
        festival_list = self.get_festivals(y, m, d, nWeek, year, month, day)
        if (len(festival_list) > 0):
            is_festival = True
        
        
        # 拼装：CalendarBean
        calendarBean = CalendarBean()

        calendarBean.is_today = is_today # 是否是今天
        calendarBean.animal = self.get_animal(year) # 生肖
        calendarBean.astro = astro  # 星座
        
        calendarBean.year = y  # 阳历 年
        calendarBean.month = m # 阳历 月
        calendarBean.day = d   # 阳历 日
        
        calendarBean.week = nWeek    # 星期 1-7
        calendarBean.week_cn = "星期" + cWeek # 星期（中文）
        
        calendarBean.is_leap = is_leap # 农历 是否是闰月
        calendarBean.l_year = year  # 农历 年
        calendarBean.l_month = month # 农历 月
        calendarBean.l_day = day   # 农历 日
        
        calendarBean.l_month_cn = ('闰' if is_leap else '') + self.to_china_month(month) # 农历 月（中文）
        calendarBean.l_day_cn = self.to_china_day(day)   # 农历 日（中文）
        
        calendarBean.is_term = is_term # 是否是节气
        calendarBean.term = term # 节气
        
        calendarBean.is_festival = is_festival # 是否是节日
        calendarBean.festival_list = festival_list  # 节日（可能一天有多个节日）
        
        # calendarBean.adjust = 0  # 是否有假期调整。0：没有调整；1：变成放假；-1：变成加班
        
        '''
        info = 'CanlendarBean = { ' + '\n'
        info += 'is_today:' + str(calendarBean.is_today) + '\n'
        info += 'animal:' + str(calendarBean.animal) + '\n'
        info += 'astro:' + str(calendarBean.astro) + '\n'
        info += 'year:' + str(calendarBean.year) + '\n'
        info += 'month:' + str(calendarBean.month) + '\n'
        info += 'day:' + str(calendarBean.day) + '\n'
        info += 'week:' + str(calendarBean.week) + '\n'
        info += 'week_cn:' + str(calendarBean.week_cn) + '\n'
        info += 'is_leap:' + str(calendarBean.is_leap) + '\n'
        info += 'l_year:' + str(calendarBean.l_year) + '\n'
        info += 'l_month:' + str(calendarBean.l_month) + '\n'
        info += 'l_day:' + str(calendarBean.l_day) + '\n'
        info += 'l_month_cn:' + str(calendarBean.l_month_cn) + '\n'
        info += 'l_day_cn:' + str(calendarBean.l_day_cn) + '\n'
        info += 'is_term:' + str(calendarBean.is_term) + '\n'
        info += 'term:' + str(calendarBean.term) + '\n'
        info += 'is_festival:' + str(calendarBean.is_festival) + '\n'
        info += 'festival_list: ['
        for i in range(len(calendarBean.festival_list)):
            if (i != 0):
                info += ','
            info += str(calendarBean.festival_list[i])
        info += ']\n'
        info += '}\n\n\n\n\n'
        
        print(info)
        '''
        
        return calendarBean
     

    def get_date_info(self, datetime):
        self.__log.info('CalendarService.get_date_info')
        
        return self.__get_date_info(datetime[0], datetime[1], datetime[2])
         
# CalendarService().__get_date_info(2022, 9, 7)
# CalendarService().__get_date_info(2025, 1, 28)





