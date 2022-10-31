# 数组转化为字符串，逗号隔开
def remove_bracket_integer(id_list):
    result = ''
    if id_list == None or len(id_list) < 1:
        return result
    else:
        for inx, item in enumerate(id_list):
            result.join(',', str(item))


def remove_bracket(id_list):
    return remove_bracket_integer(id_list)
