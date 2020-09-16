import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as gif
from dash.dependencies import Input, Output
from .tools import get_dataset_options
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px

from app import app, MODE, filename
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy
from PIL import Image
import base64
from io import BytesIO

path_img = 'page12_AttentionMapsVideos/img/'
path_gif = 'page12_AttentionMapsVideos/gif/'
path_attention_maps_videos = filename + 'page12_AttentionMapsVideos/AttentionMapsVideos/'
controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select Organ : "),
        dcc.Dropdown(
            id = 'select_organ_attention_video',
            options = get_dataset_options(['Heart']),
            placeholder ="Select an organ",
            value = 'Heart'
            ),
            html.Br()
        ]),
    dbc.FormGroup([
        html.P("Select View : "),
        dcc.Dropdown(
            id = 'select_view_attention_video',
            options = get_dataset_options(['MRI']),
            placeholder ="Select a view",
            value = 'MRI'
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select Transformation : "),
        dcc.Dropdown(
            id = 'select_transformation_attention_video',
            options = get_dataset_options(['3chambersRaw', '4chambersRaw']),
            placeholder ="Select a transformation"
            ),
        html.Br()
        ]),
    dbc.FormGroup([
        html.P("Select sex : "),
        dcc.Dropdown(
            id = 'select_sex_attention_video',
            options = [{'value' : 0, 'label' : 'Female'}, {'value' : 1, 'label' : 'Male'}],
            placeholder ="Select a sex"
            ),
        html.Br()
        ]),
    dbc.FormGroup([
        html.P("Select an age group : "),
        dcc.Dropdown(
            id = 'select_age_group_attention_video',
            options = get_dataset_options(['Young', 'Middle', 'Old']),
            placeholder ="Select an age group : "
            ),
        html.Br()
        ]),
    dbc.FormGroup([
        html.P("Select an aging rate : "),
        dcc.Dropdown(
            id = 'select_aging_rate_attention_video',
            options = get_dataset_options(['Decelerated', 'Normal', 'Accelerated']),
            placeholder ="Select an aging rate"
            ),
        html.Br()
        ]),
    ])

layout = dbc.Container([
                html.H1('AttentionMaps - Videos'),
                html.Br(),
                html.Br(),
                dbc.Row([
                    dbc.Col([controls,
                             html.Br(),
                             html.Br()], md=3),
                    dbc.Col(
                        [dcc.Loading(id = 'gif_display')],
                        style={'overflowX': 'scroll', 'width' : 1000},
                        md=9)
                    ])
            ], fluid = True)

@app.callback(Output('gif_display', 'children'),
             [Input('select_organ_attention_video', 'value'),
              Input('select_view_attention_video', 'value'),
              Input('select_transformation_attention_video', 'value'),
              Input('select_sex_attention_video', 'value'),
              Input('select_age_group_attention_video', 'value'),
              Input('select_aging_rate_attention_video', 'value'),
             ])
def _display_gif(organ, view, transformation, sex, age_group, aging_rate):
    print(organ, view, transformation, sex, age_group, aging_rate)
    if None not in [organ, view, transformation, sex, age_group, aging_rate]:
        print(organ, view, transformation, sex, age_group, aging_rate)
    #if organ is not None and view is not None and transformation is not None:
        df = pd.read_csv(path_attention_maps_videos + 'AttentionMaps-samples_Age_%s_%s_%s.csv' % (organ, view, transformation))
        df = df[(df.Sex == sex) & (df.age_category == age_group.lower()) & (df.aging_rate == aging_rate.lower())]
        eid = df.iloc[0].eid
        path_to_gif = df.iloc[0].Gif.split('/')[-1]
        path_to_gif = path_gif + path_to_gif
        path_to_jpg = df.iloc[0].Picture.split('/')[-1]
        path_to_jpg = path_img + path_to_jpg
        print(path_to_gif, path_to_jpg)
        gif_display = gif.GifPlayer(
            gif = 'assets2/' + path_to_gif,
            still = 'assets2/' + path_to_jpg
            )
        print(gif_display)
        return gif_display
    else :
        return dcc.Graph()
