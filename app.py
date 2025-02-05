import dash
from dash import Dash, html, dcc, callback, Output, Input, State
import dash_bootstrap_components as dbc

app = Dash(
    name = __name__, 
    use_pages=True,
    title = 'UK Research Dashboard',
    external_stylesheets=[dbc.themes.BOOTSTRAP, 'assets/style.css']
)

server = app.server

# sidebar
sidebar = html.Div(
    [
        dbc.Row(
            [
                "SOME LOGO",
                ## logo goes here
            ],
            className = "sidebar-logo"
        ),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink('Overview', href='/overview', active='exact'),
                dbc.NavLink('Compare Institutions', href='/compare', active='exact'),
            ],
            vertical=True,
            pills=True
        )
    ],
    className='sidebar'
)

# content
content = html.Div(
    className= 'page-content'
)

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
@import url('https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap');
</style>
"""

# layout
app.layout = html.Div(
    [
        dcc.Location(id='url', pathname="/overview"),
        sidebar,
        content,
        dash.page_container,
    ]
)

if __name__ == '__main__':
    app.run_server(debug=True)