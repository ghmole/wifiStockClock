# 导入工具类
import gc
#from lib.bean.stock_bean import StockBean 

class ClockStockUI():
    __log    = None
    __color  = None
    __screen = None
    
    def __init__(self, log, color, screen):
        self.__log = log
        self.__color = color
        self.__screen = screen
        
      
    # 画背景
    def background(self):

        self.__screen.draw_rect(5, 32, 230, 66, color=self.__color.CL_YOU, border=5, fillcolor=None)
        self.__screen.draw_rect(5, 102, 230, 66, color=self.__color.CL_YOU, border=5, fillcolor=None)
        self.__screen.draw_rect(5, 172, 230, 66, color=self.__color.CL_YOU, border=5, fillcolor=None)

        self.__screen.print_str('stock', 90, 1, color=self.__color.CYAN, backcolor=None, size=2)
    
    '初始化界面'
    def init(self):
        gc.collect()
        
        self.__screen.fill(self.__color.BLACK)
        self.background()
        
    '刷新界面信息'
    def refresh(self, datetime, stockBean):
        gc.collect()
        #self.__log.info('stock_ui.refresh():')
        stock_num=stockBean.get_stock_num()
        #self.__log.info('stock_ui.refresh(): stock_num=', stock_num)
        max_stock_page = int((stock_num+2)/3)
        
        second=datetime[6]
        
        if second % 15==2:
            self.__log.info('stock_ui.refresh(): second=', second)
            self.__log.info('stock_ui.refresh(): meet second%15=2 ')
            self.__log.info('stock_ui.refresh(): stock_num=', stock_num)
            self.__log.info('stock_ui.refresh(): max_stock_page=', max_stock_page)
            
            current_page = int(second/15)%4
            self.__log.info('stock_ui.refresh(): current_page=', current_page)
            if current_page<=max_stock_page:
                for i in range(3):
                    self.__log.info('stock_ui.refresh(): i=', i)
                    stock_index=current_page*3+i
                    if stock_index < stock_num:
                    
                        self.__log.info('stock_ui.refresh(): index=', stock_index)
                        data= stockBean.get_stock_data(stock_index)
                        self.__log.info('stock_ui.refresh(): stock code=',data.stock_code)
                        self.__screen.print_str(data.stock_code, 10, 36+i*70, \
                                                color=self.__color.WHITE, \
                                                backcolor=None,size=3)
                        self.__log.info('stock_ui.refresh(): diff_price=',data.diff_price)
                        self.__log.info('stock_ui.refresh(): diff_percent=',data.diff_percent)
                        if float(data.diff_price)>0:
                            price_color=self.__color.RED
                        elif float(data.diff_price)<0:
                            price_color=self.__color.GREEN
                        else:
                            price_color=self.__color.GAINSBORO
                            
                        self.__screen.print_str(data.diff_price, 155, 40+i*70, \
                                                color=price_color, \
                                                backcolor=None,size=2)
                        self.__screen.print_str(data.diff_percent, 170, 72+i*70, \
                                                color=price_color, \
                                                backcolor=None,size=1)
                        
            