import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, get_colorscale, dict_dataset_images_to_organ_and_view, empty_graph
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from app import app, MODE
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
import copy
from PIL import Image
import base64
from io import BytesIO

sample = 0
path_attention_maps = './' + app.get_asset_url('page9_AttentionMaps/Images/Age')
path_attention_maps_metadata = './' + app.get_asset_url('page9_AttentionMaps/Attention_maps_infos/')

if MODE != 'All':
    organ_select = dbc.FormGroup([
        html.P("Select Organ : "),
        dcc.Dropdown(
            id = 'select_organ_attention_image',
            options = get_dataset_options([MODE]),
            placeholder ="Select an organ",
            value = MODE
            ),
            html.Br()
        ], style = {'display' : 'None'})
else :
    organ_select = dbc.FormGroup([
        html.P("Select Organ : "),
        dcc.Dropdown(
            id = 'select_organ_attention_image',
            options = get_dataset_options(dict_dataset_images_to_organ_and_view.keys()),
            placeholder ="Select an organ"
            ),
            html.Br()
        ])

controls = dbc.Card([
    organ_select,
    dbc.FormGroup([
        html.P("Select View : "),
        dcc.Dropdown(
            id = 'select_view_attention_image',
            options = get_dataset_options([]),
            placeholder ="Select a view"
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select Transformation : "),
        dcc.Dropdown(
            id = 'select_transformation_attention_image',
            options = get_dataset_options([]),
            placeholder ="Select a transformation"
            ),
        html.Br()
        ]),
    ])

controls_1 = dbc.Card([
    dbc.Row([
        dbc.Col([
            dbc.FormGroup([
                html.P("Select Sex : "),
                dcc.Dropdown(
                    id = 'select_sex_attention_image_1',
                    options = get_dataset_options(['Male', 'Female']),
                    placeholder ="Select a sex"
                    )
                ])
            ]),
        dbc.Col([
            dbc.FormGroup([
                html.P("Select an age group : "),
                dcc.Dropdown(
                    id = 'select_age_group_attention_image_1',
                    options = get_dataset_options(['Young', 'Middle', 'Old']),
                    placeholder ="Select an age group"
                    ),
                html.Br()
                ])
            ]),
        dbc.Col([
            dbc.FormGroup([
                html.P("Select an aging rate : "),
                dcc.Dropdown(
                    id = 'select_aging_rate_attention_image_1',
                    options = get_dataset_options(['Decelerated', 'Normal', 'Accelerated']),
                    placeholder ="Select an aging rate"
                    ),
                ]),
            ]),
        dbc.Col([
            dbc.FormGroup([
                html.P("Select image to display : "),
                dcc.Checklist(
                    id = 'select_raw_gradcam_saliency_1',
                    options=[
                        {'label': 'Raw', 'value': 'Raw'},
                        {'label': 'GradCam', 'value': 'plot_gradcam'},
                        {'label': 'Saliency', 'value': 'plot_saliency'}
                    ],
                    value = ['Raw', 'plot_gradcam', 'plot_saliency']
                )
            ])
        ])
    ])
])
controls_2 = dbc.Card([
    dbc.Row([
        dbc.Col([
            dbc.FormGroup([
                html.P("Select Sex : "),
                dcc.Dropdown(
                    id = 'select_sex_attention_image_2',
                    options = get_dataset_options(['Male', 'Female']),
                    placeholder ="Select a sex"
                    )
                ])
            ]),
        dbc.Col([
            dbc.FormGroup([
                html.P("Select an age group : "),
                dcc.Dropdown(
                    id = 'select_age_group_attention_image_2',
                    options = get_dataset_options(['Young', 'Middle', 'Old']),
                    placeholder ="Select an age group"
                    ),
                html.Br()
                ])
            ]),
        dbc.Col([
            dbc.FormGroup([
                html.P("Select an aging rate : "),
                dcc.Dropdown(
                    id = 'select_aging_rate_attention_image_2',
                    options = get_dataset_options(['Decelerated', 'Normal', 'Accelerated']),
                    placeholder ="Select an aging rate"
                    ),
                ]),
            ]),
        dbc.Col([
            dbc.FormGroup([
                html.P("Select image to display : "),
                dcc.Checklist(
                    id = 'select_raw_gradcam_saliency_2',
                    options=[
                        {'label': 'Raw', 'value': 'Raw'},
                        {'label': 'GradCam', 'value': 'plot_gradcam'},
                        {'label': 'Saliency', 'value': 'plot_saliency'}
                    ],
                    value = ['Raw', 'plot_gradcam', 'plot_saliency']
                )
            ])
        ])
    ])
])
@app.callback(Output('select_transformation_attention_image', 'options'),
              [Input('select_organ_attention_image', 'value'), Input('select_view_attention_image', 'value')])
def generate_list_view_list(value_organ, value_view):
    if value_view is None:
        return [{'value' : '', 'label' : ''}]
    else :
        return get_dataset_options(dict_dataset_images_to_organ_and_view[value_organ][value_view])


@app.callback(Output('select_view_attention_image', 'options'),
              [Input('select_organ_attention_image', 'value')])
def generate_list_view_list(value):
    if value is None:
        return [{'value' : '', 'label' : ''}]
    else :
        return get_dataset_options(dict_dataset_images_to_organ_and_view[value])







# # Parameters (will come from the options selected on the website)
# target='Age'
# organ='Abdomen'
# view='Liver'
# transformation='Raw'
# sex='Male'
# age_group='young'
# aging_rate='accelerated'
# sample='0' #<- if we only give one image for each example to miminize the amount of data stored, we might not need this parameter and you can fix it to 0.
# # options to decide which layers to plot (tick boxes)
# plot_raw = True
# plot_saliency = True
# plot_gradcam = True
# # Load libraries
# import numpy as np
# import matplotlib.image as mpimg
# import matplotlib.pyplot as plt
# # Load images
# raw = mpimg.imread(path_image)
# saliency = np.load(path_image.replace('RawImage', 'Saliency').replace('.jpg', '.npy'))
# gradcam = np.load(path_image.replace('RawImage', 'Gradcam').replace('.jpg', '.npy'))
# # Plot
# if plot_raw:
#    plt.imshow(raw)
# if plot_saliency:
#    plt.imshow(saliency)
# if plot_gradcam:
#    plt.imshow(gradcam)

# layout =  html.Div([
#         html.H1('Attention Maps'),
#         dbc.Container([
#             dbc.Row(
#                     children = [
#                         dbc.Col([controls,
#                                  html.Br(),
#                                  controls_2,
#                                  html.Br(),
#                                  html.Br(),
#                                  ], md=4),
#                         dbc.Col(id = 'columns_attention_map',
#                             md=8)
#                         ])
#             ],
#             style={"height": "100vh"},
#             fluid = True)
#         ]
#     )

layout =  html.Div([
        html.H1('Attention Maps - Images'),
        dbc.Container([
            dbc.Row([
                dbc.Col([controls], md=3),
                dbc.Col([
                    controls_1,
                    html.Div(id = 'columns_attention_map_1'),
                    controls_2,
                    html.Div(id = 'columns_attention_map_2')
                    ], md=9)
                ])
            ],
            #style={"height": "100vh"},
            fluid = True)
        ])

@app.callback(Output('columns_attention_map_1', 'children'),
             [Input('select_organ_attention_image', 'value'),
              Input('select_view_attention_image', 'value'),
              Input('select_transformation_attention_image', 'value'),
              Input('select_sex_attention_image_1', 'value'),
              Input('select_age_group_attention_image_1', 'value'),
              Input('select_aging_rate_attention_image_1', 'value'),
              Input('select_raw_gradcam_saliency_1', 'value')
              ])
def _plot_manhattan_plot(organ, view, transformation, sex, age_group, aging_rate, raw_gradcam_saliency):
    print("raw_gradcam_saliency", raw_gradcam_saliency)
    if None not in [organ, view, transformation, sex, age_group, aging_rate, raw_gradcam_saliency]:
        path_metadata = path_attention_maps_metadata + 'AttentionMaps-samples_Age_%s_%s_%s.csv' % (organ, view, transformation)
        df_metadata = pd.read_csv(path_metadata)
        df_metadata =  df_metadata[(df_metadata.sex == sex) & (df_metadata.age_category == age_group.lower()) & (df_metadata.aging_rate == aging_rate.lower()) & (df_metadata['sample'] == sample)]
        title = 'Chronological Age = %.2f; Biological Age = %.2f' % (df_metadata['Age'].iloc[0], df_metadata['Biological_Age'].iloc[0])
        if (organ, view) in [('Eyes','Fundus'), ('Eyes','OCT'), ('Arterial', 'Carotids'), ('Musculoskeletal', 'Knees'), ('Musculoskeletal', 'Hips')] :
            path_image_left = path_attention_maps + '/%s/%s/%s/%s/%s/%s/' % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower()) + '/left/RawImage_Age_' + organ  + '_' + view + '_' + transformation + '_' + sex + '_' + age_group.lower() + '_' + aging_rate.lower() + '_%s_left.jpg' % sample
            path_image_right = path_attention_maps + '/%s/%s/%s/%s/%s/%s/' % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower()) + '/right/RawImage_Age_' + organ  + '_' + view + '_' + transformation + '_' + sex + '_' + age_group.lower() + '_' + aging_rate.lower() + '_%s_right.jpg' % sample
            raw_left = mpimg.imread(path_image_left)
            raw_right = mpimg.imread(path_image_right)
            saliency_left = np.load(path_image_left.replace('RawImage', 'Saliency').replace('.jpg', '.npy'))
            saliency_right = np.load(path_image_right.replace('RawImage', 'Saliency').replace('.jpg', '.npy'))
            saliency_left = Image.fromarray((saliency_left).astype(np.uint8)).convert('RGBA')
            saliency_right = Image.fromarray((saliency_right).astype(np.uint8)).convert('RGBA')
            gradcam_left = np.load(path_image_left.replace('RawImage', 'Gradcam').replace('.jpg', '.npy'))
            gradcam_right = np.load(path_image_right.replace('RawImage', 'Gradcam').replace('.jpg', '.npy'))
            img_left = np.zeros(raw_left.shape)
            img_right = np.zeros(raw_right.shape)

            if raw_left.shape[0] != gradcam_left.shape[0] and raw_left.shape[0] != saliency_left.size[0]:
                raw_left = Image.fromarray((raw_left).astype(np.uint8)).convert('RGB')
                raw_right = Image.fromarray((raw_right).astype(np.uint8)).convert('RGB')

                raw_left.thumbnail((gradcam_left.shape[0], gradcam_left.shape[1]), Image.ANTIALIAS)
                raw_right.thumbnail((gradcam_right.shape[0], gradcam_right.shape[1]), Image.ANTIALIAS)

                raw_left = np.asarray(raw_left)
                raw_right = np.asarray(raw_right)

            img_left = np.zeros(raw_left.shape)
            img_right = np.zeros(raw_right.shape)
            final2_left = Image.new("RGBA", (raw_left.shape[1], raw_left.shape[0]))
            final2_right = Image.new("RGBA", (raw_right.shape[1], raw_right.shape[0]))

            if raw_gradcam_saliency is not None :
                if 'Raw' in raw_gradcam_saliency :
                    img_left+= raw_left
                    img_right+= raw_right
                    final2_left = Image.fromarray(img_left.astype(np.uint8)).convert('RGBA')
                    final2_right = Image.fromarray(img_right.astype(np.uint8)).convert('RGBA')
                if 'plot_gradcam' in raw_gradcam_saliency :
                    img_left = 0.7 * img_left + 0.3 * gradcam_left #* (255 - gradcam_left[:, :, 2].reshape((gradcam_left.shape[0],gradcam_left.shape[1], 1))) / 255
                    img_right = 0.7 * img_right + 0.3 * gradcam_right# * (255 - gradcam_right[:, :, 2].reshape((gradcam_right.shape[0],gradcam_right.shape[1], 1))) / 255
                    final2_left = Image.fromarray(img_left.astype(np.uint8)).convert('RGBA')
                    final2_right = Image.fromarray(img_right.astype(np.uint8)).convert('RGBA')
                if 'plot_saliency' in raw_gradcam_saliency :
                    final2_left = Image.alpha_composite(Image.fromarray(img_left.astype(np.uint8)).convert('RGBA'), saliency_left)
                    final2_right = Image.alpha_composite(Image.fromarray(img_right.astype(np.uint8)).convert('RGBA'), saliency_right)

                final2_right = final2_right.transpose(Image.FLIP_LEFT_RIGHT)
                buffered_left = BytesIO()
                final2_left.save(buffered_left, format="PNG")
                img_base64_left = base64.b64encode(buffered_left.getvalue()).decode('ascii')
                src_left = 'data:image/png;base64,{}'.format(img_base64_left)

                buffered_right = BytesIO()
                final2_right.save(buffered_right, format="PNG")
                img_base64_right = base64.b64encode(buffered_right.getvalue()).decode('ascii')
                src_right = 'data:image/png;base64,{}'.format(img_base64_right)
                col = [
                        html.H3(title),
                        html.Img(id = 'attentionmap_left', style={'height':'50%', 'width':'50%'},
                                 src = src_left),
                        html.Img(id = 'attentionmap_right', style={'height':'50%', 'width':'50%'},
                                 src = src_right)
                     ]
                return col

        else :

            path_image = path_attention_maps + '/%s/%s/%s/%s/%s/%s/' % (organ, view, transformation, sex, age_group, aging_rate) + 'RawImage_Age_' + organ  + '_' + view + '_' + transformation + '_' + sex + '_' + age_group + '_' + aging_rate + '_%s.jpg' % sample
            raw = mpimg.imread(path_image)
            saliency = np.load(path_image.replace('RawImage', 'Saliency').replace('.jpg', '.npy'))
            saliency = Image.fromarray((saliency ).astype(np.uint8)).convert('RGBA')
            gradcam =  np.load(path_image.replace('RawImage', 'Gradcam').replace('.jpg', '.npy'))

            img = np.zeros(raw.shape)
            final = Image.new("RGBA", (raw.shape[1], raw.shape[0]))
            if raw_gradcam_saliency is not None :
                if 'Raw' in raw_gradcam_saliency :
                    img += raw
                    final2 = Image.alpha_composite(final, Image.fromarray(img.astype(np.uint8)).convert('RGBA'))
                if 'plot_gradcam' in raw_gradcam_saliency :
                    img = 0.7 * img + 0.3 * gradcam
                    final2 = Image.alpha_composite(final, Image.fromarray(img.astype(np.uint8)).convert('RGBA'))
                if 'plot_saliency' in raw_gradcam_saliency :
                    final2 = Image.alpha_composite(Image.fromarray(img.astype(np.uint8)).convert('RGBA'), saliency)

                buffered = BytesIO()
                final2.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode('ascii')
                src = 'data:image/png;base64,{}'.format(img_base64)
                col = [
                        html.H3(title),
                        html.Img(id = 'attentionmap', style={'height':'50%', 'width':'50%'},
                                 src = src),
                     ]
                return col
            else  :
                return [dcc.Graph(figure = go.Figure(empty_graph))]
    else :
        return [dcc.Graph(figure = go.Figure(empty_graph))]

