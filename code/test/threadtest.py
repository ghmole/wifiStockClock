import gc
import _thread
    
import machine
import utime
print(gc.mem_free())
gc.collect()
print(gc.mem_free())
print(gc.mem_alloc())

def thread2():
    print('----线程2开始执行----')
    print('thread id:', _thread.get_ident())
    print(gc.mem_free())
    utime.sleep(5)
    print('----Pr - 2 -结束----')
 
 
gLock = None
 
 
 
def Process1():
    print('----线程1开始执行----')
    print('thread id:', _thread.get_ident())
    print(gc.mem_free())
    utime.sleep(8)
    print('----Pr - 1 -结束----')
 
def main():
    print('----所有线程开始执行----')
    #创建互斥锁
    gLock = _thread.allocate_lock()
    
    #获得互斥锁
    gLock.acquire()
    
    #创建线程1
    _thread.start_new_thread(Process1,())
    utime.sleep(1)
    _thread.start_new_thread(thread2,())
 
    #休眠
    utime.sleep(2)
    
    #释放互斥锁
    gLock.release()
    while True:
        print('----主程序正在执行----')
        utime.sleep(1)
        
     
    
if __name__=='__main__':
    main()
 