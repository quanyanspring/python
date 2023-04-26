"""
查询订单模块有，流水没有数据
"""
t_platform_grant_list_sql = """
        select t.* from
                (select wallet_trans_no from t_platform_grant_list where is_deleted = 0
              and grant_status = 1
              and activity_no = {0}) t
        left join (select out_trans_no,id from t_company_transaction where acc_no = {1}
              and target_acc_no regexp 'XF|SH|YH|GLZ'
              and is_deleted = 0 and status = 1
              and extra = {2}) tt on tt.out_trans_no = t.wallet_trans_no
        where tt.id is null;        
    """

t_platform_grant_sql = """
        select tt.*
        from (select wallet_trans_no,id
              from t_platform_grant_list
              where is_deleted = 0
                and grant_status = 1
                and activity_no = {0}) t
                 right join (select out_trans_no, id
                            from t_company_transaction
                            where acc_no = {1}
                              and target_acc_no regexp 'XF|SH|YH|GLZ'
                              and is_deleted = 0 and status = 1
                              and extra = {2}) tt
                           on tt.out_trans_no = t.wallet_trans_no
        where t.id is null;       
    """

t_platform_grant_list_right_sql = """
        select tt.*
        from (select wallet_trans_no,id
              from t_platform_grant_list
              where is_deleted = 0
                and grant_status = 1
                and activity_no = {0}) t
                 right join (select out_trans_no, id
                            from t_company_transaction
                            where acc_no = {1}
                              and target_acc_no regexp 'XF|SH|YH|GLZ'
                              and is_deleted = 0 and status = 1
                              and extra = {2} and id >= {3} and id <= {4}) tt
                           on tt.out_trans_no = t.wallet_trans_no
        where t.id is null;       
    """

t_platform_grant_list_right_id_sql = """
        select min(r.id),max(r.id) from
        (select tt.*
        from (select wallet_trans_no,id
              from t_platform_grant_list
              where is_deleted = 0
                and grant_status = 1
                and activity_no = {0}) t
                 right join (select out_trans_no, id
                            from t_company_transaction
                            where acc_no = {1}
                              and target_acc_no regexp 'XF|SH|YH|GLZ'
                              and is_deleted = 0 and status = 1
                              and extra = {2} and id > {3}) tt
                           on tt.out_trans_no = t.wallet_trans_no
        where t.id is null order by tt.id asc limit 1000) r;       
    """

"""
查询流水id
"""
t_company_transaction_sql = """
        select id,out_trans_no,acc_no,extra from t_company_transaction where acc_no = {0} and  out_trans_no in ({1}) and is_deleted = 0 and status = 1
    """

"""
查询流水id
"""
t_company_transaction_new_sql = """
        select id,out_trans_no,acc_no from t_company_transaction where out_trans_no in ({0}) and acc_no like 'FF%' and is_deleted = 0 and status = 1;
    """

"""
校验该活动是否已正常
"""
check_activity_sql = """
        select t.result1, tt.result2
        from (select sum(if(grant_type = 1, grant_amount, -grant_amount)) as result1
              from t_platform_grant_list
              where is_deleted = 0
                and  grant_status = 1
                and activity_no = {0}) t
           , (select sum(if(trans_type = 2, trans_amt, -trans_amt)) as result2
              from t_company_transaction
              where acc_no = {1}
                and extra = {2}
                and is_deleted = 0
                and status = 1) tt;
    """

"""
查询发放账户有多少个活动
"""
select_budget_appply_ff_acc_no_sql = """
    select * from t_platform_grant_budget_apply where grant_acc_no = {0} and is_deleted = 0;
"""

"""
查询发放账户有多少个活动
"""
select_budget_appply_ff_acc_sql = """
    select apply.activity_no,apply.grant_acc_no,activity.grant_method,activity.activity_status from t_platform_grant_budget_apply apply
    JOIN t_platform_grant_activity  activity on activity.activity_no = apply.activity_no
    where apply.fk_preuse_id is NOT null and apply.grant_acc_no is NOT null
"""

"""
项目公司流水
"""
t_company_transaction_by_out_trans_no_sql = """
        select * from t_company_transaction where out_trans_no = {0} and is_deleted = 0 and status = 1 and acc_no like 'FF%';
    """

"""
B端账户
"""
lfm_account_info_sql = """    
    select t.activity_type,ttt.payment_unit_name,ttt.nc_code from lfm_account_info t
    left join t_company tt on tt.company_no = t.merchant_no
    left join t_company_project ttt on ttt.id = tt.company_project_id where t.acc_no = {0}
    """

"""
C端账户
"""
lf_account_sql = """
        select t.acc_no,t.user_id,t.oa_account,tt.name1,tt.name1 as name2 from lf_account t
        left join t_mdg_employee tt on tt.oa_account = t.oa_account
        where t.acc_no = {0}
    """

"""
订单模块数据
"""
t_platform_grant_list_all_sql = """
        select * from t_platform_grant_list where wallet_trans_no = {0} and is_deleted = 0 and grant_status = 1;
    """

"""
订单模块数据
"""
t_platform_grant_list_all_order_by_sql = """
        select * from t_platform_grant_list where activity_no = {0} and id > {1} and is_deleted = 0 and grant_status = 1 order by id asc;
    """


"""
查询项目公司活动编号为空情况
"""
t_company_transaction_extra_is_null_sql ="""
    select * from t_company_transaction where acc_no = {0} and (extra is null or extra = '') and target_acc_no regexp 'YH|XF|GLZ|SH' and is_deleted = 0 and status = 1;
"""

"""
查询项目公司活动编号为空情况
"""
t_platform_grant_list_is_null_sql ="""
    select * from t_platform_grant_list where  grant_status = 0 and is_deleted = 0 and wallet_trans_no = {0};
"""
