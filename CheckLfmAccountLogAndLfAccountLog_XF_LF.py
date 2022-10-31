import datetime
import DBConfig as config
import dbutils

# 内部用户发放比对-C端多账(调试完毕)
import strutils

if __name__ == "__main__":
    db_info = config.db_list_info[0]

    ##########################################################################################################################################################################################################################################
    # lfm_account_log < lf_account_log
    diff_sql_c = """
        select l.id, l.order_no, l.trans_amount,l.source from (select * from lfm_account_log where create_time >= {0} and create_time < {1} and account_type = '20' and (other_account_type = '1' or other_account like 'XF%') and trans_amount > 0) lm right join (
            select * from lf_account_log where create_time >={2} and create_time < {3} and acc_no like 'XF%' and (other_acc_no regexp 'FL|JL|CB|CP|FF|QYFF') = 1  and trans_amount > 0 and other_acc_no <> 'CB-QY') l on lm.order_no = l.order_no where lm.order_no is null order by l.id asc limit {4},{5};
    """

    # lfm_account_log < lf_account_log
    diff_sql_c_count = """
        select count(1) from (select * from lfm_account_log where create_time >= {0} and create_time < {1} and account_type = '20' and (other_account_type = '1' or other_account like 'XF%') and trans_amount > 0) lm right join (
            select * from lf_account_log where create_time >={2} and create_time < {3} and acc_no like 'XF%' and (other_acc_no regexp 'FL|JL|CB|CP|FF|QYFF') = 1 and trans_amount > 0 and other_acc_no <> 'CB-QY') l on lm.order_no = l.order_no where lm.order_no is null;
    """

    # 通过发放撤销继续过滤
    diff_sql_c_cx = """
        select la.id,la.order_no from
            (select * from lf_account_log where id in ({0})) la inner join (select * from t_ctrade_log where create_time >= {1} and create_time <= {2} and source = '10-01-07') tc on la.request_no = tc.id inner join (select * from t_btrade_log where create_time >= {3} and create_time <= {4} and action_type = 3 and source = '10-01-07') tb on tb.fid = tc.fid inner join 
            (select * from lfm_account_log where create_time >= {5} and create_time <={6} and acc_no like 'FF%' and other_account_type <> 25) lm on tb.id = lm.request_no;
    """

    diff_sql_c_hk = """
        select la.id,la.order_no from
            (select * from lf_account_log where id in ({0})) la left join (select * from t_ctrade_log where create_time >= {1} and create_time <= {2}) tc on la.request_no = tc.id left join (select * from t_btrade_log where create_time >= {3} and create_time <= {4} and action_type = 13) tb on tb.fid = tc.fid left join 
            (select * from lfm_account_log where create_time >= {5} and create_time <={6} and acc_no like 'FF%' and other_account_type <> 25) lm on tb.id = lm.request_no where tb.source = '10-01-13' and tc.source = '10-01-13';
    """

    diff_sql_c_tm = """
        select la.order_no from lfm_account_log la where order_no in ({0}) and account_type = '20' and (other_account_type = '1' or other_account like 'XF%');
    """
    ##########################################################################################################################################################################################################################################

    total = 0
    yh_count = 2147483647
    BATCH_SIZE = 100

    e = datetime.datetime.strptime('2022-01-20 00:00:00', '%Y-%m-%d %H:%M:%S')
    d = datetime.datetime.strptime('2020-05-20 00:00:00', '%Y-%m-%d %H:%M:%S')
    l = d
    for i in range(yh_count):
        d = l
        l = d + datetime.timedelta(days=1)

        print("==>当前日期为:" + d.strftime('%Y-%m-%d %H:%M:%S'))
        # print("==>当前日期为:" + l.strftime('%Y-%m-%d %H:%M:%S'))
        if e - d <= datetime.timedelta(days=0):
            break

        diff_sql_c_count_1 = diff_sql_c_count.format("'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                     "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                     "'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                     "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'")

        col_list_m, row_list_m = dbutils.execute_sql(diff_sql_c_count_1, "查询用户流水", db_info[1], db_info[2])
        if row_list_m is None or len(row_list_m) == 0:
            continue

        count = row_list_m[0][0]
        if count == 0:
            continue

        cicle = 1
        if count > BATCH_SIZE:
            if count % BATCH_SIZE == 0:
                cicle = count // BATCH_SIZE
            else:
                cicle = count // BATCH_SIZE + 1

        for i in range(0, cicle):
            diff_sql_c_1 = diff_sql_c.format("'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                             "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                             "'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                             "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                             BATCH_SIZE * i,
                                             BATCH_SIZE)

            col_list, row_list = dbutils.execute_sql(diff_sql_c_1, "查询用户流水", db_info[1], db_info[2])
            if row_list is None or len(row_list) == 0:
                continue

            id_list_1 = []  # 珑珠切至2.0前的数据比对（order_no）
            id_list_2 = []  # 珑珠切至2.0后的数据比对（id）
            id_list_3 = []  # 珑珠切至2.0后的数据比对（order_no）
            for j in range(len(row_list)):
                row = row_list[j]
                if row[3] > str(0):
                    # 2.0新产生的数据通过主键ID查询
                    id_list_2.append(row[0])
                    id_list_3.append(row[1])
                else:
                    # 1.0迁移的数据通过订单号查询
                    id_list_1.append(row[1])
                    # 1.0不需初始化id_list_3

            # 因时间差产生的差异，去对手账户流水查询，没有的，打印出来
            if len(id_list_1) > 0:
                diff_sql_c_tm_1 = diff_sql_c_tm.format(strutils.remove_bracket(id_list_1))
                col_list_tm, row_list_tm = dbutils.execute_sql(diff_sql_c_tm_1, "查询用户流水", db_info[1], db_info[2])
                if row_list_tm is None or len(row_list_tm) == 0:
                    for j in range(len(id_list_1)):
                        print("order_no ", id_list_1[j])
                else:
                    row_list_tm_list = []
                    for k in range(len(row_list_tm)):
                        row_list_tm_list.append(row_list_tm[k][0])

                    for k in range(len(id_list_1)):
                        order_no = id_list_1[k]
                        if order_no not in row_list_tm_list:
                            print("order_no ", order_no)

            # 因2.0发放撤销B端和C端流水号不一致产生的差异
            if len(id_list_2) > 0:
                diff_sql_c_cx_1 = diff_sql_c_cx.format(strutils.remove_bracket(id_list_2),
                                                       "'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                       "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                       "'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                       "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                       "'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                       "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'")
                col_list_cx, row_list_cx = dbutils.execute_sql(diff_sql_c_cx_1, "查询用户流水", db_info[1], db_info[2])
                if row_list_cx is None or len(row_list_cx) == 0:
                    continue

                row_list_cx_row = []
                for k in range(len(row_list_cx)):
                    row_list_cx_row.append(row_list_cx[k][1])

                if len(id_list_3) == len(row_list_cx_row):
                    continue

                id_list_4 = []  # 发放撤回欠款还款（id）
                id_list_5 = []  # 发放撤回欠款还款(order_no)
                for k in range(len(id_list_3)):
                    if id_list_3[k] not in row_list_cx_row:
                        id_list_4.append(id_list_2[k])
                        id_list_5.append(id_list_3[k])

                if len(id_list_4) > 0:
                    diff_sql_c_hk_1 = diff_sql_c_hk.format(strutils.remove_bracket(id_list_4),
                                                           "'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                           "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                           "'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                           "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                           "'" + d.strftime('%Y-%m-%d %H:%M:%S') + "'",
                                                           "'" + l.strftime('%Y-%m-%d %H:%M:%S') + "'")

                    col_list_hk, row_list_hk = dbutils.execute_sql(diff_sql_c_hk_1, "查询用户流水", db_info[1], db_info[2])
                    if row_list_hk is None or len(row_list_hk) == 0:
                        for k in range(len(id_list_4)):
                            print("order_no ", id_list_5[k])
                    else:
                        row_list_hk_row = dbutils.convert_to_list(row_list_hk, 0)
                        if len(id_list_4) == len(row_list_hk_row):
                            continue

                        for k in range(len(id_list_4)):
                            if id_list_4[k] not in row_list_hk_row:
                                print("order_no ", id_list_5[k])
