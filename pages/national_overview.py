import dash
from dash import callback, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import utils.dashboard_components as components
import json

# read in datasets
results_df = pd.read_csv('data/results_cleaned.csv')
income_df = pd.read_csv('data/income_cleaned.csv')
incomeiK_df = pd.read_csv('data/incomeiK_cleaned.csv')
phd_df = pd.read_csv('data/phd_awarded_cleaned.csv')

dash.register_page(
    module= __name__,
    external_stylesheets = [dbc.themes.BOOTSTRAP, 'assets/style.css'],
    path = '/national_overview'
)

layout = dbc.Container(
    [
        html.Div(
            [
                html.H2(
                    "Research Quality in the U.K.",
                    className="title",
                    style={'color':'#800080'}
                ),
                html.Br(),
                dbc.Row([           # master row
                    dbc.Col([       # kpi & leaderboard 
                        dbc.Row([       # kpi row 1
                            dbc.Col([         # no. of institutions
                                html.Div(
                                    components.generateKPICard(
                                        "Submissions from",
                                        '157',
                                        'Institutions',
                                        'sub-from',
                                        'Number of HEIs which made submissions to REF 2021.'
                                    ),
                                    style={"height": "130px"},
                                    className='card card-body ranking-card'
                                )
                            ], xs=12, sm=12, md=6, lg=4, xl=4),
                            dbc.Col([          # no. of submissions 
                                html.Div(
                                    components.generateKPICard(
                                        "Total of",
                                        '1,878',
                                        'Submissions',
                                        'sub-no',
                                        'Number of submissions made to REF 2021.'
                                    ),
                                    style={"height": "130px"},
                                    className='card card-body ranking-card'
                                )
                            ], xs=12, sm=12, md=6, lg=4, xl=4),
                            dbc.Col([           # no. of outputs
                                html.Div(
                                    components.generateKPICard(
                                        "Total of",
                                        '185,594',
                                        'Outputs',
                                        'output-no',
                                        'Number of outputs submitted to REF 2021.'
                                    ),
                                    style={"height": "130px"},
                                    className='card card-body ranking-card'
                                )
                            ], xs=12, sm=12, md=6, lg=4, xl=4)
                        ]),
                        dbc.Row([
                            dbc.Col([           # total income
                                html.Div(
                                    components.generateKPICard(
                                        "Research Income",
                                        '£42.1B',
                                        "13'-20' (total)",
                                        'research-inc',
                                        'Total research funding (non-in-kind) received by all institutions in the country from 2013-2020.'
                                    ),
                                    style={"height": "130px"},
                                    className='card card-body ranking-card'
                                )
                            ], xs=12, sm=12, md=6, lg=4, xl=4),
                            dbc.Col([           # staff fte
                                html.Div(
                                    components.generateKPICard(
                                        "Staff FTE",
                                        '76.1K',
                                        "13'-19' (total)",
                                        'staff-fte',
                                        'Full-time equivalent of all staff with significant responsibility for research. Total across all institutions in the country from 2013-2019.'
                                    ),
                                    style={"height": "130px"},
                                    className='card card-body ranking-card'
                                )
                            ], xs=12, sm=12, md=6, lg=4, xl=4),
                            dbc.Col([           # phds awarded
                                html.Div(
                                    components.generateKPICard(
                                        "PhDs Awarded",
                                        '162.1K',
                                        "13'-20' (total)",
                                        'phd',
                                        'Total number of research doctoral degrees awarded by all institutions in the country from 2013 to 2020'
                                    ),
                                    style={"height": "130px"},
                                    className='card card-body ranking-card'
                                )
                            ], xs=12, sm=12, md=6, lg=4, xl=4)
                        ]),
                        dbc.Row([               # selection & leaderboard
                            dbc.Col([
                                dbc.Row([       
                                    html.Div([
                                        html.Div(           # selection
                                            dcc.Dropdown(
                                                options=[
                                                    {'label':'Overall GPA', 'value':'Overall GPA'},
                                                    {'label':'Outputs GPA', 'value':'Outputs GPA'},
                                                    {'label':'Environment GPA', 'value':'Environment GPA'},
                                                    {'label':'Impact GPA', 'value':'Impact GPA'},
                                                    {'label':'Income', 'value':'Income'},
                                                    {'label':'Income In-Kind', 'value':'Income In-Kind'},
                                                    {'label':'PhDs Awarded', 'value':'PhDs Awarded'},
                                                    {'label':'Staff FTE', 'value':'Staff FTE'},
                                                ],
                                                value = 'Overall GPA',
                                                style={'width':'60%'},
                                                id = 'leaderboard-dropdown',
                                            ),
                                            className='filter-card',
                                            style={'margin-bottom':'0', 
                                                'border-bottom-right-radius':'0', 
                                                'border-bottom-left-radius':'0', }
                                        ),
                                        html.Div(           # leaderboard
                                            id = 'leaderboard',
                                        )
                                    ])
                                ])
                            ])
                        ])
                    ]),
                    dbc.Col([       # selection & map
                        dbc.Row([  
                            html.Div([
                                html.Div(       # selection
                                    dcc.Dropdown(
                                        options=[
                                            {'label':'Overall GPA', 'value':'Overall GPA'},
                                            {'label':'Outputs GPA', 'value':'Outputs GPA'},
                                            {'label':'Environment GPA', 'value':'Environment GPA'},
                                            {'label':'Impact GPA', 'value':'Impact GPA'},
                                            {'label':'Income', 'value':'Income'},
                                            {'label':'Income In-Kind', 'value':'Income In-Kind'},
                                            {'label':'PhDs Awarded', 'value':'PhDs Awarded'},
                                            {'label':'Staff FTE', 'value':'Staff FTE'},
                                        ],
                                        value = 'Overall GPA',
                                        style={'width':'60%'},
                                        id = 'map-dropdown',
                                    ),
                                    className='filter-card',
                                    style={'margin-bottom':'0', 
                                           'border-bottom-right-radius':'0', 
                                           'border-bottom-left-radius':'0', }
                                ),
                                dcc.Graph(          # map
                                    id="region-map",
                                    config={"displayModeBar": False},
                                    className="chart-card",
                                    style={"height": "89.5vh",
                                            'border-top-right-radius':'0', 
                                            'border-top-left-radius':'0'},
                                ),
                            ]),
                        ])
                    ])
                ])
            ],
            className="page-content"
        )
    ],
    fluid=True,
)

