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
        self.__log.info('stock_ui.refresh():')
        stock_num=stockBean.get_stock_num()
        self.__log.info('stock_ui.refresh(): stock_num=', stock_num)
        max_stock_page = int((stock_num+2)/3)
        self.__log.info('stock_ui.refresh(): max_stock_page=', max_stock_page)
        second=datetime[6]
        self.__log.info('stock_ui.refresh(): second=', second)
        if second % 15==1:
            self.__log.info('stock_ui.refresh(): meet second=1 ')
            current_page = int(second/15)%4
            self.__log.info('stock_ui.refresh(): current_page=', current_page)
            if current_page<=max_stock_page:
                for i in range(3):
                    self.__log.info('stock_ui.refresh(): i=', i)
                    if current_page*3+i < stock_num:
                        self.__log.info('stock_ui.refresh(): i=', i)
                        data= stockBean.get_stock_data(current_page*3+i)
                        self.__screen.print_str(data.stock_code, 10, 36+i*70, \
                                                color=self.__color.WHITE, \
                                                backcolor=self.__color.CL_YANZHONG,size=3)
                        self.__screen.print_str(data.diff_price, 155, 40+i*70, \
                                                color=self.__color.RED, \
                                                backcolor=self.__color.CL_YANZHONG,size=2)
                        self.__screen.print_str(data.diff_percent(), 170, 72+i*70, \
                                                color=self.__color.GREEN, \
                                                backcolor=self.__color.CL_YANZHONG,size=1)
                        
            