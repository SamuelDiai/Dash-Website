import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from .tools import get_dataset_options, ETHNICITY_COLS, hierarchy_biomarkers
import pandas as pd
import plotly.graph_objs as go
from plotly.subplots import make_subplots
from app import app, MODE
import glob
import os
import numpy as np
from scipy.stats import pearsonr
import dash_table
path_feat_imps = './' + app.get_asset_url('page3_featureImp/FeatureImp/')
path_score_scalar = './' + app.get_asset_url('page2_predictions/Performances/PERFORMANCES_tuned_alphabetical_eids_Age_test.csv')
list_models = ['Correlation', 'ElasticNet', 'LightGBM', 'NeuralNetwork']
targets = ['Sex', 'Age']
#list_organs = [os.path.basename(elem).replace('.csv', '').split('_')[2] for elem in glob.glob(path_feat_imps + '*.csv')]
#list_organs = sorted(list(set(list_organs)))

#if MODE != 'All':
#    list_organs = [elem for elem in list_organs if MODE in elem]
score = pd.read_csv(path_score_scalar)

if MODE == 'All' :
    organ_select = dbc.FormGroup([
        html.P("Select an Organ : "),
        dcc.Dropdown(
            id='Select_organ_1',
            options = get_dataset_options(hierarchy_biomarkers.keys())
            ),
        html.Br()
    ])
else:
    organ_select = dbc.FormGroup([
        html.P("Select an Organ : "),
        dcc.Dropdown(
            id='Select_organ_1',
            options = get_dataset_options([MODE]),
            value= MODE
            ),
        html.Br()
    ], style = {'display' : 'None'})

controls = dbc.Card([
    dbc.FormGroup([
        html.P("Select a target : "),
        dcc.RadioItems(
            id = 'select_target',
            options = get_dataset_options(['Age', 'Sex']),
            value = 'Age',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
            ),
        html.Br()
    ]),
    organ_select,
    dbc.FormGroup([
        html.P("Select Sublevel1 : "),
        dcc.Dropdown(
            id='Select_view_1',
            options = get_dataset_options([])
            ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Select Sublevel2 : "),
        dcc.Dropdown(
            id='Select_transf_1',
            options = get_dataset_options([])
            ),
        html.Br()
    ]),
])

@app.callback(Output('Select_transf_1', 'options'),
              [Input('Select_organ_1', 'value'), Input('Select_view_1', 'value')])
def generate_list_view_list(value_organ, value_view):
    if value_view is None:
        return [{'value' : '', 'label' : ''}]
    else :
        return get_dataset_options(hierarchy_biomarkers[value_organ][value_view])


@app.callback(Output('Select_view_1', 'options'),
              [Input('Select_organ_1', 'value')])
def generate_list_view_list(value):
    if value is None:
        return [{'value' : '', 'label' : ''}]
    else :
        return get_dataset_options(hierarchy_biomarkers[value])


table_df = pd.DataFrame(data = {'Corr' : ['Correlation', 'ElasticNet', 'LightGBM', 'NeuralNetwork'],
                                'Correlation' : [1, 0, 0, 0],
                                'ElasticNet' : [0, 1, 0, 0],
                                'LightGBM': [0, 0, 1, 0],
                                'NeuralNetwork' : [0, 0, 0, 1]})

table = dbc.Card([
    dbc.FormGroup([
        html.P("Select correlation type"),
        dcc.RadioItems(
            id = 'select correlation type',
            options = get_dataset_options(['Pearson', 'Spearman']),
            value = 'Pearson',
            labelStyle = {'display': 'inline-block', 'margin': '5px'}
        ),
        html.Br()
    ]),
    dbc.FormGroup([
        html.P("Correlation between feature importances/correlation : "),
        dash_table.DataTable(
            id = 'table_corr',
            columns =[{"name": i, "id": i} for i in table_df.columns],
            data = table_df.to_dict('records')
        ),
        html.Br()
    ])
])

layout =  html.Div([
    dcc.Store(id='memory'),
    dcc.Store(id = 'memory_no_str'),
    dcc.Loading([
        dbc.Container([
            html.H1('Features importances'),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col([controls,
                         html.Br(),
                         html.Br(),
                         table
                         ], md=3),
                dbc.Col([
                    html.H2(id = 'scores'),
                    dcc.Graph(
                         id='Plot Feature Imps',
                         )
                ],
                md=9,
                style={'overflowY': 'scroll', 'height' : 1000}),

                ],
                className="h-5"),
            html.Br(),
            html.Br(),
            html.H2('Feature Importances - Table'),
            html.Br(),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    dash_table.DataTable(
                        id = 'table_feature_imps',
                        sort_action="native",
                        )
                     ],
                    style={'overflowY': 'scroll', 'height': 800},
                    width={"size": 10, "offset": 1})
                ], className="h-75")
            ],
            style={"height": "100vh"},
            fluid = True)
        ],
        id = 'Loading Data'
    )])