@callback(
    Output("leaderboard", "children"),
    Input("leaderboard-dropdown", "value"),
)
def generateLeaderboard(filter):
    if filter == 'Overall GPA':
        df = results_df[results_df['Profile'] == 'Overall']
        df = df.groupby('Institution name').agg({'GPA':'mean'}).reset_index()
        df = df.sort_values(by='GPA', ascending=False)
        col_label = 'GPA'
    elif filter == 'Outputs GPA':
        df = results_df[results_df['Profile'] == 'Outputs']
        df = df.groupby('Institution name').agg({'GPA':'mean'}).reset_index()
        df = df.sort_values(by='GPA', ascending=False)
        col_label = 'GPA'
    elif filter == 'Impact GPA':
        df = results_df[results_df['Profile'] == 'Impact']
        df = df.groupby('Institution name').agg({'GPA':'mean'}).reset_index()
        df = df.sort_values(by='GPA', ascending=False)
        col_label = 'GPA'
    elif filter == 'Environment GPA':
        df = results_df[results_df['Profile'] == 'Environment']
        df = df.groupby('Institution name').agg({'GPA':'mean'}).reset_index()
        df = df.sort_values(by='GPA', ascending=False)
        col_label = 'GPA'
    elif filter == 'Income':
        df = income_df[income_df['Income source'] != 'Total income']
        df = df.groupby('Institution name').agg({'2013-2020 (total)':'sum'}).reset_index()
        df = df.sort_values(by='2013-2020 (total)', ascending=False)
        col_label = 'Income'
    elif filter == 'Income In-Kind':
        df = incomeiK_df[incomeiK_df['Income source'] != 'Total income']
        df = df.groupby('Institution name').agg({'2013-2020 (total)':'sum'}).reset_index()
        df = df.sort_values(by='2013-2020 (total)', ascending=False)
        col_label = 'Income In-Kind'
    elif filter == 'PhDs Awarded':
        df = phd_df.groupby('Institution name').agg({'Total':'sum'}).reset_index()
        df = df.sort_values(by='Total', ascending=False)
        col_label = 'Total'
    elif filter == 'Staff FTE':
        df = results_df[results_df['Profile'] == 'Overall']
        df = df.groupby('Institution name').agg({'FTE staff':'sum'}).reset_index()
        col_label = 'Staff FTE'

    leaderboard = components.create_leaderboard(
        f"Top 10 Institutions for {filter}",
        df,      
        col_label,
    )

    return leaderboard

@callback(
    Output('region-map', 'figure', allow_duplicate=True),
    Input('map-dropdown', 'value'),
    prevent_initial_call='initial_duplicate'
)
def generateRegionMap(filter):
    df = components.generateDataFrameForMap(filter, 'All')

    fig = components.generateMap(df, filter)

    return fig