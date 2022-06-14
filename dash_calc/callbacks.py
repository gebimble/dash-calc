from itertools import cycle
import numpy as np
import pandas as pd
from dash import Input, Output, State, ctx, dcc, ALL
import plotly.express as px

from main import app
from data import data, operations


@app.callback(
    Output('data-variables-container', 'children'),
    Input('datasets', 'value')
)
def update_data_variables_container(datasets):
    return [
        dcc.Dropdown(data_keys:=[x for x in data[d].keys()], value=data_keys,
                     multi=True, #id='data-variables',
                     id={
                         'type': 'data-variables',
                         'index': 0
                     },
                     placeholder=f'Select a data variable in dataset {d}...')
        for d in datasets
    ]

@app.callback(
    Output('example-graph', 'figure'),
    Input('datasets', 'value'),
    Input({'type': 'data-variables', 'index': ALL}, 'value'),
    Input('axis-slider', 'value'),
)
def update_graph(dataset_names, variable, height):
    return px.imshow(np.squeeze(data[dataset_names[0]][variable[0][0]])[height])

@app.callback(
    Output('datasets', 'options'),
    Input('operation-button', 'n_clicks'),
    State('datasets', 'value'),
    State('operation', 'value'),
    State({'type': 'data-variables', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def generate_new_data(aclick, operands, operation, variable_names):

    new_key = operations[operation].symbol.join(operands)

    new_dataset = data[operands[0]].copy(deep=True).drop(variable_names[0])

    new_dataset_name = operations[operation].symbol.join([x[0] for x in
                                                          variable_names])

    new_dataset[new_dataset_name] = (new_dataset.dims, operations[operation].operation(
        *[data[dataset][variable[0]].data
          for dataset, variable
          in zip(operands, variable_names)]
    ))

    data.update({new_key: new_dataset})
    return [x for x in data.keys()]

@app.callback(
    Output('line-graph', 'figure'),
    Input('example-graph', 'clickData'),
    State('datasets', 'value'),
    State({'type': 'data-variables', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def update_line_graph(click_data, datasets, variables):
    x, y = [click_data['points'][0][idx] for idx in ['x', 'y']]

    points = {}

    for d, vars in zip(datasets, variables):
        for v in vars:
            points.update({' - '.join([d, v]): data[d][v][x, y]})

    return px.scatter(pd.DataFrame(points))

@app.callback(
    Output('operation-button', 'children'),
    Input('operation', 'value')
)
def update_operation_button(operation):
    return operation.title()
