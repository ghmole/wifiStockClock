from libs.urllib import urequest
import gc

# 导入工具类
from lib.bean.stock_bean import * # 股票数据模板

class StockData():
    def __init__(self):
        self.stock_name = ''
        self.stock_code = ''
        self.last_price = ''
        self.pre_close = ''
        self.open_price = ''
        self.diff_price = ''
        self.diff_percent = ''
 
class StockService():
    __log = None
    __stockdata = None
    
    def __init__(self, log):
        self.__log = log
        self.__stockdata=StockData()
        
    def query_stock_list(self,code_list, stock_bean):
        for i,code in enumerate(code_list):
            self.__log.info('get stock code:' + code)
            self.__stockdata=slef.query_stock(code)
            stock_bean.update_stock_data(i, self.__stockdata)
        
    def query_stock(self,code):
        gc.collect()
        try:
            my_url='http://qt.gtimg.cn/r=0.9392363841179758&q='+code
            #my_url='https://sqt.gtimg.cn/q=sh600000'
            self.__log.info(my_url)
            my_req = urequest.urlopen(my_url)

            # 坏消息micropython 不支持gbk编码
            res = my_req.read(600)#.decode('UTF-8') #抓取约前4W个字符，节省内存。
           
            res=str(res) 
            self.__log.info(res)
            gc.collect()
           
            
            for line in res.split(';'):
                #print line
                if len(line) < 50 :
                    continue
                info = line[12: 100]
                #print info
                vargs = info.split('~')
                print(vargs)
                #print vargs
                self.__stockdata.stock_name = vargs[1]
                self.__stockdata.stock_code = vargs[2]
                self.__stockdata.last_price =  vargs[3]
                self.__stockdata.pre_close =  vargs[4]
                self.__stockdata.open_price =  vargs[5]
                self.__stockdata.diff_price =  str(int((float(vargs[3])-float(vargs[4]))*100)/100)
                self.__stockdata.diff_percent = str(int((float(vargs[3])-float(vargs[4]))/float(vargs[4])*10000+0.5)/100)                
 
        except Exception as ex:
            self.__log.error("Can not get stock!"+code)
            self.__log.error(str(type(ex))+str(dir(ex)))
            self.__log.error(str(ex.errno))
            self.__log.error(repr(ex))
             
        gc.collect() #内存回收
            
         

    def get_stock_data(self):
        return self.__stockdata
     
   

 
    
# print(dir())       
# #执行WIFI连接函数
# multiwifi.multi_wifi_connect()
# qt=QuoteSourceQtimg()
# qt.query_stock('sh000001')

