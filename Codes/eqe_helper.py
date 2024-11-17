import os
import sys
import time
from tqdm import tqdm
import xlsxwriter as xw


time_start = time.process_time()

# 1.Plan Summary Data File Name
path = input('请输入路径(将文件管理器中的路径复制过来即可):')
os.chdir(path)
first_folder = str(os.getcwd())
index = first_folder.rfind('\\')
result_name = first_folder[index+1 :] + '.xlsx'


# 2.Create Summary Data Workbook
workbook = xw.Workbook(result_name)
format = workbook.add_format({'align': 'center', 'font_color': 'red', 'bold': True})
format1 = workbook.add_format({'align': 'center'})


# 3.处理数据并写人
second_folder_list = os.listdir() # 获取所有子文件夹
integrated_Jsc_data = []
for second_folder in second_folder_list: # 遍历所有子文件夹
    os.chdir(second_folder) # 切换至对应子文件夹
    worksheet = workbook.add_worksheet(second_folder) # 根据子文件夹的名字创建表单
    file_list = os.listdir() # 遍历对应子文件夹下的所有文件
    worksheet.set_column(0, len(file_list) * 4 - 1, 15) # 计算表单总列数并设置宽度
    start_column_num = 0 # 设置第一个文件写入的起始列数为 0
    single_integrated_Jsc_data = []
    single_integrated_Jsc_data.append(second_folder)
    for file in file_list: # 遍历对应夹下的所有子文件
        file_to_read = open(file, 'r')
        data = [['file_name', 'Lambda (nm)', 'EQE (%)', 'Jsc (mA/cm^2)']] # 预设表头
        Temple_list = [] # 缓存微分值，方便积分
        lines = 1
        while True:
            if lines <= 5: # 前五行读取完就挪到下一行，不操作
                line = file_to_read.readline()
                lines += 1
            else:
                row_data = []
                line = file_to_read.readline()
                if line == '':
                    break
                else:
                    if lines == 6: # 第六行额外存储文件名
                        row_data.append(file)
                    else:
                        row_data.append('') # 存储空数据，方便后面数据写入时对其
                    line = line.strip('\n').split('\t')
                    row_data.append(eval(line[0]))
                    row_data.append(eval(line[1]))
                    Temple_list.append(eval(line[3]))
                    row_data.append(sum(Temple_list)) # 对电流进行积分
                    data.append(row_data)
                    lines += 1

        # 获取最终积分电流值方便统计
        single_integrated_Jsc_data.append(data[-1][-1])

        # 写入数据
        row_num = 0
        for single_data in data:
            for column_num in range(start_column_num, start_column_num + 4):
                if row_num == 0:
                    worksheet.write(row_num, column_num, single_data[0], format)
                    single_data.pop(0)
                else:
                    worksheet.write(row_num, column_num, single_data[0], format1)
                    single_data.pop(0)
            row_num += 1
        start_column_num += 4
    integrated_Jsc_data.append(single_integrated_Jsc_data)
    os.chdir(first_folder)

# 4.将统计好的积分电流写入一个新的表单
worksheet1 = workbook.add_worksheet('Statistical_Jsc_data')
worksheet1.set_column(0, len(integrated_Jsc_data) - 1, 15)
c = 0
for i in integrated_Jsc_data:
    for r in range(0, len(i)):
        worksheet1.write(r, c, i[r], format1)
    c += 1

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

imported_modules_list = []
for m in sys.modules:
    imported_modules_list.append(m)

if 'menu' in imported_modules_list:
    del sys.modules['menu']
    import menu
else:
    import menu