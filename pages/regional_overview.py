import dash
from dash import callback, html, dcc, Input, Output, State, ctx
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.dashboard_components import (
    returnUoAOptions,
    generateMap,
    generateScatter,
    generateDataFrameForScatter,
    create_leaderboard
)
  

# read in datasets
results_df = pd.read_csv('data/results_cleaned.csv')
income_df = pd.read_csv('data/income_cleaned.csv')
incomeiK_df = pd.read_csv('data/incomeiK_cleaned.csv')
phd_df = pd.read_csv('data/phd_awarded_cleaned.csv')

dash.register_page(
    module= __name__,
    external_stylesheets = [dbc.themes.BOOTSTRAP, 'assets/style.css'],
    path = '/regional_overview'
)

layout = dbc.Container(
    [
        dcc.Store(
            id="missing-fields-store", 
            storage_type="memory"
        ),
        dcc.Store(
            id="current-df", 
            storage_type="memory"
        ),
        html.Div(
            [
                html.H1("Regional Overview",
                    className="subtitle-medium",
                    id="page-title",
                ),
                html.H1(
                    className="title",
                    id="data-title"
                ),
                dbc.Row([           # row for titles
                    dbc.Col(html.Div("of institutions in", className="subtitle-small", id = "subs-1", hidden=True), width="auto"),
                    dbc.Col(html.Div(className="subtitle-small-color", id="region-subtitle"), width="auto"),
                    dbc.Col(html.Div("for",className="subtitle-small",id = "subs-2",hidden=True), width="auto"),
                    dbc.Col(html.Div(className="subtitle-small-color",id="uoa-subtitle"), width="auto"),
                    dbc.Col(html.Div("in the period of",id="subs-3",className="subtitle-small",hidden=True), width="auto"),
                    dbc.Col(html.Div(className="subtitle-small-color",id="period-subtitle"), width="auto"),
                ], align="center"),
                html.Br(),
                html.Div(               # div for filters
                    children=[
                        dbc.Row(            # row for filters?
                            [
                                dbc.Col([    # search and select unis (dropdown)
                                    html.Header(
                                        "Data",
                                        className="subtitle-small",
                                    ),
                                    dcc.Dropdown(
                                        options=[
                                            "GPA",
                                            "Income",
                                            "Income In-Kind",
                                            "PhDs Awarded",
                                            "Staff FTE"
                                        ],
                                        id="data-selection",
                                        placeholder="Select Data"
                                    ),
                                ],
                                width=3
                                ),
                                dbc.Col([
                                    html.Header(
                                        "Unit of Assessment"
                                    ),  
                                    dcc.Dropdown(
                                        options = returnUoAOptions(),
                                        id='uoa-selection',
                                        placeholder="Please select Data to view options",
                                        disabled=True,
                                    ),
                                ],
                                width=3
                                ),
                                dbc.Col([    
                                    html.Header(
                                        "Period"
                                    ),
                                    dcc.Dropdown(
                                        id='period-selection',
                                        placeholder="Please select Data to view options",
                                        disabled=True,
                                    ),               
                                ],
                                width=3
                                ),
                                dbc.Col([    
                                    html.Header(
                                        "Region"
                                    ),
                                    dcc.Dropdown(
                                        options=[
                                            {"label":"All Regions", "value":"All"},
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
                                            {"label":"Scotland", "value":"All"},
                                        ],
                                        id='region-selection',
                                        placeholder="Please select Data to view options",
                                        disabled=True,
                                    ),               
                                ],
                                width=3
                                ),
                            ]
                        ),
                        html.Div([
                            dbc.Row(
                                dbc.Col([
                                    html.Label("Aggregate Function", style={"margin-right": "10px"}),
                                    dcc.Dropdown(
                                        id="agg-func",
                                        options=[
                                            {'label': 'Sum', 'value': 'sum'},
                                            {'label': 'Median', 'value': 'median'},
                                            {'label': 'Mean', 'value': 'mean'},
                                        ],
                                        placeholder="Select Aggregate Function"
                                    )], 
                                    width=3
                                ),
                            ),
                        ],
                        style={"align-items": "center", "margin-top": "10px"},
                        id="agg-func-div",
                        hidden=True
                        ),
                        html.Br(),
                        html.Div(
                            html.Button(
                                "Apply Selection",
                                id="apply-filters-btn",
                                className="btn-custom",
                            ),
                            style={"display": "flex", "justify-content": "flex-end"}
                        ),
                    ],
                    className="filter-card"
                ),
                html.Br(),
                dbc.Alert(
                    id="alert-msg",
                    is_open=False,
                    color="danger"
                ),
                dbc.Row([            # row for metrics
                    html.Div(
                        dbc.Col(
                            id = "leaderboard",
                            width=6,
                        ),
                        id = "leaderboard-div",
                        hidden = True,
                    ),
                ]),
                html.Br(),
                dbc.Row([            # row for graphs
                    dbc.Col(        # map
                        [
                            dcc.Loading(
                                [
                                    html.Div(
                                        dcc.Graph(
                                            id="region-map",
                                            config={"displayModeBar": False},
                                            className="chart-card",
                                            style={"height": "700px"},
                                        ),
                                        id="region-map-div",
                                        hidden=True
                                    ),
                                ]
                            ), 
                        ],
                        width=6
                    ),
                    dbc.Col(        # scatter plots 
                        [
                            dcc.Loading(        # plot of data vs time
                                [
                                    html.Div([
                                        dcc.Graph(
                                            id="scatter-plot",
                                            config={"displayModeBar": False},
                                            className="chart-card",
                                            style={"height": "700px"},
                                        ),
                                        html.Div([
                                            html.Label("X-Axis Scale:", style={"font-weight": "bold", "margin-right": "10px"}),
                                            dcc.RadioItems(
                                                id="xaxis-scale",
                                                options=[
                                                    {'label': 'Linear', 'value': 'linear'},
                                                    {'label': 'Log', 'value': 'log'}
                                                ],
                                                value='linear',  # Default value
                                                labelStyle={'display': 'inline-block', 'margin-right': '10px'}
                                            ),
                                        ], 
                                        style={"display": "flex", "align-items": "center", "margin-top": "10px"},
                                        id="scatter-plot-config-div",
                                        className="filter-card"
                                        ),
                                    ],
                                    id="scatter-plot-div",
                                    hidden=True
                                    ),
                                ]
                            ),
                        ]
                    )

                ]),
            ],
            className="page-content"
        )
    ],
    fluid=True,
)

