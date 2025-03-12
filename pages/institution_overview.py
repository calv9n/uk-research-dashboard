import dash
from dash import callback, html, dcc, Input, Output, State, ctx
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
                dbc.Col(            # master col
                    [
                        dbc.Row(            # row 1
                            [
                                dbc.Col(        # col left
                                    [
                                        html.Div([      # div for dropdowns           
                                            dbc.Row([
                                                dbc.Col([
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
                                                    )],
                                                    xs=12, sm=12, md=12, lg=5, xl=5
                                                ),
                                                dbc.Col([
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
                                                xs=12, sm=12, md=12, lg=5, xl=5
                                                ),
                                                dbc.Col([
                                                    dbc.Button(
                                                        "Update Dashboard",
                                                        className="btn-custom",
                                                        id="update-dashboard-btn",
                                                        disabled=False
                                                    )
                                                ],
                                                xs=4, sm=4, md=4, lg=2, xl=2
                                                ),
                                            ])
                                        ],className="filter-card"),
                                        html.Div([
                                            html.Div([       # div for gpa KPI
                                                dbc.Row(
                                                    [
                                                        dbc.Col(        # outputs score col
                                                            components.create_gpa_kpi_card("Outputs", "outputs-card", "fa-file"),
                                                            xs=12, sm=12, md=6, lg=3, xl=3

                                                        ), 
                                                        dbc.Col(        # impact score col
                                                            components.create_gpa_kpi_card("Impact", "impact-card", "fa-users"),
                                                            xs=12, sm=12, md=6, lg=3, xl=3
                                                        ),
                                                        dbc.Col(        # env score col
                                                            components.create_gpa_kpi_card("Environment", "env-card", "fa-seedling"),
                                                            xs=12, sm=12, md=6, lg=3, xl=3
                                                        ),
                                                        dbc.Col(        # overall score col
                                                            components.create_gpa_kpi_card("Overall", "overall-card", "fa-ranking-star"),
                                                            xs=12, sm=12, md=6, lg=3, xl=3
                                                        ),
                                                    ]
                                                )
                                            ]),
                                            html.Div([       # div for submissions quality, gpa dist, phd
                                                dbc.Row(
                                                    [
                                                        dbc.Col([
                                                            dcc.Loading(
                                                                html.Div(
                                                                    id="staff-fte-kpi",
                                                                    style={"height": "130px", 'margin-bottom':'1rem'},
                                                                )
                                                            )
                                                        ],xs=12, sm=12, md=6, lg=3, xl=3),
                                                        dbc.Col([
                                                            dcc.Loading(
                                                                html.Div(
                                                                    id="income-kpi",
                                                                    style={"height": "130px", 'margin-bottom':'1rem'},
                                                                )
                                                            )
                                                        ],xs=12, sm=12, md=6, lg=3, xl=3),
                                                        dbc.Col([
                                                            dcc.Loading(
                                                                html.Div(
                                                                    id="in-kind-kpi",
                                                                    style={"height": "130px", 'margin-bottom':'1rem'},
                                                                )
                                                            )
                                                        ],xs=12, sm=12, md=6, lg=3, xl=3),
                                                        dbc.Col([
                                                            dcc.Loading(
                                                                html.Div(
                                                                    id="phd-kpi",
                                                                    style={"height": "130px", 'margin-bottom':'1rem'},
                                                                )
                                                            )
                                                        ], xs=12, sm=12, md=6, lg=3, xl=3)
                                                    ]
                                                )
                                            ]),
                                            html.Div([       # div for output quality, gpa dist, phd
                                                dbc.Row(
                                                    [
                                                       dbc.Col(        # submissions quality
                                                            dcc.Loading([
                                                                html.Div([
                                                                    html.Div(
                                                                        dcc.Dropdown(
                                                                            id='submissions-radios',
                                                                            options=[
                                                                                {"label": "Outputs", "value": "Outputs"},
                                                                                {"label": "Impact", "value": "Impact"},
                                                                                {"label": "Environment", "value": "Environment"},
                                                                                {"label": "Overall", "value": "Overall"},
                                                                            ],
                                                                            value="Overall",
                                                                            clearable=False
                                                                        ),
                                                                        className = 'submissions-dropdown'
                                                                    ),
                                                                    dcc.Graph(
                                                                        id="submissions-quality",
                                                                        config={"displayModeBar": False},
                                                                        className="chart-card",
                                                                        style={"height": "38vh"},
                                                                    ),
                                                                ], style={'background-color':'#fff', 
                                                                          'border-radius':'8px'}),
                                                            ]),
                                                            xs=12, sm=12, md=12, lg=12, xl=4
                                                        ),
                                                        dbc.Col(        # phds awarded
                                                            dcc.Loading(
                                                                dcc.Graph(
                                                                    id="phd-awarded-chart",
                                                                    config={"displayModeBar": False},
                                                                    className="chart-card",
                                                                    style={"height": "44.5vh"},
                                                                ),
                                                                type="circle",
                                                                color="#000000",
                                                            ),
                                                            xs=12, sm=12, md=12, lg=12, xl=4,
                                                        ),
                                                        dbc.Col(        # avg research income plot
                                                            dcc.Loading(
                                                                dcc.Graph(
                                                                    id="income-chart",
                                                                    config={"displayModeBar": False},
                                                                    className="chart-card",
                                                                    style={"height": "44.5vh"},
                                                                ),
                                                                type="circle",
                                                                color="#000000",
                                                            ),
                                                            xs=12, sm=12, md=12, lg=12, xl=4,
                                                        ), 
                                                    ]
                                                )
                                            ]),
                                        ],id="left-col", hidden=False),                                            
                                    ],
                                    xs=12, sm=12, md=12, lg=12, xl=8
                                ),
                                dbc.Col(
                                    [
                                        html.Div([      # div for ranking & treemap
                                            dbc.Row([       # ranking
                                                dbc.Col([
                                                    dcc.Loading(
                                                        html.Div(
                                                            id="nat-ranking",
                                                            style={"height": "130px"},
                                                        )
                                                    )
                                                ],width=6),
                                                dbc.Col([
                                                    dcc.Loading(
                                                        html.Div(
                                                            id="reg-ranking",
                                                            style={"height": "130px"},
                                                        )
                                                    )
                                                ], width=6)
                                            ],style={"margin-bottom":"1rem"}),
                                            dbc.Row(        # income in-kind category treemap
                                                dbc.Col(        
                                                    dcc.Loading(
                                                        dcc.Graph(
                                                            id="income-cat-chart",
                                                            config={"displayModeBar": False},
                                                            className="chart-card",
                                                            style={"height": "72vh"},
                                                        ),
                                                        type="circle",
                                                        color="#000000",
                                                    ),
                                                    width=12,
                                                )
                                            )
                                        ], id="right-col", hidden=False)
                                    ],
                                    xs=12, sm=12, md=12, lg=12, xl=4
                                ),
                            ],
                        ),
                        dbc.Alert(
                            id='ins-ov-alert-msg',
                            is_open=False,
                            color='danger'
                        ),
                    ],
                    width=12
                ),
            ],
            className="page-content"
        )
    ],
    fluid=True,
)

