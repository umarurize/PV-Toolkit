import os
import sys
import time
import xlsxwriter as xw
from tqdm import tqdm
from openpyxl import load_workbook

time_start = time.process_time()

# 1.规划汇总数据文件名
path = input('请输入路径(将文件管理器中的路径复制过来即可):')
os.chdir(path)
first_folder = str(os.getcwd())
index = first_folder.rfind('\\')
result_name = first_folder[index+1 :] + '.xlsx'


# 2.创建汇总数据工作簿
workbook = xw.Workbook(result_name)
format = workbook.add_format({'align': 'center', 'font_color': 'red', 'bold': True})
format1 = workbook.add_format({'align': 'center'})

# 3.定义修正计算函数（修正 FF 和 PCE 参数）
def recalculate(temple_data):
    # 重新计算 FF
    temple_data.append(round(temple_data[5] / (temple_data[3] * temple_data[4]), 6))
    # 重新计算 PCE 并加入缓存列表
    temple_data.append(round(temple_data[3] * temple_data[4] * temple_data[6], 6))

# 4.读取并写入数据
folders_list = os.listdir() # 获取所有子文件夹
single_data = [] # 缓存单个文件数据
data = [] # 缓存单组所有文件数据
find_Voc = [] # 缓存正确 Voc
find_Jsc = [] # 缓存正确 Jsc
find_P_max = [] # 缓存正确 P_max

for i in folders_list:
    # 创建对应组名的工作表
    worksheet = workbook.add_worksheet(i)
    worksheet.set_column(0, 5, 15)
    worksheet.set_column(6, 7, 25)
    worksheet.write(0, 0, 'file name', format)
    worksheet.write(0, 1, 'Mode', format)
    worksheet.write(0, 2, 'Voc (V)', format)
    worksheet.write(0, 3, 'Jsc (mA/cm^2)', format)
    worksheet.write(0, 4, 'FF (%)', format)
    worksheet.write(0, 5, 'PCE (%)', format)
    worksheet.write(0, 6, 'Device area (cm^2)', format)
    worksheet.write(0, 7, 'Author: umaru', format)
    worksheet.write(1, 7, 'From', format)
    worksheet.write(2, 7, '1 kWh Group', format)
    worksheet.write(3, 7, 'Funsom - Soochow.U', format)
    os.chdir(i)
    files_list = os.listdir()
    for j in files_list:
        lines = 1
        file_to_read = open(j, 'rb') # 以二进制打开文件，方便后面的指针操作
        single_data.append(j)
        while True:
            if lines == 1:
                line = file_to_read.readline().decode("utf - 8")
                line = line.strip('\n\r')
                line = line.lstrip('Voc (V) = ')
                if_mode = float(line)
                if if_mode < 0:
                    single_data.append('Reverse')
                    lines += 1
                else:
                    single_data.append('Forward')
                    lines += 1
            elif lines == 7:
                line = file_to_read.readline().decode("utf - 8")
                line = line.strip('\r\n')
                line = line.strip('Device area (cm^2) = ')
                single_data.append(line)
                lines += 1
            elif lines == 8: # 识别空扫数据
                line = file_to_read.readline().decode("utf - 8")
                line = line.strip('\r\n')
                line = line.strip('Isd (A) = ')
                if float(line) == 0:
                    single_data = []
                    break
                else:
                    lines += 1
                    continue
            elif lines >= 11:
                line = file_to_read.readline().decode("utf - 8")
                line = line.strip('\r\n')
                index1 = line.rfind('\t')
                if_V = float(line[0:index1])
                if_I = float(line[index1 + 1:])
                if if_V < 0 and if_I > 0:
                    if_P_max = abs(if_V) * if_I
                    find_P_max.append(if_P_max)
                if single_data[1] == 'Reverse':
                    if find_Voc == []:
                        if float(line[index1+1:]) >= 0:
                            find_Voc.append(line)
                            back_cursor1 = len(line) * 2 + 5
                            file_to_read.seek(-back_cursor1, 1)
                            line = file_to_read.readline().decode("utf - 8")
                            line = line.strip('\r\n')
                            index2 = line.rfind('\t')
                            find_Voc.append(line)
                            correct_Voc = float(find_Voc[1][0:index2]) - float(find_Voc[1][index2+1:]) * ((float(find_Voc[0][0:index1]) - float(find_Voc[1][0:index2])) / (float(find_Voc[0][index1+1:]) - float(find_Voc[1][index2+1:])))
                            correct_Voc = abs(round(correct_Voc, 6))
                            single_data.append(correct_Voc)
                            lines += 1
                        else:
                            pass
                    if float(line[0:index1]) >= 0:
                        find_Jsc.append(line)
                        back_cursor2 = len(line) * 2 + 5
                        file_to_read.seek(-back_cursor2, 1)
                        line = file_to_read.readline().decode("utf - 8")
                        line = line.strip('\r\n')
                        index3 = line.rfind('\t')
                        find_Jsc.append(line)
                        correct_Jsc = float(find_Jsc[0][index1+1:]) - float(find_Jsc[0][0:index1]) * ((float(find_Jsc[1][index3+1:]) - float(find_Jsc[0][index1+1:])) / (float(find_Jsc[1][0:index3]) - float(find_Jsc[0][0:index1])))
                        correct_Jsc = abs(round(correct_Jsc, 6))
                        single_data.append(correct_Jsc)
                        single_data.append(max(find_P_max))
                        recalculate(single_data)
                        data.append(single_data)
                        single_data = []
                        find_Voc = []
                        find_Jsc = []
                        find_P_max = []
                        file_to_read.close()
                        break

                if single_data[1] == 'Forward':
                    if find_Jsc == []:
                        if float(line[0:index1]) <= 0:
                            find_Jsc.append(line)
                            back_cursor3 = len(line) * 2 + 3
                            file_to_read.seek(-back_cursor3, 1)
                            line = file_to_read.readline().decode("utf - 8")
                            line.strip('\r\n')
                            index4 = line.rfind('\t')
                            find_Jsc.append(line)
                            correct_Jsc = float(find_Jsc[0][index1+1:]) - float(find_Jsc[0][0:index1]) * ((float(find_Jsc[1][index4+1:]) - float(find_Jsc[0][index1+1:])) / (float(find_Jsc[1][0:index4]) - float(find_Jsc[0][0:index1])))
                            correct_Jsc = abs(round(correct_Jsc, 6))
                            single_data.append(correct_Jsc)
                            lines += 1
                        else:
                            pass
                    if float(line[index1+1:]) <= 0:
                        find_Voc.append(line)
                        back_cursor4 = len(line) * 2 + 3
                        file_to_read.seek(-back_cursor4, 1)
                        line = file_to_read.readline().decode("utf - 8")
                        line.strip('\r\n')
                        index5 = line.rfind('\t')
                        find_Voc.append(line)
                        correct_Voc = float(find_Voc[1][0:index5]) - float(find_Voc[1][index5+1:]) * ((float(find_Voc[0][0:index1]) - float(find_Voc[1][0:index5])) / (float(find_Voc[0][index1+1:]) - float(find_Voc[1][index5+1:])))
                        correct_Voc = abs(round(correct_Voc, 6))
                        single_data.append(correct_Voc)
                        single_data.append(max(find_P_max))
                        recalculate(single_data)
                        data.append(single_data)
                        single_data = []
                        find_Voc = []
                        find_Jsc = []
                        find_P_max = []
                        file_to_read.close()
                        break
                lines += 1
            else:
                line = file_to_read.readline()
                lines += 1
                continue

    data.sort(key=lambda x:x[7], reverse=True) # 根据 PCE 对 data 进行降序排列

    # 写入缓存数据至目标工作表
    n =1
    for m in data:
        if n <= len(data):
            # 写入文件名
            worksheet.write(n, 0, m[0], format1)
            # 写入扫描模式
            worksheet.write(n, 1, m[1], format1)
            if m[1] == 'Reverse':
                # 写入 Voc
                worksheet.write(n, 2, m[3], format1)
                # 写入 Jsc
                worksheet.write(n, 3, m[4], format1)
            else:
                # 写入 Jsc
                worksheet.write(n, 3, m[3], format1)
                # 写入 Voc
                worksheet.write(n, 2, m[4], format1)
            # 写入 FF
            worksheet.write(n, 4, m[6], format1)
            # 写入 PCE
            worksheet.write(n, 5, m[7], format1)
            # 写入有效面积
            worksheet.write(n, 6, m[2], format1)
            n += 1
    data = [] # 清空缓存
    os.chdir(first_folder)

