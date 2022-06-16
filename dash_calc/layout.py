from itertools import combinations

from dash import html, dcc
import dash_bootstrap_components as dbc

from main import app
from data import data, operations
from figures import fig, line_fig


app.layout = html.Div(children=[
    dbc.Card(
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Graph(
                                id='example-graph', figure=fig,
                                config={
                                    'modeBarButtonsToAdd': ['select2d']
                                }
                            ),
                            width=6
                        ),
                        dbc.Col(dcc.Graph(id='line-graph', figure=line_fig), width=6)
                    ],
                    justify='evenly'
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(children=[], id='axis-sliders-container')
                            ],
                            width=6
                        ),
                        dbc.Col(
                            [
                                dbc.Col(
                                    dcc.Dropdown(
                                        coords:=[', '.join(x) for x in combinations([x for x in data['1'].coords.keys()], 2)],
                                        value=coords[0],
                                        id='coords',
                                        placeholder='Select a set of coordinates...'
                                    )
                                ),
                            ],
                            width=6
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Row(
                                    [
                                        dbc.Col(dcc.Dropdown(keys:=[x for x in data.keys()], value=['1'],
                                                             multi=True,
                                                             id='datasets',
                                                             placeholder='Select a dataset...')),
                                    ]
                                ),
                                dbc.Row(
                                    [
                                        dbc.Col(dcc.Dropdown(operation_keys:=[x for x in operations.keys()],
                                                             id='operation',
                                                             value='add',
                                                             placeholder='Select an operation...'),
                                                width=5),
                                        dbc.Col(dbc.Button('add', id='operation-button',
                                                           type='text'), 
                                                width=1),
                                    ]
                                )
                            ],
                            width=6
                        ),
                        dbc.Col(
                            [
                                html.Div(children=[], id='data-variables-container')
                            ],
                            width=6
                        )
                    ]
                ),
            ]
        ),
    )
])

