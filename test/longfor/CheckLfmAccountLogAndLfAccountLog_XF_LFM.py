import datetime
import DBConfig as config
import constants
import dbutils


# 内部用户发放比对-B端多账（调试完毕）
import strutils

if __name__ == "__main__":
    db_info = config.db_list_info[0]

    ##########################################################################################################################################################################################################################################
    # lfm_account_log > lf_account_log
    diff_sql_b = """
        select lm.kid, lm.order_no, lm.trans_amount,lm.source from (select * from lfm_account_log where create_time >= {0} and create_time < {1} and account_type = '20' and (other_account_type = '1' or other_account like 'XF%') and trans_amount > 0) lm left join (
            select * from lf_account_log where create_time >={2} and create_time < {3} and acc_no like 'XF%' and (other_acc_no regexp 'FL|JL|CB|CP|FF|QYFF') = 1  and trans_amount > 0 and other_acc_no <> 'CB-QY') l on lm.order_no = l.order_no where l.order_no is null order by lm.id asc limit {4},{5};
        """

    # lfm_account_log > lf_account_log
    diff_sql_b_count = """
        select count(1) from (select * from lfm_account_log where create_time >= {0} and create_time < {1} and account_type = '20' and (other_account_type = '1' or other_account like 'XF%') and trans_amount > 0) lm left join (
            select * from lf_account_log where create_time >={2} and create_time < {3} and acc_no like 'XF%' and (other_acc_no regexp 'FL|JL|CB|CP|FF|QYFF') = 1 and trans_amount > 0 and other_acc_no <> 'CB-QY') l on lm.order_no = l.order_no where l.order_no is null;
        """

    # 通过发放撤销继续过滤
    diff_sql_b_cx = """
        select lm.kid,lm.order_no from
            (select * from lfm_account_log where kid in ({0}) and other_account_type = 2 and action_type = 8) lm inner join (select * from t_btrade_log where create_time >= {1} and create_time <= {2}) tb on lm.request_no = tb.id inner join (select * from t_ctrade_log where create_time >= {3} and create_time <= {4}) tc on tb.fid = tc.fid inner join 
            (select * from lf_account_log where create_time >= {5} and create_time <= {6}) la on tc.id = la.request_no where tb.source = '10-01-07' and tc.source = '10-01-07';
        """

    # 检查是否有因时间差产生的差异
    diff_sql_b_tm = """
        select la.order_no from lf_account_log la where order_no in ({0}) and acc_no like 'XF%' and (other_acc_no regexp 'FL|JL|CB|CP|FF|QYFF') = 1 and trans_amount > 0 and other_acc_no <> 'CB-QY';
        """

    # 检查是否有冲正的单子
    diff_sql_b_cz = """
        select kid,order_no from lfm_account_log where order_no in ({0}) and action_type = 4;
    """
    ##########################################################################################################################################################################################################################################

    total_count = 2147483647
    BATCH_SIZE = 100

    e = datetime.datetime.strptime('2022-01-20 00:00:00', constants.date_time_format)
    d = datetime.datetime.strptime('2020-02-24 00:00:00', constants.date_time_format)
    l = d
    for i in range(total_count):
        d = l
        l = d + datetime.timedelta(days=1)

        print("==>当前日期为:" + d.strftime(constants.date_time_format))
        # print("==>当前日期为:" + l.strftime(constants.date_time_format))
        if e - d <= datetime.timedelta(days=0):
            break

        diff_sql_m_count1 = diff_sql_b_count.format("'" + d.strftime(constants.date_time_format) + "'",
                                                    "'" + l.strftime(constants.date_time_format) + "'",
                                                    "'" + d.strftime(constants.date_time_format) + "'",
                                                    "'" + l.strftime(constants.date_time_format) + "'")

        col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询用户流水", db_info[1], db_info[2])
        if row_list_m is None or len(row_list_m) == 0:
            continue

        count = row_list_m[0][0]
        if count == 0:
            continue

        circle = 1
        if count > BATCH_SIZE:
            if count % BATCH_SIZE == 0:
                circle = count // BATCH_SIZE
            else:
                circle = count // BATCH_SIZE + 1

        for i in range(0, circle):
            diff_sql1 = diff_sql_b.format("'" + d.strftime(constants.date_time_format) + "'",
                                          "'" + l.strftime(constants.date_time_format) + "'",
                                          "'" + d.strftime(constants.date_time_format) + "'",
                                          "'" + l.strftime(constants.date_time_format) + "'",
                                          BATCH_SIZE * i,
                                          BATCH_SIZE)

            col_list, row_list = dbutils.execute_sql(diff_sql1, "查询用户流水", db_info[1], db_info[2])
            if row_list is None or len(row_list) == 0:
                continue

            id_list_1 = []  # 珑珠切2.0前的数据比对（order_no）
            id_list_2 = []  # 珑珠切2.0后的数据比对（kid）
            id_list_3 = []  # 珑珠切2.0后的数据比对（order_no）
            for j in range(len(row_list)):
                row = row_list[j]
                if row[3] > str(0):
                    # 2.0新产生的数据通过主键ID查询
                    id_list_2.append(row[0])
                    id_list_3.append(row[1])
                else:
                    order_no = row[1]
                    # 2.0未迁移的订单（共20笔）
                    # 2.0迁移的05605账号发放失败的109条流水，因为就是单边账，需要过滤掉
                    if order_no in GlobalWhitelist.white_list_05605_109_ff \
                            or order_no in GlobalWhitelist.white_list_05605_109_cx \
                            or order_no in GlobalWhitelist.white_list_wqy:
                        continue
                    # 1.0迁移的数据通过订单号查询
                    id_list_1.append(order_no)

            # 因时间差产生的差异，去对手账户流水查询，没有的，打印出来
            if len(id_list_1) > 0:
                diff_sql_b_tm_1 = diff_sql_b_tm.format(strutils.remove_bracket(id_list_1))
                col_list_tm, row_list_tm = dbutils.execute_sql(diff_sql_b_tm_1, "查询用户流水", db_info[1], db_info[2])
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
                diff_sql_b_cx_1 = diff_sql_b_cx.format(strutils.remove_bracket(id_list_2),
                                                       "'" + d.strftime(constants.date_time_format) + "'",
                                                       "'" + l.strftime(constants.date_time_format) + "'",
                                                       "'" + d.strftime(constants.date_time_format) + "'",
                                                       "'" + l.strftime(constants.date_time_format) + "'",
                                                       "'" + d.strftime(constants.date_time_format) + "'",
                                                       "'" + l.strftime(constants.date_time_format) + "'")
                col_list_cx, row_list_cx = dbutils.execute_sql(diff_sql_b_cx_1, "查询用户流水", db_info[1], db_info[2])

                id_list_4 = []
                if row_list_cx is None or len(row_list_cx) == 0:
                    id_list_4 = id_list_3
                else:
                    row_list_cx_row = dbutils.convert_to_list(row_list_cx, 0)

                    # 过滤出没有找到对应映射的单子
                    for k in range(len(id_list_2)):
                        if id_list_2[k] not in row_list_cx_row:
                            id_list_4.append(id_list_3[k])

                id_list_4 = list(set(id_list_4))  # 去重
                # 检查是否有冲正的单子
                if len(id_list_4) > 0:
                    diff_sql_b_cz_1 = diff_sql_b_cz.format(strutils.remove_bracket(id_list_4))
                    col_list_cz, row_list_cz = dbutils.execute_sql(diff_sql_b_cz_1, "查询用户流水", db_info[1], db_info[2])
                    # 没有记录，说明没有冲正，则打印
                    if row_list_cz is None or len(row_list_cz) == 0:
                        for k in range(len(id_list_4)):
                            print("order_no:", id_list_4[k])
                        continue
                    else:
                        row_list_cz_res = dbutils.convert_to_list(row_list_cz, 1)
                        if len(row_list_cz_res) == len(id_list_4):
                            continue

                        for k in range(len(id_list_4)):
                            order_no = id_list_4[k]
                            if order_no not in row_list_cz_res:
                                print("order_no:", order_no)
