import pandas as pd

# 创建一个示例数据帧
def mather():

    df = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
                       'B': ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
                       'C': [1, 2, 3, 4, 5, 6, 7, 8],
                       'D': [10, 20, 30, 40, 50, 60, 70, 80]})

    # 根据列'A'和列'B'进行分组
    grouped = df.groupby(['A', 'B'])

    # 对分组后的数据应用聚合函数
    result = grouped.agg({'C': min, 'D': sum})

    # 打印合并单元格后的结果
    print(grouped)


if __name__ == "__main__":
    mather()

