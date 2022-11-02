from libs.urllib import urequest
import time

import gc

# 导入工具类


class StockData():
    uid=0
    stock_name = ''
    stock_code = ''
    last_price = ''
    pre_close = ''
    open_price = ''
    diff_price = ''
    diff_percent = ''
    def __init__(self,uid):
        self.uid=uid
       
    
 
class StockService():
    __log = None
    __stock_data = None
    #__stock_bean = None
    
    def __init__(self, log):
        self.__log = log
        self.__stock_data = StockData(0)
 
        
#     def query_stock_list(self,code_list):
#         for i,code in enumerate(code_list):
#             self.__log.info('get stock code:' + code)
#             self.__stock_data=slef.query_stock(code)
#             self.__stock_bean.update_stock_data(i, self.__stock_data)
        
    def query_stock(self, code):
        gc.collect()
        try:
#             my_url='http://qt.gtimg.cn/r=0.9392363841179758&q='+code
            #my_url='https://web.sqt.gtimg.cn/q=' + code
            #my_url='https://sqt.gtimg.cn/q='+code
            my_url='http://qt.gtimg.cn/q=' + code
            self.__log.info(my_url)
            my_req = urequest.urlopen(my_url)

            # 坏消息micropython 不支持gbk编码
            res = my_req.read(800)#.decode('UTF-8') #抓取约前4W个字符，节省内存。
           
            res=str(res) 
            self.__log.info(res)
            gc.collect()
            time.sleep_ms(50)
            
            for line in res.split(';'):
                #print line
                if len(line) < 50 :
                    continue
                info = line[12: 100]
                #print info
                vargs = info.split('~')
                self.__log.info(vargs)
                #print vargs
                self.__stock_data.stock_name = vargs[1]
                self.__stock_data.stock_code = code # vargs[2]
                if 'sh5' in code:
                    self.__stock_data.last_price =  self.pad_price(float(vargs[3]), fmt='{0:>+7.3f}');
                    self.__stock_data.pre_close =  self.pad_price(float(vargs[4]), fmt='{0:>+7.3f}');
                    self.__stock_data.open_price =  self.pad_price(float(vargs[5]), fmt='{0:>+7.3f}');
                else:
                    self.__stock_data.last_price =  self.pad_price(float(vargs[3]));
                    self.__stock_data.pre_close =  self.pad_price(float(vargs[4]));
                    self.__stock_data.open_price =  self.pad_price(float(vargs[5]));
                if vargs[3]=='' or vargs[4]=='':
                    self.__stock_data.diff_price=''
                    self.__stock_data.diff_percent=''
                else:
                    if 'sh5' in code:
                        vdiff=int((float(vargs[3])-float(vargs[4]))*1000)/1000
                        self.__stock_data.diff_price =  self.pad_diff(vdiff,fmt='{0:>+7.3f}')
                    else:
                        vdiff=int((float(vargs[3])-float(vargs[4]))*100)/100
                        self.__stock_data.diff_price =  self.pad_diff(vdiff)
                    self.__log.info('vdiff : %f\n' % (vdiff))
                    
                    vpercent=int((float(vargs[3])-float(vargs[4]))/float(vargs[4])*10000+0.5)/100
                    self.__log.info('vpercent : %f\n' % (vpercent))
                    self.__stock_data.diff_percent = self.pad_percent(vpercent)
                             
 
                self.__log.info('stock_name: %s\n' % self.__stock_data.stock_name)
                self.__log.info('stock_code: %s\n' % self.__stock_data.stock_code)
                self.__log.info('last_price: %s\n' % self.__stock_data.last_price)
                self.__log.info('pre_close: %s\n' % self.__stock_data.pre_close)
                self.__log.info('open_price: %s\n' % self.__stock_data.open_price)
                self.__log.info('diff_price: %s\n' % (self.__stock_data.diff_price))
                self.__log.info('diff_percent: %s  \n' % (self.__stock_data.diff_percent))
            
            gc.collect() #内存回收
            return True
            
        except Exception as ex:
            self.__log.error("Can not get stock!"+code)
            self.__log.error(str(type(ex))+str(dir(ex)))
            self.__log.error(str(ex.errno))
            self.__log.error(repr(ex))
             
        gc.collect() #内存回收
        return False
            
         

    def get_stock_data(self): 
        return self.__stock_data
     
    
    def pad_diff(self, f, fmt='{0:>+4.2f}', w=6):
        self.__log.info('StockService.pad_diff():')
        self.__log.info('StockService.pad_diff():f=', f)
        
        # '{0:>+10.2f}'.format()
        s=fmt.format(f)
         
        self.__log.info('StockService.pad_diff():s=',s)
         
        if len(s)<w:
            s=' '*(w-len(s))+s 
 
        return s
    
    def pad_percent(self, f, fmt='{0:>+4.2f}', w=6):
        self.__log.info('StockService.pad_percent():')
        s= fmt.format(f)
        if len(s)<w:
            s= ' '*(w-len(s))+s 
        return s+'%'
    
    
    def pad_price(self, f, fmt='{0:>+7.2f}', w=7):
        self.__log.info('StockService.pad_price()')
        s= fmt.format(f)
 
        self.__log.info('StockService.pad_price(): len=',len(s),'value=',s)
        if len(s)<w:
            s=' '*(w-len(s))+s 
        
        return s
 
