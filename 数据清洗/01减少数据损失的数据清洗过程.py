import pandas as pd
import os
import glob

# 定义要删除的列名
columns_to_drop = [
    '报送省份', '报送日期','样本来源（输入：来源国；本土：省份和地市信息）', '监测地点(输入；入境口岸/入境日期；本土：就诊或住院医院名称)',
    '几代测序，测序仪型号', '覆盖度','发病日期(年/月/日)','就诊日期(年/月/日)','捕获试剂盒厂家及货号','报送\n省份','报送市区','报送\n日期','是否是有效序列','是否重症','是否死亡'
]

# 定义数据存放的文件夹路径
data_folder = 'G:\\SARS-CoV-2\\rawdata\\2'

# 获取指定文件夹下所有的xlsx文件
xlsx_files = glob.glob(os.path.join(data_folder, '*.xlsx'))


# 定义一个函数来清洗数据
def clean_data(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path, header=0)

    # 删除指定的列
    df.drop(columns=[col for col in columns_to_drop if col in df.columns], inplace=True, errors='ignore')

    # 保存清洗后的数据
    clean_file_path = os.path.join(data_folder, os.path.basename(file_path).replace('.xlsx', '_cleaned.xlsx'))
    df.to_excel(clean_file_path, index=False)
    print(f'Cleaned data saved to {clean_file_path}')


# 遍历并清洗每个文件
for file in xlsx_files:
    clean_data(file)