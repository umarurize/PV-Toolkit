import io

import plotly.graph_objs as go
from plotly.subplots import make_subplots
import plotly.io as pio


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










