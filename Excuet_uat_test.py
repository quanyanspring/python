import TestDBConfig as config
import dbutils_UAT as dbutils

if __name__ == "__main__":

    id_start = 81636;
    page_limit = 10000;

    info = config.db_list_info

    select_sql= """
        select id,trans_no,code from t_activity_result_log where id > {0} order by id limit {1};
    """

    update_sql = """
        update t_activity_result_log set code = {0} where trans_no = {1};
    """

    while True:
        query = dbutils.execute_select_sql_uat(select_sql.format(id_start, page_limit), info[0])
        if query is not None or len(query) > 0:
            for index,item in enumerate(query):
                print(item)
                if index == len(query)-1:
                    id_start = item[0]
                update = dbutils.execute_update_sql_uat(update_sql.format("'" + str(item[2]) + "'", "'" + str(item[1]) + "'"), info[1])
                print("更新条数",str(update))
        else:
            break

