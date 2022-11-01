#ostest

import os
import sys
# print (sys._getframe().f_lineno)
folders=os.listdir('/data/config/')

for d in folders:
    print(d)
    
# print (sys._getframe().f_lineno)