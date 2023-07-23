import DBConfig as config
import dbutils

if __name__ == "__main__":
    db_info = config.db_list_info[0]

    js_acc_no_sql = """
        select acc_no from lfm_account_info where account_type = 21 order by acc_no;
    """

    diff_grant_js_sql = """
        select lai.acc_no, (t.amt - j.balance - j.settle_amount) result
        from lfm_account_balance j
                 join lfm_account_info lai on j.account_id = lai.account_id
                 left join (select sum(if(action_type in (1, 3, 4, 6, 8), trans_amount, -trans_amount)) amt, acc_no
                            from lfm_account_log
                            where acc_no = {0}
                              and other_account_type in (20,21)
                              and action_type in (0, 1, 2, 3, 4, 6, 7, 8)
                              and order_no not like 'DLX%'
                            group by acc_no) t on t.acc_no = lai.acc_no
        where lai.acc_no = {1} and lai.account_type = 21
        having result != 0;
    """

    col_list_m, row_list_m = dbutils.execute_sql(js_acc_no_sql, "查询差异", db_info[1], db_info[2])
    if len(row_list_m) > 0:
        for idx,item in enumerate(row_list_m):
            print("idx = %s , acc_no = %s" % (idx,item))

            acc_no = item[0]

            diff_sql = diff_grant_js_sql.format("'" + acc_no + "'", "'" + acc_no + "'")

            col_list_js, row_list_js = dbutils.execute_sql(diff_sql, "查询差异", db_info[1], db_info[2])

            if row_list_js is not None and len(row_list_js) > 0:
                for diff in row_list_js:
                    print("acc_no = %s,result = %n" % (diff[0], diff[1]))

