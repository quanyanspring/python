from functools import reduce
import unittest, os, time, random
from multiprocessing import Queue
from multiprocessing import Process
import hashlib
import hmac
from html.parser import HTMLParser
from html.entities import name2codepoint
import psutil
import socket


def fn(x, y):
    return x * 10 + y


def not_empty(s):
    return s and s.strip()


def _by_name(t):
    return t[0]


def inc():
    x = 0

    def fn():
        nonlocal x
        x = x + 1
        return x

    return fn


def createCounter():
    x = 0

    def counter():
        nonlocal x
        x = x + 1
        return x

    return counter


class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score

    def get_grade(self):
        if self.score >= 80:
            return 'B'
        if self.score >= 60:
            return 'A'
        return 'C'


def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

# 写数据进程执行的代码:
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

def login(name,password):

    shal = hashlib.sha1()
    shal.update(name.encode('utf-8'))
    shal.update(password.encode('utf-8'))
    return shal.hexdigest() == db[name]

db = {
        'michael': 'e10adc3949ba59abbe56e057f20f883e',
        'bob': '878ef96e86145580c38c87f0410ad153',
        'alice': '99b1c2188db85afee403b1536010c2c9'
    }

def hmac_md5(key, s):
    return hmac.new(key.encode('utf-8'), s.encode('utf-8'), 'MD5').hexdigest()

class User(object):
    def __init__(self, username, password):
        self.username = username
        self.key = ''.join([chr(random.randint(48, 122)) for i in range(20)])
        self.password = hmac_md5(self.key, password)

if __name__ == "__main__":

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("www.sina.com.cn",80))
    s.send(b'GET / HTTP/1.1\r\nHost: www.sina.com.cn\r\nConnection: close\r\n\r\n')
    buffer = []
    while True:
        b = s.recv(1024,0)
        if b:
            buffer.append(b)
        else:
            break
    data = b''.join(buffer)
    s.close()

    header, html = data.split(b'\r\n\r\n', 1)
    print(header.decode('utf-8'))
    # 把接收的数据写入文件:
    with open('/Users/admin/Desktop/sina.html', 'wb') as f:
        f.write(html)



    # count = psutil.cpu_count(logical=False)
    # print(count)
    # memory = psutil.virtual_memory()
    # print(memory)
    #
    #
    # print(psutil.pids())
    #
    # for pid in psutil.pids():
    #     p = psutil.Process(pid)
    #     b = p.name().lower() == 'java'
    #     if b:
    #         print("%s,%n" + p.name() + p.pid)


    # with open("/Users/admin/Desktop/apollo_public_key") as file:
    #     s = file.read()
    #     print(s)
    # file.close()

    # for i in range(20)):
    #     print(i)
    #     print(chr(i+1))
    #
    # range_ = [chr(random.randint(48, 122)) for i in range(20)]
    # print(range_)
    #
    # assert login('michael', '123456')
    # assert login('bob', 'abc999')
    # assert login('alice', 'alice2008')
    # assert not login('michael', '1234567')
    # assert not login('bob', '123456')
    # assert not login('alice', 'Alice2008')
    # print('ok')

    # print(reduce(fn, [1, 3, 5, 7, 9]))

    # print(list(filter(not_empty, ['1', 'b', None, '', ' '])))

    # L = [('Bob', 75), ('Adam', 92), ('Bart', 66), ('Lisa', 88)]
    # print(list(sorted(L, key=_by_name)))

    # print(inc()())

    # counterA = createCounter()
    # print(counterA(), counterA(), counterA(), counterA(), counterA())  # 1 2 3 4 5
    # counterB = createCounter()
    # if [counterB(), counterB(), counterB(), counterB()] == [1, 2, 3, 4]:
    #     print('测试通过!')a
    # else:
    #     print('测试失败!')

    # L = list(filter(lambda x: x % 2 == 1, range(1, 20)))
    # print(L)

    # unittest.main()

    # print('Parent process %s.' % os.getpid())
    # # p = Pool(4)
    # for i in range(5):
    #     pool = Pool(long_time_task, args=(i,))
    # print('Waiting for all subprocesses done...')
    # p.close()
    # p.join()
    # print('All subprocesses done.')

    # str = "wang/lin/quan"
    # title = str.capitalize()
    # print(title)
    # title = str.casefold()
    # print(title)
    # lower = str.lower()
    # print(lower)
    # upper = str.upper()
    # print(upper)
    # title = str.title()
    # print(title)
    #
    # for i in range(1,11):
    #     print(i)
    #     print(random.random())

    # 父进程创建Queue，并传给各个子进程：
    # q = Queue()
    # pw = Process(target=write, args=(q,))
    # pr = Process(target=read, args=(q,))
    # # 启动子进程pw，写入:
    # pw.start()
    # # 启动子进程pr，读取:
    # pr.start()
    # # 等待pw结束:
    # pw.join()
    # # pr进程里是死循环，无法等待其结束，只能强行终止:
    # pr.terminate()
