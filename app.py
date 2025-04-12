import dash
from dash import Dash, html, dcc, callback, Output, Input
import dash_bootstrap_components as dbc

# dash app initialisation
app = Dash(
    __name__,
    use_pages=True,
    title="UK Research Dashboard",
    external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/style.css']
)

server = app.server

# sidebar nav
sidebar = html.Div(
    [
        dbc.Row(
            [html.Img(src="assets/logo-black.png", style={"height": "auto"})],
            className="sidebar-logo"
        ),
        html.Hr(),
        dbc.Nav(
            [
                # National Overview page with info button
                dbc.NavItem(
                    dbc.Row(
                        [
                            dbc.Col(dbc.NavLink('National Overview', href='/national_overview', active='exact')),
                            dbc.Col(
                                html.I(
                                    className="fa fa-info-circle",
                                    id="info-national-overview",
                                    style={"fontSize": "15px", "cursor": "pointer", "padding": "0", 'color':'#800080'}
                                ),
                                width="auto"
                            )
                        ],
                        align="center"
                    )
                ),
                dbc.Tooltip(
                    "Explore the overview of national research data, including performance and trends across the U.K.",
                    target="info-national-overview",
                    placement="right"
                ),
                # Multi-level View page with info button
                dbc.NavItem(
                    dbc.Row(
                        [
                            dbc.Col(dbc.NavLink('Multi-level View', href='/multi_level_view', active='exact')),
                            dbc.Col(
                                html.I(
                                    className="fa fa-info-circle",
                                    id="info-multi-level-view",
                                    style={"fontSize": "15px", "cursor": "pointer", "padding": "0", 'color':'#800080'}
                                ),
                                width="auto"
                            )
                        ],
                        align="center"
                    )
                ),
                dbc.Tooltip(
                    "Analyse research trends at the multi-level view, from institutions to regions and across U.K.",
                    target="info-multi-level-view",
                    placement="right"
                ),
                # Regional Trends page with info button
                dbc.NavItem(
                    dbc.Row(
                        [
                            dbc.Col(dbc.NavLink('Regional Trend Analysis', href='/regional_trends', active='exact')),
                            dbc.Col(
                                html.I(
                                    className="fa fa-info-circle",
                                    id="info-regional-trends",
                                    style={"fontSize": "15px", "cursor": "pointer", "padding": "0", 'color':'#800080'}
                                ),
                                width="auto"
                            )
                        ],
                        align="center"
                    )
                ),
                dbc.Tooltip(
                    "Explore regional research performance and trends across the different parts of the U.K.",
                    target="info-regional-trends",
                    placement="right"
                ),
                dbc.NavLink('Back to Home', href='/', active='exact'),

            ],
            vertical=True,
            pills=True
        ),
    ],
    className='sidebar'
)

# content container
content = html.Div(id="page-content", className='page-content')

# custom HTML template
app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        {%css%}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.7.2/css/all.min.css">
        <link rel="icon" href="/assets/logos/favicon.svg" type="image/x-icon">
    </head>
    <body>
        {%app_entry%}
        {%config%}
        {%scripts%}
        {%renderer%}
    </body>
</html>

<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@100;400;700&display=swap');
</style>
"""

# main app layout
app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=False),  # tracks URL changes
        html.Div(id="sidebar-container"),  # sidebar will be inserted dynamically
        content,
        dash.page_container, 
    ]
)

# Callback to Show/Hide Sidebar
@callback(
    Output("sidebar-container", "children"),
    Output("sidebar-container", "style"),
    Input("url", "pathname")
)
def toggle_sidebar(pathname):
    if pathname == "/": 
        return "", {'display':'none'}
    return sidebar, {'display':'block'}


if __name__ == '__main__':
    app.run_server(debug=True)
