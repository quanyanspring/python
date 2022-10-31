import DBConfig as config
import dbutils
from decimal import *


def to_decimal(num, exp="0.0", rounding=ROUND_HALF_UP) -> Decimal:
    """
       转 Decimal，四舍五入
       :param num: int,str,float,Decimal
       :param exp: 精度
       :param rounding: 圆整模式
       :return: Decimal
       """
    if not num:
        return Decimal("0").quantize(exp=Decimal(exp), rounding=rounding)
    if not isinstance(num, str):
        num = str(num)
    return Decimal(num).quantize(exp=Decimal(exp), rounding=rounding)


def findMinAndMax(L):
    if len(L) == 0:
        return (None, None)
    elif len(L) == 1:
        return (L[0], L[0])
    else:
        return (min(L), max(L))

if __name__ == "__main__":

    if findMinAndMax([]) != (None, None):
        print('测试失败!')
    elif findMinAndMax([7]) != (7, 7):
        print('测试失败!')
    elif findMinAndMax([7, 1]) != (1, 7):
        print('测试失败!')
    elif findMinAndMax([7, 1, 3, 9, 5]) != (1, 9):
        print('测试失败!')

    else:
        print('测试成功!')


    db_info = config.db_list_info[0]

    js_acc_no_sql = """
        select * from lfm_account_log where acc_no = 'JS-200522-00079' and `source` > 0 and id > {0} order by create_time
    """

    id = 350004279

    while (True):

        try:
            diff_sql = js_acc_no_sql.format(id)

            col_list_m, row_list_m = dbutils.execute_sql(diff_sql, "查询差异", db_info[1], db_info[2])
            if len(row_list_m) > 0:

                tempBalance = Decimal(str('0.0'))
                flag = False

                for idx, item in enumerate(row_list_m):

                    # 2,3,10,11
                    id = item[0]
                    action_type = item[12]
                    trans_amount = Decimal(str(item[14]))
                    balance = Decimal(str(item[15]))

                    if idx == 0:
                        tempBalance = balance
                    else:
                        if action_type == 3:
                            result = tempBalance + trans_amount
                        else:
                            result = tempBalance - trans_amount

                        tempBalance = result

                        flag = balance.compare(result) == 1
                        if flag:
                            print("余额错误，id = %n" % id)
            else:
                break

        except Exception as e:
            print("出错啦，id = %n" % id)
