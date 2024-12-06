import pandas as pd
import os
from glob import glob

# 定义数据存放的文件夹路径
data_folder = 'G:\\SARS-CoV-2\\rawdata\\2\\cleaned data'

# 获取指定文件夹下所有的xlsx文件
xlsx_files = glob(os.path.join(data_folder, '*.xlsx'))

# 读取每个文件并确定其表头
headers = {}
for file in xlsx_files:
    df = pd.read_excel(file)
    header = tuple(df.columns.tolist())  # 将列名元组化，以便作为字典键
    if header in headers:
        headers[header]['files'].append(file)
        headers[header]['data'].append(df)
    else:
        headers[header] = {'files': [file], 'data': [df]}

# 根据表头种类合并数据
for header, content in headers.items():
    # 合并具有相同表头的所有数据
    merged_data = pd.concat(content['data'], ignore_index=True)
    # 生成文件名，如 result_0.xlsx, result_1.xlsx, ...
    file_name = f"result_{list(headers.keys()).index(header)}.xlsx"
    # 保存合并后的数据到新文件
    merged_data.to_excel(os.path.join(data_folder, file_name), index=False)
    print(f"Merged data saved to {file_name}")