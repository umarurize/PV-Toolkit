import os
import numpy
from xlsxwriter import Workbook


def data_process_two(path: str, device_area: str):
    path = path.replace('/', '\\')

    device_area = eval(device_area)

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
    result_workbook_format_3 = result_workbook.add_format(
        {
            'align': 'center',
            'font_color': 'blue',
            'bold': True
        }
    )

    # Initial result workbook
    # Write sheet headers for result workbook
    result_worksheet = result_workbook.add_worksheet('result')
    sheet_header_list = [
        'File name',
        'Device area (cm^2)',
        'Voc_1 (V)',
        'Jsc_1 (mA/cm^2)',
        'FF_1',
        'PCE_1 (%)',
        'Voc_2 (V)',
        'Jsc_2 (mA/cm^2)',
        'FF_2',
        'PCE_2 (%)'
    ]
    for i in range(len(sheet_header_list)):
        if i <= 5:
            result_worksheet.write(0, i, sheet_header_list[i], result_workbook_format_2)
        else:
            result_worksheet.write(0, i, sheet_header_list[i], result_workbook_format_3)

    # Data process
    total_data = []
    file_list = os.listdir(path)

    for i, file in enumerate(file_list, start=1):
        single_data = [file.strip('.txt'), device_area]

        point_data_reverse = []
        recorder_reverse = []

        point_data_forward = []
        recorder_forward = []

        file_path = os.path.join(path, file)
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

            # Get all points data
            for line in lines[1:]:
                content = line.strip('\n').split('\t')
                if len(content[-1]) == 0:
                    point_data_reverse.append([eval(content[1]), eval(content[0])])
                else:
                    point_data_reverse.append([eval(content[1]), eval(content[0])])
                    point_data_forward.append([eval(content[4]), eval(content[3])])

        # Calculate parameters (reverse and forward)
        try:
            # Reverse
            # Calculate Voc_reverse
            for data in point_data_reverse:
                index = point_data_reverse.index(data)
                next_point = point_data_reverse[index + 1]
                if numpy.sign(data[1]) == numpy.sign(next_point[1]):
                    continue
                else:
                    Voc_reverse = data[0] - data[1] * ((next_point[0] - data[0]) / (next_point[1] - data[1]))
                    single_data.append(abs(round(Voc_reverse, 4)))
                    recorder_reverse.append(Voc_reverse)
                    break

            # Calculate Jsc_reverse
            for data in point_data_reverse:
                index = point_data_reverse.index(data)
                next_point = point_data_reverse[index + 1]
                if numpy.sign(data[0]) == numpy.sign(next_point[0]):
                    continue
                else:
                    Jsc_reverse = data[1] - data[0] * ((next_point[1] - data[1]) / (next_point[0] - data[0]))
                    single_data.append(abs(round(Jsc_reverse * 1000 / device_area, 4)))
                    recorder_reverse.append(Jsc_reverse)
                    break

            # Calculate P_max reverse
            temple_list_reverse = []
            for data in point_data_reverse:
                if (
                    numpy.sign(data[0]) == numpy.sign(recorder_reverse[0])
                    and
                    numpy.sign(data[1]) == numpy.sign(recorder_reverse[1])
                ):
                    temple_list_reverse.append(abs(data[0] * data[1] * 1000 / device_area))

            P_max_reverse = max(temple_list_reverse)

            FF_reverse = P_max_reverse / abs(recorder_reverse[0] * recorder_reverse[1] * 1000 / device_area)
            single_data.append(round(FF_reverse, 4))
            recorder_reverse.append(FF_reverse)

            PCE_reverse = abs(recorder_reverse[0] * recorder_reverse[1] * recorder_reverse[2] * 1000 / device_area)
            single_data.append(round(PCE_reverse, 4))

            # Forward
            # Calculate Voc_forward
            for data in point_data_forward:
                index = point_data_forward.index(data)
                next_point = point_data_forward[index + 1]
                if numpy.sign(data[1]) == numpy.sign(next_point[1]):
                    continue
                else:
                    Voc_forward = data[0] - data[1] * ((next_point[0] - data[0]) / (next_point[1] - data[1]))
                    single_data.append(abs(round(Voc_forward, 4)))
                    recorder_forward.append(Voc_forward)
                    break

            # Calculate Jsc_forward
            point_a = point_data_forward[0]
            point_b = point_data_forward[1]
            k = (point_a[1] - point_b[1]) / (point_a[0] - point_a[1])
            Jsc_forward = point_a[1] - (point_a[0] * k)
            single_data.append(abs(round(Jsc_forward * 1000 / device_area, 4)))
            recorder_forward.append(Jsc_forward)

            # Calculate P_max forward
            temple_list_forward = []
            for data in point_data_forward:
                if (
                    numpy.sign(data[0]) == numpy.sign(recorder_forward[0])
                    and
                    numpy.sign(data[1]) == numpy.sign(recorder_forward[1])
                ):
                    temple_list_forward.append(abs(data[0] * data[1] * 1000 / device_area))

            P_max_forward = max(temple_list_forward)

            FF_forward = P_max_forward / abs(recorder_forward[0] * recorder_forward[1] * 1000 / device_area)
            single_data.append(round(FF_forward, 4))
            recorder_forward.append(FF_forward)

            PCE_forward = abs(recorder_forward[0] * recorder_forward[1] * recorder_forward[2] * 1000 / device_area)
            single_data.append(round(PCE_forward, 4))
        except:
            del single_data[1:]
            for i in range(9):
                single_data.append('Bad data')

        total_data.append(single_data)

        # Return progress to UI
        progress = int((i / len(file_list)) * 100)
        data_to_send = [
            single_data[0],  # File name
            single_data[2],  # Voc_1
            single_data[3],  # Jsc_1
            single_data[4],  # FF_1
            single_data[5],  # PCE_1
            single_data[6],  # Voc_2
            single_data[7],  # Voc_2
            single_data[8],  # FF_2
            single_data[9]  # FF_2
        ]
        data_intime = [data_to_send, progress]
        yield data_intime

    # Write data to result workbook
    row_num = 1
    for data_to_write in total_data:
        if row_num <= len(total_data):
            for i in range(6):
                result_worksheet.write(row_num, i, data_to_write[i], result_workbook_format_1)
            for i in range(6, 10):
                result_worksheet.write(row_num, i, data_to_write[i], result_workbook_format_1)
        row_num += 1

    result_workbook.close()

















