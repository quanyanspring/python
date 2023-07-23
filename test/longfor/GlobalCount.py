import xlwt

col_list = [
    ["acc_no"],
    ["person_ad"],
    ["balance_amt"],
    ["frozen_amt"],
    ["status"],
    ["create_time"],
    ["create_user"],
    ["modify_time"],
    ["modify_user"],
    ["is_delete1"],
]

if __name__ == "__main__":
    workbook = xlwt.Workbook(encoding='ascii')
    worksheet = workbook.add_sheet('My Worksheet')
    for i in range(len(col_list)):
        col_str = col_list[i]
        worksheet.write(0, i, col_str[0])

    workbook.save('/Users/admin/Desktop/大等式/测试数据_2.xls')
