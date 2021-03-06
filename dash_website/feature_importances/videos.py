from dash_website.app import APP
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as gif
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

from dash_website.utils.aws_loader import load_feather
from dash_website.utils.controls import get_options_from_dict, get_item_radio_items
from dash_website.datasets import CHAMBERS_LEGEND, SEX_LEGEND, AGE_GROUP_LEGEND
from dash_website.feature_importances import AGING_RATE_LEGEND


def get_data_scores():
    return load_feather("feature_importances/scores_all_samples_per_participant.feather").to_dict()


def get_data_features():
    return load_feather("feature_importances/videos/information.feather").to_dict()


def get_controls_videos():
    return [
        dbc.Col(html.H4("Heart MRI with :"), width="auto"),
        dbc.Col(
            dcc.RadioItems(
                id="chamber_type_features",
                options=get_options_from_dict(CHAMBERS_LEGEND),
                value=list(CHAMBERS_LEGEND.keys())[1],
                labelStyle={"display": "inline-block", "margin": "5px"},
            )
        ),
    ]


@APP.callback(
    Output("title_videos_features", "children"),
    [
        Input("chamber_type_features", "value"),
        Input("memory_scores_features", "data"),
    ],
)
def _display_score(chamber_type, data_scores):
    scores_raw = pd.DataFrame(data_scores).set_index(["dimension", "subdimension", "sub_subdimension"]).round(3)
    scores = (
        scores_raw.loc[("Heart", "MRI", f"{chamber_type}chambersRaw")]
        .set_index("algorithm")
        .sort_values("r2", ascending=False)
    )

    title = ""
    for algorithm in scores.index:
        title += f"The {algorithm} has a R² of {scores.loc[algorithm, 'r2']} +- {scores.loc[algorithm, 'r2_std']}. "

    return title


def get_controls_side_video(side):
    if side == "left":
        value_idx = 0
    else:  # side == "right":
        value_idx = 1

    return [
        get_item_radio_items(f"sex_{side}_video_features", SEX_LEGEND, "Select sex :", value_idx=value_idx),
        get_item_radio_items(f"age_{side}_video_features", AGE_GROUP_LEGEND, "Select age group :", value_idx=1),
        get_item_radio_items(
            f"aging_rate_{side}_video_features", AGING_RATE_LEGEND, "Select aging rate :", value_idx=1
        ),
    ]


@APP.callback(
    [Output("gif_display_left_video_features", "children"), Output("title_left_video_features", "children")],
    [
        Input("chamber_type_features", "value"),
        Input("sex_left_video_features", "value"),
        Input("age_left_video_features", "value"),
        Input("aging_rate_left_video_features", "value"),
        Input("memory_videos_features", "data"),
    ],
)
def _display_left_gif_features(chamber_type, sex, age_group, aging_rate, data_videos):
    return display_gif_features(chamber_type, sex, age_group, aging_rate, data_videos)


@APP.callback(
    [Output("gif_display_right_video_features", "children"), Output("title_right_video_features", "children")],
    [
        Input("chamber_type_features", "value"),
        Input("sex_right_video_features", "value"),
        Input("age_right_video_features", "value"),
        Input("aging_rate_right_video_features", "value"),
        Input("memory_videos_features", "data"),
    ],
)
def _display_right_gif_features(chamber_type, sex, age_group, aging_rate, data_videos):
    return display_gif_features(chamber_type, sex, age_group, aging_rate, data_videos)


def display_gif_features(chamber_type, sex, age_group, aging_rate, data_videos):
    chronological_age, biological_age = (
        pd.DataFrame(data_videos)
        .set_index(["chamber", "sex", "age_group", "aging_rate"])
        .loc[(int(chamber_type), sex, age_group, aging_rate), ["chronological_age", "biological_age"]]
        .tolist()
    )
    title = f"The participant is an {aging_rate} ager: {np.round_(biological_age - chronological_age, 1)} years"

    gif_display = html.Div(
        gif.GifPlayer(
            gif=f"../data/feature_importances/videos/{chamber_type}_chambers/{sex}/{age_group}/{aging_rate}.gif",
            still=f"../data/feature_importances/videos/{chamber_type}_chambers/{sex}/{age_group}/{aging_rate}.png",
        ),
        style={"padding-left": 400},
    )
    return gif_display, title


LAYOUT = dbc.Container(
    [
        dcc.Loading(
            [
                dcc.Store(id="memory_scores_features", data=get_data_scores()),
                dcc.Store(id="memory_videos_features", data=get_data_features()),
            ]
        ),
        html.H1("Model interpretability - Videos"),
        html.Br(),
        html.Br(),
        dbc.Row(get_controls_videos(), justify="center"),
        dbc.Row(html.Br()),
        dbc.Row(html.H2(id="title_videos_features"), justify="center"),
        dbc.Row(html.Br()),
        dbc.Row(
            [
                dbc.Col(dbc.Card(get_controls_side_video("left")), width={"size": 6}),
                dbc.Col(dbc.Card(get_controls_side_video("right")), width={"size": 6}),
            ]
        ),
        dbc.Row(
            [
                dbc.Col(
                    [html.H3(id="title_left_video_features"), dcc.Loading(id="gif_display_left_video_features")],
                    width={"size": 6},
                ),
                dbc.Col(
                    [html.H3(id="title_right_video_features"), dcc.Loading(id="gif_display_right_video_features")],
                    width={"size": 6},
                ),
            ]
        ),
    ],
    fluid=True,
)
