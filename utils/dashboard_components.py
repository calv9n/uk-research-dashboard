import pandas as pd
import numpy as np
from dash import dcc, html
import dash_bootstrap_components as dbc
import textwrap
import plotly.express as px
import plotly.graph_objects as go
import json

# read in datasets
results_df = pd.read_csv('data/results_cleaned.csv')
income_df = pd.read_csv('data/income_cleaned.csv')
incomeiK_df = pd.read_csv('data/incomeiK_cleaned.csv')
phd_df = pd.read_csv('data/phd_awarded_cleaned.csv')
regions_mapping = pd.read_csv("data/regions.csv")

with open("assets/countries.geojson") as f:
    countries_geojson = json.load(f)

with open("assets/regions.geojson") as f:
    regions_geojson = json.load(f)

def format_value(value):
    if int(value) < 1e6:
        return f"{int(value) / 1e3:.1f}K"                   # Values below 1 million in thousands
    elif int(value) < 1e9:
        return f"{int(value) / 1e6:.1f}M"                  # Values above 1 million in millions
    else:
        return f"{int(value) / 1e9:.2f}B"                   # values above 1 billion in billions
    
def create_gpa_kpi_card(title, card_id, icon_class):
    return dbc.Card(
        dcc.Loading(
            dbc.CardBody(
                [
                    dbc.Col([
                        dbc.Row([
                            dbc.Col([
                                html.I(
                                    className=f"fas {icon_class} card-icon",
                                ),
                            ],
                            className="d-flex justify-content-center align-items-center p-0",
                            width=5
                            ),
                            dbc.Col([
                                html.H3(title, className="card-title"),
                                html.H4(id=card_id, className="card-text"),
                            ],
                            width=7
                            ),
                        ]),
                    ]),
                ],
                className="card-body"
            ),
        ), 
        className="card",
    )

def create_leaderboard(title, df, col, region):
    if region:
        th = "Region",
        td_data_col = "Region"
    else:
        th = "Institution name"
        td_data_col = "Institution name"

    return dbc.Card(
    dcc.Loading(  # Adding the loading spinner
        dbc.CardBody(  # The body of the card
            [
                html.Div(
                    [
                        html.I(  # Icon for the card (you can adjust the icon as per your needs)
                            className=f"fas fa-ranking-star card-icon",
                        ),
                        html.H3(title, className="card-title"),
                    ],
                    className="d-flex align-items-center",  # Flexbox for alignment
                ),
                
                # Table inside the card body
                dbc.Table(
                    [
                        html.Thead(
                            html.Tr(
                                [
                                    html.Th("Rank"),
                                    html.Th(th),
                                    html.Th(col),
                                ]
                            )
                        ),
                        html.Tbody(
                            [
                                html.Tr(
                                    [
                                        html.Td(i + 1),
                                        html.Td(row[td_data_col]),
                                        html.Td(np.round(row[col], 2) if col == "GPA" or col == "FTE staff" else format_value(row[col])),
                                    ]
                                )
                                for i, row in df.sort_values(col, ascending=False).head(5).reset_index(drop=True).iterrows()
                            ]
                        ),
                    ],
                    hover=True,
                    responsive=True,
                ),
            ],
            className="card-body",  # Card body styles
        ),
    ),
    className="card",  # Card styling
)

