from itertools import combinations
import pandas as pd
from dash import Input, Output, State, dcc, ALL
import plotly.express as px

from main import app
from data import data, operations


def get_coords_for_sliders(coords, dataset):
    split_coords = [x.strip() for x in coords.split(',')]

    coords_for_sliders = [x for x in dataset.coords.keys()]

    for c in split_coords:
        coords_for_sliders.remove(c)

    return coords_for_sliders

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
    Output('axis-sliders-container', 'children'),
    Input('datasets', 'value'),
    Input('coords', 'value')
)
def update_axis_sliders_container(datasets, coords):
    dataset = data[datasets[0]]

    coords_for_sliders = get_coords_for_sliders(coords, dataset)

    sliders = []

    for c in coords_for_sliders:
        coord = dataset.get_index(c)
        c_min, c_max = [getattr(coord, m)() for m in ('min', 'max')]
        marks = {f'{v:.2f}': f'{v:.2f}' for v in coord}

        sliders.append(
            dcc.Slider(min=c_min,
                       max=c_max,
                       value=c_min,
                       marks=marks,
                       id={
                           'type': 'axis-sliders',
                           'index': 0
                       },
                      )
        )

    return sliders

@app.callback(
    Output('coords', 'options'),
    Output('coords', 'value'),
    Input('datasets', 'value')
)
def update_coords(dataset):
    coords = [', '.join(x) 
              for x in combinations([x for x in data[dataset[0]].coords.keys()], 2)]
    return coords, coords[0]


@app.callback(
    Output('example-graph', 'figure'),
    Input('datasets', 'value'),
    Input({'type': 'data-variables', 'index': ALL}, 'value'),
    Input({'type': 'axis-sliders', 'index': ALL}, 'value'),
    Input('coords', 'value')
)
def update_graph(dataset_names, variable, sliders, coords):
    dataset = data[dataset_names[0]][variable[0][0]]
    coords_for_sliders = get_coords_for_sliders(coords, dataset)
    selection_dict = {c: s for c, s in zip(coords_for_sliders, sliders)}
    reduced_data = dataset.sel(**selection_dict, method='nearest', drop=True)
    try:
        return px.imshow(reduced_data, zmax=float(dataset.max()))
    except:
        return {}

@app.callback(
    Output('datasets', 'options'),
    Input('operation-button', 'n_clicks'),
    State('datasets', 'value'),
    State('operation', 'value'),
    State({'type': 'data-variables', 'index': ALL}, 'value'),
    prevent_initial_call=True
)
def data_operation(aclick, operands, operation, variable_names):

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
    State({'type': 'axis-sliders', 'index': ALL}, 'value'),
    State('coords', 'value'),
    prevent_initial_call=True
)
def update_line_graph(click_data, datasets, variables, slider_values, coords):
    positions = [click_data['points'][0][idx] for idx in ['x', 'y']]

    dataset = data[datasets[0]]
    selection_coords = [x.strip() for x in coords.split(',')]
    last_dim = get_coords_for_sliders(coords, dataset)[-1]
    last_dim_dict = {last_dim: slider_values[-1]}


    selection_dict = {c: p for c, p in zip(selection_coords, positions)}

    points = {
        d: data[d][v].sel(**selection_dict,
                          **last_dim_dict,
                          method='nearest',
                          drop=True).to_dataframe()
        for d, v in zip(datasets, variables)
    }

    df = pd.concat(points, axis=1)
    df.columns = pd.Index([' - '.join(x) for x in df.columns.to_flat_index()])

    return px.scatter(df)

@app.callback(
    Output('operation-button', 'children'),
    Input('operation', 'value')
)
def update_operation_button(operation):
    return operation.title()
