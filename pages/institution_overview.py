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
        dcc.Store(
            id='dropdowns-valid', data=False
        ),
        html.Div(
            [
                dbc.Col(            # master col
                    [
                        html.Div([          # div for dropdowns 
                            dbc.Row([       #dropdowns
                                dbc.Col([
                                    html.Label(
                                        "View",
                                        className='subtitle-small',
                                    ),
                                    dcc.Dropdown(               # dropdown for uni filter
                                        id='view-dropdown',
                                        options=[
                                            {"label": 'Institution', "value": 'ins'},
                                            {"label": 'Regional', "value": 'reg'},
                                            {"label": 'National', "value": 'nat'},
                                        ],
                                        # value="All",
                                        clearable=True,
                                        multi=False,            
                                        placeholder="Select View",
                                        className="custom-dropdown",
                                    )],
                                    xs=6, sm=6, md=6, lg=2, xl=2
                                ),
                                dbc.Col([
                                    html.Label(
                                        "Institution",
                                        className='subtitle-small',
                                        id='institution-dropdown-heading',
                                    ),
                                    dcc.Dropdown(               # dropdown for institution/region
                                        id='institution-dropdown',
                                        options=[
                                            {"label": col, "value": col}
                                            for col in sorted(
                                                results_df["Institution name"].unique()
                                            )
                                        ],
                                        clearable=True,
                                        multi=False,            # can extend to be multi-select
                                        placeholder="Select Institution",
                                        className="custom-dropdown",
                                    )],
                                    xs=12, sm=12, md=12, lg=3, xl=3,
                                    id='institution-col'
                                ),
                                dbc.Col([
                                    html.Label(
                                        "Region",
                                        className='subtitle-small',
                                        id='region-dropdown-heading',
                                    ),
                                    dcc.Dropdown(               # dropdown for institution/region
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
                                        multi=False,            # can extend to be multi-select
                                        placeholder="Select Region",
                                        className="custom-dropdown",
                                    )],
                                    xs=12, sm=12, md=12, lg=3, xl=3,
                                    id='region-col'
                                ),
                                dbc.Col([
                                    html.Label(
                                        "Unit of Assessment",
                                        className='subtitle-small',
                                        id='uoa-dropdown=heading'
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
                                xs=12, sm=12, md=12, lg=3, xl=3,
                                id='uoa-col'
                                ),
                                dbc.Col(

                                ),
                                dbc.Col([
                                    html.Div(
                                        dbc.Button(
                                            "Update Dashboard",
                                            className="btn-custom",
                                            id="update-dashboard-btn",
                                        ),
                                        style={"display": "flex", 
                                                "flexDirection": "column", 
                                                "height": "100%", 
                                                "justifyContent": "flex-end"}
                                    ) 
                                ],
                                xs=12, sm=12, md=12, lg=2, xl=2
                                ),
                            ]),
                        ],className="filter-card"),
                        dbc.Row(            # row 1
                            [
                                dbc.Col(        # col left
                                    [
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
                                                                    style={"height": "130px"},
                                                                    className='card card-body ranking-card'
                                                                )
                                                            )
                                                        ],xs=12, sm=12, md=6, lg=3, xl=3),
                                                        dbc.Col([
                                                            dcc.Loading(
                                                                html.Div(
                                                                    id="income-kpi",
                                                                    style={"height": "130px"},
                                                                    className='card card-body ranking-card'
                                                                )
                                                            )
                                                        ],xs=12, sm=12, md=6, lg=3, xl=3),
                                                        dbc.Col([
                                                            dcc.Loading(
                                                                html.Div(
                                                                    id="in-kind-kpi",
                                                                    style={"height": "130px"},
                                                                    className='card card-body ranking-card'
                                                                )
                                                            )
                                                        ],xs=12, sm=12, md=6, lg=3, xl=3),
                                                        dbc.Col([
                                                            dcc.Loading(
                                                                html.Div(
                                                                    id="phd-kpi",
                                                                    style={"height": "130px"},
                                                                    className='card card-body ranking-card'
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
                                                                ], id='submissions-pie-div', style={'background-color':'#fff', 
                                                                          'border-radius':'8px'}),
                                                            ]),
                                                            className = 'col-12 col-xl-4', id='submissions-col'
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
                                                            className = 'col-12 col-xl-4', id = 'phd-col'
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
                                                            className = 'col-12 col-xl-4', id = 'inc-chart-col'
                                                        ), 
                                                    ]
                                                )
                                            ]),
                                        ],id="left-col", hidden=True),                                            
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
                                                            className='card card-body ranking-card'
                                                        )
                                                    )
                                                ],width=6, id='nat-ranking-col'),
                                                dbc.Col([
                                                    dcc.Loading(
                                                        html.Div(
                                                            id="reg-ranking",
                                                            style={"height": "130px"},
                                                            className='card card-body ranking-card'
                                                        )
                                                    )
                                                ], width=6, id='reg-ranking-col')
                                            ]),
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
                                        ], id="right-col", hidden=True)
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
    Output("institution-col", "style"),
    Output("region-col", "style"),
    Output("uoa-col", "style"),
    Input("view-dropdown", "value"),
    # prevent_initial_call=True,
)
def updateDropdownsbyView(view):
    if view == None:
        return ({"display": "none"}, {"display": "none"}, {"display": "none"})
    elif view == 'ins':
        return ({"display": "block"}, {"display": "none"}, {"display": "block"})
    elif view == 'reg':
        return ({"display": "none"}, {"display": "block"}, {"display": "block"})
    elif view == 'nat':
        return ({"display": "none"}, {"display": "none"}, {"display": "block"})

