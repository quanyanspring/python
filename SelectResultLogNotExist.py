import DBConfig as config
import dbutils
import constants
import datetime


def select(start_time, temp_time):

    diff_sql_m_count1 = diff_sql.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                        "'" + temp_time.strftime(constants.date_time_format) + "'",
                                        "'" + start_time.strftime(constants.date_time_format) + "'",
                                        "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        arr_1 = []
        for idex, itsm in enumerate(row_list_m):
            arr_1.append("'" + itsm[0] + "'")
        join = ",".join(arr_1)
        diff = "(" + join + ")"
        sql_format = diff_trans_sql.format(diff)
        col_list_m, row_list_t = dbutils.execute_sql(sql_format, "查询流水", db_info[1], db_info[2])
        if row_list_t is None or len(row_list_t) != len(row_list_m):
            arr_2 = []
            if row_list_t is not None:
                for index,itsm_2 in enumerate(row_list_t):
                    arr_2.append("'" + itsm_2[0] + "'")

            list_1 = list(set(arr_1) - set(arr_2))

            file = open('/Users/admin/Desktop/insert_2.txt', mode='a', encoding='utf-8')
            arr = []
            for idex, itsm in enumerate(list_1):
                print("消费/退款订单异常单号：",itsm)
                arr.append("'" + str(itsm + "',\n"))
            file.writelines(arr)
            file.close()


if __name__ == "__main__":
    db_info = config.db_list_info[0]

    diff_sql = """
            SELECT request_no
                  from t_grant_record t
                     left join (SELECT id, trans_no
                                from t_activity_result_log
                                where id >= 46237147
                                  and trans_type = 0
                                  and create_time >= {0}
                                  and create_time < {1}
                                ) tt on tt.trans_no = t.request_no
            WHERE t.create_time >= {2} and t.create_time < {3} and t.`status` = 1 and t.`source` = '1.0' and tt.id is null;
            """

    diff_trans_sql = """
                select wallet_trans_no from t_platform_grant_list where  wallet_trans_no in {0} 
            """

    total_count = 2147483647
    BATCH_SIZE = 100

    start_time = datetime.datetime.strptime('2020-08-28 00:00:00', constants.date_time_format)
    end_time = datetime.datetime.strptime('2022-01-02 00:00:00', constants.date_time_format)
    temp_time = start_time
    red_count = 0
    for i in range(total_count):
        print("==>当前日期为:" + start_time.strftime(constants.date_time_format))
        if end_time - temp_time <= datetime.timedelta(days=0):
            break

        # 时间间隔递增1天
        temp_time = temp_time + datetime.timedelta(days=5)

        select(start_time,temp_time)

        # 开始时间 + 1天
        start_time = start_time + datetime.timedelta(days=5)
