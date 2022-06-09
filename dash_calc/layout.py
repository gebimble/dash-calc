from dash import html, dcc
import dash_bootstrap_components as dbc

from main import app
from data import data
from figures import fig, line_fig


app.layout = html.Div(children=[
    dcc.Loading(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dcc.Slider(0, 9, 1, id='axis-slider'),
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id='example-graph',
                            figure=fig
                        ),
                    ),
                    dbc.Col(
                        dcc.Graph(
                            id='line-graph',
                            figure=line_fig
                        ),
                    )
                ],
                justify='evenly'
            )
        ]
    ),

    file_list := dcc.Dropdown(keys:=[x for x in data.keys()], value=['0'],
                              multi=True, id='datasets'),
    html.Button('Generate Data', id='generate-button', type='text'),
    html.Button('Add', id='add-button', type='text'),
])

