import dash
from dash import callback, html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import io
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import utils.dashboard_components as components
  

# read in datasets
results_df = pd.read_csv('data/results_cleaned.csv')
income_df = pd.read_csv('data/income_cleaned.csv')
incomeiK_df = pd.read_csv('data/incomeiK_cleaned.csv')
phd_df = pd.read_csv('data/phd_awarded_cleaned.csv')
regions_df = pd.read_csv('data/regions.csv')

dash.register_page(
    module= __name__,
    external_stylesheets = [dbc.themes.BOOTSTRAP, 'assets/style.css'],
    path = '/regional_overview'
)

layout = dbc.Container(
    [
        html.Div(
            [
                dbc.Col([               # master col
                    dbc.Row([           # master row
                        dbc.Col([       # left col
                            html.Div([      # div for region dropdown & update btn
                                dbc.Row([
                                    dbc.Col([       # region dropdown
                                        html.H3(
                                            "Region(s)",
                                            className='subtitle-small',
                                        ),
                                        dcc.Dropdown(               # dropdown for uni filter
                                            id='region-dropdown',
                                            options=[
                                                {"label":"London", "value":"London"},
                                                {"label":"South West", "value":"South West"},
                                                {"label":"South East", "value":"South East"},
                                                {"label":"East of England", "value":"East of England"},
                                                {"label":"West Midlands", "value":"West Midlands"},
                                                {"label":"East Midlands", "value":"East Midlands"},
                                                {"label":"North West", "value":"North West"},
                                                {"label":"North East", "value":"North East"},
                                                {"label":"Yorkshire and The Humber", "value":"Yorkshire and The Humber"},
                                                {"label":"Northern Ireland", "value":"Northern Ireland"},
                                                {"label":"Wales", "value":"Wales"},
                                                {"label":"Scotland", "value":"Scotland"},
                                            ],
                                            value="All",
                                            clearable=True,
                                            multi=True,
                                            placeholder="Select Region(s)",
                                            className="custom-dropdown",
                                        )
                                    ], width=10),
                                    dbc.Col([
                                        dbc.Button(
                                            "Update Dashboard",
                                            className="btn-custom",
                                            id="reg-update-dashboard-btn",
                                            disabled=False
                                        )
                                    ], width=2),
                                ])
                            ],className="filter-card"),
                            html.Div([              # div for trend graphs
                                html.Div([          # div for phd & inc ik
                                    dbc.Row([
                                        dbc.Col([       # col for phd trenc
                                            dcc.Loading([
                                                dcc.Graph(
                                                    id = 'phd-trend-graph',
                                                    className='chart-card',
                                                    style={'height':'370px'}
                                                )
                                            ])
                                        ], width=6),
                                        dbc.Col([       # col for inc ik trend
                                            dcc.Loading([
                                                dcc.Graph(
                                                    id='inc-ik-trend-graph',
                                                    className='chart-card',
                                                    style={'height':'370px'}
                                                )
                                            ])
                                        ], width=6),
                                    ])
                                ], style={"margin-bottom":"1rem"}),
                                html.Div([          # div for gpa dist & gpa v. phds scatter
                                    dbc.Row([
                                        dbc.Col([       # col for gpa dist
                                            dcc.Loading([
                                                dcc.Graph(
                                                    id='gpa-dist-graph',
                                                    className='chart-card',
                                                    style={'height':'370px'}
                                                )
                                            ])
                                        ], width=6),
                                        dbc.Col([
                                            dcc.Loading([
                                                dcc.Graph(
                                                    id='gpa-phd-scatter-graph',
                                                    className='chart-card',
                                                    style={'height':'370px'}
                                                )
                                            ])
                                        ], width=6)
                                    ])
                                ], style={"margin-bottom":"1rem"})
                            ], id='reg-left-col', hidden=True)
                        ], width=6),
                        dbc.Col([       # right col
                            html.Div([      # div for right col
                                html.Div([          # div for scatter plots 2
                                    html.Div([      # div for gpa vs income & gpa vs income in kind
                                        dbc.Row([
                                            dbc.Col([       # gpa vs income
                                                dcc.Loading([
                                                    dcc.Graph(
                                                        id='gpa-inc-scatter-graph',
                                                        className='chart-card',
                                                        style={'height':'370px'}
                                                    )
                                                ])
                                            ], width=6),
                                            dbc.Col([       # gpa vs income in kind
                                                dcc.Loading([
                                                    dcc.Graph(
                                                        id='gpa-inc-ik-scatter-graph',
                                                        className='chart-card',
                                                        style={'height':'370px'}
                                                    )
                                                ])
                                            ], width=6),
                                        ])
                                    ], style={"margin-bottom":"1rem"}),
                                ]),
                                html.Div([          # div for income bar chart
                                    dbc.Row([
                                        dbc.Col([       # col for income bar chart
                                            dcc.Loading([
                                                dcc.Graph(
                                                    id='inc-sankey-chart',
                                                    className='chart-card',
                                                    style={'height':'53.8vh'}
                                                )
                                            ])
                                        ], width=12),
                                    ])
                                ], style={"margin-bottom":"1rem"})
                            ], id='reg-right-col', hidden=True),
                        ])
                    ]),
                    dbc.Alert(
                        id='reg-ov-alert-msg',
                        is_open=False,
                        color='danger'
                    ),
                ], width=12),                
            ],
            className="page-content"
        )
    ],
    fluid=True,
)

@callback(
    Output("reg-left-col", 'hidden'),
    Output("reg-right-col", 'hidden'),
    Output("reg-ov-alert-msg", "children"), 
    Output("reg-ov-alert-msg", "is_open"),
    Output('reg-update-dashboard-btn', 'disabled'),
    Input("reg-update-dashboard-btn", 'n_clicks'),
    State("region-dropdown", "value"),
    prevent_initial_call = True
)
def showCardsAndDisableUpdateButton(n_clicks, region):
    if region == None or region == []:
        return True, True, "Please select at least ONE(1) Region.", True, False
    else:
        return False, False, "", False, True  # Hide alert & disabled update dashboard btn when valid
    
@callback(
    Output("reg-update-dashboard-btn", "disabled", allow_duplicate=True),
    Input("region-dropdown", "value"),
    prevent_initial_call=True
)
def enableUpdateButton(region):
    return False  # Re-enable button when dropdown changes

@callback(
    Output("phd-trend-graph", "figure"),
    Output("inc-ik-trend-graph", "figure"),
    Output("gpa-dist-graph", 'figure'),
    Output('gpa-phd-scatter-graph', 'figure'),
    Output('gpa-inc-scatter-graph', 'figure'),
    Output('gpa-inc-ik-scatter-graph', 'figure'),
    Output("inc-sankey-chart", "figure"),
    Output('reg-left-col', 'hidden', allow_duplicate=True),
    Output('reg-right-col', 'hidden', allow_duplicate=True),
    Input("reg-update-dashboard-btn", "n_clicks"),
    State('region-dropdown', 'value'),
    prevent_initial_call = True
)
def updatePage(n_clicks, region):
    if region == None or region == []:
        raise dash.exceptions.PreventUpdate
    return(
        components.generateRegionLineCharts('phd', region),
        components.generateRegionLineCharts('incomeik', region),
        components.generateRegionGPADist(region),
        components.generateRegionScatterPlots('phd', region),
        components.generateRegionScatterPlots('income', region),
        components.generateRegionScatterPlots('incomeik', region),
        components.generateRegionIncomeSankey(region),
        False, False
    )