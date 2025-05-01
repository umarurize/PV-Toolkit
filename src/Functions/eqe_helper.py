import io
import os.path

import plotly.graph_objs as go
import plotly.io as pio
from plotly.subplots import make_subplots
from xlsxwriter import Workbook


def curve_preview_four(path: str):

    path = path.replace('/', '\\')

    Lambda_list = []
    EQE_list = []
    raw_Jsc_list = []
    Jsc_list = []

    index = path.rfind('\\')
    result = [path[index+1:]]

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for line in lines[5:]:
            content = line.strip('\n').split('\t')

            Lambda_list.append(eval(content[0]))

            EQE_list.append(eval(content[1]))

            raw_Jsc_list.append(eval(content[3]))
            Jsc_list.append(sum(raw_Jsc_list))

        result.append(round(Jsc_list[-1], 4))

        fig = make_subplots(specs=[[{'secondary_y': True}]])
        fig.add_trace(
            go.Scatter(
                x = Lambda_list,
                y = EQE_list,
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
                x=Lambda_list,
                y=Jsc_list,
                line=dict(
                    color='red'
                )
            ),
            secondary_y=True
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
                range=[min(Lambda_list), max(Lambda_list)]
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
                range=[min(EQE_list), 100],
                showgrid=False
            ),
            yaxis2=dict(
                gridcolor='black',
                linecolor='black',
                linewidth=3,
                zerolinecolor='black',
                mirror=True,
                tickfont=dict(
                    size=20,
                    weight='bold'
                ),
                range=[min(Jsc_list), max(Jsc_list) + 0.5],
                showgrid=False
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

def type_transfer_three(path: str) -> None:
    path = path.replace('/', '\\')

    index = path.rfind('\\')
    workbook_name = path[index+1:].strip('.txt') + '.xlsx'
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

    worksheet = workbook.add_worksheet('data')
    sheet_header_list = [
        'Lambda (nm)',
        'EQE (%)',
        'Jsc (mA/cm^2)'
    ]
    for i in range(len(sheet_header_list)):
        worksheet.write(0, i, sheet_header_list[i], workbook_format_2)

    raw_data = []
    raw_Jsc_data = []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for line in lines[5:]:
            content = line.strip('\n').split('\t')

            raw_Jsc_data.append(eval(content[3]))

            raw_data.append(
                [
                    eval(content[0]), # Lambda
                    eval(content[1]), # EQE
                    sum(raw_Jsc_data) # Cal.Jsc
                ]
            )

    row_num = 1
    for data in raw_data:
        if row_num <= len(raw_data):
            for i in range(3):
                worksheet.write(row_num, i, data[i], workbook_format_1)
            row_num += 1

    workbook.close()