def create_info_cards(data, df, col, region):
    df = df.sort_values(col, ascending=False).reset_index(drop=True)
    best_text = df["Institution name"].iloc[0]
    best_value = np.round(df[col].iloc[0],2)
    worst_text = df["Institution name"].iloc[-1]
    worst_value = np.round(df[col].iloc[-1],2)

    if data in ["Income", "Income In-Kind"]:
        best_value = format_value(best_value)
        worst_value = format_value(worst_value)

    return html.Div(
        [
            dbc.Card(
                dcc.Loading(
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.I(
                                        className=f"fas fa-medal card-icon",
                                    ),
                                    html.H3(f"Best Performing Institution in {region}", className="card-title"),
                                ],
                                className="d-flex align-items-center",
                            ),
                            html.H4(
                                best_text,
                                className="title-color"
                            ),
                            html.H4(
                                best_value,
                                className="subtitle-medium-color"
                            )
                        ],
                        className="card-body",
                    ),
                ), 
                className="card",
            ),
            html.Div(style={"padding":"6px"}),
            dbc.Card(
                dcc.Loading(
                    dbc.CardBody(
                        [
                            html.Div(
                                [
                                    html.I(
                                        className=f"fa-solid fa-circle-exclamation card-icon",
                                    ),
                                    html.H3(f"Worst Performing Institution in {region}", className="card-title"),
                                ],
                                className="d-flex align-items-center",
                            ),
                            html.H4(
                                worst_text,
                                className="title-color"

                            ),
                            html.H4(
                                worst_value,
                                className="subtitle-medium-color"
                            )
                        ],
                        className="card-body",
                    ),
                ), 
                className="card",
            )        
        ]
    )
    
## Helper Functions
def customwrap(s, width=30):
    if (s != None):
        return "<br>".join(textwrap.wrap(s,width=width))
    else:
        return None

def returnUoAOptions():
    options = [
        {'label': "All UoAs", 'value': "All"}
        ] + [
        {'label': col, 'value': col}
        for col in sorted(
            results_df["UOA name"].unique()
        )
        ]
    return options

def generateIncomeChart(uni, uoa, df, inkind=False):
    # agg functions
    if (inkind):
        agg_func_dict = {
            '2013-14': 'sum',
            '2014-15': 'sum',
            '2016-17': 'sum',
            '2017-18': 'sum',
            '2018-19': 'sum',
            '2019-20': 'sum',
        }
        title = f"Research Income In-Kind"
        col_name = "Total income"
    else:
        agg_func_dict = {
            '2013-14': 'sum',
            '2014-15': 'sum',
            '2015-2020 (avg)': 'sum',
            '2013-2020 (avg)': 'sum',
        }
        title = f"Research Income"
        col_name = "Total income"

    # copy of income df to filter
    if (uoa == "All"):
        df_filtered = df.loc[(df["Institution name"] == uni) 
                            & (df['Income source'] == col_name)
                            ].agg(agg_func_dict)
    else:
        df_filtered = df.loc[(df["Institution name"] == uni) 
                            & (df['Income source'] == col_name)
                            & (df["UOA name"] == uoa)].agg(agg_func_dict)
        
    # graph cards
    if (inkind):
        chart = px.line(df_filtered,
                        markers=True,)
        xaxis_title = "Year"
        yaxis_title = "Amount (£)"
        chart.update_traces(
            marker_color="#800080",
            hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.1)", font_size=12),
            hovertemplate="<b>%{x}</b><br>Value: £%{y:,}",
        )
    else:
        chart = px.bar(df_filtered,
                        text_auto=True,
                        orientation='h',)
        xaxis_title = "Amount (£)"
        yaxis_title = "Year"
        chart.update_traces(
            marker_color="#800080",
            hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.1)", font_size=12),
            hovertemplate="<b>%{y}</b><br>Value: £%{x:,}",
        )
    
    chart.update_layout(
        title=dict(text=title, font=dict(color="#9b58b6")),
        xaxis=dict(
            title=dict(text=xaxis_title, font=dict(size=14)), 
            color="#9b58b6",
            tickfont=dict(color="#9b58b6")
            ),
        yaxis=dict(
            title=dict(text=yaxis_title, font=dict(size=14)), 
            color="#9b58b6",
            tickfont=dict(color="#9b58b6")
            ),
        showlegend=False,
        plot_bgcolor="rgba(0, 0, 0, 0)",
        title_font_size=18,
        font_family="Inter, sans-serif",
        margin = dict(t=50, l=35, r=35, b=10),
    )

    return chart

