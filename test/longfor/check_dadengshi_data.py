import datetime
import os

import DBConfig as config
import constants
import dbutils


# 写入文件
def print(msg):
    path = "/Users/admin/Desktop/订单模块排查/msg_result.json"
    file = None
    try:
        if not os.path.exists(path):
            file = open(path, mode="a", encoding="utf-8")
            file.write(msg)
    except Exception as e:
        print(e)
    finally:
        if file is not None:
            file.close()





#等式二问题确认脚本（调试完毕）

def consume(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_cousume.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                                "'" + temp_time.strftime(constants.date_time_format) + "'",
                                                "'" + start_time.strftime(constants.date_time_format) + "'",
                                                "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("消费/退款订单异常单号：out_trans_no:", itsm[1])


def cancel(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_cancel.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                               "'" + temp_time.strftime(constants.date_time_format) + "'",
                                               "'" + start_time.strftime(constants.date_time_format) + "'",
                                               "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("取消订单异常单号：out_trans_no:", itsm[1])


def left(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_left.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                             "'" + temp_time.strftime(constants.date_time_format) + "'",
                                             "'" + start_time.strftime(constants.date_time_format) + "'",
                                             "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("用户有商户没有异常单号：out_trans_no:", itsm[0])


def right(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_rignt.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                              "'" + temp_time.strftime(constants.date_time_format) + "'",
                                              "'" + start_time.strftime(constants.date_time_format) + "'",
                                              "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("商户有用户没有异常单号：out_trans_no:", itsm[1])


def sh(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_sh.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                           "'" + temp_time.strftime(constants.date_time_format) + "'",
                                           "'" + start_time.strftime(constants.date_time_format) + "'",
                                           "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("发放到商户异常单号：out_trans_no:", itsm[1])


def sh_left(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_sh_left.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                                "'" + temp_time.strftime(constants.date_time_format) + "'",
                                                "'" + start_time.strftime(constants.date_time_format) + "'",
                                                "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("发放到商户_left异常单号：out_trans_no:", itsm[0])


def sh_right(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_sh_right.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                                 "'" + temp_time.strftime(constants.date_time_format) + "'",
                                                 "'" + start_time.strftime(constants.date_time_format) + "'",
                                                 "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("发放到商户_right异常单号：out_trans_no:", itsm[0])


def glz(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_glz.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                            "'" + temp_time.strftime(constants.date_time_format) + "'",
                                            "'" + start_time.strftime(constants.date_time_format) + "'",
                                            "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("发放到管理者异常单号：out_trans_no:", itsm[1])


def glz_left(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_glz_left.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                                 "'" + temp_time.strftime(constants.date_time_format) + "'",
                                                 "'" + start_time.strftime(constants.date_time_format) + "'",
                                                 "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("发放到管理者-left异常单号：out_trans_no:", itsm[0])


def glz_right(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_glz_right.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                                  "'" + temp_time.strftime(constants.date_time_format) + "'",
                                                  "'" + start_time.strftime(constants.date_time_format) + "'",
                                                  "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("发放到管理者-right异常单号：out_trans_no:", itsm[0])


def xf(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_xf.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                           "'" + temp_time.strftime(constants.date_time_format) + "'",
                                           "'" + start_time.strftime(constants.date_time_format) + "'",
                                           "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("发放到内部异常单号：out_trans_no:", itsm[1])


def xf_left(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_xf_left.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                                "'" + temp_time.strftime(constants.date_time_format) + "'",
                                                "'" + start_time.strftime(constants.date_time_format) + "'",
                                                "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("发放到内部-left异常单号：out_trans_no:", itsm[0])


def xf_right(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_xf_right.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                                 "'" + temp_time.strftime(constants.date_time_format) + "'",
                                                 "'" + start_time.strftime(constants.date_time_format) + "'",
                                                 "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("发放到内部-right异常单号：out_trans_no:", itsm[0])


def yh(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_yh.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                           "'" + temp_time.strftime(constants.date_time_format) + "'",
                                           "'" + start_time.strftime(constants.date_time_format) + "'",
                                           "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("发放到外部异常单号：out_trans_no:", itsm[1])


def yh_left(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_yh_left.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                                "'" + temp_time.strftime(constants.date_time_format) + "'",
                                                "'" + start_time.strftime(constants.date_time_format) + "'",
                                                "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("发放到外部-left异常单号：out_trans_no:", itsm[0])


def yh_right(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_yh_right.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                                 "'" + temp_time.strftime(constants.date_time_format) + "'",
                                                 "'" + start_time.strftime(constants.date_time_format) + "'",
                                                 "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("发放到外部-right异常单号：out_trans_no:", itsm[0])


def xy(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_xy.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                           "'" + temp_time.strftime(constants.date_time_format) + "'",
                                           "'" + start_time.strftime(constants.date_time_format) + "'",
                                           "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("信用账户异常单号：out_trans_no:", itsm[1])


def red(start_time, temp_time):
    diff_sql_m_count1 = diff_sql_red.format("'" + start_time.strftime(constants.date_time_format) + "'",
                                            "'" + temp_time.strftime(constants.date_time_format) + "'",
                                            "'" + start_time.strftime(constants.date_time_format) + "'",
                                            "'" + temp_time.strftime(constants.date_time_format) + "'")

    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_m_count1, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("红包异常单号：name:{0},cnt:{1}".format(itsm[0], str(itsm[1])))


def sh_balance(start_time, temp_time):
    col_list_m, row_list_m = dbutils.execute_sql(diff_sql_sh_balance, "查询流水", db_info[1], db_info[2])
    if row_list_m is None or len(row_list_m) == 0:
        pass
    else:
        for idex, itsm in enumerate(row_list_m):
            print("查询商户流水和余额对比异常：account_id:{0},result:{1}".format(itsm[0], str(itsm[13])))


if __name__ == "__main__":
    db_info = config.db_list_info[0]

    ##########################################################################################################################################################################################################################################
    # 消费/退款
    diff_sql_cousume = """
        select t.*, tt.*
            from (select sum(trans_amt) outcome, out_trans_no
                  from t_merchant_transaction
                  where target_acc_no not like 'FF%'
                    and target_acc_no not like 'SH%'
                    and status != 5
                    and create_time > {0}
                    and create_time <= {1}
                  group by out_trans_no) t
                     left join (select sum(trans_amount) income, order_no
                                from lf_account_log
                                where other_acc_no like 'SH%'
                                  and create_time > {2}
                                  and create_time <= {3}
                                group by order_no) tt on tt.order_no = t.out_trans_no
            where tt.income != outcome;
        """

    # 取消订单
    diff_sql_cancel = """
        select t.*, tt.*
        from (select sum(trans_amt) outcome, out_trans_no
              from t_merchant_transaction
              where target_acc_no not like 'FF%'
                and target_acc_no not like 'SH%'
                and status = 5
                and create_time > {0}
                and create_time <= {1}
              group by out_trans_no) t
                 left join (select sum(if(action_type = 5, trans_amount, -trans_amount)) income, order_no
                            from lf_account_log
                            where other_acc_no like 'SH%'
                              and create_time > {2}
                              and create_time <= {3}
                            group by order_no) tt on tt.order_no = t.out_trans_no
        where tt.income + outcome != outcome
        """

    # 消费判断差异账sql
    diff_sql_left = """
        select t.*
        from (select order_no
              from lf_account_log
              where account_type in (1, 2)
                and other_acc_no like 'SH%'
                and create_time > {0}
                and create_time <= {1}
                and action_type = 3) t
                 left join (select id, out_trans_no
                            from t_merchant_transaction
                            where create_time > {2} and create_time <= {3} and status = 1) tt on tt.out_trans_no = t.order_no
        where tt.id is null
    """

    # 消费判断差异账sql  and create_time > {0} and create_time <= {1}
    diff_sql_rignt = """
           select tt.*
            from (select id, order_no
                  from lf_account_log
                  where account_type in (1, 2)
                    and other_acc_no like 'SH%'
                    and create_time > {0}
                    and create_time <= {1}) t
                     right join (select id, out_trans_no
                                 from t_merchant_transaction
                                 where create_time > {2}
                                   and create_time <= {3}
                                   and target_acc_no not like 'FF%'
                                   and target_acc_no not like 'SH%') tt on tt.out_trans_no = t.order_no
            where t.id is null
       """

    # 发放到商户sql
    diff_sql_sh = """
              select t.*
                from (select sum(trans_amount) outcoome, order_no order_no_lfm
                      from lfm_account_log
                      where account_type = 20
                        and other_account_type = 22
                        and create_time > {0}
                        and create_time <= {1}
                      group by order_no) t
                         left join (select sum(trans_amt) income, out_trans_no out_trans_no_lf
                                    from t_merchant_transaction
                                    where target_acc_no like 'FF%'
                                      and create_time > {2}
                                      and create_time <= {3}
                                    group by out_trans_no) tt on tt.out_trans_no_lf = t.order_no_lfm
                where tt.income != t.outcoome
          """

    # 发放到商户sql——left
    diff_sql_sh_left = """
                  select t.*
                    from (select order_no
                          from lfm_account_log
                          where account_type = 20
                            and other_account_type = 22
                            and create_time > {0}
                            and create_time <= {1}
                          group by order_no) t
                             left join (select id,out_trans_no
                                        from t_merchant_transaction
                                        where target_acc_no like 'FF%'
                                          and create_time > {2}
                                          and create_time <= {3}
                                        group by out_trans_no) tt on tt.out_trans_no = t.order_no
                    where tt.id is null
              """

    # 发放到商户sql——left
    diff_sql_sh_right = """
                      select tt.*
                        from (select id,order_no
                              from lfm_account_log
                              where account_type = 20
                                and other_account_type = 22
                                and create_time > {0}
                                and create_time <= {1}
                              group by order_no) t
                                 right join (select out_trans_no
                                            from t_merchant_transaction
                                            where target_acc_no like 'FF%'
                                              and create_time > {2}
                                              and create_time <= {3}
                                            group by out_trans_no) tt on tt.out_trans_no = t.order_no
                        where t.id is null
                  """

    # 发放到管理者sql
    diff_sql_glz = """
                 select t.*, tt.*
                from (select sum(trans_amount) outcoome, order_no as order_no_lfm
                      from lfm_account_log
                      where account_type = 20
                        and other_account_type = 3
                        and create_time > {0}
                        and create_time <= {1}
                      group by order_no) t
                         right join (select sum(trans_amount) income, order_no as order_no_lf
                                     from lf_account_log
                                     where account_type = 3
                                       and other_account_type = 20
                                       and create_time > {2}
                                       and create_time <= {3}
                                     group by order_no) tt on tt.order_no_lf = t.order_no_lfm
                where tt.income != t.outcoome
             """

    # 发放到管理者sql-left
    diff_sql_glz_left = """
                     select t.*
                    from (select order_no
                          from lfm_account_log
                          where account_type = 20
                            and other_account_type = 3
                            and create_time > {0}
                            and create_time <= {1}
                          group by order_no) t
                             left join (select id,order_no
                                         from lf_account_log
                                         where account_type = 3
                                           and other_account_type = 20
                                           and create_time > {2}
                                           and create_time <= {3}
                                         group by order_no) tt on tt.order_no = t.order_no
                    where tt.id is null 
                 """

    # 发放到管理者sql
    diff_sql_glz_right = """
    
                     select tt.*
                    from (select id,order_no
                          from lfm_account_log
                          where account_type = 20
                            and other_account_type = 3
                            and create_time > {0}
                            and create_time <= {1}
                          group by order_no) t
                             right join (select order_no
                                         from lf_account_log
                                         where account_type = 3
                                           and other_account_type = 20
                                           and create_time > {2}
                                           and create_time <= {3}
                                         group by order_no) tt on tt.order_no = t.order_no
                    where t.id is null
                 """

    # 发放到内部sql
    diff_sql_xf = """
                 select t.*, tt.*
                from (select sum(trans_amount) outcoome, order_no order_no_lfm
                      from lfm_account_log
                      where account_type = 20
                        and other_account_type = 1
                        and create_time > {0}
                        and create_time <= {1}
                      group by order_no) t
                         left join (select sum(trans_amount) income, order_no order_no_lf
                                     from lf_account_log
                                     where account_type = 1
                                       and other_account_type = 20
                                       and create_time > {2}
                                       and create_time <= {3}
                                     group by order_no) tt on tt.order_no_lf = t.order_no_lfm
                where tt.income != t.outcoome
             """

    # 发放到内部sql
    diff_sql_xf_left = """
                     select t.*
                    from (select order_no
                          from lfm_account_log
                          where account_type = 20
                            and other_account_type = 1
                            and create_time > {0}
                            and create_time <= {1}
                          group by order_no) t
                             left join (select id,order_no
                                         from lf_account_log
                                         where account_type = 1
                                           and other_account_type = 20
                                           and create_time > {2}
                                           and create_time <= {3}
                                         group by order_no) tt on tt.order_no = t.order_no
                    where tt.id is null 
                 """

    # 发放到内部sql
    diff_sql_xf_right = """
                     select tt.*
                    from (select id,order_no
                          from lfm_account_log
                          where account_type = 20
                            and other_account_type = 1
                            and create_time > {0}
                            and create_time <= {1}
                          group by order_no) t
                             right join (select order_no
                                         from lf_account_log
                                         where account_type = 1
                                           and other_account_type = 20
                                           and create_time > {2}
                                           and create_time <= {3}
                                         group by order_no) tt on tt.order_no = t.order_no
                    where t.id is null 
                 """

    # 发放到外部sql
    diff_sql_yh = """
                    select t.*, tt.*
                    from (select sum(trans_amount) outcoome, order_no as order_no_lfm
                          from lfm_account_log
                          where account_type = 20
                            and other_account_type = 2
                            and create_time > {0}
                            and create_time <= {1}
                          group by order_no) t
                             left join (select sum(trans_amount) income, order_no as order_no_lf
                                         from lf_account_log
                                         where account_type = 2
                                           and other_account_type = 20
                                           and create_time > {2}
                                           and create_time <= {3}
                                         group by order_no) tt on tt.order_no_lf = t.order_no_lfm
                    where tt.income != t.outcoome
                """

    # 发放到外部sql
    diff_sql_yh_left = """
                        select t.*
                        from (select order_no as order_no_lfm
                              from lfm_account_log
                              where account_type = 20
                                and other_account_type = 2
                                and create_time > {0}
                                and create_time <= {1}
                              group by order_no) t
                                 left join (select id, order_no as order_no_lf
                                             from lf_account_log
                                             where account_type = 2
                                               and other_account_type = 20
                                               and create_time > {2}
                                               and create_time <= {3}
                                             group by order_no) tt on tt.order_no_lf = t.order_no_lfm
                        where tt.id is null 
                    """

    # 发放到外部sql
    diff_sql_yh_right = """
    
                        select tt.*
                        from (select id,order_no as order_no_lfm
                              from lfm_account_log
                              where account_type = 20
                                and other_account_type = 2
                                and create_time > {0}
                                and create_time <= {1}
                              group by order_no) t
                                 right join (select order_no as order_no_lf
                                             from lf_account_log
                                             where account_type = 2
                                               and other_account_type = 20
                                               and create_time > {2}
                                               and create_time <= {3}
                                             group by order_no) tt on tt.order_no_lf = t.order_no_lfm
                        where t.id is null 
                    """

    # 信用账户sql
    diff_sql_xy = """
                    select t.*, tt.*
                    from (select sum(trans_amount) outcome, order_no_lfm
                          from lfm_account_log
                          where acc_no = 'XY-200722-00001'
                            and create_time > {0}
                            and create_time <= {1}
                          group by order_no) t
                             right join (select sum(trans_amount) income, order_no_lf
                                         from lf_account_log
                                         where other_acc_no = 'XY-200722-00001'
                                           and create_time > {2}
                                           and create_time <= {3}
                                         group by order_no) tt on tt.order_no = t.order_no
                    where t.outcome != tt.income
                """

    # 红包核对sql
    diff_sql_red = """
                    select '1-发红包-前置存在账户不存在笔数'as biz1,count(1) as cnt1 from t_pkg_out_log il left join
                    (select request_no, sum(trans_amount) as amt from lf_account_log
                    where source = '10-01-04' and create_time > '2021-11-25 03:10:00'and is_deleted = '0' group by request_no) as tt
                    on il.id = tt.request_no
                    where il.create_time > '2021-11-25 03:10:00' and il.status = '1' and (il.amount<> tt.amt or isnull(tt.request_no))
                    
                    union
                    select '1-发红包-账户存在前置不存在笔数'as biz2,count(1) as cnt2 from
                    (select request_no, sum(trans_amount) as amt from lf_account_log where source = '10-01-04' and create_time>'2021-11-25 03:10:00'
                    and is_deleted = '0' group by request_no) as tt left join
                    (select *from t_pkg_out_log il where il.create_time  > '2021-11-25 03:10:00'  and status = '1' ) as ee
                    on tt.request_no = ee.id where (tt.amt <> ee.amount or isnull(ee.id))
                    
                    union
                    select '1-领退红包-前置存在账户不存在笔数'as biz3,count(1) as cnt3 from t_pkg_in_log il left join
                    (select request_no, sum(trans_amount) as amt from lf_account_log where source = '10-01-05' and create_time > '2021-11-25 03:10:00' and is_deleted = '0' group by request_no) as tt
                    on il.id = tt.request_no
                    where il.create_time > '2021-11-25 03:10:00' and il.status = '1' and (il.amount<> tt.amt or isnull(tt.request_no))
                    
                    union
                    select '1-领退红包-账户存在前置不存在笔数'as biz4,count(1) as cnt4 from
                    (select request_no, sum(trans_amount) as amt from lf_account_log where source = '10-01-05' and create_time > '2021-11-25 03:10:00' and is_deleted = '0' group by request_no) as tt left join
                    (select *from t_pkg_in_log il where il.create_time > '2021-11-25 03:10:00' and status = '1' ) as ee
                    on tt.request_no = ee.id where (tt.amt <> ee.amount or isnull(ee.id))
                """

    diff_sql_sh_balance = """
        select b.*, (t.incoome - b.balance - b.settle_amount) result
        from lfm_account_balance b
                 join lfm_account_info l on b.account_id = l.account_id
                 left join (select sum(if(trans_type = 1, trans_amt, -trans_amt)) incoome, acc_no
                            from t_merchant_transaction
                            where status = 1
                            group by acc_no) t on t.acc_no = l.acc_no
        where l.account_type = 22
        having result != 0
    """

    ##########################################################################################################################################################################################################################################

    total_count = 2147483647
    BATCH_SIZE = 100

    start_time = datetime.datetime.strptime('2022-10-10 00:00:00', constants.date_time_format)
    end_time = datetime.datetime.strptime('2022-10-15 00:00:00', constants.date_time_format)
    temp_time = start_time
    red_count = 0
    for i in range(total_count):
        print("==>当前日期为:" + start_time.strftime(constants.date_time_format))
        if end_time - temp_time <= datetime.timedelta(days=0):
            break

        # 时间间隔递增1天
        temp_time = temp_time + datetime.timedelta(days=1)

        # 消费/退款
        consume(start_time, temp_time)

        # 取消订单
        cancel(start_time, temp_time)

        # 左确认
        left(start_time, temp_time)

        # 右确认
        right(start_time, temp_time)

        # 发放-商户
        sh(start_time, temp_time)

        # 发放-商户-left
        sh_left(start_time, temp_time)

        # 发放-商户-right
        sh_right(start_time, temp_time)

        # 商户 流水和账户余额
        # sh_balance(start_time, temp_time)

        # 发放-管理者
        glz(start_time, temp_time)

        # 发放-管理者-left
        glz_left(start_time, temp_time)

        # 发放-管理者-right
        glz_right(start_time, temp_time)

        # 发放-内部
        xf(start_time, temp_time)

        # 发放-内部-left
        xf_left(start_time, temp_time)

        # 发放-内部-right
        xf_right(start_time, temp_time)

        # 发放-外部
        yh(start_time, temp_time)

        # 发放-外部-left
        yh_left(start_time, temp_time)

        # 发放-外部-right
        yh_right(start_time, temp_time)

        # 红包
        red_count = red_count + 1
        if red_count < 2:
            red(start_time, temp_time)

        # 开始时间 + 1天
        start_time = start_time + datetime.timedelta(days=1)
