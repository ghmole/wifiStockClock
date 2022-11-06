# 导入工具类
import gc
#from lib.bean.stock_bean import StockBean 

class ClockStockUI():
    __log    = None
    __color  = None
    __screen = None
    __page   = 0
    
    def __init__(self, log, color, screen):
        self.__log = log
        self.__color = color
        self.__screen = screen   
      
    # 画背景
    def background(self):

        self.__screen.draw_rect(3, 32, 236, 66, color=self.__color.CL_YOU, border=5, fillcolor=None)
        self.__screen.draw_rect(3, 102, 236, 66, color=self.__color.CL_YOU, border=5, fillcolor=None)
        self.__screen.draw_rect(3, 172, 236, 66, color=self.__color.CL_YOU, border=5, fillcolor=None)

        self.__screen.print_str('stock', 90, 1, color=self.__color.CYAN, backcolor=None, size=2)
    
    '初始化界面'
    def init(self):
        gc.collect()
        
        self.__screen.fill(self.__color.BLACK)
        self.background()
    
    # 时间显示
    def datetime_display(self, datetime):
        #时间显示
        second = datetime[6]
        minute = datetime[5]
        hour = datetime[4]
        gc.collect()
    
        if hour > 9:
            self.__screen.print_str(str(hour), 160, 5, self.__color.GREEN, backcolor=None, size=1)
        else:
            self.__screen.print_str('0'+str(hour), 160, 5, self.__color.GREEN, backcolor=None, size=1)
        
        self.__screen.print_str(':', 180, 5, self.__color.GRAY, backcolor=None, size=1)
        
        if minute > 9:
            self.__screen.print_str(str(minute), 190, 5, self.__color.YELLOW, backcolor=None, size=1)
        else:
            self.__screen.print_str('0'+str(minute), 190, 5, self.__color.YELLOW, backcolor=None, size=1)
            
        self.__screen.print_str(':', 210, 5, self.__color.GRAY, backcolor=None, size=1)
        
        if second > 9:
            self.__screen.print_str(str(second), 220, 5, self.__color.RED, backcolor=None, size=1)
        else:
            self.__screen.print_str('0'+str(second), 220, 5, self.__color.RED, backcolor=None, size=1)
        
        gc.collect()
        
        
    '刷新界面信息'
    def refresh(self, datetime, stockBean):
        gc.collect()
        
        self.datetime_display(datetime)
        
        #self.__log.info('stock_ui.refresh():')
        stock_num=stockBean.get_stock_num()
        #self.__log.info('stock_ui.refresh(): stock_num=', stock_num)
        max_stock_page = int((stock_num+2)/3)
        
        
        second=datetime[6]
        
        if second % 15==2:
            #self.__log.info('stock_ui.refresh(): second=', second)
            #self.__log.info('stock_ui.refresh(): meet second%15=2 ')
            self.__log.info('stock_ui.refresh(): stock_num=', stock_num)
            self.__log.info('stock_ui.refresh(): max_stock_page=', max_stock_page)
            
            #current_page = int(second/15)%4
            current_page =  self.__page % max_stock_page
            self.__log.info('stock_ui.refresh(): current_page=', current_page+1)
            if current_page<=max_stock_page:
                for i in range(3):
                    #self.__log.info('stock_ui.refresh(): i=', i)
                    stock_index=current_page*3+i
                    if stock_index < stock_num:
                    
                        self.__log.info('stock_ui.refresh(): index=', stock_index)
                        data= stockBean.get_stock_data(stock_index)
                        self.__log.info('stock_ui.refresh(): stock code=',data.stock_code)
                        self.__screen.print_str(data.stock_code, 15, 36+i*70, \
                                                color=self.__color.GRAY, \
                                                backcolor=None,size=3)
                        self.__log.info('stock_ui.refresh(): diff_price=',data.diff_price)
                        self.__log.info('stock_ui.refresh(): diff_perct=',data.diff_percent)
                        
                        if data.diff_price is not '':
                            if float(data.diff_price)>0:
                                price_color=self.__color.RED
                            elif float(data.diff_price)<0:
                                price_color=self.__color.GREEN
                            else:
                                price_color=self.__color.GAINSBORO
                                
                            self.__screen.print_str(data.diff_price, 145, 40+i*70, \
                                                    color=price_color, \
                                                    backcolor=None,size=2)
                            self.__screen.print_str(data.diff_percent, 165, 72+i*70, \
                                                    color=price_color, \
                                                    backcolor=None,size=1)
                            
                            
                            self.__screen.print_str(data.pre_close, 15, 72+i*70, color=self.__color.GAINSBORO, backcolor=None,size=1)
                            self.__screen.print_str('/', 87, 72+i*70, color=self.__color.WHITE, backcolor=None,size=1)
                            self.__screen.print_str(data.last_price, 95, 72+i*70, color=price_color, backcolor=None,size=1)
                        else:
                            self.__screen.print_str(' '*7, 145, 40+i*70, \
                                                    color=self.__color.BLACK, \
                                                    backcolor=None,size=2)
                            self.__screen.print_str(' '*7, 165, 72+i*70, \
                                                    color=self.__color.BLACK, \
                                                    backcolor=None,size=1)

                            self.__screen.print_str(' '*9, 15, 72+i*70, color=self.__color.BLACK, backcolor=None,size=1)
                            self.__screen.print_str(' ', 87, 72+i*70, color=self.__color.BLACK, backcolor=None,size=1)
                            self.__screen.print_str(' '*9, 95, 72+i*70, color=self.__color.BLACK, backcolor=None,size=1)

                    else:
                        self.__screen.print_str(' '*8, 15, 36+i*70, \
                                                color=self.__color.GRAY, \
                                                backcolor=None,size=3)
                        self.__screen.print_str(' '*7, 145, 40+i*70, \
                                                    color=self.__color.BLACK, \
                                                    backcolor=None,size=2)
                        self.__screen.print_str(' '*8, 165, 72+i*70, \
                                                    color=self.__color.BLACK, \
                                                    backcolor=None,size=1)
                            
                        self.__screen.print_str(' '*9, 15, 72+i*70, color=self.__color.BLACK, backcolor=None,size=1)
                        self.__screen.print_str(' ', 87, 72+i*70, color=self.__color.BLACK, backcolor=None,size=1)
                        self.__screen.print_str(' '*9, 95, 72+i*70, color=self.__color.BLACK, backcolor=None,size=1)

                self.__page +=1