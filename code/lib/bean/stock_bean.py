from lib.service.stockservice import StockData


class StockBean():
    __stock_data = []
    __max_num = 12
    __stock_num = 0
    __log = None
    
    def __init__(self, log):
        self.__log = log
#         for i in range(self.__max_num):
#             self.__stock_data.append(None)
    
    def add_stock_data(self,stockdata):
        if self.__stock_num+1 >= self.__max_num:
            raise ValueError("__stock_num : exceed max stock bean size!")
        else:
            d = StockData(0)
            # 必须复制数据，否则都是一个数据的引用
            self.copy_stock_data(d, stockdata)
            self.__stock_data.append(d)
            self.__stock_num +=1
            self.__log.info('StockBean.add_stock_data(): __stock_num=', self.__stock_num)
    
    
    def del_stock_data(self, stockindex):
        if stockindex>=0 and stockindex<len(self.__stock_data):
            self.__log.info('StockBean.del_stock_data(): index=', stockindex)
            self.__log.info('StockBean.del_stock_data(): code=', self.__stock_data[stockindex].stock_code)
            del self.__stock_data[stockindex]
            self.__stock_num -=1

    # 复制数据
    def copy_stock_data(self,dest,src):
        dest.uid = src.uid
        dest.stock_name = src.stock_name
        dest.stock_code = src.stock_code
        dest.last_price = src.last_price
        dest.pre_close = src.pre_close
        dest.open_price = src.open_price
        dest.diff_price = src.diff_price
        dest.diff_percent = src.diff_percent
        
    def update_stock_data(self,index, stockdata):
        self.__log.info('StockBean.update_stock_data(): index=', index)
        self.__log.info('StockBean.update_stock_data(): stock_num=', self.__stock_num)
        self.__log.info('StockBean.update_stock_data(): max_num=', self.__max_num)
        if index >=self.__max_num or self.__stock_num >= self.__max_num or self.__stock_num==0:
            raise ValueError("index :" + str(index) + " exceed max stock index!")
        else:
            if stockdata is not None:
                stockdata.uid=index
                d = StockData(0)
                self.copy_stock_data(d,stockdata)
                self.__stock_data[index] = d
                self.__log.info('StockBean.update_stock_data(): stock.uid=', d.uid)
                self.__log.info('StockBean.update_stock_data(): stock.code=', stockdata.stock_code)
                self.__log.info('StockBean.update_stock_data(): stock.lastprice=', stockdata.last_price)
                self.__log.info('StockBean.update_stock_data(): stock.diff_price=', stockdata.diff_price)
            else:
                del self.__stock_data[index]
                self.__stock_num -= 1
                self.__log.info('StockBean.update_stock_data(): data[index] = None  __stock_num-1=', self.__stock_num)
        
    def get_stock_data(self,index):
        if index >=self.__max_num or self.__stock_num >= self.__max_num:
            
            raise ValueError("index :" + str(index) + " exceed max stock index!")
        else:
            return self.__stock_data[index]
        
    def get_stock_num(self):
        return self.__stock_num
    
    
    def check_bean_data(self):
        self.__log.info('StockBean.check_bean_data() ')
        for data in self.__stock_data:
            self.__log.info('-'*30)
            self.__log.info('StockBean.check_bean_data(): stock.uid=', data.uid)
            self.__log.info('StockBean.check_bean_data(): stock.code=', data.stock_code)
            self.__log.info('StockBean.check_bean_data(): stock.lastprice=', data.last_price)
            self.__log.info('StockBean.check_bean_data(): stock.diff_price=', data.diff_price)

        self.__log.info('-'*30)
        
    def clean_data(self):
        self.__stock_data.clear()