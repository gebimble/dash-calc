from itertools import combinations

import numpy as np
import pandas as pd

from dash import Input, Output, State, ALL
from dash import dcc, html

import plotly.express as px
import plotly.graph_objects as go

import pyvista as pv

from main import app
from data import data, operations


def split_coordinates(coords):
    return [x.strip() for x in coords.split(",")]


pv.set_plot_theme("document")


def get_coords_for_sliders(coords, dataset):
    split_coords = split_coordinates(coords)

    coords_for_sliders = [x for x in dataset.coords.keys()]

    for c in split_coords:
        coords_for_sliders.remove(c)

    return coords_for_sliders


@app.callback(
    Output("data-variables-container", "children"), Input("datasets", "value")
)
def update_data_variables_container(datasets):
    return [
        dcc.Dropdown(
            data_keys := [x for x in data[d].keys()],
            value=data_keys,
            multi=True,  # id='data-variables',
            id={"type": "data-variables", "index": i},
            placeholder=f"Select a data variable in dataset {d}...",
        )
        for i, d in enumerate(datasets)
    ]


@app.callback(
    Output("axis-sliders-container", "children"),
    Input("datasets", "value"),
    Input("coords", "value"),
)
def update_axis_sliders_container(datasets, coords):
    dataset = data[datasets[0]]

    coords_for_sliders = get_coords_for_sliders(coords, dataset)

    sliders = []

    for i, c in enumerate(coords_for_sliders):

        coord = dataset.get_index(c)
        (size,) = coord.shape
        c_min, c_max = (getattr(coord, m)() for m in ("min", "max"))
        marks = {i: f"{v:.2f}" for i, v in enumerate(coord)}

        sliders.append(
            dcc.Slider(
                min=0,
                max=size - 1,
                value=c_min,
                marks=marks,
                included=False,
                id={"type": "axis-sliders", "index": i},
                tooltip={"placement": "bottom", "always_visible": True},
            )
        )

    sliders[0].id["index"] = -1  # no longer need to know the length of
    # `sliders` for pattern matching
    # callbacks

    return sliders


@app.callback(
    Output("axis-names-container", "children"),
    Input("coords", "value"),
    State("datasets", "value"),
)
def update_axis_names(coords, datasets):
    dataset = data[datasets[0]]

    split_coords = get_coords_for_sliders(coords, dataset)

    return [
        html.Div(
            f"{coord}-axis",
            id={"type": "axis-names", "index": 0},
            style={"text-align": "right", "line-height": "175%"},
        )
        for coord in split_coords
    ]


@app.callback(
    Output("coords", "options"), Output("coords", "value"), Input("datasets", "value")
)
def update_coords(dataset):
    coords = [
        ", ".join(x)
        for x in combinations([x for x in data[dataset[0]].coords.keys()], 2)
    ]
    return coords, coords[0]


@app.callback(
    Output("main-graph", "figure"),
    Input("datasets", "value"),
    Input({"type": "data-variables", "index": 0}, "value"),
    Input({"type": "axis-sliders", "index": ALL}, "value"),
    Input("coords", "value"),
)
def update_graph(dataset_names, variable, sliders, coords):
    dataset = data[dataset_names[0]][variable[0]]
    coords_for_sliders = get_coords_for_sliders(coords, dataset)
    selection_dict = {c: s for c, s in zip(coords_for_sliders, sliders)}
    reduced_data = dataset.sel(**selection_dict, method="nearest", drop=True)

    try:
        return px.imshow(reduced_data, zmax=float(dataset.max()))
    except:
        return {}


@app.callback(
    Output("datasets", "options"),
    Input("operation-button", "n_clicks"),
    State("datasets", "value"),
    State("operation", "value"),
    State({"type": "data-variables", "index": ALL}, "value"),
    prevent_initial_call=True,
)
def data_operation(aclick, operands, operation, variable_names):

    new_key = operations[operation].symbol.join(operands)

    new_dataset = data[operands[0]].copy(deep=True).drop(variable_names[0])

    new_dataset_name = operations[operation].symbol.join([x[0] for x in variable_names])

    new_dataset[new_dataset_name] = (
        new_dataset.dims,
        operations[operation].operation(
            *[
                data[dataset][variable[0]].data
                for dataset, variable in zip(operands, variable_names)
            ]
        ),
    )

    data.update({new_key: new_dataset})
    return [x for x in data.keys()]


