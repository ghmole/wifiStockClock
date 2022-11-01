import time
import uasyncio

async def SleepTime(ts):
    if ts == 3:
        await uasyncio.sleep(10) #当ts等于3的时候，让挂起的时间为10s，其他的按正常挂起，验证协程时间。
    else:
        await uasyncio.sleep(ts)

async def main(loop):
    tasks = []
    for i in range(6):
        print("time begin %s"%i)
        tasks.append(loop.create_task(SleepTime(i))) #相当于开启了一个线程
        print("sleep time end %s"%i)
        print("*********************")
    await uasyncio.wait_for(tasks[2],50) #等待所有的任务完成。

if __name__ == "__main__":
    # main()
    print("begin test")
    tb = time.time()
    print(tb) #记录当前时间
    loop = uasyncio.get_event_loop()
    loop.run_until_complete(main(loop))
    loop.close()
    print(time.time()-tb) #记录结束时间
    print("end")
 