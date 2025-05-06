import io
import os
import json

import numpy
from xlsxwriter import Workbook
import plotly.graph_objs as go
import plotly.io as pio


def curve_preview_three(path: str, device_area: str):
    # Read config
    dir = os.getcwd()
    config_path = os.path.join(dir, 'configurations', '319[1] - IV Helper', 'config.json')
    with open(config_path, 'r', encoding='utf-8') as f:
        config_data = json.loads(f.read())

    path = path.replace('/', '\\')

    device_area = eval(device_area)

    pre_Voc_list = []
    pre_Jsc_list = []

    point_data = []

    recorder = []

    index = path.rfind('\\')
    result = [path[index+1:], device_area]

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for line in lines[35:]:
            content = line.strip('\n').split(',')
            pre_Voc_list.append(eval(eval(content[2])))
            pre_Jsc_list.append(eval(eval(content[3])) * 1000 / device_area)
            point_data.append(
                [
                    eval(eval(content[2])),
                    eval(eval(content[3]))
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
                result.append(abs(round(Voc, 4)))
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
                result.append(abs(round(Jsc * 1000 / device_area, 4)))
                break

        # Calculate P_max
        temple_list = []
        for data in point_data:
            if (
                numpy.sign(data[0]) == numpy.sign(recorder[0])
                and
                numpy.sign(data[1]) == numpy.sign(recorder[1])
            ):
                temple_list.append(abs(data[0] * data[1] * 1000 / device_area))
        P_max = max(temple_list)

        FF = P_max / abs(recorder[0] * recorder[1] * 1000 / device_area)
        recorder.append(FF)
        result.append(round(FF * 100, 4))

        PCE = abs(recorder[0] * recorder[1] * recorder[2] * 1000 / device_area)
        result.append(round(PCE, 4))

        # Judge the sweep mode
        if point_data[0][0] < point_data[-1][0]:
            direction = 'low_to_high'
        else:
            direction = 'high_to_low'
        mode = config_data[direction]
        result.append(mode)
    except:
        del result[1:]
        result.append('Bad data')

    if len(result) == 2:
        pass
    else:
        if recorder[0] < 0:
            Voc_list = [-i for i in pre_Voc_list]
        else:
            Voc_list = pre_Voc_list
        if recorder[1] < 0:
            Jsc_list = [-i for i in pre_Jsc_list]
        else:
            Jsc_list = pre_Jsc_list

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=Voc_list,
                y=Jsc_list,
                mode='markers+lines',
                marker=dict(
                    size=9
                ),
                line=dict(
                    color='red'
                )
            )
        )

        fig.update_layout(
            annotations=[
                dict(
                    text='Powered by PV-Toolkit',
                    xref="paper",
                    yref="paper",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                    font=dict(
                        size=36,
                        color="rgba(128, 128, 128, 0.3)"
                    )
                )
            ],
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
                range=[0, max(Voc_list)]
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
                range=[0, max(Jsc_list) + 0.5]
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=45, r=45, t=45, b=45),
            showlegend=False
        )

        img_byte_arr = io.BytesIO()
        pio.write_image(fig, img_byte_arr, format='png')
        img_byte_arr.seek(0)
        result.append(img_byte_arr)

    return result


def type_converse_two(path: str, device_area: str):
    path = path.replace('/', '\\')

    device_area = eval(device_area)

    index = path.rfind('\\')
    workbook_name = path[index+1:].strip('.csv') + '.xlsx'
    workbook_path = os.path.join(path[0: index+1], workbook_name)

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

    worksheet = workbook.add_worksheet('curve')
    sheet_header_list = [
        'Voc',
        'Jsc'
    ]
    for i in range(len(sheet_header_list)):
        worksheet.write(0, i, sheet_header_list[i], workbook_format_2)

    raw_data = []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for line in lines[35:]:
            content = line.strip('\n').split(',')
            raw_data.append(
                [
                    eval(eval(content[2])),
                    eval(eval(content[3])) * 1000 / device_area
                ]
            )

    row_num = 1
    for data in raw_data:
        if row_num <= len(raw_data):
            for i in range(2):
                worksheet.write(row_num, i, data[i], workbook_format_1)
            row_num += 1

    workbook.close()













