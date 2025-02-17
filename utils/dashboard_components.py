from dash import dcc
import dash_bootstrap_components as dbc
from dash import html

def format_value(value):
    if int(value) < 1e6:
        return f"{int(value) / 1e3:.1f}K"                   # Values below 1 million in thousands
    else:
        return f"{int(value) / 1e6:.1f}M"                  # Values above 1 million in millions

def create_card(title, card_id, icon_class):
    return dbc.Card(
        dcc.Loading(
            dbc.CardBody(
                [
                    html.Div(
                        [
                            html.I(
                                className=f"fas {icon_class} card-icon",
                            ),
                            html.H3(title, className="card-title"),
                        ],
                        className="d-flex align-items-center",
                    ),
                    html.H4(id=card_id),
                ],
                className="card-body",
            ),
        ), 
        className="card",
    )