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
    path = '/regional_trends'
)

layout = dbc.Container(
    [
        html.Div(
            [
                dbc.Col([               # master col
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
                                    clearable=True,
                                    multi=True,
                                    placeholder="Select Region(s)",
                                    className="custom-dropdown",
                                )
                            ], xs=12, sm=12, md=12, lg=6, xl=4),
                            dbc.Col([       # region dropdown
                                html.H3(
                                    "Unit of Assessment",
                                    className='subtitle-small',
                                ),
                                dcc.Dropdown(               # dropdown for uni filter
                                    id='uoa-dropdown',
                                    options=components.returnUoAOptions(),
                                    clearable=True,
                                    placeholder="Select Unit of Assessment",
                                    className="custom-dropdown",
                                )
                            ], xs=12, sm=12, md=12, lg=6, xl=4),
                            dbc.Col([       # gpa profile dropdown
                                html.H3(
                                    "GPA Profile",
                                    className='subtitle-small',
                                ),
                                dcc.Dropdown(               # dropdown for uni filter
                                    id='gpa-profile-dropdown',
                                    options=[
                                        {'label':'Overall', 'value':'Overall'},
                                        {'label':'Outputs', 'value':'Outputs'},
                                        {'label':'Environment', 'value':'Environment'},
                                        {'label':'Impact', 'value':'Impact'},
                                    ],
                                    value = 'Overall',
                                    clearable=True,
                                    placeholder="Select GPA Profile",
                                    className="custom-dropdown",
                                )
                            ], xs=12, sm=12, md=6, lg=3, xl=2),
                            dbc.Col([
                                    html.Div(
                                        dbc.Button(
                                            "Update Dashboard",
                                            className="btn-custom",
                                            id="reg-update-dashboard-btn",
                                        ),
                                        style={"display": "flex", 
                                                "flexDirection": "column", 
                                                "height": "100%", 
                                                "justifyContent": "flex-end"}
                                    ) 
                                ],xs=12, sm=12, md=6, lg=3, xl=2),
                        ])
                    ],className="filter-card"),
                    dbc.Row([           # master row
                        html.Div([              # div for trend graphs
                                html.Div([          # div for phd & inc
                                    dbc.Row([
                                        dbc.Col([       # col for phd trend
                                            dcc.Loading([
                                                dcc.Graph(
                                                    id = 'phd-trend-graph',
                                                    className='chart-card',
                                                    style={'height':'370px'}
                                                )
                                            ])
                                        ], xs=12, sm=12, md=6, lg=6, xl=4),
                                        dbc.Col([       # col for inc trend
                                            dcc.Loading([
                                                dcc.Graph(
                                                    id='inc-trend-graph',
                                                    className='chart-card',
                                                    style={'height':'370px'}
                                                )
                                            ])
                                        ], xs=12, sm=12, md=6, lg=6, xl=4),
                                        dbc.Col([       # col for gpa dist
                                            dcc.Loading([
                                                dcc.Graph(
                                                    id='gpa-dist-graph',
                                                    className='chart-card',
                                                    style={'height':'370px'}
                                                )
                                            ])
                                        ], xs=12, sm=12, md=6, lg=6, xl=4),
                                        dbc.Col([
                                            dcc.Loading([
                                                dcc.Graph(
                                                    id='gpa-phd-scatter-graph',
                                                    className='chart-card',
                                                    style={'height':'370px'}
                                                )
                                            ])
                                        ], xs=12, sm=12, md=6, lg=6, xl=4),
                                        dbc.Col([       # gpa vs income
                                            dcc.Loading([
                                                dcc.Graph(
                                                    id='gpa-inc-scatter-graph',
                                                    className='chart-card',
                                                    style={'height':'370px'}
                                                )
                                            ])
                                        ], xs=12, sm=12, md=6, lg=6, xl=4),
                                        dbc.Col([       # gpa vs income in kind
                                            dcc.Loading([
                                                dcc.Graph(
                                                    id='gpa-inc-ik-scatter-graph',
                                                    className='chart-card',
                                                    style={'height':'370px'}
                                                )
                                            ])
                                        ], xs=12, sm=12, md=6, lg=6, xl=4),
                                    ])
                                ]),
                                html.Div([
                                    dbc.Row([
                                        dbc.Col([       # col for income bar chart
                                            dcc.Loading([
                                                dcc.Graph(
                                                    id='inc-sankey-chart',
                                                    className='chart-card',
                                                    style={'height':'65vh'}
                                                )
                                            ])
                                        ], width=12),
                                    ])
                                ])
                            ], id='content-col', hidden=True),
                    ]),
                    dbc.Alert(
                        [
                            html.H4("Welcome to the Regional Trend Analysis Page.", className="alert-heading"),
                            html.P(
                                "Explore the research performance and trends across different regions in the U.K. "
                                "You will be able to compare the trends in PhD awards and income, GPA distribution and more.",
                            ),
                            html.Hr(),
                            html.P(
                                "To get started, choose the region/regions you would like to compare from the dropdown menu and choose the relevant filters. ",
                                className="mb-0",
                            ),
                        ], 
                        color="light",
                        id = "ins-ov-info",
                    ),
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
    Output("content-col", 'hidden'),
    Output("reg-ov-alert-msg", "children"), 
    Output("reg-ov-alert-msg", "is_open"),
    Output('reg-update-dashboard-btn', 'disabled'),
    Input("reg-update-dashboard-btn", 'n_clicks'),
    State("region-dropdown", "value"),
    State('uoa-dropdown', 'value'),
    prevent_initial_call = True
)
def showCardsAndDisableUpdateButton(n_clicks, region, uoa):
    if (region == None or region == []) and (uoa is None):
        return True, "Please select at least ONE(1) Region and a Unit of Assessment.", True, False
    elif (region == None or region == []):
        return True, 'Please select at least ONE(1) Region', True, False
    elif (uoa is None):
        return True, 'Please select a Unit of Assessment', True, False
    else:
        return False, "", False, True  # Hide alert & disabled update dashboard btn when valid
    
