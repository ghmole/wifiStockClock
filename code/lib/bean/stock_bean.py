from lib.service.stockservice import StockData

class StockBean():
    __stock_data=[]
    __max_num=12
    
    def __init__(self):
        for i in range(self.__max_num):
            self.__stock_data.add(StockData())
            
    def update_stock_data(self,index, stockdata):
        if index >=self.__max_num:
             raise ValueError("index :" + str(index) + " exceed max stock index!")
        else:
            self.__stock_data[index]=stockdata
        
    def get_stock_data(self,index):
        if index >=self.__max_num:
             raise ValueError("index :" + str(index) + " exceed max stock index!")
        else:
            return self.__stock_data[index]