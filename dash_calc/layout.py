from dash import html, dcc
import dash_bootstrap_components as dbc

from main import app
from data import data, operations
from figures import fig, line_fig


app.layout = html.Div(children=[
    dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(dcc.Slider(0, 9, 1, id='axis-slider', value=0)),
                dbc.Row(
                    [
                        dbc.Col(dcc.Graph(id='example-graph', figure=fig), width=6),
                        dbc.Col(dcc.Graph(id='line-graph', figure=line_fig), width=6)
                    ],
                    justify='evenly'
                ),
                dbc.Row(
                    [
                        dcc.Dropdown(data_keys:=[x for x in data['1'].keys()], value=data_keys,
                                     multi=True, id='data-variables')
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Dropdown(keys:=[x for x in data.keys()], value=['1'],
                                             multi=True, id='datasets'), width=4),
                        dbc.Col(dbc.Button('Generate Data', id='generate-button', type='text'), width=2),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Dropdown(operation_keys:=[x for x in operations.keys()],
                                             id='operation', value='add'), width=4),
                        dbc.Col(dbc.Button('add', id='operation-button',
                                           type='text'), width=2),
                    ]
                )
            ]
        ),
    )
])

