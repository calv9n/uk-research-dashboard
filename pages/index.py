import dash
from dash import html, dcc
import dash_bootstrap_components as dbc

dash.register_page(
    module= __name__,
    external_stylesheets = [dbc.themes.BOOTSTRAP, 'assets/style.css'],
    path = '/'
)

layout = dbc.Container([
    html.Div([
        html.Div([
            html.Img(
                src='/assets/logo-white.png', 
                className="mb-4",
                style={'max-height': '100px', 'max-width': '100%'}),
            html.P(
                "Interactive insights into UK higher education research performance",
                className="lead text-white"
            ),
            html.Hr(className="my-4 bg-white opacity-25"),
            html.P(
                "Explore research quality, funding, and performance metrics across UK institutions and regions.",
                className="text-white mb-4"
            ),
            dbc.Button(
                "Explore Dashboard", 
                href="/national_overview", 
                color='light',
                size="lg",
                className="fw-bold transparent-text",
            ),
        ], className="py-5")
    ], className="mb-3 p-5 text-center", style={
        'background': 'linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(128,0,128,1) 100%)',
        'borderRadius': '0.5rem',
        'boxShadow': '0 4px 6px rgba(0, 0, 0, 0.1)'
    }),
    
    # Key Metrics Section
    html.Div([
        html.H2("Comprehensive Insights from REF2021", className="text-center mb-5"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    html.Div(html.I(className="fas fa-award fa-3x", style={'color':'#800080'}), className="text-center mt-4"),
                    dbc.CardBody([
                        html.H4("Research Quality", className="card-title text-center"),
                        html.P(
                            "Analyse the trends in Overall, Outputs, Environment and Impact quality.",
                            className="card-info text-center"
                        ),
                    ]),
                ], className="h-100 shadow-sm")
            ], md=3, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    html.Div(html.I(className="fas fa-pound-sign fa-3x", style={'color':'#800080'}), className="text-center mt-4"),
                    dbc.CardBody([
                        html.H4("Research Income", className="card-title text-center"),
                        html.P(
                            "Explore funding patterns and their correlation with research outcomes.",
                            className="card-info text-center"
                        ),
                    ]),
                ], className="h-100 shadow-sm")
            ], md=3, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    html.Div(html.I(className="fas fa-graduation-cap fa-3x", style={'color':'#800080'}), className="text-center mt-4"),
                    dbc.CardBody([
                        html.H4("Doctoral Degrees", className="card-title text-center"),
                        html.P(
                            "Visualise PhD completions and research development across UK institutions.",
                            className="card-info text-center"
                        ),
                    ]),
                ], className="h-100 shadow-sm")
            ], md=3, className="mb-4"),
            
            dbc.Col([
                dbc.Card([
                    html.Div(html.I(className="fas fa-chart-line fa-3x", style={'color':'#800080'}), className="text-center mt-4"),
                    dbc.CardBody([
                        html.H4("Rankings", className="card-title text-center"),
                        html.P(
                            "Compare institutional and regional performance with interactive rankings.",
                            className="card-info text-center"
                        ),
                    ]),
                ], className="h-100 shadow-sm")
            ], md=3, className="mb-4"),
        ]),
    ], className="py-5", style={'font-family':'Inter'}),
], fluid=True, style={'padding-right':'16.3rem'})