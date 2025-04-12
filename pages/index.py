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
            html.H2(
                'Research Excellence Framework 2021',
                style={
                    'background': 'linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(128,0,128,1) 67%)',
                    '-webkit-background-clip': 'text',
                    'background-clip': 'text',
                    '-webkit-text-fill-color': 'transparent', 
                    'text-fill-color': 'transparent',
                    'font-size':'3rem'
                }
            ),
            html.H1(
                'Visualised',
                style={
                    'background': 'linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(128,0,128,1) 67%)',
                    '-webkit-background-clip': 'text',
                    'background-clip': 'text',
                    '-webkit-text-fill-color': 'transparent', 
                    'text-fill-color': 'transparent',
                    'font-size':'8rem'
                }
            ),
            html.P(
                "Interactive Insights into Research Quality in the United Kingdom",
                style={
                    'background': 'linear-gradient(90deg, rgba(2,0,36,1) 0%, rgba(128,0,128,1) 67%)',
                    '-webkit-background-clip': 'text',
                    'background-clip': 'text',
                    '-webkit-text-fill-color': 'transparent', 
                    'text-fill-color': 'transparent',
                    'font-size':'1.5rem'
                }
            ),
            html.Br(),
            dbc.Button(
                "Explore Dashboard", 
                href="/national_overview", 
                size="lg",
                className="cta-button",
            ),
        ], className="py-5")
    ], className="mb-3 p-5 text-center", 
    style={
        "display": "flex",
        "flex-direction": "column",
        "justify-content": "center",
        "align-items": "center",
        "height": "100vh",  # Full viewport height
        "text-align": "center"  # Center text inside the div
    },
    ),
    
    # Key Metrics Section
    html.Div([
        html.Div(
            html.Img(
                src='/assets/logo-black.png', 
                className="mb-4",
                style={'max-height': '70px', 'max-width': '100%',}),
            style={
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',}
        ),
        html.H2("Interactive Insights from REF 2021", className="text-center mb-6", style={'font-size':'1.5rem'}),
        
        # Steps Section
        dbc.Row(
            [
                # Step 1
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.Img(src="/assets/national_overview.png", style={"width": "100%", "margin-bottom": "20px"}),
                                    html.P("National Overview", style={"text-align": "center"})
                                ],
                                style={"background-color": "#EAE8F9", "padding": "20px", "border-radius": "10px"}
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.H5("Gain Insights on National Research Performance", className="card-text", style={'margin-bottom':'2.5rem', 'margin-top':'2.5rem', 'padding-left':'1rem'}),
                                    html.P(
                                        "View key facts from REF2021 and compare the top performing institutions and regions in the U.K.\n",
                                        className="card-title",
                                        style={'font-size':'1.5rem', 'white-space':'wrap', 'margin-bottom':'2.5rem', 'padding-left':'1rem'}
                                    ),
                                    dbc.Button("Learn more", color="dark", href='/national_overview')
                                ],
                                style={'text-align':'right'}
                            ),
                            width=8,
                        )
                    ],
                    style={"margin-bottom": "40px"}
                ),
                
                # Step 2
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.Img(src="/assets/multi_level_view.png", style={"width": "100%", "margin-bottom": "20px"}),
                                    html.P("Multi Level View", style={"text-align": "center"})
                                ],
                                style={"background-color": "#EAE8F9", "padding": "20px", "border-radius": "10px"}
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.H5("Explore Performance From Different Perspectives", className="card-text", style={'margin-bottom':'2.5rem', 'margin-top':'2.5rem', 'padding-left':'1rem'}),
                                    html.P(
                                        "Understand the REF 2021 findings on varying scales. Choose between an institution view, regional view, or delve deeper into national performance.\n",                                        className="card-title",
                                        style={'font-size':'1.5rem', 'white-space':'wrap', 'margin-bottom':'2.5rem', 'padding-left':'1rem'}
                                    ),
                                    dbc.Button("Learn more", color="dark", href='/multi_level_view')
                                ],
                                style={'text-align':'right'}
                            ),
                            width=8,
                        )
                    ],
                    style={"margin-bottom": "40px"}
                ),

                # Step 3
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(
                                [
                                    html.Img(src="/assets/reg_trend_analysis.png", style={"width": "100%", "margin-bottom": "20px"}),
                                    html.P("Regional Trend Analysis", style={"text-align": "center"})
                                ],
                                style={"background-color": "#EAE8F9", "padding": "20px", "border-radius": "10px"}
                            ),
                            width=4,
                        ),
                        dbc.Col(
                            html.Div(
                                [
                                    html.H5("Compare Regional Trends Across Various Metrics", className="card-text", style={'margin-bottom':'2.5rem', 'margin-top':'2.5rem', 'padding-left':'1rem'}),
                                    html.P(
                                        "Analyse regional trends in key metrics such as research income, PhDs awarded, and others. Find out how well institutions within each region are funded with an interactive breakdown of their income sources.\n",
                                        className="card-title",
                                        style={'font-size':'1.5rem', 'white-space':'wrap', 'margin-bottom':'2.5rem', 'padding-left':'1rem'}
                                    ),
                                    dbc.Button("Learn more", color="dark", href='/regional_trends')
                                ],
                                style={'text-align':'right'}
                            ),
                            width=8,
                        )
                    ],
                    style={"margin-bottom": "40px"}
                )


            ],
            justify="center",
            style={"margin-top": "40px"}
        ),

        # dbc.Row([
        #     dbc.Col([
        #         dbc.Card([
        #             html.Div(html.I(className="fas fa-award fa-3x", style={'color':'#800080'}), className="text-center mt-4"),
        #             dbc.CardBody([
        #                 html.H4("Research Quality", className="card-title text-center"),
        #                 html.P(
        #                     "Analyse the trends in Overall, Outputs, Environment and Impact quality.",
        #                     className="card-info text-center"
        #                 ),
        #             ]),
        #         ], className="h-100 shadow-sm")
        #     ], md=3, className="mb-4"),
            
        #     dbc.Col([
        #         dbc.Card([
        #             html.Div(html.I(className="fas fa-pound-sign fa-3x", style={'color':'#800080'}), className="text-center mt-4"),
        #             dbc.CardBody([
        #                 html.H4("Research Income", className="card-title text-center"),
        #                 html.P(
        #                     "Explore funding patterns and their correlation with research outcomes.",
        #                     className="card-info text-center"
        #                 ),
        #             ]),
        #         ], className="h-100 shadow-sm")
        #     ], md=3, className="mb-4"),
            
        #     dbc.Col([
        #         dbc.Card([
        #             html.Div(html.I(className="fas fa-graduation-cap fa-3x", style={'color':'#800080'}), className="text-center mt-4"),
        #             dbc.CardBody([
        #                 html.H4("Doctoral Degrees", className="card-title text-center"),
        #                 html.P(
        #                     "Visualise PhD completions and research development across UK institutions.",
        #                     className="card-info text-center"
        #                 ),
        #             ]),
        #         ], className="h-100 shadow-sm")
        #     ], md=3, className="mb-4"),
            
        #     dbc.Col([
        #         dbc.Card([
        #             html.Div(html.I(className="fas fa-chart-line fa-3x", style={'color':'#800080'}), className="text-center mt-4"),
        #             dbc.CardBody([
        #                 html.H4("Rankings", className="card-title text-center"),
        #                 html.P(
        #                     "Compare institutional and regional performance with interactive rankings.",
        #                     className="card-info text-center"
        #                 ),
        #             ]),
        #         ], className="h-100 shadow-sm")
        #     ], md=3, className="mb-4"),
        # ]),
    ], className="py-5", style={'font-family':'Inter'}),
], fluid=True, style={'padding-right':'16.3rem'})