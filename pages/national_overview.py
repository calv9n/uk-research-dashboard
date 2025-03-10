import dash
from dash import callback, html, dcc, Input, Output
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
                    "National Overview",
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
                dbc.Row(            # 
                ),
                html.Br(),
                dbc.Row(            # row for set of graphs 2

                ),
            ],
            className="page-content"
        )
    ],
    fluid=True,
)