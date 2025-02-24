import dash
from dash import callback, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import utils.dashboard_components as components

# read in datasets
results_df = pd.read_csv('data/results_cleaned.csv')
income_df = pd.read_csv('data/income_cleaned.csv')
incomeiK_df = pd.read_csv('data/incomeiK_cleaned.csv')
phd_df = pd.read_csv('data/phd_awarded_cleaned.csv')

dash.register_page(
    module= __name__,
    external_stylesheets = [dbc.themes.BOOTSTRAP, 'assets/style.css'],
    path = '/institution_overview'
)

# layout
layout = dbc.Container(
    [
        html.Div(
            [
                html.H1(
                    'Institution Overview',
                    className='subtitle-medium',
                    id='page-title'
                ),
                html.H1(
                    '',
                    className='title',
                    id='uni-name-heading',

                ),
                html.H1(
                    '',
                    className='subtitle-small-color',
                    id='uoa-name-subheading',
                ),
                html.Br(),
                dbc.Row(            # row for dropdown
                    [
                        dbc.Col(
                            [
                                html.H3(
                                    "Institution",
                                    className='subtitle-small',
                                ),
                                dcc.Dropdown(               # dropdown for uni filter
                                    id='uni-dropdown',
                                    options=[
                                        {"label": col, "value": col}
                                        for col in sorted(
                                            results_df["Institution name"].unique()
                                        )
                                    ],
                                    value="All",
                                    clearable=True,
                                    multi=False,            # can extend to be multi-select
                                    placeholder="Select Institution",
                                    className="custom-dropdown",
                                ),
                            ],
                            width = 3,
                        ),
                        dbc.Col(
                            [
                                html.H3(
                                    "Unit of Assessment",
                                    className='subtitle-small',
                                ),
                                dcc.Dropdown(               # dropdown for uoa filter
                                    id='uoa-dropdown',
                                    options=[],
                                    value="All",
                                    clearable=True,
                                    multi=False,            # can extend to be multi-select
                                    placeholder="Select Unit of Assessment",
                                    className="custom-dropdown",
                                ),
                            ],
                            width=3,
                        ),
                    ]
                ),
                html.Br(),
                dbc.Row(                # row for cards
                    [
                        dbc.Col(        # overall score col
                            components.create_card("Overall Quality (GPA)", "overall-card", "fa-ranking-star"),
                            width=3,
                        ),
                        dbc.Col(        # outputs score col
                            components.create_card("Outputs Quality (GPA)", "outputs-card", "fa-file"),
                            width=3,
                        ), 
                        dbc.Col(        # impact score col
                            components.create_card("Impact Quality (GPA)", "impact-card", "fa-users"),
                            width=3,
                        ),
                        dbc.Col(        # env score col
                            components.create_card("Environment Quality (GPA)", "env-card", "fa-seedling"),
                            width=3,
                        ),
                    ]
                ),
                html.Br(),
                dbc.Row(                # row for plots
                    [
                        dbc.Col(        # avg research income plot
                            dcc.Loading(
                                dcc.Graph(
                                    id="income-chart",
                                    config={"displayModeBar": False},
                                    className="chart-card",
                                    style={"height": "400px"},
                                ),
                                type="circle",
                                color="#000000",
                            ),
                            width=4,
                        ),
                        dbc.Col(        # research income in-kind plot
                            dcc.Loading(
                                dcc.Graph(
                                    id="income-ik-chart",
                                    config={"displayModeBar": False},
                                    className="chart-card",
                                    style={"height": "400px"},
                                ),
                                type="circle",
                                color="#000000",
                            ),
                            width=4,
                        ),
                        dbc.Col(        # phd awarded plot
                            dcc.Loading(
                                dcc.Graph(
                                    id="phd-awarded-chart",
                                    config={"displayModeBar": False},
                                    className="chart-card",
                                    style={"height": "400px"},
                                ),
                                type="circle",
                                color="#000000",
                            ),
                            width=4,
                        )
                    ]
                ),
                html.Br(),
                dbc.Row(                # row for income breakdowns
                    [
                        dbc.Col(        # income category treemap
                            dcc.Loading(
                                dcc.Graph(
                                    id="income-cat-chart",
                                    config={"displayModeBar": False},
                                    className="chart-card",
                                    style={"height": "450px"},
                                ),
                                type="circle",
                                color="#000000",
                            ),
                            width=8,
                        ),
                        dbc.Col(        # income in-kind category treemap
                            dcc.Loading(
                                dcc.Graph(
                                    id="income-ik-cat-chart",
                                    config={"displayModeBar": False},
                                    className="chart-card",
                                    style={"height": "450px"},
                                ),
                                type="circle",
                                color="#000000",
                            ),
                            width=4,
                        )
                    ]
                )
            ],
            className="page-content"
        )
    ],
    fluid=True,
)

## Callback Functions
@callback(
    Output("uni-name-heading", "children"),
    Output("uoa-name-subheading", "children"),
    Input("uni-dropdown", "value"),
    Input("uoa-dropdown", "value"),
    prevent_initial_call=True,
)
def updatePageTitle(uni, uoa):
    uni_rtn = ""
    uoa_rtn = ""

    if (uni != None):
        uni_rtn = uni

    if (uoa != None):
        if (uoa == "All"):
            uoa_rtn = "All UoAs"
        else:
            uoa_rtn = uoa

    return uni_rtn, uoa_rtn

@callback(
    Output("uoa-dropdown", "options"),
    Input("uni-dropdown", "value"),
    prevent_initial_call=True,
)
def updateUOAbyUni(selected_uni):
    options=[
        {"label": "All", "value": "All"}
        ] + [
        {"label": col, "value": col}
        for col in sorted(
            results_df[(results_df["Institution name"] == selected_uni)]["UOA name"].unique()
        )
    ]

    return options

@callback(
    Output("overall-card", "children"),
    Output("outputs-card", "children"),
    Output("impact-card", "children"),
    Output("env-card", "children"),
    Output("income-chart", "figure"),
    Output("income-ik-chart", "figure"),
    Output("phd-awarded-chart", "figure"),
    Output("income-cat-chart", "figure"),
    Output("income-ik-cat-chart", "figure"),
    Input("uni-dropdown", "value"),
    Input("uoa-dropdown", "value"),
    prevent_initial_call = True,
)
def updatePage(uni, uoa):

    # GPA cards
    if (uoa == "All"):
        filtered_df = results_df[
            (results_df['Institution name'] == uni) 
        ]
    else:
        filtered_df = results_df[
            (results_df['Institution name'] == uni) &
            (results_df['UOA name'] == uoa)
        ]


    # GPA cards
    overall = np.round(np.mean(filtered_df.loc[(filtered_df["Profile"] == "Overall")]["GPA"]),2)

    outputs = np.round(np.mean(filtered_df.loc[(filtered_df["Profile"] == "Outputs")]["GPA"]), 2)

    impact = np.round(np.mean(filtered_df.loc[(filtered_df["Profile"] == "Impact")]["GPA"]), 2)

    env = np.round(np.mean(filtered_df.loc[(filtered_df["Profile"] == "Environment")]["GPA"]), 2)

    return (overall, outputs, impact, env, 
            components.generateIncomeChart(uni, uoa, income_df), 
            components.generateIncomeChart(uni, uoa, incomeiK_df, True),  
            components.generatePhdChart(uni, uoa), 
            components.generateIncomeCategoryChart(uni, uoa),
            components.generateIncomeInKindPieChart(uni, uoa))
