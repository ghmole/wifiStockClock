# 导入相关模块
import gc,tftlcd,json

# 导入工具类

class Screen:
    __log   = None
    
    def __init__(self, log):
        self.__log = log


    __lcd = tftlcd.LCD15(portrait = 1)
    __file_font_num = 15
    
    '''
    '显示中文'
    def print_chinese(self, text, x, y, color = (0,0,0), backcolor = (255,255,255), size = 1):
        gc.collect()
        
        font_size = [0,16,24,32,40,48] # 分别对应size=1,2,3,4,5的字体尺寸，0无效。
    
        # 定义字体颜色, RGB888转RGB565
        fc = ((color[0]>>3)<<11) + ((color[1]>>2)<<5) + (color[2]>>3)  # 字体
        bc = ((backcolor[0]>>3)<<11) + ((backcolor[1]>>2)<<5) + (backcolor[2]>>3)  # 字体背景颜色
        
        try:
            f = open('/data/Fonts/fonts_index.txt', 'r')
            fonts_index = json.loads(f.read())
            f.close()
                
            xs = x
            for i in range(0, len(text)):
                ch_buf = []
                
                f = open('/data/Fonts/fonts' + str(int(int(fonts_index[text[i]]) / (self.__file_font_num * 4)) + 1) + '.txt', 'r')
                fonts = json.loads('{' + f.read() + '}')
                f.close()
                
                fonts = fonts[text[i]][str(font_size[size])]
                
                str_arr = fonts.split(',')
                ch_buf = [0 for z in range(len(str_arr))]
                for z in range(len(str_arr)):
                    ch_buf[z] = int(str_arr[z], 16)
                
                
                rgb_buf = []
                
                t1 = font_size[size] // 8
                t2 = font_size[size] % 8

                for i in range(0, len(ch_buf)):
                    for j in range(0, 8):
                        if (ch_buf[i] << j) & 0x80 == 0x00:
                            rgb_buf.append(bc & 0xff)
                            rgb_buf.append(bc >> 8)
                        else:
                            rgb_buf.append(fc & 0xff)
                            rgb_buf.append(fc >> 8)

                self.__lcd.write_buf(bytearray(rgb_buf), xs, y, font_size[size], font_size[size])
                
                xs += font_size[size]
                
                ch_buf = []
                rgb_buf = []
                f = None
                line = None
                fonts = None
                str_arr = None
                
                gc.collect()
        except BaseException as e:
            self.__log.error("Screen.printChinese  test = " + text)
            
            ch_buf = []
            rgb_buf = []
            gc.collect()
            
            raise
    '''    
        
        
       
    '显示中文'
    def print_chinese(self, text, x, y, color = (0,0,0), backcolor = (255,255,255), size = 1):
        gc.collect()
        
        font_size = [0,16,24,32,40,48] # 分别对应size=1,2,3,4,5的字体尺寸，0无效。
    
        # 定义字体颜色, RGB888转RGB565
        fc = ((color[0]>>3)<<11) + ((color[1]>>2)<<5) + (color[2]>>3)  # 字体
        bc = ((backcolor[0]>>3)<<11) + ((backcolor[1]>>2)<<5) + (backcolor[2]>>3)  # 字体背景颜色
        
        try:
            f = open('/data/Fonts/fonts_index.txt', 'r')
            fonts_index = json.loads(f.read())
            f.close()
                
            xs = x
            for i in range(0, len(text)):
                ch_buf = []
                
                f = open('/data/Fonts/fonts' + str(int(int(fonts_index[text[i]]) / (self.__file_font_num * 4)) + 1) + '.txt', 'r')
                
                target_index = int(fonts_index[text[i]]) % (self.__file_font_num * 4)
                line = ' '
                fonts = ''
                index = 0
                while line:
                    line = f.readline()
                    
                    if (index == target_index):
                        
                        for k in range(size):
                            line = f.readline()
                        
                        pos = 0
                        l = len(line)
                        for j in range(l):
                            if (line[l - 1 - j] == '"'):
                                pos = -1 - j
                                break
                        fonts = line[10:pos]
                        break
                    
                    index = index + 1
                    
                    if (index % 10 == 0):
                        gc.collect()
                f.close()
                
                str_arr = fonts.split(',')
                ch_buf = [0 for z in range(len(str_arr))]
                for z in range(len(str_arr)):
                    ch_buf[z] = int(str_arr[z], 16)
                
                
                rgb_buf = []
                
                t1 = font_size[size] // 8
                t2 = font_size[size] % 8

                for i in range(0, len(ch_buf)):
                    for j in range(0, 8):
                        if (ch_buf[i] << j) & 0x80 == 0x00:
                            rgb_buf.append(bc & 0xff)
                            rgb_buf.append(bc >> 8)
                        else:
                            rgb_buf.append(fc & 0xff)
                            rgb_buf.append(fc >> 8)

                self.__lcd.write_buf(bytearray(rgb_buf), xs, y, font_size[size], font_size[size])
                
                xs += font_size[size]
                
                ch_buf = []
                rgb_buf = []
                f = None
                line = None
                fonts = None
                str_arr = None
                
                gc.collect()
        except BaseException as e:
            self.__log.error(__file__ + ', ' + "Screen.printChinese  test = " + text + "  -> " +text[i])
            
            ch_buf = []
            rgb_buf = []
            gc.collect()
            
            raise
    
    
    def fill(self, color):
        self.__lcd.fill(color)
    def write_buf(self, byte_array, x, y, width, height):
        self.__lcd.write_buf(byte_array, x, y, width, height)
    def print_str(self, text, x, y, color, backcolor, size):
        self.__lcd.printStr(text, x, y, color, backcolor, size)
    def draw_rect(self, x, y, width, height, color, border, fillcolor):
        self.__lcd.drawRect(x, y, width, height, color, border, fillcolor)
    def draw_line(self, x0, y0, x1, y1, color):
        self.__lcd.drawLine(x0, y0, x1, y1, color)
    def picture(self, x, y, file):
        gc.collect()
        
        try:
            self.__lcd.Picture(x, y, file)
        except BaseException as e:
            self.__log.error(  __file__ + ', '"Screen.picture" )
            
            gc.collect()
            raise
        
    def draw_pixel(self, x, y, color):
        self.__lcd.draw_pixel(x, y, color)
    
    def clear(self, x, y, width, height, color):
        font_width =  [0,8, 12]
        font_height = [0,16,24]
  
        size = 5
        for i in range(3):
            if (font_width[2 - i] <= width):
                size = min(size, 2 - i)
                break
        for i in range(3):
            if (font_height[2 - i] <= height):
                size = min(size, 2 - i)
                break
        
        if (size == 0):
            if (width < height):
                for i in range(width):
                    self.draw_line(x + i, y, x + i, y + height, color)
            elif (width > height):
                for i in range(height):
                    self.draw_line(x, y + i, x + width, y + i, color)
            else:
                self.draw_rect(x, y, width, height, color, 0, color)
                
            #for i in range(width):
            #    for j in range(height):
            #        self.drawPixel(x + i, y + j, color)
        else:
            row_num = int(height / font_height[size])
            col_num = int(width / font_width[size])
            

            text = ''
            for i in range(col_num):
                text = text + ' '
                
            for i in range(row_num):
                self.print_str(text, x, y + i * font_height[size], color, color, size)
            
            # 解决横竖各差一个像素的bug
            for i in range(row_num):
                self.print_str(' ', x + width - font_width[size] + 1, y + i * font_height[size], color, color, size)
            for i in range(col_num):
                self.print_str(' ', x + i * font_width[size], y + height - font_height[size] + 1, color, color, size)
            self.print_str(' ', x + width - font_width[size] + 1, y + height - font_height[size] + 1, color, color, size)
   
   
   
        