def generatePhdChartAndKPICard(uni, uoa):
    agg_func_dict = {
            '2013': 'sum',
            '2014': 'sum',
            '2015': 'sum',
            '2016': 'sum',
            '2017': 'sum',
            '2018': 'sum',
            '2019': 'sum',
            'Total':'sum'
        }
    
    if (uoa == "All"):
        df_filtered = phd_df.loc[(phd_df["Institution name"] == uni)].agg(agg_func_dict)
    else:
        df_filtered = phd_df.loc[(phd_df["Institution name"] == uni) &
                                 (phd_df["UOA name"] == uoa)].agg(agg_func_dict)
        
    total_phds = df_filtered['Total']

    df_filtered = df_filtered.drop('Total')         # removing 'Total' value - not needed for plots

    phd_awarded_chart = px.line(df_filtered,
                                markers=True)

    phd_awarded_chart.update_traces(
        marker_color="#800080",
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.1)", font_size=12),
        hovertemplate="<b>%{x}</b><br>PhDs Awarded: %{y}",
    )

    phd_awarded_chart.update_layout(
        title=dict(text="PhDs Awarded", font=dict(color="#9b58b6")),
        xaxis=dict(
            title=dict(text="Year", font=dict(size=14)),
            color="#9b58b6",
            tickfont=dict(color="#9b58b6")
            ),
        yaxis=dict(
            title=dict(text="PhDs awarded", font=dict(size=14)), 
            color="#9b58b6",
            tickfont=dict(color="#9b58b6")
            ),
        showlegend = False,
        plot_bgcolor="rgba(0, 0, 0, 0)",
        title_font_size=18,
        font_family="Inter, sans-serif",
        margin = dict(t=50, l=35, r=35, b=20),
    )

    phd_kpi_card = html.Div([
        html.H1("PhDs Awarded", className='subtitle-medium-18-color'),
        html.H1(np.round(total_phds, 1), className="ranking-title-color"),
        html.H3("2013-2019 (Total)", className='subtitle-small-color'),
    ], className='card card-body ranking-card')  

    return phd_awarded_chart, phd_kpi_card

def generateIncomeCategoryChartAndKPICard(uni, uoa):
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
    
    total_income = income_filter_agg['2013-2020 (total)'].sum()

    # defining the treemap chart
    income_cat_chart = go.Figure(go.Treemap(
                    labels=["Total income"] + income_filter_agg['Income source'].tolist(),
                    parents=[""] + (len(income_filter_agg)) * ["Total income"],
                    values=[0] + income_filter_agg['2013-2020 (total)'].tolist(),
                    marker_colorscale = ["#FFFFFF", "#800080"],
                ))
    

    income_cat_chart.update_layout(
        margin = dict(t=50, l=25, r=25, b=25),
        title="Income Sources (2013-2020)",
        title_font_size=18,
        title_font_color='#9b58b6',
        font_family="Inter, sans-serif",
        font_size=14,
    )
    
    income_cat_chart.update_traces(
        hovertemplate='%{label}<br>Total funding: £%{value}<br>',
        texttemplate="%{label}<br><br>£%{value}",
    )

    inc_kpi_card = html.Div([
        html.H1("Research Income", className='subtitle-medium-18-color'),
        html.H1(f'£ {format_value(int(total_income))}', className="ranking-title-color"),
        html.H3("2013-2020 (Total)", className='subtitle-small-color'),
    ], className='card card-body ranking-card')    

    return income_cat_chart, inc_kpi_card

def generateIncomeInKindBarChart(uni, uoa):
    if (uoa == 'All'):
        income_filtered = incomeiK_df.loc[
            (incomeiK_df["Institution name"] == uni) &
            (incomeiK_df["Income source"] != "Total income")
        ]
        income_filtered = income_filtered.groupby("Income source").agg({"2013-2020 (total)":"sum"}).reset_index()
    else:
        income_filtered = incomeiK_df.loc[
            (incomeiK_df["Institution name"] == uni) &
            (incomeiK_df["Income source"] != "Total income") &
            (incomeiK_df["UOA name"] == uoa)
        ]

    chart = px.bar(income_filtered,
                   x="Income source",
                   y="2013-2020 (total)",
                   text_auto=True,
                   color_discrete_sequence=["#800080"]
                )

    chart.update_layout(
        title=dict(text="In-Kind Income Sources (2013-2020)", font=dict(color="#9b58b6")),
        xaxis=dict(
            title="",
            tickfont=dict(color="#9b58b6")
            ),
        yaxis=dict(
            title=dict(text="Amount (£)", font=dict(size=14)), 
            color="#9b58b6",
            tickfont=dict(color="#9b58b6")
            ),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        title_font_size=18,
        font_family="Inter, sans-serif",
        margin = dict(t=50, l=35, r=35, b=0),
    )

    return chart

