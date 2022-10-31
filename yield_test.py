import asyncio,os,json,time
from datetime import datetime

def consumes():
    r = ''
    while True:
        n = yield r
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        r = '200 OK'


@asyncio.coroutine
def produce(c):
    c.send(None)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        r = c.send(n)
        print('[PRODUCER] Consumer return: %s' % r)
    c.close()


if __name__ == "__main__":
    # c = consumes()
    # produce(c)
    s = ''
    if not s:
        print(s)
    else:
        print(2)
