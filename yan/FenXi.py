import pandas as pd

# 读取Excel文件
file_path = '/Users/elsa/Desktop/数据统计/一般情况调查.xlsx'
df = pd.read_excel(file_path)

columns_to_stat = ['性别', '婚姻状况', '身体健康情况', '子女情况', '养老方式', '是否再就业']

# 创建一个新的DataFrame来存储占比结果
result_df = pd.DataFrame(columns=['数字', '占比'])

# 定义要统计的数字列表
numbers_to_count = [1, 2, 3, 4]

# 遍历每一列并计算占比
for column_name in columns_to_stat:
    column = df[column_name]
    counts = column.value_counts().sort_index()

    # 初始化一个字典用于存储占比结果
    proportions = {num: 0 for num in numbers_to_count}

    # 计算每个数字的占比
    total_count = counts.sum()
    for num in numbers_to_count:
        if num in counts:
            proportions[num] = counts[num] / total_count

    # 添加占比结果到结果DataFrame中
    result_df = result_df.append({'数字': column_name, '占比': proportions}, ignore_index=True)

result_file_path = '/Users/elsa/Desktop/数据统计/一般情况统计.xlsx'
result_df.to_excel(result_file_path, index=False)