def generateMap(df, data, period):
    color = period

    if data == "Staff FTE":
        color = "FTE staff"
    if data == "GPA":
        color = "GPA"

    map_graph = px.choropleth(df,
                        geojson=regions_geojson,  
                        locations="Region",
                        featureidkey="properties.RGN24NM",  # Match with GeoJSON key
                        color=color,
                        color_continuous_scale=["#FFFFFF", "#800080"],
                        center={"lat": 55.0, "lon": -2.0},  # Approximate UK center
                        scope="europe")
    
    map_graph.update_geos(
        fitbounds = "locations",
        visible = False,
        projection_scale=1  # Adjust the scale
    )

    map_graph.update_layout(
        margin=dict(t=75, l=25, r=25, b=25),  # Adjust margins
        title="Some title",
    )
    
    return map_graph

def generateScatter(df, data, period, region):
    x_col = period
    y_col = "GPA" 
    color = "Region"
     
    if (data == "GPA") or (data == "Staff FTE"):
        x_col = "FTE staff"
    if region != "All":
        color = None
    else:
        color = "Region"

    scatter_graph = px.scatter(
        df,
        x=x_col,
        y=y_col,
        hover_name="Institution name",
        color=color,
    )

    scatter_graph.update_layout(
        yaxis=dict(range=[1,4]),
    )

    return scatter_graph

def generateDataFrameForMap(data, uoa, period, aggfunc):
    agg_func_dict = {
        period:aggfunc
    }

    if (data == "GPA"):
        df = results_df    
        agg_func_dict = {
            "GPA":"mean"
        }
    if (data == "Staff FTE"):
        df = results_df
        agg_func_dict = {
            "FTE staff":aggfunc
        }
    if data == "PhDs Awarded":
        df = phd_df
        
    if data == "Income":
        df = income_df
        
    if data == "Income In-Kind":
        df = incomeiK_df
    
    if uoa != "All":
        df = df[df['UOA name'] == uoa]
    
    df = df.groupby("Region").agg(agg_func_dict).reset_index()

    return df

def generateDataFrameForScatter(data, uoa, period, region, aggfunc):
    agg_func_dict = {
            "GPA":"mean",
            period:aggfunc
        }  
    
    agg_results = results_df[results_df['Profile'] == "Overall"].groupby("Institution name").agg({"GPA":"mean"}).reset_index()
    
    if (data == "GPA") or (data == "Staff FTE"):
        df = results_df
        agg_func_dict = {
            "FTE staff":aggfunc,
            "GPA":"mean"
        }
    if data == "PhDs Awarded":
        df = phd_df.merge(agg_results, on="Institution name")
    if data == "Income":
        df = income_df.merge(agg_results, on="Institution name")
    if data == "Income In-Kind":
        df = incomeiK_df.merge(agg_results, on="Institution name")

    if uoa != "All":
        df = df[df['UOA name'] == uoa]

    if region != "All":
        df = df[df['Region'] == region]

    df = df.groupby(["Institution name", "Region"]).agg(agg_func_dict).reset_index()

    return df

