from functools import reduce


def str2num(s):
    return int(s)


def calc(exp):
    ss = exp.split('+')
    ns = map(str2num, ss)
    return reduce(lambda acc, x: acc + x, ns)


def main():
    r = calc('100 + 200 + 345')
    print('100 + 200 + 345 =', r)
    r = calc('99 + 88 + 6')
    print('99 + 88 + 6 =', r)


def my_abs(s):
    if not isinstance(s, (int, float)):
        raise TypeError('bad type error')
    if s < 18:
        pass
    elif s > 18 and s < 20:
        return s
    else:
        return -s


def mul(**y):
    if len(y) == 1:
        return y

    sum = 1
    for n in y:
        sum = sum * n

    return sum


print(my_abs(23))

main()
