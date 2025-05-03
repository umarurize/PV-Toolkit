import io

import numpy

import plotly.graph_objs as go
import plotly.io as pio


def curve_preview_five(path: str, device_area: str):
    path = path.replace('/', '\\')

    device_area = eval(device_area)

    index = path.rfind('\\')
    result = [path[index+1:], device_area]

    point_data = []
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

        for line in lines[2:]:
            content = line.strip('\n').split('\t')

            point_data.append(
                [
                    eval(content[0]),
                    eval(content[1]) * 1000 / device_area
                ]
            )

    time_list = [data[0] for data in point_data]
    Jsc_list = [data[1] for data in point_data]

    # Experimental function
    x = numpy.array(time_list[20:])
    y = numpy.array(Jsc_list[20:])

    A = numpy.vstack([x, numpy.ones(len(x))]).T
    k, c = numpy.linalg.lstsq(A, y, rcond=None)[0]

    result.append(round(c, 4))

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=time_list,
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
            range=[min(time_list), max(time_list)]
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
            range=[min(Jsc_list), max(Jsc_list) + 0.5]
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









