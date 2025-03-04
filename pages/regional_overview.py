import dash
from dash import callback, html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.dashboard_components import create_card, format_value, generateMap

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
        html.Div(
            [
                html.H2(
                    "Regional Overview",
                    className="title",
                ),
                html.Br(),
                dbc.Row(            # row for filters?
                    [
                        dbc.Col(    # search and select unis (dropdown)

                        ),
                        dbc.Col(    # show selected unis (dialog)
                                        
                        ),
                    ]
                ),
                html.Br(),
                dbc.Row([            # row for set of graphs 1
                    dbc.Col(        # col for filters
                        [
                            html.Div(
                                [
                                    html.H6(
                                        "Data Selection"
                                    ),
                                    dcc.Dropdown(
                                        options=[
                                            "GPA",
                                            "Income",
                                            "Income In-Kind",
                                            "PhDs Awarded",
                                            "Staff FTE"
                                        ],
                                        id="map-data-selection",
                                        placeholder="Select Data"
                                    ),
                                    html.Div(
                                        dcc.Dropdown(
                                            id='period-selection',
                                            placeholder="Select Period"
                                        ),
                                        id="period-selection-div",
                                        hidden=True
                                    ),
                                    html.Div(
                                        dcc.Dropdown(
                                            id='uoa-selection',
                                            options = [
                                                {'label': "All UoAs", 'value': "All"}
                                                ]
                                                +[
                                                {'label': col, 'value': col}
                                                for col in sorted(
                                                    results_df["UOA name"].unique()
                                                )
                                            ],
                                            placeholder="Select UOA"
                                        ),
                                        id="uoa-selection-div",
                                        hidden=True
                                    ),
                                    html.Br(),
                                    html.Button(
                                        "Apply Selection",
                                        id="apply-filters",
                                        className="btn-custom",
                                    )
                                ],
                                className="filter-card"
                            ), 
                        ],
                        width=4,
                    ),
                    # dbc.Col(        # col for plots
                    #     [

                    #     ],
                    #     width=4,
                    # )
                ]),
                html.Br(),
                dbc.Row(            # row for set of graphs 2
                    dbc.Col(
                        [
                            dcc.Loading(
                                id="region-map",
                                children=[

                                ]
                            ), 
                        ],
                        width=6
                    )
                ),
            ],
            className="page-content"
        )
    ],
    fluid=True,
)

@callback(
    Output("region-map", "children"),
    Input("apply-filters", "n_clicks"),
    State("map-data-selection", "value"),
    State("uoa-selection", "value"),
    State("period-selection", "value"),
    prevent_initial_call = True
)
def buildMap(n_clicks, mapdata, uoa, period):
    figure = generateMap(mapdata, uoa, period)
    graphcomponent = [
        dcc.Graph(
            figure=figure,
            config={"displayModeBar": False},
            className="chart-card",
            style={"height": "700px"},
            )
    ]
    return graphcomponent

@callback(
    Output("period-selection-div", "hidden"),
    Output("uoa-selection-div", "hidden"),
    Input("map-data-selection", "value"),
    prevent_initial_call = True
)
def displayFilters(mapdata):
    if (mapdata == "GPA") or (mapdata == "Staff FTE"):
        return True, False
    else:
        return False, False

@callback(
    Output("period-selection", "options"),
    Input("map-data-selection", "value"),
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
                "2013-2020 (total)",
                "2013-2020 (avg)"]
    
    else:
        return []