@callback(
    Output("data-title", "children"),
    Output("region-subtitle", "children"),
    Output("uoa-subtitle", "children"),
    Output("period-subtitle", "children"),
    Output("subs-1", "hidden"),
    Output("subs-2", "hidden"),
    Output("subs-3", "hidden"),
    Input("missing-fields-store", "data"),
    Input("apply-filters-btn", "n_clicks"),
    State("data-selection", "value"),
    State("uoa-selection", "value"),
    State("period-selection", "value"),
    State("region-selection", "value"),
    prevent_initial_call = True,
)
def updateHeadings(missing_fields, n_clicks, data, uoa, period, region):
    if missing_fields:
        return dash.no_update

    hide_subs1 = False
    hide_subs2 = False
    hide_subs3 = True
    if uoa == "All":
        uoa = "All UoAs"
    if region == "All":
        region = "All Regions"
    if period != None:
        hide_subs3 = False

    return data, region, uoa, period, hide_subs1, hide_subs2, hide_subs3

@callback(
    Output("xaxis-scale", "value"),
    Input("apply-filters-btn", "n_clicks"),
    prevent_initial_call = True
)
def resetXAxisScaleWhenFiltersApplied(n_clicks):
    return "linear"

@callback(
    Output("region-map", "figure"),
    Output("region-map-div", "hidden"),
    Output("scatter-plot", "figure"),
    Output("scatter-plot-div", "hidden"),
    Output("leaderboard", "children"),
    Output("leaderboard-div", "hidden"),
    Output("alert-msg", "children"),
    Output("alert-msg", "is_open"),
    Output("missing-fields-store", "data"),
    Input("apply-filters-btn", "n_clicks"),
    State("data-selection", "value"),
    State("uoa-selection", "value"),
    State("period-selection", "value"),
    State("region-selection", "value"),
    State("agg-func", "value"),
    State("agg-func-div", "hidden"),
    prevent_initial_call = True
)
def validateDropdownsAndGenerateDataViz(n_clicks, data, uoa, period, region, aggfunc, aggfunc_hidden):
    missing_fields = []
    
    if not data:
        missing_fields.append("Data")
    if not uoa:
        missing_fields.append("Unit of Assessment")
    if not period and data != "GPA" and data != "Staff FTE":
        missing_fields.append("Period")
    if not region:
        missing_fields.append("Region")
    if not aggfunc_hidden and not aggfunc:
        missing_fields.append("Aggregate Function")

    if missing_fields:
        missing_fields_msg = "The following fields are empty: " + ", ".join(missing_fields)
        return {}, True, {}, True, {}, True, missing_fields_msg, True, missing_fields
    
    if data == "GPA":
        aggfunc = "mean"

    df = generateDataFrameForScatter(data, uoa, period, region, aggfunc)
    mapfig = generateMap(data, uoa, period, aggfunc)
    scatterfig = generateScatter(df, data, uoa, period, region, aggfunc)

    if data == "Staff FTE":
        col_data = "FTE staff"
    if data == "GPA":
        col_data = data
    if data in ["Income", "Income In-Kind", "PhDs Awarded"]:
        col_data = period

    leaderboard = create_leaderboard(
        "Ranking",
        5,
        df, 
        col_data,
    )

    return mapfig, False, scatterfig, False, leaderboard, False, "", False, missing_fields
    

