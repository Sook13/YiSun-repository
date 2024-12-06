import pandas as pd
import os
import glob

# 定义要删除的列名
columns_to_drop = [
    '报送省份', '本土标本来源地区（地级市；区）', '监测地点（输入：入境口岸和入境日期；本土：XX医院门诊或急诊或住院）',
    '几代测序，测序仪型号', '覆盖度'
]

# 定义数据存放的文件夹路径
data_folder = 'G:\\SARS-CoV-2\\rawdata\\2'

# 加载模板文件的表头
template_file = os.path.join(data_folder, '202301.xlsx')
template_df = pd.read_excel(template_file, header=0)

# 获取模板表头
template_columns = template_df.columns.tolist()


# 定义一个函数来清洗数据
def clean_data(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path, header=0)

    # 删除指定的列
    df.drop(columns=columns_to_drop, errors='ignore', inplace=True)

    # 筛选出存在于数据框架中的模板列
    existing_columns = [col for col in template_columns if col in df.columns]

    # 重新排列列以匹配模板文件的表头
    df = df[existing_columns]

    # 保存清洗后的数据
    clean_file_path = os.path.join(data_folder, os.path.basename(file_path).replace('.xlsx', '_cleaned.xlsx'))
    df.to_excel(clean_file_path, index=False)
    print(f'Cleaned data saved to {clean_file_path}')


# 获取指定文件夹下所有的xlsx文件
xlsx_files = glob.glob(os.path.join(data_folder, '*.xlsx'))

# 遍历并清洗每个文件
for file in xlsx_files:
    if file != template_file:  # 排除模板文件本身
        clean_data(file)