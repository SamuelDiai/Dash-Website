from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import dash

import pandas as pd

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_item_radio_items, get_options
from dash_website import CORRELATION_TYPES
from dash_website.datasets import TREE_SCALARS, ETHNICITIES, SEX_VALUE, SEX_COLOR
from dash_website.xwas import BAR_PLOT_TABLE_COLUMNS, FEATURES_CORRELATIONS_TABLE_COLUMNS


def get_layout():
    return dbc.Container(
        [
            html.H1("Feature importances - Scalars"),
            html.Br(),
            html.Br(),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dbc.Card(get_controls_scalars_features()),
                            html.Br(),
                            html.Br(),
                            dbc.Card(get_controls_table_scalars_features()),
                        ],
                        md=5,
                    ),
                    dbc.Col(
                        dcc.Loading([html.H2(id="title_scalars_features"), dcc.Graph(id="bar_plot_scalars_features")]),
                        md=7,
                    ),
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        [
                            dash_table.DataTable(
                                id="table_scalars_features",
                                columns=[{"name": i, "id": i} for i in list(BAR_PLOT_TABLE_COLUMNS.values())],
                                style_cell={"textAlign": "left"},
                                sort_action="custom",
                                sort_mode="single",
                            )
                        ],
                        width={"size": 8, "offset": 3},
                    )
                ]
            ),
        ],
        fluid=True,
    )


def get_controls_scalars_features():
    first_dimension = list(TREE_SCALARS.keys())[0]
    first_subdimension = list(TREE_SCALARS[first_dimension].keys())[0]

    return [
        get_item_radio_items(
            "dimension_scalars_features", list(TREE_SCALARS.keys()), "Select main aging dimesion :", from_dict=False
        ),
        get_item_radio_items(
            "subdimension_scalars_features",
            list(TREE_SCALARS[first_dimension].keys()),
            "Select subdimension :",
            from_dict=False,
        ),
        get_item_radio_items(
            "sub_subdimension_scalars_features",
            TREE_SCALARS[first_dimension][first_subdimension],
            "Select sub-subdimension :",
            from_dict=False,
        ),
    ]


@APP.callback(
    [
        Output("subdimension_scalars_features", "options"),
        Output("subdimension_scalars_features", "value"),
        Output("sub_subdimension_scalars_features", "options"),
        Output("sub_subdimension_scalars_features", "value"),
    ],
    [Input("dimension_scalars_features", "value"), Input("subdimension_scalars_features", "value")],
)
def _change_subdimensions_features(dimension, subdimension):
    context = dash.callback_context.triggered

    if not context or context[0]["prop_id"].split(".")[0] == "dimension_scalars_features":
        first_subdimension = list(TREE_SCALARS[dimension].keys())[0]
        return (
            get_options(list(TREE_SCALARS[dimension].keys())),
            list(TREE_SCALARS[dimension].keys())[0],
            get_options(TREE_SCALARS[dimension][first_subdimension]),
            TREE_SCALARS[dimension][first_subdimension][0],
        )
    else:
        return (
            get_options(list(TREE_SCALARS[dimension].keys())),
            subdimension,
            get_options(TREE_SCALARS[dimension][subdimension]),
            TREE_SCALARS[dimension][subdimension][0],
        )


def get_controls_table_scalars_features():
    return [
        get_item_radio_items(
            "correlation_type_scalars_features",
            CORRELATION_TYPES,
            "Select sub-subdimension :",
        ),
        dbc.FormGroup(
            [
                html.P("Correlation between feature importances/correlation : "),
                dash_table.DataTable(
                    id="table_correlation_scalars_features",
                    columns=[{"name": i, "id": i} for i in list(FEATURES_CORRELATIONS_TABLE_COLUMNS.values())],
                    style_cell={"textAlign": "left"},
                    sort_action="custom",
                    sort_mode="single",
                ),
                html.Br(),
            ]
        ),
    ]


# @APP.callback(
#     [
#         Output("bar_plot_scalars_features", "figure"),
#         Output("table_scalars_features", "data"),
#         Output("table_correlation_scalars_features", "data"),
#     ],
#     [
#         Input("dimension_scalars_features", "value"),
#         Input("subdimension_scalars_features", "value"),
#         Input("sub_subdimension_scalars_features", "value"),
#         Input("correlation_type_scalars_features", "value"),
#     ],
# )
# def _fill_bar_plot_feature(dimension, subdimension, sub_subdimension, correlation_type):
#     import plotly.graph_objects as go

#     features = load_feather(
#         f"feature_importances/scalars/{dimension}/{subdimension}/{sub_subdimension}.feather"
#     ).set_index("feature")
#     features.columns = pd.MultiIndex.from_tuples(
#         list(map(eval, features.columns.tolist())), names=["algorithm", "observation"]
#     )
#     features.reset_index(inplace=True).set_index(["algorithm"])

#     features = pd.DataFrame(data_features).set_index(["algorithm", "variable"])
#     sorted_variables = (
#         (features.loc[best_algorithm].abs() / features.loc[best_algorithm].abs().sum())
#         .sort_values(by=["feature_importance"], ascending=False)
#         .index
#     )

#     algorithms = features.index.get_level_values("algorithm").drop_duplicates()

#     table_features = pd.DataFrame(None, columns=BAR_PLOT_TABLE_COLUMNS.keys())
#     table_features["variable"] = sorted_variables

#     for algorithm in algorithms:
#         sorted_algorithm_variable = [[algorithm, variable] for variable in sorted_variables]

#         table_features[f"feature_{algorithm}"] = features.loc[sorted_algorithm_variable].values
#         table_features[f"percentage_{algorithm}"] = (
#             features.loc[sorted_algorithm_variable].abs() / features.loc[sorted_algorithm_variable].abs().sum()
#         )["feature_importance"].values

#     bars = []
#     hovertemplate = "Variable: %{y} <br>Percentage of overall feature importance: %{x:.3f} <br>Feature importance: %{customdata:.3f} <br><extra></extra>"

#     for algorithm in algorithms:
#         bars.append(
#             go.Bar(
#                 name=ALGORITHMS_RENDERING[algorithm],
#                 x=table_features[f"percentage_{algorithm}"].values[::-1],
#                 y=sorted_variables[::-1],
#                 orientation="h",
#                 customdata=table_features[f"feature_{algorithm}"].values[::-1],
#                 hovertemplate=hovertemplate,
#             )
#         )

#     fig = go.Figure(bars)

#     fig.update_layout(
#         {
#             "width": 800,
#             "height": int(25 * len(sorted_variables)),
#             "xaxis": {"title": "Percentage of overall feature importance", "showgrid": False},
#             "yaxis": {"title": "Variables", "showgrid": False},
#         }
#     )

#     table_correlations_raw = table_features[
#         [
#             f"percentage_{'correlation'}",
#             f"percentage_{'elastic_net'}",
#             f"percentage_{'light_gbm'}",
#             f"percentage_{'neural_network'}",
#         ]
#     ]

#     table_correlations = (
#         table_correlations_raw.corr(method=correlation_type)
#         .round(3)
#         .rename(index=FEATURES_CORRELATIONS_TABLE_COLUMNS)
#         .reset_index()
#     )

#     return (
#         fig,
#         table_features.round(3).rename(columns=BAR_PLOT_TABLE_COLUMNS).to_dict("records"),
#         table_correlations.rename(columns=FEATURES_CORRELATIONS_TABLE_COLUMNS).to_dict("records"),
#         title,
#     )