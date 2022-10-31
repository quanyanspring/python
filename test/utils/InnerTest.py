import time
from functools import wraps


def timer(func):
    def inner(*arg,**kwargs):
        start = time.time()
        re = func(*arg, **kwargs)
        print(time.time() - start)
        return re
    return inner


def deco(func):
    @wraps(func)  # 加在最内层函数正上方
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    return wrapper

@timer
def func1(a,b):
    print("a,bin func1,%s,%s" % (a,b))


@timer
def func2(a):
    print("bin func2,%s" % a)

func1("123","234")
func2("345")

print(func1.__name__)
print(func2.__name__)
print(func1.__doc__)
print(func2.__doc__)