## Callback Functions
@callback(
    Output("uoa-dropdown", "options"),
    Input("uni-dropdown", "value"),
    prevent_initial_call=True,
)
def updateUOAbyUni(selected_uni):
    options=[
        {"label": "All Units of Assessment", "value": "All"}
        ] + [
        {"label": col, "value": col}
        for col in sorted(
            results_df[(results_df["Institution name"] == selected_uni)]["UOA name"].unique()
        )
    ]

    return options

@callback(
    Output("left-col", 'hidden'),
    Output("right-col", 'hidden'),
    Output("ins-ov-alert-msg", "children"), 
    Output("ins-ov-alert-msg", "is_open"),
    Output('update-dashboard-btn', 'disabled'),
    Input("update-dashboard-btn", 'n_clicks'),
    State("uni-dropdown", "value"),
    State("uoa-dropdown", "value"),
    prevent_initial_call = True
)
def showCardsAndDisableUpdateButton(n_clicks, uni, uoa):
    if uni is None and uoa is None:
        return True, True, "Please select both Institution and UOA.", True, False
    elif uni is None:
        return True, True, "Please select an Institution.", True, False
    elif uoa is None:
        return True, True, "Please select a UOA.", True, False
    else:
        return False, False, "", False, True  # Hide alert & disabled update dashboard btn when valid
    
@callback(
    Output("update-dashboard-btn", "disabled", allow_duplicate=True),
    Input("uni-dropdown", "value"),
    Input("uoa-dropdown", "value"),
    prevent_initial_call=True
)
def enableUpdateButton(uni, uoa):
    return False  # Re-enable button when dropdown changes

@callback(
    Output("submissions-quality", 'figure', allow_duplicate=True),
    Input('submissions-radios', 'value'),
    State('uni-dropdown', 'value'),
    State('uoa-dropdown', 'value'),
    prevent_initial_call = True
)
def updateSubmissionsPieChart(profile, uni, uoa):
    return components.generateQualityPieChart(uni, uoa, profile)

@callback(
    Output("overall-card", "children"),
    Output("outputs-card", "children"),
    Output("impact-card", "children"),
    Output("env-card", "children"),
    Output("income-chart", "figure"),
    Output("phd-awarded-chart", "figure"),
    Output("income-cat-chart", "figure"),
    Output('submissions-quality', 'figure'),
    Output("nat-ranking", "children"),
    Output("reg-ranking", "children"),
    Output("staff-fte-kpi", "children"),
    Output("income-kpi", "children"),
    Output("in-kind-kpi", "children"),
    Output("phd-kpi", "children"),
    Input("update-dashboard-btn", 'n_clicks'),
    State("uni-dropdown", "value"),
    State("uoa-dropdown", "value"),
    State("submissions-radios", 'value'),
    prevent_initial_call = True,
)
def updatePage(update, uni, uoa, gpa_profile):

    if uni is None or uoa is None:
        raise dash.exceptions.PreventUpdate

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

    ranking_cards = components.generateRankingCards(uni, uoa)

    income_charts = components.generateIncomeCategoryChartAndKPICard(uni, uoa)

    phd_charts = components.generatePhdChartAndKPICard(uni, uoa)

    return (overall, outputs, impact, env, 
            components.generateIncomeChart(uni, uoa, income_df), 
            phd_charts[0], 
            income_charts[0],
            components.generateQualityPieChart(uni, uoa, gpa_profile),
            ranking_cards[0],
            ranking_cards[1],
            components.generateStaffFTEKPICard(uni,uoa),
            income_charts[1],
            components.generateInKindKPICard(uni, uoa),
            phd_charts[1])