@app.callback(Output('columns_attention_map_2', 'children'),
             [Input('select_organ_attention_image', 'value'),
              Input('select_view_attention_image', 'value'),
              Input('select_transformation_attention_image', 'value'),
              Input('select_sex_attention_image_2', 'value'),
              Input('select_age_group_attention_image_2', 'value'),
              Input('select_aging_rate_attention_image_2', 'value'),
              Input('select_raw_gradcam_saliency_2', 'value')
              ])
def _plot_manhattan_plot(organ, view, transformation, sex, age_group, aging_rate, raw_gradcam_saliency):
    print("raw_gradcam_saliency", raw_gradcam_saliency)
    if None not in [organ, view, transformation, sex, age_group, aging_rate, raw_gradcam_saliency]:
        path_metadata = path_attention_maps_metadata + 'AttentionMaps-samples_Age_%s_%s_%s.csv' % (organ, view, transformation)
        df_metadata = pd.read_csv(path_metadata)
        df_metadata =  df_metadata[(df_metadata.sex == sex) & (df_metadata.age_category == age_group.lower()) & (df_metadata.aging_rate == aging_rate.lower()) & (df_metadata['sample'] == sample)]
        title = 'Chronological Age = %.2f; Biological Age = %.2f' % (df_metadata['Age'].iloc[0], df_metadata['Biological_Age'].iloc[0])
        if (organ, view) in [('Eyes','Fundus'), ('Eyes','OCT'), ('Arterial', 'Carotids'), ('Musculoskeletal', 'Knees'), ('Musculoskeletal', 'Hips')] :
            path_image_left = path_attention_maps + '/%s/%s/%s/%s/%s/%s/' % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower()) + '/left/RawImage_Age_' + organ  + '_' + view + '_' + transformation + '_' + sex + '_' + age_group.lower() + '_' + aging_rate.lower() + '_%s_left.jpg' % sample
            path_image_right = path_attention_maps + '/%s/%s/%s/%s/%s/%s/' % (organ, view, transformation, sex, age_group.lower(), aging_rate.lower()) + '/right/RawImage_Age_' + organ  + '_' + view + '_' + transformation + '_' + sex + '_' + age_group.lower() + '_' + aging_rate.lower() + '_%s_right.jpg' % sample
            raw_left = mpimg.imread(path_image_left)
            raw_right = mpimg.imread(path_image_right)
            saliency_left = np.load(path_image_left.replace('RawImage', 'Saliency').replace('.jpg', '.npy'))
            saliency_right = np.load(path_image_right.replace('RawImage', 'Saliency').replace('.jpg', '.npy'))
            saliency_left = Image.fromarray((saliency_left).astype(np.uint8)).convert('RGBA')
            saliency_right = Image.fromarray((saliency_right).astype(np.uint8)).convert('RGBA')
            gradcam_left = np.load(path_image_left.replace('RawImage', 'Gradcam').replace('.jpg', '.npy'))
            gradcam_right = np.load(path_image_right.replace('RawImage', 'Gradcam').replace('.jpg', '.npy'))

            img_left = np.zeros(raw_left.shape)
            img_right = np.zeros(raw_right.shape)

            if raw_left.shape[0] != gradcam_left.shape[0] and raw_left.shape[0] != saliency_left.size[0]:
                raw_left = Image.fromarray((raw_left).astype(np.uint8)).convert('RGB')
                raw_right = Image.fromarray((raw_right).astype(np.uint8)).convert('RGB')

                raw_left.thumbnail((gradcam_left.shape[0], gradcam_left.shape[1]), Image.ANTIALIAS)
                raw_right.thumbnail((gradcam_right.shape[0], gradcam_right.shape[1]), Image.ANTIALIAS)

                raw_left = np.asarray(raw_left)
                raw_right = np.asarray(raw_right)

            img_left = np.zeros(raw_left.shape)
            img_right = np.zeros(raw_right.shape)
            final_left = Image.new("RGBA", (raw_left.shape[1], raw_left.shape[0]))
            final_right = Image.new("RGBA", (raw_right.shape[1], raw_right.shape[0]))

            if raw_gradcam_saliency is not None :
                if 'Raw' in raw_gradcam_saliency :
                    img_left+= raw_left
                    img_right+= raw_right
                    final2_left = Image.alpha_composite(final_left, Image.fromarray(img_left.astype(np.uint8)).convert('RGBA'))
                    final2_right = Image.alpha_composite(final_right, Image.fromarray(img_right.astype(np.uint8)).convert('RGBA'))
                if 'plot_gradcam' in raw_gradcam_saliency :
                    img_left = 0.7 * img_left + 0.3 * gradcam_left #* (255 - gradcam_left[:, :, 2].reshape((gradcam_left.shape[0],gradcam_left.shape[1], 1))) / 255
                    img_right = 0.7 * img_left + 0.3 * gradcam_right# * (255 - gradcam_right[:, :, 2].reshape((gradcam_right.shape[0],gradcam_right.shape[1], 1))) / 255
                    final2_left = Image.alpha_composite(final_left, Image.fromarray(img_left.astype(np.uint8)).convert('RGBA'))
                    final2_right = Image.alpha_composite(final_right, Image.fromarray(img_right.astype(np.uint8)).convert('RGBA'))
                if 'plot_saliency' in raw_gradcam_saliency :
                    final2_left = Image.alpha_composite(Image.fromarray(img_left.astype(np.uint8)).convert('RGBA'), saliency_left)
                    final2_right = Image.alpha_composite(Image.fromarray(img_right.astype(np.uint8)).convert('RGBA'), saliency_right)
                buffered_left = BytesIO()
                final2_left.save(buffered_left, format="PNG")
                img_base64_left = base64.b64encode(buffered_left.getvalue()).decode('ascii')
                src_left = 'data:image/png;base64,{}'.format(img_base64_left)
                # flip right image to keep symmetry :
                final2_right = final2_right.transpose(Image.FLIP_LEFT_RIGHT)
                buffered_right = BytesIO()
                final2_right.save(buffered_right, format="PNG")
                img_base64_right = base64.b64encode(buffered_right.getvalue()).decode('ascii')
                src_right = 'data:image/png;base64,{}'.format(img_base64_right)
                col = [
                        html.H3(title),
                        html.Img(id = 'attentionmap_left', style={'height':'50%', 'width':'50%'},
                                 src = src_left),
                        html.Img(id = 'attentionmap_right', style={'height':'50%', 'width':'50%'},
                                 src = src_right)
                     ]
                return col
        else :
            path_image = path_attention_maps + '/%s/%s/%s/%s/%s/%s/' % (organ, view, transformation, sex, age_group, aging_rate) + 'RawImage_Age_' + organ  + '_' + view + '_' + transformation + '_' + sex + '_' + age_group + '_' + aging_rate + '_%s.jpg' % sample
            raw = mpimg.imread(path_image)
            saliency = np.load(path_image.replace('RawImage', 'Saliency').replace('.jpg', '.npy'))
            saliency = Image.fromarray((saliency ).astype(np.uint8)).convert('RGBA')
            gradcam =  np.load(path_image.replace('RawImage', 'Gradcam').replace('.jpg', '.npy'))
            print(raw.shape, gradcam.shape, saliency.size)
            img = np.zeros(raw.shape)
            final = Image.new("RGBA", (raw.shape[1], raw.shape[0]))
            if raw_gradcam_saliency is not None :
                if 'Raw' in raw_gradcam_saliency :
                    img += raw
                    final2 = Image.alpha_composite(final, Image.fromarray(img.astype(np.uint8)).convert('RGBA'))
                if 'plot_gradcam' in raw_gradcam_saliency :
                    img = 0.7 * img + 0.3 * gradcam #* (255 - gradcam[:, :, 2].reshape((gradcam.shape[0],gradcam.shape[1], 1))) / 255
                    final2 = Image.alpha_composite(final, Image.fromarray(img.astype(np.uint8)).convert('RGBA'))
                if 'plot_saliency' in raw_gradcam_saliency :
                    final2 = Image.alpha_composite(Image.fromarray(img.astype(np.uint8)).convert('RGBA'), saliency)

                buffered = BytesIO()
                final2.save(buffered, format="PNG")
                img_base64 = base64.b64encode(buffered.getvalue()).decode('ascii')
                src = 'data:image/png;base64,{}'.format(img_base64)
                col = [
                        html.H3(title),
                        html.Img(id = 'attentionmap', style={'height':'50%', 'width':'50%'},
                                 src = src),
                     ]
                return col
            else  :
                return [dcc.Graph(figure = go.Figure(empty_graph))]
    else :
        return [dcc.Graph(figure = go.Figure(empty_graph))]