@callback(
    Output("reg-update-dashboard-btn", "disabled", allow_duplicate=True),
    Input("region-dropdown", "value"),
    Input("uoa-dropdown", 'value'),
    Input('gpa-profile-dropdown', 'value'),
    prevent_initial_call=True
)
def enableUpdateButton(region, uoa, gpa_profile):
    return False  # Re-enable button when dropdown changes

@callback(
    Output("phd-trend-graph", "figure"),
    Output("inc-trend-graph", "figure"),
    Output("gpa-dist-graph", 'figure'),
    Output('gpa-phd-scatter-graph', 'figure'),
    Output('gpa-inc-scatter-graph', 'figure'),
    Output('gpa-inc-ik-scatter-graph', 'figure'),
    Output("inc-sankey-chart", "figure"),
    Output('content-col', 'hidden', allow_duplicate=True),
    Input("reg-update-dashboard-btn", "n_clicks"),
    State('region-dropdown', 'value'),
    State('uoa-dropdown', 'value'),
    State('gpa-profile-dropdown', 'value'),
    prevent_initial_call = True
)
def updatePage(n_clicks, region, uoa, gpa_profile):
    if region == None or region == [] or uoa is None:
        raise dash.exceptions.PreventUpdate
    return(
        components.generateRegionLineCharts('phd', region, uoa),
        components.generateRegionLineCharts('income', region, uoa),
        components.generateRegionGPADist(region, uoa, gpa_profile),
        components.generateRegionScatterPlots('phd', region, uoa, gpa_profile),
        components.generateRegionScatterPlots('income', region, uoa, gpa_profile),
        components.generateRegionScatterPlots('incomeik', region, uoa, gpa_profile),
        components.generateRegionIncomeSankey(region, uoa),
        False
    )