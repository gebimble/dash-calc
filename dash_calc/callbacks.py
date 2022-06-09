import numpy as np
import pandas as pd
from dash import Input, Output, State, ctx
import plotly.express as px

from main import app
from data import data, operations


@app.callback(
    Output('example-graph', 'figure'),
    [Input('datasets', 'value'),
    Input('axis-slider', 'value')],
)
def update_graph(dataset_name, height):
    return px.imshow(np.squeeze(data[dataset_name[0]])[height])

@app.callback(
    Output('datasets', 'options'),
    Input('generate-button', 'n_clicks'),
    Input('operation-button', 'n_clicks'),
    State('datasets', 'value'),
    State('operation', 'value'),
    prevent_initial_call=True
)
def generate_new_data(gclick, aclick, operands, operation):
    button_id = ctx.triggered_id if not None else None

    if button_id == 'generate-button':
        new_key = str(max([int(x) for x in data.keys()]) + 1)
        data.update({new_key: np.random.random((10,10))})
        return [x for x in data.keys()]

    if button_id == 'operation-button':
        new_key = operations[operation].symbol.join(operands)
        data.update(
            {
                new_key: operations[operation].operation(
                    *[data[x] for x in operands]
                )
            }
        )
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