@app.callback([Output("memory", "data"), Output("memory_no_str", "data"), Output("table_feature_imps", 'columns'), Output("Plot Feature Imps", "figure"), Output("scores", "children")],
              [Input('select_target', 'value'), Input('Select_organ_1', 'value'), Input('Select_view_1', 'value'), Input('Select_transf_1', 'value')])
def _plot_r2_scores(value_target, value_organ, value_view, value_transformation):
    if value_transformation is not None :
        print(score)
        score_model = score[(score['organ'] == value_organ) & (score['view'] == value_view) & (score['transformation'] == value_transformation)][['architecture', 'R-Squared_all', 'N_all']]
        score_lightgbm = score_model[score_model['architecture'] == 'LightGBM']['R-Squared_all']
        score_nn = score_model[score_model['architecture'] == 'NeuralNetwork']['R-Squared_all']
        score_elasticnet = score_model[score_model['architecture'] == 'ElasticNet']['R-Squared_all']
        sample_size = score_model[score_model['architecture'] == 'ElasticNet']['N_all']

        title = 'Bar Plot - R-Squared : ElasticNet %.3f, LightGBM %.3f, NeuralNetwork %.3f, Sample Size %d' % (score_elasticnet, score_lightgbm, score_nn, sample_size)
        list_models = []
        list_df = glob.glob(path_feat_imps + 'FeatureImp_%s_%s_%s_%s_*.csv' % (value_target, value_organ, value_view, value_transformation))
        list_df_sd = glob.glob(path_feat_imps + 'FeatureImp_sd_%s_%s_%s_%s_*.csv' % (value_target, value_organ, value_view, value_transformation))

        for idx, elem in enumerate(list_df):

            df_new = pd.read_csv(elem, na_filter = False).set_index('features')
            print(df_new)
            _, _, _, _, _, model = os.path.basename(elem).split('_')
            model = model.replace('.csv', '').replace('LightGbm', 'LightGBM')
            list_models.append(model)
            df_new.columns = [model]
            if idx == 0:
                df = df_new
            else :
                df = df.join(df_new)
        df = np.abs(df)/np.abs(df).sum()

        list_models_sd = []
        for idx, elem in enumerate(list_df_sd):
            df_new_sd = pd.read_csv(elem, na_filter = False).set_index('features')
            _, _, _, _, _, _, model = os.path.basename(elem).split('_')
            model = model.replace('.csv', '').replace('LightGbm', 'LightGBM')
            list_models_sd.append(model)
            df_new_sd.columns = [model]
            if idx == 0:
                df_sd = df_new_sd
            else :
                df_sd = df_sd.join(df_new_sd)

        ## Sort by mean of 3 models :
        # df['mean'] = df.mean(axis = 1)
        # df = df.sort_values('mean', ascending = True).drop(columns = ['mean'])

        ## Sort by best model :
        if score_lightgbm.values > score_nn.values and score_lightgbm.values > score_elasticnet.values:
            df = df.sort_values('LightGBM')
            df_sd = df_sd.sort_values('LightGBM')
        elif score_nn.values > score_lightgbm.values and score_nn.values > score_elasticnet.values:
            df = df.sort_values('NeuralNetwork')
            df_sd = df_sd.sort_values('NeuralNetwork')
        else :
            df = df.sort_values('ElasticNet')
            df_sd = df_sd.sort_values('ElasticNet')
        features = df.index

        df_sd = df_sd.loc[features]

        # list_models_mean = []
        # for idx, elem in enumerate(list_models_mean):
        #     df_new_sd = pd.read_csv(elem, na_filter = False).set_index('features')
        #     _, _, _, _, _, _,  model = os.path.basename(elem).split('_')
        #     model = model.replace('.csv', '')
        #     list_models_sd.append(model)
        #     df_new_mean.columns = [model]
        #     if idx == 0:
        #         df_mean = df_new_mean
        #     else :
        #         df_mean = df_mean.join(df_new_mean)
        # df_mean = df_mean.loc[features]




        df_str = df.round(4).astype(str) + ' ± '  + df_sd.round(4).astype(str)
        df.index = df.index.str.replace('.0$', '', regex = True)
        df_str.index = df_str.index.str.replace('.0$', '', regex = True)
        print(df_str)

        ## Plot
        d = {'data' : [go.Bar(name = model, x = df[model], y = df.index, orientation='h') for model in sorted(df.columns)],
             'layout' : dict(height = len(df.index) * 20,
                             margin={'l': 40, 'b': 30, 't': 10, 'r': 0},
                             xaxis_title='Feature importance')}
        matrix = df[sorted(list_models)].corr()
        matrix.index.name = 'Corr'
        matrix = matrix.reset_index().round(3)
        #print("Matrix : ", matrix)

        table = dbc.Card([
            dbc.FormGroup([
                html.P("Select correlation type"),
                dcc.RadioItems(
                    id = 'select correlation type',
                    options = get_dataset_options(['pearson', 'spearman']),
                    value = 'pearson',
                    labelStyle = {'display': 'inline-block', 'margin': '5px'}
                ),
                html.Br()
            ]),
            dbc.FormGroup([
                html.P("Correlation between feature importances/correlation : "),
                dash_table.DataTable(
                    id = 'table_corr',
                    columns =[{"name": i, "id": i} for i in table_df.columns],
                    style_cell={'textAlign': 'left'},
                    data = matrix.to_dict('records')
                ),
                html.Br()
            ])
        ])


        return df_str.iloc[::-1].to_dict(), df.iloc[::-1].to_dict(), [{"name": i, "id": i} for i in ['Features'] + sorted(df.columns)], go.Figure(d), title
    else :
        return None, None, None, go.Figure(), ''



@app.callback(Output('table_feature_imps', 'data'),
              [Input('table_feature_imps', 'sort_by'), Input('memory', 'data')])

def _sort_table(sort_by_col, data):
    df = pd.DataFrame(data = data)
    df = df[sorted(df.columns)]
    df.index.name = 'Features'
    df = df.reset_index()
    if sort_by_col is not None and len(sort_by_col):
        sorting = sort_by_col[0]
        ascending = (sorting['direction'] == 'asc')
        df = df.sort_values(sorting['column_id'], ascending = ascending)
    df = df.round(5)
    return df.to_dict('records')


@app.callback(Output('table_corr', 'data'),
              [Input('select correlation type', 'value'), Input('memory_no_str', 'data')])
def _change_corr_method(value, data):
    df = pd.DataFrame(data = data)
    df = df[sorted(df.columns)]
    corr_matrix = df.corr(method=value.lower())
    corr_matrix.index.name = 'Corr'
    corr_matrix = corr_matrix.reset_index().round(3)
    return corr_matrix.to_dict('record')
