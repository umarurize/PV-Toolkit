import os
import json
import numpy
from xlsxwriter import Workbook


def data_process(path: str):
    # Read config
    dir = os.getcwd()

    dir_1 = os.path.join(dir, 'configurations')
    if not os.path.exists(dir_1):
        os.mkdir(dir_1)

    dir_2 = os.path.join(dir_1, '319 - IV Helper')
    if not os.path.exists(dir_2):
        os.mkdir(dir_2)

    config_path = os.path.join(dir_2, 'config.json')

    if not os.path.exists(config_path):
        with open(config_path, 'w', encoding='utf-8') as f:
            config_data = {
                'low_to_high': 'reverse',
                'high_to_low': 'forward'
            }
            json_str = json.dumps(config_data, indent=4, ensure_ascii=False)
            f.write(json_str)
    else:
        with open(config_path, 'r', encoding='utf-8') as f:
            config_data = json.loads(f.read())

    path = path.replace('/', '\\')

    # Set the name for result workbook
    index = path.rfind('\\')
    result_workbook_name = path[index + 1:] + '.xlsx'
    result_workbook_path = os.path.join(path, result_workbook_name)

    # Create result workbook
    result_workbook = Workbook(result_workbook_path)

    # Add formats for result workbook
    result_workbook_format_1 = result_workbook.add_format(
    {
        'align': 'center'
    }
    )
    result_workbook_format_2 = result_workbook.add_format(
    {
        'align': 'center',
        'font_color': 'red',
        'bold': True
    }
    )

    # Initial result workbook
    # Write sheet headers for result workbook
    result_worksheet = result_workbook.add_worksheet('result')
    sheet_header_list = [
        'File name',
        'Device area (cm^2)',
        'Voc (V)',
        'Jsc (mA/cm^2)',
        'FF',
        'PCE (%)',
        'Mode',
    ]
    for i in range(len(sheet_header_list)):
        result_worksheet.write(0, i, sheet_header_list[i], result_workbook_format_2)

    # Data process
    totale_data = []
    file_list = os.listdir(path)

    for i, file in enumerate(file_list, start=1):
        single_data = [file.strip('.txt')]
        recorder = []

        file_path = os.path.join(path, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            # Get device area
            area = eval(lines[6].strip('Device area (cm^2) = ').strip('\n'))
            single_data.append(area)

            # Get all points data
            point_data = []
            for line in lines[10:]:
                content = line.strip('\n').split('\t')
                point_data.append(
                    [
                        eval(content[0]),
                        eval(content[1])
                    ]
                )

        # Calculate device parameters
        try:
            # Calculate Voc
            for data in point_data:
                next_point_index = point_data.index(data) + 1
                next_point = point_data[next_point_index]
                if numpy.sign(data[1]) == numpy.sign(next_point[1]):
                    continue
                else:
                    Voc = data[0] - data[1] * ((next_point[0] - data[0]) / (next_point[1] - data[1]))
                    recorder.append(Voc)
                    single_data.append(abs(round(Voc, 4)))
                    break

            # Calculate Jsc
            for data in point_data:
                next_point_index = point_data.index(data) + 1
                next_point = point_data[next_point_index]
                if numpy.sign(data[0]) == numpy.sign(next_point[0]):
                    continue
                else:
                    Jsc = data[1] - data[0] * ((next_point[1] - data[1]) / (next_point[0] - data[0]))
                    recorder.append(Jsc)
                    single_data.append(abs(round(Jsc, 4)))
                    break

            # Calculate P_max
            temple_list = []
            for data in point_data:
                if (numpy.sign(data[0]) == numpy.sign(recorder[0])
                        and
                        numpy.sign(data[1]) == numpy.sign(recorder[1])
                ):
                    temple_list.append(abs(data[0] * data[1]))
            P_max = max(temple_list)

            FF = P_max / abs(recorder[0] * recorder[1])
            recorder.append(FF)
            single_data.append(round(FF, 4))

            PCE = abs(recorder[0] * recorder[1] * recorder[2])
            single_data.append(round(PCE, 4))

            # Judge the sweep mode
            if point_data[0][0] < point_data[-1][-1]:
                direction = 'low_to_high'
            else:
                direction = 'high_to_low'
            mode = config_data[direction]
            single_data.append(mode)
        except ValueError:
            del single_data[1:]
            for i in range(6):
                single_data.append('Bad data')

        totale_data.append(single_data)

        # Return progress to UI
        progress = int((i / len(file_list)) * 100)
        data_to_send = [
            single_data[0],
            single_data[2],
            single_data[3],
            single_data[4],
            single_data[5]
        ]
        data_intime = [data_to_send, progress]
        yield data_intime

    # Write data to result workbook
    row_num = 1
    for data_to_write in totale_data:
        if row_num <= len(totale_data):
            for i in range(7):
                result_worksheet.write(row_num, i, data_to_write[i], result_workbook_format_1)
        row_num += 1

    result_workbook.close()


