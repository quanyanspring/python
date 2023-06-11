import pandas as pd

# 创建一个包含数据的DataFrame
data = {'Name': ['John', 'Jane', 'Sam'],
        'Age': [25, 30, 28],
        'City': ['New York', 'London', 'Paris']}
df = pd.DataFrame(data)

# 创建一个样式对象
style = df.style

# 合并单元格
style.set_properties(subset=['Name'], **{'text-align': 'center', 'font-weight': 'bold'})
style.set_properties(subset=['Age', 'City'], **{'font-weight': 'bold'})
style.set_table_styles([{'selector': '.row_heading', 'props': [('display', 'none')]}])
style.set_table_attributes('border="1"')

# 显示合并后的DataFrame
styled_df = style.render()
print(styled_df)
