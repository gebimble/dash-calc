import numpy as np
import pandas as pd
from dash import Input, Output, State, ctx
import plotly.express as px

from main import app
from data import data, operations


@app.callback(
    Output('example-graph', 'figure'),
    [Input('datasets', 'value'),
     Input('data-variables', 'value'),
     Input('axis-slider', 'value')],
)
def update_graph(dataset_names, variable, height):
    return px.imshow(np.squeeze(data[dataset_names[0]][variable[0]])[height])

@app.callback(
    Output('datasets', 'options'),
    Input('generate-button', 'n_clicks'),
    Input('operation-button', 'n_clicks'),
    State('datasets', 'value'),
    State('operation', 'value'),
    State('data-variables', 'value'),
    prevent_initial_call=True
)
def generate_new_data(gclick, aclick, operands, operation, variable_names):
    button_id = ctx.triggered_id if not None else None

    if button_id == 'generate-button':
        new_key = str(max([int(x) for x in data.keys()]) + 1)
        data.update({new_key: np.random.random((10,10))})
        return [x for x in data.keys()]

    if button_id == 'operation-button':
        new_key = operations[operation].symbol.join(operands)

        new_dataset = data[operands[0]].copy(deep=True).drop(variable_names[0])

        new_dataset_name = operations[operation].symbol.join(variable_names)

        breakpoint()

        new_dataset[new_dataset_name] = (new_dataset.dims, operations[operation].operation(
            *[data[dataset][variable].data
              for dataset, variable
              in zip(operands, variable_names)]
        ))

        data.update({new_key: new_dataset})
        breakpoint()
        return [x for x in data.keys()]

@app.callback(
    Output('line-graph', 'figure'),
    Input('example-graph', 'clickData'),
    State('datasets', 'value'),
    prevent_initial_call=True
)
def update_line_graph(click_data, datasets):
    x, y = [click_data['points'][0][idx] for idx in ['x', 'y']]
    points = {d:data[d][x, y] for d in datasets}
    return px.scatter(pd.DataFrame(points))

@app.callback(
    Output('operation-button', 'children'),
    Input('operation', 'value')
)
def update_operation_button(operation):
    return operation.title()

@app.callback(
    Output('data-variables', 'options'),
    Output('data-variables', 'value'),
    Input('datasets', 'value')
)
def update_data_variables(dataset):
    k = []

    for ds in dataset:
        k += [x for x in data[ds].keys()]

    return k, k
