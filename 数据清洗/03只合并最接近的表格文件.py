import pandas as pd
import os

# 指定目录路径
directory = 'G:\\SARS-CoV-2\\rawdata\\2\\cleaned data\\合并2'

# 读取result_0.xlsx文件以获取其列名作为参考
reference_file = 'result_13.xlsx'
reference_path = os.path.join(directory, reference_file)
reference_df = pd.read_excel(reference_path)
reference_columns = set(reference_df.columns.tolist())

# 初始化合并的DataFrame，并包含参考文件的数据
merged_df = pd.DataFrame(reference_df)

# 用于存储合并和未合并的文件名
merged_files = [reference_file]  # 先添加参考文件
unmerged_files = []

# 列出所有以result_开头的Excel文件
files = [f for f in os.listdir(directory) if f.startswith('result_') and f.endswith('.xlsx')]

# 遍历文件列表，检查表头并合并数据
for file in files:
    if file == reference_file:  # 已经包含参考文件，跳过
        continue

    file_path = os.path.join(directory, file)
    df = pd.read_excel(file_path)
    file_columns = set(df.columns.tolist())

    # 检查列名是否包含result_0.xlsx的所有列名
    if reference_columns.issubset(file_columns):
        merged_files.append(file)
        merged_df = pd.concat([merged_df, df], ignore_index=True)
    else:
        unmerged_files.append(file)

# 如果有文件被合并，将合并后的数据保存到新的Excel文件
if merged_files:
    # 创建输出文件名，使用所有合并文件的名称的组合
    output_filename = ''.join(merged_files) + 'merge.xlsx'
    output_path = os.path.join(directory, output_filename)
    merged_df.to_excel(output_path, index=False)

    # 输出合并和未合并的文件信息
    print(f'Files have been merged and saved to {output_path}')
    print(f'Files merged: {len(merged_files)}')
    for file in merged_files:
        print(file)

    print(f'Files not merged: {len(unmerged_files)}')
    for file in unmerged_files:
        print(file)
else:
    print('No files were merged.')