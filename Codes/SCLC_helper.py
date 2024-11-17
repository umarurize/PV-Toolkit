import os
import sys
import time
import xlsxwriter as xw
from tqdm import tqdm

time_start = time.process_time()

# 1.规划汇总数据文件名
path = input('请输入路径(将文件管理器中的路径复制过来即可):')
os.chdir(path)
first_folder = str(os.getcwd())
index = first_folder.rfind('\\')
result_name = first_folder[index+1 :] + '.xlsx'

# 2.创建汇总数据工作簿
workbook = xw.Workbook(result_name)
format = workbook.add_format({'align': 'center'})



# 3.读取数据并汇总写入
points_data = []
all_points_data = []
folder_list = os.listdir()
for folder in folder_list:
    # 对应文件夹创建对应工作表
    worksheet = workbook.add_worksheet(folder)
    os.chdir(folder)
    file_list = os.listdir()
    for file in file_list:
        points_data.append(file)
        file_to_read = open(file, 'r', encoding='utf-8')
        file_content = file_to_read.readlines()
        for line in file_content:
            line = line.split(',')
            if line[0] == 'DataValue':
                if eval(line[1]) < 0:
                    points_data.append([eval(line[1]), abs(eval(line[2]))])
                else:
                    points_data.append([eval(line[1]), eval(line[2])])
        all_points_data.append(points_data)
        points_data = []

    column_num = 0
    for i in all_points_data:
        worksheet.write(0, column_num, i[0], format)
        row_num = 1
        worksheet.set_column(column_num, column_num+1, 25)
        for j in i[1:]:
            if row_num <= len(i[1:]):
                worksheet.write(row_num, column_num, j[0], format)
                worksheet.write(row_num, column_num + 1, j[1], format)
                row_num += 1
        column_num += 3
    all_points_data = []
    os.chdir(first_folder)

workbook.close()

time_end = time.process_time()
time_sum = round((time_end - time_start), 2)
counter = int(time_sum / 0.01)

for k in tqdm(range(counter)):
    time.sleep(0.01)

print('数据处理完毕...')

imported_modules_list = []
for m in sys.modules:
    imported_modules_list.append(m)

if 'menu' in imported_modules_list:
    del sys.modules['menu']
    import menu
else:
    import menu
