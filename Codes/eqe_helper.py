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
result_workbook = xw.Workbook(result_name)
format = result_workbook.add_format({'align': 'center', 'font_color': 'red', 'bold': True})
format1 = result_workbook.add_format({'align': 'center'})


# 3.Read every single txt data and rewrite them to summary Workbook
files_list = os.listdir()
Jsc_data = []
data = []

for i in files_list:
    worksheet = result_workbook.add_worksheet(i)
    worksheet.set_column(0, 3, 15)
    worksheet.write(0, 0, 'file name', format)
    worksheet.write(1, 0, i, format1)
    worksheet.write(0, 1, 'Lambda(nm)', format)
    worksheet.write(0, 2, 'EQE (%)', format)
    worksheet.write(0, 3, 'Jsc (mA/cm^2)', format)
    file_to_read = open(i, 'r')
    lines =1
    while True:
        if lines <= 5:
            line = file_to_read.readline()
            lines += 1
        else:
            line = file_to_read.readline()
            if line == '':
                Jsc_data = []
                break
            else:
                line = line.strip('\n')
                line = line.split('\t')
                Jsc_data.append(float(line[3]))
                line.pop(2)
                line.pop(2)
                line.pop(2)
                line.pop(2)
                Jsc_point = 0
                for j in Jsc_data:
                    Jsc_point += j
                line.append(Jsc_point)
                data.append(line)
                lines += 1

    n = 1
    for m in data:
        if n <= len(data):
            worksheet.write(n, 1, eval(m[0]), format1)
            worksheet.write(n, 2, eval(m[1]), format1)
            worksheet.write(n, 3, m[2], format1)
            n += 1
    data = []

result_workbook.close()

time_end = time.process_time()
time_sum = time_end - time_start
counter = int(time_sum / 0.01)

for k in tqdm(range(counter)):
    time.sleep(0.01)

print('数据处理完...')

imported_modules_list = []
for m in sys.modules:
    imported_modules_list.append(m)

if 'menu' in imported_modules_list:
    del sys.modules['menu']
    import menu
else:
    import menu


