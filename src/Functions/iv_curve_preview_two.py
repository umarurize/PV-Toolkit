import io
import os

import numpy
from xlsxwriter import Workbook
import plotly.graph_objs as go
import plotly.io as pio


def curve_preview_two(path: str, device_area: str) -> list:
    path = path.replace('/', '\\')

    device_area = eval(device_area)

    pre_Voc_list_reverse = []
    pre_Jsc_list_reverse = []
    point_data_reverse = []
    recorder_reverse = []

    pre_Voc_list_forward = []
    pre_Jsc_list_forward = []
    point_data_forward = []
    recorder_forward = []

    index = path.rfind('\\')
    result = [path[index + 1:], device_area]

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for line in lines[1:]:
            content = line.strip('\n').split('\t')
            if len(content[-1]) == 0:
                pre_Voc_list_reverse.append(eval(content[1]))
                pre_Jsc_list_reverse.append(eval(content[0]) * 1000 / device_area)
                point_data_reverse.append([eval(content[1]), eval(content[0])])
            else:
                pre_Voc_list_reverse.append(eval(content[1]))
                pre_Jsc_list_reverse.append(eval(content[0]) * 1000 / device_area)
                point_data_reverse.append([eval(content[1]), eval(content[0])])
                pre_Voc_list_forward.append(eval(content[4]))
                pre_Jsc_list_forward.append(eval(content[3]) * 1000 / device_area)
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
                result.append(abs(round(Voc_reverse, 4)))
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
                result.append(abs(round(Jsc_reverse * 1000 / device_area, 4)))
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
        result.append(round(FF_reverse * 100, 4))
        recorder_reverse.append(FF_reverse)

        PCE_reverse = abs(recorder_reverse[0] * recorder_reverse[1] * recorder_reverse[2] * 1000 / device_area)
        result.append(round(PCE_reverse, 4))

        # Forward
        # Calculate Voc_forward
        for data in point_data_forward:
            index = point_data_forward.index(data)
            next_point = point_data_forward[index + 1]
            if numpy.sign(data[1]) == numpy.sign(next_point[1]):
                continue
            else:
                Voc_forward = data[0] - data[1] * ((next_point[0] - data[0]) / (next_point[1] - data[1]))
                result.append(abs(round(Voc_forward, 4)))
                recorder_forward.append(Voc_forward)
                break

        # Calculate Jsc_forward
        point_a = point_data_forward[0]
        point_b = point_data_forward[1]
        k = (point_a[1] - point_b[1]) / (point_a[0] - point_a[1])
        Jsc_forward = point_a[1] - (point_a[0] * k)
        result.append(abs(round(Jsc_forward * 1000 / device_area, 4)))
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
        result.append(round(FF_forward * 100, 4))
        recorder_forward.append(FF_forward)

        PCE_forward = abs(recorder_forward[0] * recorder_forward[1] * recorder_forward[2] * 1000 / device_area)
        result.append(round(PCE_forward, 4))
    except:
        del result[1:]
        result.append('Bad data')

    if len(result) == 2:
        pass
    else:
        if recorder_reverse[0] < 0:
            Voc_list_reverse = [-i for i in pre_Voc_list_reverse]
        else:
            Voc_list_reverse = pre_Voc_list_reverse

        if recorder_reverse[1] < 0:
            Jsc_list_reverse = [-i for i in pre_Jsc_list_reverse]
        else:
            Jsc_list_reverse = pre_Jsc_list_reverse

        if recorder_forward[0] < 0:
            Voc_list_forward = [-i for i in pre_Voc_list_forward]
        else:
            Voc_list_forward = pre_Voc_list_forward

        if recorder_forward[1] < 0:
            Jsc_list_forward = [-i for i in pre_Jsc_list_forward]
        else:
            Jsc_list_forward = pre_Jsc_list_forward

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=Voc_list_reverse,
                y=Jsc_list_reverse,
                mode='markers+lines',
                marker=dict(
                    size=9
                ),
                line=dict(
                    color='red'
                )
            )
        )

        fig.add_trace(
            go.Scatter(
                x=Voc_list_forward,
                y=Jsc_list_forward,
                mode='markers+lines',
                marker=dict(
                    size=9
                ),
                line=dict(
                    color='blue'
                )
            )
        )

        fig.update_layout(
            xaxis=dict(
                gridcolor='black',
                linecolor='black',
                linewidth=3,
                zerolinecolor='black',
                mirror=True,
                tickfont=dict(
                    size=20,
                    weight='bold'
                ),
                range=[0, max(max(Voc_list_reverse), max(Voc_list_forward))]
            ),
            yaxis=dict(
                gridcolor='black',
                linecolor='black',
                linewidth=3,
                zerolinecolor='black',
                mirror=True,
                tickfont=dict(
                    size=20,
                    weight='bold'
                ),
                range=[0, max(max(Jsc_list_reverse), max(Jsc_list_forward)) + 0.5]
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=55, r=65, t=45, b=55),
            showlegend=False
        )

        img_byte_arr = io.BytesIO()
        pio.write_image(fig, img_byte_arr, format='png')
        img_byte_arr.seek(0)
        result.append(img_byte_arr)

    return result


def type_transfer(path: str, device_area: str):
    path = path.replace('/', '\\')

    device_area = eval(device_area)

    index = path.rfind('\\')
    workbook_name = path[index+1:].strip('.txt') + '.xlsx'
    workbook_path = os.path.join(path[0:index+1], workbook_name)

    workbook = Workbook(workbook_path)

    workbook_format_1 = workbook.add_format(
        {
            'align': 'center'
        }
    )
    workbook_format_2 = workbook.add_format(
        {
            'align': 'center',
            'font_color': 'red',
            'bold': True
        }
    )
    workbook_format_3 = workbook.add_format(
        {
            'align': 'center',
            'font_color': 'blue',
            'bold': True
        }
    )

    worksheet = workbook.add_worksheet('curve')
    sheet_header_list = [
        'Voc_1',
        'Jsc_1',
        'Voc_2',
        'Jsc_2'
    ]
    for i in range(len(sheet_header_list)):
        if i <= 1:
            worksheet.write(0, i, sheet_header_list[i], workbook_format_2)
        else:
            worksheet.write(0, i, sheet_header_list[i], workbook_format_3)

    raw_data = []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for line in lines[1:]:
            content = line.strip('\n').split('\t')

            if len(content[-1]) == 0:
                raw_data.append(
                    [
                        eval(content[1]),
                        eval(content[0]) * 1000 / device_area,
                        '',
                        ''
                    ]
                )
            else:
                raw_data.append(
                    [
                        eval(content[1]),
                        eval(content[0]) * 1000 / device_area,
                        eval(content[4]),
                        eval(content[3]) * 1000 / device_area
                    ]
                )

    row_num = 1
    for data in raw_data:
        if row_num <= len(raw_data):
            for i in range(4):
                worksheet.write(row_num, i, data[i], workbook_format_1)
            row_num += 1

    workbook.close()













