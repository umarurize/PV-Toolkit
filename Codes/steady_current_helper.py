# 导入操作模块
import os
import xlsxwriter as xw
import time
from tqdm import tqdm

# 1.用户自定义电池有效面积
while True:
    device_area = input('请输入电池的有效面积(小数或整数):')
    try:
        if type(eval(device_area)) == int or type(eval(device_area)) == float:
            confirm_flag = input(f'你输入的有效面结是{device_area}, 输入1确认有效面积，按任意键重新输入:')
            if confirm_flag == '1':
                print('有效面积确认成功...')
                break
    except:
        print('输入无效，不是小数或整数...')

time_start = time.process_time()

# 2.规划汇总数据文件名
path = input ('请输入路径(将文件管理器中的路径复制过来即可):')
os.chdir(path)
first_folder = str(os.getcwd())
index = first_folder.rfind('\\')
result_name = first_folder[index+1 :] + '.xlsx'

# 3.创建汇总数据工作簿
workbook = xw.Workbook(result_name)
format = workbook.add_format({'align': 'center', 'font_color': 'red', 'bold': True})
format1 = workbook.add_format({'align': 'center'})

# 4.读取数据并统计电流众数
folders_list = os.listdir() # 获取文件下所有子文件
for folder in folders_list:
    if folder == 'current-helper-alpha-240830.py' or folder == 'current-helper-alpha-240830.exe':
        pass
    else:
        worksheet = workbook.add_worksheet(folder)
        worksheet.set_column(0, 5, 15)
        worksheet.write(0, 0, 'file name', format)
        worksheet.write(0, 1, 'Isc (A)', format)
        os.chdir(folder)
        files_list = os.listdir()
        data_to_write =[]
        for file in files_list:
            current_data = []  # 存储所有电流值
            single_data_to_write = []
            file_to_read = open(file, 'r')
            single_data_to_write.append(file)
            lines = 1
            while True:
                if 1 <= lines <= 2:
                    line = file_to_read.readline()
                    lines += 1
                    continue
                else:
                    line = file_to_read.readline()
                    if line == '':
                        break
                    else:
                        line = line.strip('\n').split('\t')
                        current_data.append(eval(line[1]))
                        lines += 1

            # 4.1 将电流保留5位小数，寻找电流众数
            d = {}
            for i in current_data:
                d[round(i, 5)] = d.get(round(i, 5), 0) + 1
            Temple_list = list(d.items())
            Temple_list.sort(key=lambda x:x[1], reverse=True)
            model_current = Temple_list[0][0]

            # 4.2 计算最终稳态电流值
            final_current_data = []
            for j in current_data:
                if round(j, 5) == model_current:
                    final_current_data.append(j)
                else:
                    continue
            correct_current_data = round((sum(final_current_data) / len(final_current_data)) / eval(device_area) * 1000, 6)
            single_data_to_write.append(correct_current_data)
            data_to_write.append(single_data_to_write)

        # 4.3 将文件名和相应稳态电流值写入目标工作表
        n = 1
        for m in data_to_write:
            if n <= len(data_to_write):
                # 写入文件名
                worksheet.write(n, 0, m[0], format1)
                # 写入稳态电流值
                worksheet.write(n, 1, m[1], format1)
                n += 1
        os.chdir(first_folder)

workbook.close()

time_end = time.process_time()
time_sum = round((time_end - time_start), 2)
counter = int(time_sum / 0.01)

for k in tqdm(range(counter)):
    time.sleep(0.01)

print('数据处理完毕...')
import menu