@callback(
    Output("uoa-dropdown", "options", allow_duplicate=True),
    Input("institution-dropdown", "value"),
    State("view-dropdown", "value"),
    prevent_initial_call=True,
)
def updateUOAbyUni(ins, view):
    if view == 'ins':
        options=[
            {"label": "All Units of Assessment", "value": "All"}
            ] + [
            {"label": col, "value": col}
            for col in sorted(
                results_df[(results_df["Institution name"] == ins)]["UOA name"].unique()
            )
        ]
    else:
        options = []

    return options

@callback(
    Output("uoa-dropdown", "options", allow_duplicate=True),
    Input("view-dropdown", "value"),
    prevent_initial_call=True,
)
def updateUOAIfRegionalOrNational(view):
    if view == 'nat' or view == 'reg':
        options=[
            {"label": "All Units of Assessment", "value": "All"}
            ] + [
            {"label": col, "value": col}
            for col in sorted(
                results_df["UOA name"].unique()
            )
        ]
    else:
        options=[]

    return options

@callback(
    Output("left-col", 'hidden'),
    Output("right-col", 'hidden'),
    Output("ins-ov-alert-msg", "children"), 
    Output("ins-ov-alert-msg", "is_open"),
    Input("update-dashboard-btn", 'n_clicks'),
    State("view-dropdown", "value"),
    State("uoa-dropdown", "value"),
    State("institution-dropdown", "value"),
    State("region-dropdown", "value"),
    prevent_initial_call = True
)
def showCardsAndDisableUpdateButton(n_clicks, view, uoa, ins, reg):
    if view is None:
        return True, True, "Please select a View", True
    
    if view == 'ins':
        if uoa is None and ins is None:
            return True, True, "Please make a selection for Institution and Unit of Assessment.", True
        elif uoa is None:
            return True, True, "Please select a Unit of Assessment.", True
        elif ins is None:
            return True, True, "Please select an Institution.", True
    elif view == 'reg':
        if uoa is None and reg is None:
            return True, True, "Please make a selection for Region and Unit of Assessment.", True
        elif uoa is None:
            return True, True, "Please select a Unit of Assessment.", True
        elif reg is None:
            return True, True, "Please select a Region.", True
    elif view == 'nat':
        if uoa is None:
            return True, True, "Please select a Unit of Assessment.", True
        
    return False, False, '', False

