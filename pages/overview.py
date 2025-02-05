import dash
from dash import callback, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import numpy as np
import plotly.express as px
from utils.dashboard_components import create_card

## Global variables

inc_sources = [
    "BEIS Research Councils, The Royal Society, British Academy and The Royal Society of Edinburgh",
    "EU (excluding UK) other",
    "EU government bodies",
    "EU industry, commerce and public corporations",
    "EU-based charities (open competitive process)",
    "Health research funding bodies",
    "Non-EU industry commerce and public corporations",
    "Non-EU other",
    "Non-EU-based charities (open competitive process)",
    "UK central government bodies/local authorities, health and hospital authorities",
    "UK central government tax credits for research and development expenditure",
    "UK industry, commerce and public corporations",
    "UK other sources",
    "UK-based charities (open competitive process)",
    "UK-based charities (other)"
]

dash.register_page(
    module= __name__,
    external_stylesheets = [dbc.themes.BOOTSTRAP, 'assets/style.css'],
    path = '/overview'
)

# read in datasets
results_df = pd.read_csv('data/results_cleaned.csv')
income_df = pd.read_csv('data/income_cleaned.csv')
incomeiK_df = pd.read_csv('data/incomeiK_cleaned.csv')
phd_df = pd.read_csv('data/phd_awarded_cleaned.csv')

# layout
layout = dbc.Container(
    [
        html.Div(
            [
                html.H2(
                    'UK Research Dashboard',
                    className='title',
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
                                dcc.Dropdown(
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
                            width=6,
                        ),
                        dbc.Col(        # breakdown of research income 

                        )
                    ]
                ),
                html.Br(),
                dbc.Row(
                    [
                        dbc.Col(        # phd awarded plot

                        ),
                        dbc.Col(        # research income in kind plot

                        )
                    ]
                )
            ],
            className="page-content"
        )
    ],
    fluid=True,
)

@callback(
    Output("overall-card", "children"),
    Output("outputs-card", "children"),
    Output("impact-card", "children"),
    Output("env-card", "children"),
    Output("income-chart", "figure"),
    Input("uni-dropdown", "value"),
    prevent_initial_call = True
)
def update_cards(selected_uni):

    # GPA cards
    overall = np.mean(results_df.loc[(results_df["Institution name"] == selected_uni) & (results_df["Profile"] == "Overall")]["GPA"])
    # ri = "{:,.0f}".format(np.round(np.mean(income_df.loc[income_df["Institution name"] == selected_uni]["2013-2020 (avg)"]), -2)) // ref for next time
    outputs = np.mean(results_df.loc[(results_df["Institution name"] == selected_uni) & (results_df["Profile"] == "Outputs")]["GPA"])
    impact = np.mean(results_df.loc[(results_df["Institution name"] == selected_uni) & (results_df["Profile"] == "Impact")]["GPA"])
    env = np.mean(results_df.loc[(results_df["Institution name"] == selected_uni) & (results_df["Profile"] == "Environment")]["GPA"])
    
    # agg functions
    agg_func = {
        '2013-14': 'sum',
        '2014-15': 'sum',
        '2015-2020 (avg)': 'sum',
    }

    # copy of income df to filter
    income_filtered = income_df.loc[(income_df["Institution name"] == selected_uni) & (income_df['Income source'] != 'Total income')].agg(agg_func)

    # graph cards
    income_chart = px.bar(income_filtered.T,
                          text_auto=True,)

    income_chart.update_traces(
        marker_color="#f79500",
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.1)", font_size=12),
        hovertemplate="<b>%{x}</b><br>Value: %{y:,}<extra></extra>",
    )

    income_chart.update_layout(
        xaxis_title="Year",
        yaxis_title="Amount (£)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=35, r=35, t=60, b=40),
    )

    return np.round(overall,2), np.round(outputs,2), np.round(impact,2), np.round(env,2), income_chart