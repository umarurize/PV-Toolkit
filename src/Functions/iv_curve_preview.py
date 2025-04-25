import io
import os
import json
import numpy
import plotly.graph_objs as go
import plotly.io as pio


def curve_preview(path: str):
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

    pre_Voc_list = []
    pre_Jsc_list = []

    point_data = []

    recorder = []

    index = path.rfind('\\')
    result = [path[index + 1:]]

    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        # Get device area
        area = eval(lines[6].strip('Device area (cm^2) = ').strip('\n'))
        result.append(area)

        for line in lines[10:]:
            content = line.strip('\n').split('\t')
            pre_Voc_list.append(eval(content[0]))
            pre_Jsc_list.append(eval(content[1]))
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
                result.append(abs(round(Jsc, 4)))
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
        result.append(round(FF, 4))

        PCE = abs(recorder[0] * recorder[1] * recorder[2])
        result.append(round(PCE, 4))

        # Judge the sweep mode
        if point_data[0][0] < point_data[-1][-1]:
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
                zerolinecolor = 'black',
                mirror=True,
                tickfont=dict(
                    size=20,
                    weight='bold'
                ),
                range=[0, max(Jsc_list) + 0.5]
            ),
            plot_bgcolor='white',
            paper_bgcolor='white',
            margin=dict(l=55, r=65, t=45, b=55)
        )

        img_byte_arr = io.BytesIO()
        pio.write_image(fig, img_byte_arr, format='png')
        img_byte_arr.seek(0)
        result.append(img_byte_arr)

    return result
