# 数组转化为字符串，逗号隔开
def remove_bracket_integer(id_list):
    result = ','
    if id_list == None or len(id_list) < 1:
        return result
    else:
        tmp_list = []
        for inx, item in enumerate(id_list):
           tmp_list.append("'" + item[0] + "'")
        return result.join(tmp_list)


def remove_bracket(id_list):
    return remove_bracket_integer(id_list)
