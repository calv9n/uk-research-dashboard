import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")  # This sets it as the default homepage

layout = dbc.Container(
    [
        dbc.Row(
            dbc.Col(
                html.Div(
                    [
                        html.H1("Welcome to the UK Research Dashboard", className="landing-title"),
                        html.P("Explore data insights with interactive charts and analytics.", className="landing-subtitle"),
                        dbc.Button("Enter Dashboard", href="/institution_overview", color="primary", className="landing-button"),
                    ],
                    className="landing-container",
                ),
                width=12,
            ),
            className="align-items-center justify-content-center vh-100",
        )
    ],
    fluid=True,
)