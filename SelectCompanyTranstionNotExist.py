import DBConfig as config
import dbutils
import constants
import datetime


def select(start_time, temp_time):
    prehandle_id_start = 0
    prehandle_id_end = 0
    transaction_id_start = 0
    transaction_id_end = 0

    #prehandle 开始
    prehandle_id_sql_start = prehandle_id_sql.format("'" + start_time.strftime(constants.date_time_format) + "'")
    col_list_m, row_list_m = dbutils.execute_sql(prehandle_id_sql_start, "prehandle_id查询", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            prehandle_id_start = itsm[0]
            print("prehandle_id开始：", itsm[0])

    # prehandle 结束
    prehandle_id_sql_end = prehandle_id_sql.format("'" + temp_time.strftime(constants.date_time_format) + "'")
    col_list_m, row_list_m = dbutils.execute_sql(prehandle_id_sql_end, "prehandle_id查询", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            prehandle_id_end = itsm[0]
            print("prehandle_id结束：", itsm[0])

    #transaction 开始
    transaction_id_sql_start = transaction_id_sql.format("'" + start_time.strftime(constants.date_time_format) + "'")
    col_list_m, row_list_m = dbutils.execute_sql(transaction_id_sql_start, "prehandle_id查询", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            transaction_id_start = itsm[0]
            print("transaction_id开始：", itsm[0])

    ##transaction 结束
    transaction_id_sql_end = transaction_id_sql.format("'" + temp_time.strftime(constants.date_time_format) + "'")
    col_list_m, row_list_m = dbutils.execute_sql(transaction_id_sql_end, "prehandle_id查询", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            transaction_id_end = itsm[0]
            print("transaction_id结束：", itsm[0])


    diff_sql_m_count1 = diff_sql.format(prehandle_id_start,
                                        prehandle_id_end,
                                        transaction_id_start,
                                        transaction_id_end)

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        file = open('/Users/admin/Desktop/transNo.txt', mode='a', encoding='utf-8')
        arr = []
        for idex, itsm in enumerate(row_list_m):
            print("消费/退款订单异常单号：",itsm[0],",out_trans_no:", itsm[1])
            arr.append("'" + str(itsm[0] + "',\n"))
        file.writelines(arr)
        file.close()


if __name__ == "__main__":
    db_info = config.db_list_info[0]

    diff_sql = """
            select t.*
                from (select trans_no, id
                      from t_activity_detail_prehandle
                      where biz_sys_id = '117'
                        and status = 1
                        and id >= {0}
                        and id <= {1}) t
                         left join (select out_trans_no, id
                                    from t_company_transaction
                                    where biz_sys_id = '117'
                                      and acc_no like 'FF%'
                                      and id >= {2}
                                      and id <= {3}) tt
                                   on t.trans_no = tt.out_trans_no
                where tt.id is null;
            """

    prehandle_id_sql = """
        select min(id) from t_activity_detail_prehandle where create_time >= {0};
    """

    transaction_id_sql = """
        select min(id) from t_company_transaction where create_time >= {0}
    """


    total_count = 2147483647
    BATCH_SIZE = 100

    start_time = datetime.datetime.strptime('2021-10-01 00:00:00', constants.date_time_format)
    end_time = datetime.datetime.strptime('2022-06-24 00:00:00', constants.date_time_format)
    temp_time = start_time
    red_count = 0
    for i in range(total_count):
        print("==>当前日期为:" + start_time.strftime(constants.date_time_format))
        if end_time - temp_time <= datetime.timedelta(days=0):
            break

        # 时间间隔递增1天
        temp_time = temp_time + datetime.timedelta(days=30)

        select(start_time,temp_time)

        # 开始时间 + 1天
        start_time = start_time + datetime.timedelta(days=30)