@app.callback(
    Output("line-graph", "figure"),
    Input("main-graph", "clickData"),
    Input("datasets", "value"),
    Input({"type": "data-variables", "index": ALL}, "value"),
    Input({"type": "axis-sliders", "index": ALL}, "value"),
    Input("coords", "value"),
)
def update_line_graph(click_data, datasets, variables, slider_value, coords):
    try:
        positions = [click_data["points"][0][idx] for idx in ["x", "y"]]
    except:
        positions = [0.0, 0.0]

    selection_coords = [x.strip() for x in coords.split(",")]
    selection_dict = {c: p for c, p in zip(selection_coords, positions)}

    dataset = data[datasets[0]]

    last_dim = get_coords_for_sliders(coords, dataset)[-1]
    last_dim_dict = {last_dim: slider_value[-1]}

    points = {
        d: data[d][v]
        .sel(**selection_dict, **last_dim_dict, method="nearest", drop=True)
        .to_dataframe()
        for d, v in zip(datasets, variables)
    }

    df = pd.concat(points, axis=1)
    df.columns = pd.Index([" - ".join(x) for x in df.columns.to_flat_index()])

    fig = px.scatter(df, x=df.columns, y=df.index)
    fig.update_xaxes(autorange="reversed")

    return fig


@app.callback(Output("operation-button", "children"), Input("operation", "value"))
def update_operation_button(operation):
    return operation.title()


@app.callback(
    Output("hist-graph", "figure"),
    Input("main-graph", "selectedData"),
    Input("line-graph", "selectedData"),
    Input("datasets", "value"),
    Input({"type": "data-variables", "index": ALL}, "value"),
    Input({"type": "axis-sliders", "index": ALL}, "value"),
    Input("coords", "value"),
)
def update_histogram_graph(
    main_selected, line_selected, datasets, variables, sliders, coords
):
    slice_config = {}

    try:
        slice_config.update(
            {
                par: slice(*main_selected["range"][par])
                for par in [x.strip() for x in coords.split(",")]
            }
        )
    except:
        pass

    slider_coords = get_coords_for_sliders(coords, data[datasets[0]][variables[0][0]])

    try:
        slice_config.update({slider_coords[0]: slice(*line_selected["range"]["y"])})
    except:
        pass

    slice_config.update({slider_coords[-1]: slice(sliders[-1])})

    fig = go.Figure()
    for d, vs in zip(datasets, variables):
        for v in vs:
            fig.add_trace(
                go.Histogram(y=data[d][v].sel(**slice_config).values.flatten())
            )

    fig.update_layout(barmode="overlay")
    fig.update_traces(opacity=0.5)

    return fig


@app.callback(
    Output("placeholder", "children"),
    Input("vtk-button", "n_clicks"),
    State("datasets", "value"),
    State({"type": "data-variables", "index": 0}, "value"),
    prevent_initial_call=True,
)
def vtk_button(vclicks, datasets, variables):

    dataset = data[datasets[0]][variables[0]].sel(t=0, method="nearest", drop=True)

    coord_values = [d.values for d in dataset.coords.values()]

    x, y, z = (
        np.hstack([-0.5, np.vstack([d[1:], d[:-1]]).mean(axis=0), 0.5])
        for d in coord_values
    )

    rect_grid = pv.RectilinearGrid(x, y, z)
    rect_grid.cell_data[variables[0]] = dataset.values.flatten()

    rect_grid.plot()

    return []


@app.callback(Output("main-graph", "layout"), Input("vtk-button", "n_clicks"))
def example_layout(click):
    layout = {}
    return layout
