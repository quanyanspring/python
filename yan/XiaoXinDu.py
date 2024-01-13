import pandas as pd
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_kmo

# 读取Excel文件
file_path = '/Users/elsa/Desktop/202309-202401/刘琰老师数据统计/数据处理/双向代际关系的副本.xlsx'  # 替换成你的Excel文件路径
df = pd.read_excel(file_path)

# 提取数据
scores_columns = ['score_1', 'score_2', 'score_3', 'score_4', 'score_5', 'score_6', 'score_7', 'score_8', 'total_score']
scores_data = df[scores_columns]

# 定义分组（经济支持、照料支持、情感支持）
economic_support = scores_data[['score_1', 'score_2']]
care_support = scores_data[['score_3', 'score_4', 'score_5']]
emotion_support = scores_data[['score_6', 'score_7', 'score_8']]


# total_score = scores_data[['total_score']]

# 计算Cronbach's Alpha和KMO检验
def calculate_alpha_and_kmo(data):
    # 计算Cronbach's Alpha
    def calculate_cronbach_alpha(data):
        item_means = data.mean(axis=0)
        overall_mean = item_means.mean()
        variance_total = data.var(axis=0, ddof=1)
        covariance_matrix = data.cov()
        num_items = len(item_means)
        sum_covariance_matrix = covariance_matrix.sum().sum()

        if sum_covariance_matrix == 0:
            return 0  # 返回0或者其他值，代表计算无法进行

        alpha = (num_items / (num_items - 1)) * (1 - (variance_total.sum() / sum_covariance_matrix))
        return alpha

    # 计算KMO检验
    def calculate_kmo_value(data):
        kmo_per_variable, kmo_total = calculate_kmo(data)
        return kmo_per_variable, kmo_total

    # 计算信度和效度
    alpha_values = {}
    kmo_values = {}

    for group_name, group_data in data.items():
        try:
            alpha_values[group_name] = calculate_cronbach_alpha(group_data)
        except ZeroDivisionError:
            print(f"Error calculating Alpha for group: {group_name}")
            alpha_values[group_name] = "Error"

        kmo_values[group_name] = calculate_kmo_value(group_data)

    return alpha_values, kmo_values


# 计算信度和效度
alpha_values, kmo_values = calculate_alpha_and_kmo({
    'economic_support': economic_support,
    'care_support': care_support,
    'emotion_support': emotion_support,
    # 'total_score': total_score
})

# 输出结果
print("Cronbach's Alpha（信度）:")
for group_name, alpha_value in alpha_values.items():
    print(f"{group_name}: {alpha_value}")

print("\nKMO检验值（效度）:")
for group_name, kmo_value in kmo_values.items():
    print(f"{group_name}: {kmo_value}")
# 结果中的 array 表示每个变量（或题目）在因子分析中的相关性