@callback(
    Output("submissions-quality", 'figure', allow_duplicate=True),
    Input('submissions-radios', 'value'),
    State('institution-dropdown', 'value'),
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
    Output('submissions-pie-div', 'hidden'),
    Output('submissions-col', 'style'),
    Output('phd-col', 'className'),
    Output('inc-chart-col', 'className'),
    Output("nat-ranking", "children"),
    Output("reg-ranking", "children"),
    Output("staff-fte-kpi", "children"),
    Output("income-kpi", "children"),
    Output("in-kind-kpi", "children"),
    Output("phd-kpi", "children"),
    Output('nat-ranking', 'style'),
    Output('reg-ranking', 'style'),
    Input("update-dashboard-btn", 'n_clicks'),
    State("view-dropdown", "value"),
    State("institution-dropdown", "value"),
    State("region-dropdown", "value"),
    State("uoa-dropdown", "value"),
    State("submissions-radios", 'value'),
    prevent_initial_call = True,
)
def updatePage(update, view, ins, reg, uoa, gpa_profile):

    if view is None:
        raise dash.exceptions.PreventUpdate
    
    if view == 'ins' and (ins is None or uoa is None):
        raise dash.exceptions.PreventUpdate
    
    if view == 'reg' and (reg is None or uoa is None):
        raise dash.exceptions.PreventUpdate
    
    if view == 'nat' and (uoa is None):
        raise dash.exceptions.PreventUpdate
    
    if view == 'ins':
        if uoa == 'All':
            df = results_df[
                (results_df['Institution name'] == ins) 
            ]
            hide_submissions = True
            submissions_col_style = {'display':'none'}
            phd_inc_col_class = 'col-12 col-xl-6'
            ranking_col_style = {}
        else:
            df = results_df[
                (results_df['Institution name'] == ins) &
                (results_df['UOA name'] == uoa)
            ]
            hide_submissions = False
            submissions_col_style = {}
            phd_inc_col_class = 'col-12 col-xl-4'
            ranking_col_style = {}
    elif view == 'reg':
        df = results_df[results_df['Region'] == reg]
        if uoa == 'All':
            df = df.groupby(['Region', 'Profile']).agg({'GPA':'mean'}).reset_index()
        else:
            df = df.groupby(['Region', 'Profile', 'UOA name']).agg({'GPA':'mean'}).reset_index()
            df = df[df['UOA name'] == uoa]
        hide_submissions = True
        submissions_col_style = {'display':'none'}
        phd_inc_col_class = 'col-12 col-xl-6'
        ranking_col_style = {'display':'none'}
    else:
        if uoa != 'All':
            df = results_df[results_df['UOA name'] == uoa]
        else:
            df = results_df
        hide_submissions = True
        submissions_col_style = {'display':'none'}
        phd_inc_col_class = 'col-12 col-xl-6'
        ranking_col_style = {'display':'none'}

    # GPA cards
    if view == 'nat':
        overall = np.round(np.mean(df[df['Profile'] == 'Overall']['GPA']),2)
        outputs = np.round(np.mean(df[df['Profile'] == 'Outputs']['GPA']),2)
        impact = np.round(np.mean(df[df['Profile'] == 'Impact']['GPA']),2)
        env = np.round(np.mean(df[df['Profile'] == 'Environment']['GPA']),2)
    else:
        overall = np.round(np.mean(df.loc[(df["Profile"] == "Overall")]["GPA"]),2)
        outputs = np.round(np.mean(df.loc[(df["Profile"] == "Outputs")]["GPA"]), 2)
        impact = np.round(np.mean(df.loc[(df["Profile"] == "Impact")]["GPA"]), 2)
        env = np.round(np.mean(df.loc[(df["Profile"] == "Environment")]["GPA"]), 2)

    ranking_cards = components.generateRankingCards(view, ins, uoa)

    income_charts = components.generateIncomeCategoryChartAndKPICard(view, ins, uoa, reg)

    phd_charts = components.generatePhdChartAndKPICard(view, ins, uoa, reg)



    return (overall, outputs, impact, env, 
            components.generateIncomeChart(view, ins, uoa, reg), 
            phd_charts[0], 
            income_charts[0],
            components.generateQualityPieChart(ins, uoa, gpa_profile),
            hide_submissions,
            submissions_col_style,
            phd_inc_col_class,
            phd_inc_col_class,
            ranking_cards[0],
            ranking_cards[1],
            components.generateStaffFTEKPICard(view, ins, uoa, reg),
            income_charts[1],
            components.generateInKindKPICard(view, ins, uoa, reg),
            phd_charts[1],
            ranking_col_style,
            ranking_col_style)


