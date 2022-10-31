import dbutils
import DBConfig as config






def query():
    query_sql_fromat = query_sql.format(id)
    col_list, row_list = dbutils.execute_sql(query_sql_fromat, "查询用户流水", db_info[1], db_info[2])





if __name__ == "__main__":
    db_info = config.db_list_info[0]
    #导入账户信息
    #遍历单个账户流水，分页 t_grant_record
    #查询对比信息
    #导入账户信息

    id = 56595


    query_sql = """
        select trans_no,code from t_activity_result_log where id >= {0} order by id limit 1000; 
    """

    update_sql = """
            update t_activity_result_log set code = {0} where trans_no = {1}; 
        """


