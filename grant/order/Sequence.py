from test.longfor import dbutils


def createTroNo():
    create_tro_no_sql = """
        select concat(replace(current_timestamp(3)+0,'.',''),substring(convert(rand(),char),3,5))
    """

    col_list_m, row_list_c = dbutils.execute_sql(create_tro_no_sql, "生成trans_no")
    if row_list_c is None or len(row_list_c) != 1:
        print("生成trans_no,错误")
        raise TypeError
    else:
        return row_list_c[0][0]