workbook.close()

# 5.生成统计文件 -- 方便绘制统计图
target_workbook = load_workbook(result_name)

Statistical_Voc = []
Statistical_Jsc = []
Statistical_FF = []
Statistical_PCE = []
for sheet in target_workbook.worksheets:
    row_num = sheet.max_row
    Temple_Voc, Temple_Jsc, Temple_FF, Temple_PCE = [], [], [], []
    for row in range(2, row_num+2):
        if sheet.cell(row, 3).value != None:
            Temple_Voc.append(sheet.cell(row, 3).value)
            Temple_Jsc.append(sheet.cell(row, 4).value)
            Temple_FF.append(sheet.cell(row, 5).value)
            Temple_PCE.append(sheet.cell(row, 6).value)
        else:
            Statistical_Voc.append(Temple_Voc)
            Statistical_Jsc.append(Temple_Jsc)
            Statistical_FF.append(Temple_FF)
            Statistical_PCE.append(Temple_PCE)
            break

Statistical_workbook = xw.Workbook('Statistical data.xlsx')
format2 = Statistical_workbook.add_format({'align': 'center'})
Voc_sheet = Statistical_workbook.add_worksheet('Voc')
Jsc_sheet = Statistical_workbook.add_worksheet('Jsc')
FF_sheet = Statistical_workbook.add_worksheet('FF')
PCE_sheet = Statistical_workbook.add_worksheet('PCE')

def write_data(data_list, target_sheet):
    c_num = 0
    columns_num = len(data_list)
    target_sheet.set_column(0, columns_num-1, 15)
    for data in data_list:
        if c_num <= len(data_list)-1:
            r_num = 0
            for i in data:
                if r_num <= len(data)-1:
                    target_sheet.write(r_num, c_num, i, format2)
                    r_num += 1
            c_num += 1

write_data(Statistical_Voc, Voc_sheet)
write_data(Statistical_Jsc, Jsc_sheet)
write_data(Statistical_FF, FF_sheet)
write_data(Statistical_PCE, PCE_sheet)

Statistical_workbook.close()


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

