#!//Users/admin/Desktop/python/test python3
# -*-coding: utf-8 -*-
' a test model'
__author__ = 'wanglinquan'

import sys


def test():
    argv = sys.argv
    if len(argv) == 1:
        print('HELLO WORLD')
    elif len(argv) == 2:
        print('Hello,%s!' % argv[1])
    else:
        print('too many arguments!')


# if __name__ == '__main__':
    # test()


db_list_info = [
    ["2.0tidb数据库", "tidb10.31.48.7_脱敏查询", "longem_tidb"],
    ["C端C1库", "10.31.54.176_脱敏查询", "longgem_caccount_c1"],
    ["C端C0库", "10.31.54.177_脱敏查询", "longgem_caccount_c0"],
    ["B端库", "10.31.54.213_脱敏查询", "longgem_baccount"],
    ["前置数据库", "10.31.54.11_脱敏查询", "longgem_integrate"],
    ["1.0tidb数据库", "珑珠_tidb2_查询", "tidb_wallet"]
]

if __name__ == "__main__":

    temp_order_no = ""
    temp_order_no_list = []

    for i in range(len(db_list_info)):
        row = db_list_info[i]
        temp_order_no_list.append("'" + row[0] + "'")

        temp_order_no = ",".join(temp_order_no_list)
    temp_order_no = "(" + temp_order_no + "),"

    print(temp_order_no)