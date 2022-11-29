# 发放｜撤回
ff_company_transaction_sql = """
                SELECT acc_no,sum(if(trans_type in (2,6),trans_amt,-trans_amt)),extra FROM t_company_transaction WHERE acc_no = {0} AND target_acc_no regexp 'XF|YH|SH|GLZ' AND `status` = 1 AND extra is not null AND extra != '' GROUP BY extra;
            """

# 活动预算
platform_grant_budget_apply_sql = """
                SELECT activity_no,apply_amount,fk_preuse_id FROM t_platform_grant_budget_apply WHERE activity_no in {0};
            """

# 活动发放数据汇总
platform_grant_list_sql = """
                SELECT
                    activity_no,
                    sum(case when grant_status=0 AND grant_type=1 then grant_amount else 0 end) preGrantSum,
                    sum(case when grant_status=1 AND grant_type=1 then grant_amount else 0 end) doneGrantSum,
                    sum(case when grant_status=2 AND grant_type=1 then grant_amount else 0 end) failGrantSum,
                    sum(case when grant_status=3 AND grant_type=1 then grant_amount else 0 end) processingGrantSum,
                    sum(case when grant_status=4 AND grant_type=1 then grant_amount else 0 end) frozenGrantSum,
                    sum(case when grant_status=1 AND grant_type=2 then refunded_amount else 0 end) refundedAmountSum,
                    sum(case when grant_status=5 AND grant_type=1 then grant_amount else 0 end) unRegistExpiresGrantSum 
                FROM t_platform_grant_list 
                WHERE activity_no in {0} AND is_deleted = 0
                GROUP BY activity_no;
            """

#活动回充
platform_grant_backwash_sql = """
                    SELECT 
                        pgad.activity_no,
                        IFNULL(SUM(t3.backwash_amount), 0)
                    FROM t_platform_grant_activity pga
                    LEFT JOIN t_platform_grant_activity_detail pgad ON pga.activity_no = pgad.activity_no
                    LEFT JOIN t_platform_grant_backwash t3 ON pga.activity_no = t3.activity_no
                    WHERE pga.logic_flag = 1
                      AND pga.is_deleted = 0
                      AND t3.backwash_status in (1, 3) AND pgad.activity_no in {0} 
                    GROUP BY pgad.activity_no
                """
#活动清零
platform_grant_clear_sql = """
                 SELECT 
                     pgad.activity_no,
                     IFNULL(sum(t3.clear_amt), 0)
                 FROM t_platform_grant_activity pga
                 LEFT JOIN t_platform_grant_activity_detail pgad ON pga.activity_no = pgad.activity_no
                 LEFT JOIN t_platform_grant_clear t3 ON pga.activity_no = t3.activity_no
                 WHERE pga.logic_flag = 1
                  AND pga.is_deleted = 0
                  AND t3.is_deleted = 0
                  AND pgad.activity_no in {0}
                GROUP BY pgad.activity_no;
         """

# 发放账户清零
account_ff_clear_transaction_sql = """
            SELECT acc_no,sum(clear_amt) FROM t_account_ff_clear_transaction WHERE acc_no = {0};
         """

# 发放账户余额｜冻结
account_ff_balance_freeze_sql = """
            SELECT
              tt.acc_no,
              t.balance,
              t.freeze_amount
            FROM
              lfm_account_balance t
              join lfm_account_info tt ON t.account_id = tt.account_id
            WHERE
              tt.acc_no = {0}
         """

# 发放账户充值
account_ff_cz_sql = """
           SELECT acc_no,trans_amt,serial_number FROM t_company_transaction WHERE acc_no = {0} AND target_acc_no not regexp 'XF|YH|SH|GLZ' AND `status` = 1 and trans_type = 1 AND is_deleted = 0;
         """

# 发放账户充值
account_tmp_ff_cz_sql = """
           SELECT acc_no,trans_amt,serial_number FROM t_company_transaction WHERE acc_no = {0} AND target_acc_no not regexp 'XF|YH|SH|GLZ' AND `status` = 1 and trans_type = 1 AND is_deleted = 0;
         """

account_tmp_ff_cz_tmp_sql = """
           SELECT acc_no,trans_amt,serial_number FROM t_company_transaction_tmp WHERE acc_no = {0} AND target_acc_no not regexp 'XF|YH|SH|GLZ' AND `status` = 1 and trans_type = 1 AND is_deleted = 0;
         """

# 发放账户流水总额-净发放金额
account_ff_ff_sql = """
           SELECT acc_no,sum(if(trans_type in (2,6),trans_amt,-trans_amt))
           FROM t_company_transaction 
           WHERE acc_no = {0} and extra = {1} AND target_acc_no regexp 'XF|YH|SH|GLZ' AND `status` = 1 and is_deleted = 0;
         """

# 活动发放总额-净发放金额
account_ff_order_sql = """
           SELECT
                activity_no,
                sum(if(grant_type = 1,grant_amount,-grant_amount)) grantSum
            FROM t_platform_grant_list 
            WHERE activity_no = {0} AND is_deleted = 0 AND grant_status=1 
            GROUP BY activity_no;
         """

# 发放账户流水总额-净发放金额
account_ff_out_trans_no_sql = """
           SELECT out_trans_no
           FROM t_company_transaction
           WHERE acc_no = {0} and target_acc_no regexp 'XF|YH|SH|GLZ' and (extra is null or extra = '') AND `status` = 1 limit 10
         """