import random
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import plotly.figure_factory as ff #requires numpy

external_stylesheets = [
    {
        "href": "https://fonts.googleapis.com/css2?"
        "family=Lato:wght@400;700&display=swap",
        "rel": "stylesheet",
    },
    dbc.themes.BOOTSTRAP
]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Avocado Analytics: Understand Your Avocados!"

progress = html.Div(
    [
        dcc.Interval(id="progress-interval", n_intervals=0, interval=500),
        dbc.Progress(id="progress"),
    ]
)

@app.callback(
    [Output("progress", "value"), Output("progress", "children")],
    [Input("progress-interval", "n_intervals")],
)
def update_progress(n):
    # check progress of some background process, in this example we'll just
    # use n_intervals constrained to be in 0-100
    progress = min(n % 110, 100)
    # only add text after 5% progress to ensure text isn't squashed too much
    return progress, f"{progress} %" if progress >= 5 else ""

heatmap = go.Figure(data=go.Heatmap(
                   z=[[1, None, 30, 50, 1], [20, 1, 60, 80, 30], [30, 60, 1, -10, 20]],
                   x=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                   y=['Morning', 'Afternoon', 'Evening'],
                   hoverongaps = False))


z = [[.1, .3, .5, .7],
     [1.0, .8, .6, .4],
     [.6, .4, .2, 0.0],
     [.9, .7, .5, .3]]
x = ['a', 'b', 'c', 'd']
y = ['a', 'b', 'c', 'd']

colorscale = [[0, 'navy'], [1, 'plum']]
font_colors = ['white', 'black']
conf_matrix = ff.create_annotated_heatmap(z, x=x, y=y, colorscale=colorscale, font_colors=font_colors)


months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
          'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

bars = go.Figure()
bars.add_trace(go.Bar(
    x=months,
    y=[20, 14, 25, 16, 18, 22, 19, 15, 12, 16, 14, 17],
    name='Primary Product',
    marker_color='indianred'
))
bars.add_trace(go.Bar(
    x=months,
    y=[19, 14, 22, 14, 16, 19, 15, 14, 10, 12, 12, 16],
    name='Secondary Product',
    marker_color='lightsalmon'
))
bars.update_traces(texttemplate='%{text:.2s}', textposition='outside')
# Here we modify the tickangle of the xaxis, resulting in rotated labels.
bars.update_layout(barmode='group', xaxis_tickangle=-45)

minibars = go.Figure(go.Bar(
            x=[20, 14, 23],
            y=['giraffes', 'orangutans', 'monkeys'],
            orientation='h',
            text=['a', 'b', 'c'],
            textposition='auto'))
minibars.update_traces(marker_color='rgb(158,202,225)', marker_line_color='rgb(8,48,107)',
                  marker_line_width=1.5, opacity=0.6)

app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.P(children="🥑", className="header-emoji"),
                html.H1(
                    children="Avocado Analytics", className="header-title"
                ),
                html.P(
                    children="Analyze the behavior of avocado prices"
                    " and the number of avocados sold in the US"
                    " between 2015 and 2018",
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Region", className="menu-title"),
                        dcc.Dropdown(
                            id="region-filter",
                            options=[
                                {"label": region, "value": region}
                                for region in ["Madrid", "Barcelona", "Valencia"]
                            ],
                            value="Madrid",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
                html.Div(
                    children=[
                        html.Div(children="Type", className="menu-title"),
                        dcc.Dropdown(
                            id="type-filter",
                            options=[
                                {"label": avocado_type, "value": avocado_type}
                                for avocado_type in ["Big", "Medium", "Small"]
                            ],
                            value="Big",
                            clearable=False,
                            searchable=False,
                            className="dropdown",
                        ),
                    ],
                ),
            ],
            className="menu",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            children=dcc.Graph(
                                id="price-chart",
                                config={"displayModeBar": False},
                            ),
                            className="card",
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            children=dcc.Graph(
                                id="volume-chart",
                                config={"displayModeBar": False},
                            ),
                            className="card",
                        ),
                    )
                ],
            ),
            className="wrapper",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            children= dcc.Graph(
                                id="heatmap",
                                figure=heatmap,
                                config={"displayModeBar": False},
                            ),
                            className="card",
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            children= dcc.Graph(
                                id="hitmap",
                                figure={
                                    'data': [{
                                        'z': [[1.0, 0.3], [0.2, 0.9]],
                                        'y': ['True', 'False'],
                                        'x': ['True', 'False'],
                                        'ygap': 2,
                                        'reversescale': 'true',
                                        'colorscale': [[0, 'white'], [1, 'blue']],
                                        'type': 'heatmap',
                                    }],
                                    'layout': {
                                        #'height': 350,
                                        #'width': 350,
                                        'xaxis': {'side':'top'},
                                        'margin': {
                                            'l': 100,
                                            'r': 100,
                                            'b': 150,
                                            't': 100
                                        }
                                    }
                                }
                            ),
                            className="card",
                        ),
                    )
                ],
            ),
            className="wrapper",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            children=dcc.Graph(
                                id="confusion-matrix",
                                figure=conf_matrix
                            ),
                            className="card",
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            children=dcc.Graph(
                                id="bars",
                                figure=bars
                            ),
                            className="card",
                        ),
                    )
                ],
            ),
            className="wrapper",
        ),
        html.Div(
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            dcc.Textarea(
                                id='textarea-example',
                                value='Here some text',
                                style={'width': '100%', 'height': 300},
                            ),
                            className="card",
                        ),
                    ),
                    dbc.Col(
                        html.Div(
                            children=dcc.Graph(
                                id="minibars",
                                figure=minibars
                            ),
                            className="card",
                        ),
                    )
                ],
            ),
            className="wrapper",
        ),
        html.Div(
            progress
        ),
    ]
)



@app.callback(
    [Output("price-chart", "figure"), Output("volume-chart", "figure")],
    [
        Input("region-filter", "value"),
        Input("type-filter", "value"),
    ],
)
def update_charts(region, avocado_type):

    price_chart_figure = {
        "data": [
            {
                "x": [1,2,3,4,5,6,7,8,9,10],
                "y": [1,2,3,2,1,2,3,2,1,2],
                "type": "lines",
                "hovertemplate": "$%{y:.2f}<extra></extra>",
            },
        ],
        "layout": {
            "title": {
                "text": "Average Price of Avocados",
                "x": 0.05,
                "xanchor": "left",
            },
            "xaxis": {"fixedrange": True},
            "yaxis": {"tickprefix": "$", "fixedrange": True},
            "colorway": ["#17B897"],
        },
    }

    volume_chart_figure = {
        "data": [
            {
                "x": [1,2,3,4,5,6,7,8,9,10],
                "y": [1,2,3,2,1,2,3,2,1,2],
                "type": "lines",
            },
        ],
        "layout": {
            "title": {"text": "Avocados Sold", "x": 0.05, "xanchor": "left"},
            "xaxis": {"fixedrange": True},
            "yaxis": {"fixedrange": True},
            "colorway": ["#E12D39"],
        },
    }
    return price_chart_figure, volume_chart_figure


if __name__ == "__main__":
    app.run_server(debug=True)