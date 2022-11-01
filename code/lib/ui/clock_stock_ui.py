# 导入工具类
import gc


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
    def refresh(self, datetime,  stock_bean):
        gc.collect()
        