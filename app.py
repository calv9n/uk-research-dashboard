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
            [html.Img(src="assets/refined-analytics-high-resolution-logo-transparent.png", style={"height": "auto"})],
            className="sidebar-logo"
        ),
        html.Hr(),
        dbc.Nav(
            [
                # dbc.NavLink('Subject Overview', href='/subject_overview', active='exact'),
                # dbc.NavLink('Regional Overview Test', href='/regional_overview_test', active='exact'),
                dbc.NavLink('Institution Overview', href='/institution_overview', active='exact'),
                dbc.NavLink('Regional Overview', href='/regional_overview', active='exact'),
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
    Input("url", "pathname")
)
def toggle_sidebar(pathname):
    if pathname == "/": 
        return ""
    return sidebar

if __name__ == '__main__':
    app.run_server(debug=True)