def generateQualityPieChart(uni, uoa):
    # filtering profile & uni
    df = results_df[
        (results_df["Profile"] == "Overall") &
        (results_df["Institution name"] == uni)
        ].reset_index()

    # filter uoa
    if uoa != "All":
        df = df[df["UOA name"] == uoa].reset_index()


    df = df.groupby(["Institution name"]).agg(
        {
            '4*':'mean',
            '3*':'mean',
            '2*':'mean',
            '1*':'mean',
            "0*":"mean"
            }).reset_index()

    df_melted = df.melt(
        id_vars=["Institution name"],  # Columns to keep
        var_name="Rating",  # Name for new column that holds '4*', '3*', etc.
        value_name="Percentage"  # Name for new column that holds the values
    ).sort_values(by="Percentage", ascending=False)

    chart = go.Figure(
        data=[
            go.Pie(
                labels=df_melted['Rating'],
                values=df_melted['Percentage'],
            )
        ]
    )

    chart.update_traces(
        marker=dict(colors=["#800080", "#9f1987", "#b6229c", "#d18cc1", "#e2b4d6"]),
        hole=0.5,
        textinfo="label+percent",
        textposition="inside",
        texttemplate="%{label}<br>%{percent:.0%}"
    )

    chart.update_layout(
        margin = dict(t=10, l=10, r=10, b=10),
        showlegend = False,
    )

    chart.add_annotation(
        x=0.5,
        y=0.5,
        align="center",
        xref="paper",
        yref="paper",
        showarrow=False,
        font_size=18,
        font_family="Inter, sans-serif",
        font_color="#9b58b6",
        text="Outputs<br>Quality",
    )

    return chart

def generateUOADistChart(uni, uoa):
    df = results_df

    df = df[(df["Institution name"] == uni) &
            (df["Profile"] == "Overall")]

    df = df.groupby("UOA name").agg({'GPA':'mean'}).reset_index().sort_values(by="GPA", ascending=True)

    chart = px.histogram(
        df, 
        x="GPA",
        nbins=10,
        marginal="rug",
        hover_data="UOA name",
        color_discrete_sequence=["#800080"]
    )

    chart.update_layout(
        title=dict(text="GPA Distribution", font=dict(color="#9b58b6")),
        xaxis=dict(
            title=dict(text="GPA (Overall)", font=dict(size=14)),
            color="#9b58b6",
            tickfont=dict(color="#9b58b6")
            ),
        yaxis=dict(
            title=dict(text="Frequency", font=dict(size=14)), 
            color="#9b58b6",
            tickfont=dict(color="#9b58b6")
            ),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        title_font_size=18,
        font_family="Inter, sans-serif",
        margin = dict(t=50, l=35, r=35, b=20),
    )

    return chart

def generateRankingCards(uni, uoa):
    results_overall = results_df[results_df["Profile"] == "Overall"]
    # results_outputs = results_df[results_df["Profile"] == "Outputs"]
    # results_impact = results_df[results_df["Profile"] == "Impact"]
    # results_environment = results_df[results_df["Profile"] == "Environment"]

    if uoa != "All":
        results_overall = results_overall[results_overall["UOA name"] == uoa]

    region = results_df.loc[
        results_df["Institution name"] == uni,
        "Region"
        ].values[0]

    national_overall = results_overall.groupby(
        "Institution name"
    ).agg({
        "GPA":"mean"
    }).sort_values(by='GPA', ascending=False).reset_index()

    overall_reg_df = results_overall[results_overall["Region"] == region]

    regional_overall = overall_reg_df.groupby(
        "Institution name",
    ).agg({
        "GPA":"mean"
    }).sort_values(by='GPA', ascending=False).reset_index()

    nat_ranking = int(national_overall.index[national_overall["Institution name"] == uni][0])
    reg_ranking = int(regional_overall.index[regional_overall["Institution name"] == uni][0])

    fig_nat = html.Div([
        html.H1("National Ranking", className='subtitle-medium-18-color'),
        html.H1(nat_ranking+1, className="ranking-title-color"),
        html.H3("Overall Research Quality", className='subtitle-small-color'),
    ], className='card card-body ranking-card')

    fig_reg = html.Div([
        html.H1("Regional Ranking", className='subtitle-medium-18-color'),
        html.H1(reg_ranking+1, className="ranking-title-color"),
        html.H3("Overall Research Quality", className='subtitle-small-color'),
    ], className='card card-body ranking-card')

    return [fig_nat, fig_reg]
