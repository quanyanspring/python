from multiprocessing import Pool,Manager
import time
import random


def write(q):
    for i in [11,22,33]:
        if not q.full():
            q.put(i)
            print("put %d in quee" % i)
            time.sleep(random.random())

def read(q):
    while True:
        if not q.empty():
            value = q.get()
            print("get %d from quee" % value)
            time.sleep(random.random())
        # else:
        #     break


if __name__ == "__main__":
    queue = Manager().Queue()
    pool = Pool()
    pool.apply_async(write,args=(queue,))
    pool.apply_async(read,args=(queue,))
    pool.close()
    pool.join()



