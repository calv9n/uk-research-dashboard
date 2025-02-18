import dash
from dash import callback, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from utils.dashboard_components import create_card, format_value
import textwrap

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
                html.H2(
                    'Institution Overview',
                    className='title',
                    id='title'
                ),
                html.Br(),
                dbc.Row(            # row for dropdown
                    [
                        dbc.Col(
                            [
                                html.H3(
                                    "Select University",
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
                                    placeholder="Select University",
                                    className="custom-dropdown",
                                ),
                                html.Br(),
                                html.H3(
                                    "Select Unit of Assessment",
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
                                )
                            ],
                            width = 4,
                        ),
                    ]
                ),
                html.Br(),
                dbc.Row(                # row for cards
                    [
                        dbc.Col(        # overall score col
                            create_card("Overall Quality (GPA)", "overall-card", "fa-ranking-star"),
                            width=3,
                        ),
                        dbc.Col(        # outputs score col
                            create_card("Outputs Quality (GPA)", "outputs-card", "fa-file"),
                            width=3,
                        ), 
                        dbc.Col(        # impact score col
                            create_card("Impact Quality (GPA)", "impact-card", "fa-users"),
                            width=3,
                        ),
                        dbc.Col(        # env score col
                            create_card("Environment Quality (GPA)", "env-card", "fa-seedling"),
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
                dbc.Row(
                    [
                        dbc.Col(        # phd awarded plot
                            dcc.Loading(
                                dcc.Graph(
                                    id="income-cat-chart",
                                    config={"displayModeBar": False},
                                    className="chart-card",
                                    style={"height": "400px"},
                                ),
                                type="circle",
                                color="#000000",
                            ),
                        ),
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
    Output("title", "children"),
    Input("uni-dropdown", "value"),
    Input("uoa-dropdown", "value"),
    prevent_initial_call=True,
)
def updatePageTitle(uni, uoa):
    uni_rtn = ""
    uoa_rtn = ""

    if (uni != None):
        uni_rtn = f" - {uni}"

    if (uoa != None):
        if (uoa == "All"):
            uoa_rtn = f" - All UoAs"
        else:
            uoa_rtn = f" - {uoa}"

    return f"Institution Overview{uni_rtn}{uoa_rtn}" 

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
    Input("uni-dropdown", "value"),
    Input("uoa-dropdown", "value"),
    prevent_initial_call = True,
)
def update_cards(uni, uoa):

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
            generateIncomeChart(uni, uoa, income_df), 
            generateIncomeChart(uni, uoa, incomeiK_df, True),  
            generatePhdChart(uni, uoa), 
            generateIncomeCategoryChart(uni, uoa))

## Helper Functions
def customwrap(s, width=40):
    if (s != None):
        return "<br>".join(textwrap.wrap(s,width=width))
    else:
        return None

def generateIncomeChart(uni, uoa, df, inkind=False):
    # agg functions
    if (inkind):
        agg_func = {
            '2013-14': 'sum',
            '2014-15': 'sum',
            '2016-17': 'sum',
            '2017-18': 'sum',
            '2018-19': 'sum',
            '2019-20': 'sum',
        }
        title = f"Research Income In-Kind"
        col_name = "Total income-in-kind"
    else:
        agg_func = {
            '2013-14': 'sum',
            '2014-15': 'sum',
            '2015-2020 (avg)': 'sum',
        }
        title = f"Research Income"
        col_name = "Total income"

    # copy of income df to filter
    if (uoa == "All"):
        df_filtered = df.loc[(df["Institution name"] == uni) 
                            & (df['Income source'] == col_name)
                            ].agg(agg_func)
    else:
        df_filtered = df.loc[(df["Institution name"] == uni) 
                            & (df['Income source'] == col_name)
                            & (df["UOA name"] == uoa)].agg(agg_func)
        

    # graph cards
    if (inkind):
        chart = px.line(df_filtered,
                        title=title,
                        markers=True,)
    else:
        chart = px.bar(df_filtered,
                        text_auto=True,
                        title=title,)
    

    chart.update_traces(
        marker_color="#800080",
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.1)", font_size=12),
        hovertemplate="<b>%{x}</b><br>Value: £%{y:,}",
    )

    chart.update_layout(
        xaxis_title="Year",
        yaxis_title="Amount (£)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=35, r=35, t=60, b=40),
        showlegend=False,
    )

    return chart

def generatePhdChart(uni, uoa):

    agg_func = {
            '2013': 'sum',
            '2014': 'sum',
            '2016': 'sum',
            '2017': 'sum',
            '2018': 'sum',
            '2019': 'sum',
        }
    
    if (uoa == "All"):
        df_filtered = phd_df.loc[(phd_df["Institution name"] == uni)].agg(agg_func)
    else:
        df_filtered = phd_df.loc[(phd_df["Institution name"] == uni) &
                                 (phd_df["UOA name"] == uoa)].agg(agg_func)


    phd_awarded_chart = px.line(df_filtered,
                                markers=True,
                                title=f"Total PhDs Awarded")

    phd_awarded_chart.update_traces(
        marker_color="#800080",
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.1)", font_size=12),
        hovertemplate="<b>%{x}</b><br>PhDs Awarded: %{y}",
    )

    phd_awarded_chart.update_layout(
        xaxis_title="Year",
        yaxis_title="# of PhD degrees awarded",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=35, r=35, t=60, b=40),
        showlegend=False,
    )

    return phd_awarded_chart

def generateIncomeCategoryChart(uni, uoa):
    # agg functions
    agg_func = {
        '2013-2020 (total)': 'sum',
    }

    if (uoa == 'All'):
        income_filtered = income_df.loc[
            (income_df["Institution name"] == uni) &
            (income_df["Income source"] != "Total income")
        ]
    else:
        income_filtered = income_df.loc[
            (income_df["Institution name"] == uni) &
            (income_df["Income source"] != "Total income") &
            (income_df["UOA name"] == uoa)
        ]

    income_filtered.loc[:,'Income source'] = income_filtered['Income source'].apply(customwrap)

    # copy of income df to filter
    income_filter_agg = income_filtered.groupby('Income source')\
                                    .agg({'2013-2020 (total)':'sum'})\
                                    .reset_index()\
                                    .sort_values(by="2013-2020 (total)",ascending=False)

    # defining the treemap chart
    income_cat_chart = go.Figure(go.Treemap(
                    labels=["Total income"] + income_filter_agg['Income source'].tolist(),
                    parents=[""] + (len(income_filter_agg)) * ["Total income"],
                    values=[0] + income_filter_agg['2013-2020 (total)'].tolist(),
                    marker_colorscale = 'Blues',
                ))
    

    income_cat_chart.update_layout(
        margin = dict(t=50, l=25, r=25, b=25),
        title="Research Income Sources (2013-2020)",
        uniformtext=dict(
            minsize=14,
        )
        )
    
    income_cat_chart.update_traces(
        hovertemplate='<b>%{label} </b><br>Funding Amount: £%{value}<br>',
        texttemplate="<b>%{label}</b><br><br>£%{value}",
    )

    return income_cat_chart
