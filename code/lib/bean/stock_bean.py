from lib.service.stockservice import StockData

class StockBean():
    __stock_data = []
    __max_num = 12
    __stock_num = 0
    
    def __init__(self):
        for i in range(self.__max_num):
            self.__stock_data.add(StockData())
            
            
    def update_stock_data(self,index, stockdata):
        if index >=self.__max_num or \
           self.__stock_num >= self.__max_num or \
           self.__stock_num==0:
             raise ValueError("index :" + str(index) + " exceed max stock index!")
        else:
            if stockdata is not None:
                self.__stock_data[index] = stockdata
                self.__stock_num += 1
            else
                del self.__stock_data[index]
                self.__stock_num -= 1
        
    def get_stock_data(self,index):
        if index >=self.__max_num or self.__stock_num >= self.__max_num:
             raise ValueError("index :" + str(index) + " exceed max stock index!")
        else:
            return self.__stock_data[index]
        
    def get_stock_numa(self):
        return self.__stock_num
        
    def clean_data(self):
        self.__stock_data.clear()