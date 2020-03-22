from plotly.subplots import make_subplots
import plotly.graph_objects as go


def display_experiment(dataframe, group_key=None, x_axis=None, y_axis=None, title=None):
    fig = make_subplots()

    grouped_metrics = dataframe.groupby(group_key)

    flag = True
    drop_down_list = []
    for idx, i in enumerate(grouped_metrics):
        fig.add_trace(go.Scatter(
            x=i[1][x_axis],
            y=i[1][y_axis],
            name=i[0],
            mode='markers',
            visible=flag
        )
        )
        flag = False
        visible = [False] * len(grouped_metrics)
        visible[idx] = True
        drop_down_list.append(
            dict(
                label=i[0],
                method="update",
                args=[
                    {
                        "visible": visible
                    }
                ]
            )
        )

    fig.update_layout(
        updatemenus=[
            dict(
                active=0,
                buttons=list(
                    drop_down_list
                )
            )
        ]
    )

    fig.update_layout(
        title=title,
        xaxis_title=x_axis,
        yaxis_title=y_axis,
        height=800
    )

    fig.show()