@callback(
    Output("scatter-plot", "figure", allow_duplicate=True),
    Input("xaxis-scale", "value"),
    State("scatter-plot", "figure"),
    prevent_initial_call = True
)
def updateXAxis(scale, fig):
    if not fig:
        return dash.no_update

    fig["layout"]["xaxis"]["type"] = scale

    return fig

@callback(
    Output("uoa-selection", "disabled"),
    Output("period-selection", "disabled"),
    Output("region-selection", "disabled"),
    Output("uoa-selection", "placeholder"),
    Output("period-selection", "placeholder"),
    Output("region-selection", "placeholder"),
    Output("agg-func-div", "hidden"),
    Input("data-selection", "value"),
    prevent_initial_call = True
)
def displayFilters(mapdata):
    aggfunc = False
    if not mapdata:
        placeholder = "Please select Data to view options"
        return True, True, True, placeholder, placeholder, placeholder, True
    if (mapdata == "GPA") or (mapdata == "Staff FTE"):
        if (mapdata == "GPA"):
            aggfunc = True
        return False, True, False, "Select UoA", "Not Applicable", "Select Region", aggfunc
    else:
        return False, False, False, "Select UoA", "Select Period", "Select Region", aggfunc

@callback(
    Output("period-selection", "options"),
    Input("data-selection", "value"),
    prevent_initial_call = True
)
def displayAvailablePeriodsForData(mapdata):
    if mapdata == "PhDs Awarded":
        return ["2013",
                "2014",
                "2015",
                "2016",
                "2017",
                "2018",
                "2019",
                "Total",
                "Average",
                ]
    
    elif mapdata == "Income":
        return ["2013-14",
                "2014-15",
                "2015-2020 (avg)",
                "2013-2020 (avg)",
                "2013-2020 (total)"]
    
    elif mapdata == "Income In-Kind":
        return ["2013-14",
                "2014-15",
                "2015-16",
                "2016-17",
                "2017-18",
                "2018-19",
                "2019-20",
                "2013-2020 (avg)",
                "2013-2020 (total)"]
    else:
        return []