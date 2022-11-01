import uasyncio
import time


async def testa(x):
    print("in test a")
    await uasyncio.sleep(2)
    print("Resuming a")
    return x


async def testb(x):
    print("in test b")
    await uasyncio.sleep(1)
    print('Resuming b')
    return x


async def main():
    start = time.time()
#     resulta = await testa(1)
#     print("use %s time"%(time.time()-start))
#     resultb = await testb(2)
    resulta,resultb = await uasyncio.gather(testa(1),testb(2))
    print("test a result is %d"%resulta)
    print("test b result is %d"%resultb)
    print("use %s s"%(time.time()-start))

async def main2():
    start = time.time()

    taska = loop.create_task(testa(1))
    taskb = loop.create_task(testb(2))
    print(dir(taska))
    print(taska)
    print(taskb)
    print(taska.done(), taskb.done())
    await taskb
    await taska
    print(taska.done(), taskb.done())

    #print(taskb.data())
    #print(taska.state())
    print("use %s s" % (time.time() - start)) 
    
if __name__ == '__main__':
    
    loop = uasyncio.get_event_loop()
    loop.run_until_complete(main2())