import pandas as pd
import numpy as np
from dash import dcc, html
import dash_bootstrap_components as dbc
import textwrap
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
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
    elif int(value) < 1e8:
        return f"{int(value) / 1e6:.1f}M"                  # Values above 1 million in millions
    else:
        return f"{int(value) / 1e9:.2f}B"                   # values above 100 million in billions
    
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
                            width=7, style={'padding-left':'0'}
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
    agg_func_dict = {
        '2013-14': 'sum',
        '2014-15': 'sum',
        '2015-2020 (avg)': 'sum',
    }

    # copy of income df to filter
    if (uoa == "All"):
        df_filtered = df.loc[(df["Institution name"] == uni) 
                            & (df['Income source'] == "Total income")
                            ].agg(agg_func_dict)
    else:
        df_filtered = df.loc[(df["Institution name"] == uni) 
                            & (df['Income source'] == "Total income")
                            & (df["UOA name"] == uoa)].agg(agg_func_dict)
    
    df_filtered = df_filtered.rename({
        '2013-14':"13'-14'",
        '2014-15':"14'-15'",
        '2015-2020 (avg)':"15'-20' (avg)",
    })
        
    chart = px.line(df_filtered,
                    markers=True,)

    chart.update_traces(
        marker_color="#800080",
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.1)", font_size=12),
        hovertemplate="<b>%{x}</b><br>Value: £%{y:,}",
    )
    
    chart.update_layout(
        title=dict(text="Research Income", font=dict(color="#9b58b6")),
        xaxis=dict(
            title=dict(text="Year", font=dict(size=14)), 
            color="#9b58b6",
            tickfont=dict(color="#9b58b6")
            ),
        yaxis=dict(
            title=dict(text="Amount (£)", font=dict(size=14)), 
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

    df_filtered = df_filtered.rename({
        '2013':"13'",
        '2014':"14'",
        '2015':"15'",
        '2016':"16'",
        '2017':"17'",
        '2018':"18'",
        '2019':"19'",
    })

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
        html.H1(format_value(total_phds), className="ranking-title-color"),
        html.H3("2013-2019 (Total)", className='subtitle-small-color'),
    ])  

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
    ])    

    return income_cat_chart, inc_kpi_card

def generateStaffFTEKPICard(uni,uoa):
    if (uoa == 'All'):
        df = results_df.loc[
            (results_df["Institution name"] == uni)
        ]
    else:
        df = results_df.loc[
            (results_df["Institution name"] == uni) &
            (results_df["UOA name"] == uoa)
        ]
    
    total = df['FTE staff'].sum()

    fte_kpi_card = html.Div([
        html.H1("Staff FTE", className='subtitle-medium-18-color'),
        html.H1(format_value(total), className="ranking-title-color"),
        html.H3("Full Time Equivalent", className='subtitle-small-color'),
    ]) 

    return fte_kpi_card

def generateInKindKPICard(uni, uoa):
    if (uoa == 'All'):
        df = incomeiK_df.loc[
            (incomeiK_df["Institution name"] == uni)
        ]
    else:
        df = incomeiK_df.loc[
            (incomeiK_df["Institution name"] == uni) &
            (incomeiK_df["UOA name"] == uoa)
        ]
    
    total = df['2013-2020 (total)'].sum()

    ik_kpi_card = html.Div([
        html.H1("Income In-Kind", className='subtitle-medium-18-color'),
        html.H1(f'£ {format_value(int(total))}', className="ranking-title-color"),
        html.H3("2013-2020 (Total)", className='subtitle-small-color'),
    ])   

    return ik_kpi_card

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

def generateQualityPieChart(uni, uoa, profile):
    # filtering profile & uni
    df = results_df[
        (results_df["Profile"] == profile) &
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
        textfont_size=14,
        textfont_family="Inter, sans-serif",
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
        text=f"{profile}<br>Quality",
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
    ])

    fig_reg = html.Div([
        html.H1("Regional Ranking", className='subtitle-medium-18-color'),
        html.H1(reg_ranking+1, className="ranking-title-color"),
        html.H3("Overall Research Quality", className='subtitle-small-color'),
    ])

    return [fig_nat, fig_reg]

def generateRegionScatterPlots(chart_type, region):
    if chart_type == 'phd':
        df = phd_df
        x_value = 'Total'
        x_label = 'PhDs Awarded (log scale)'
        title = 'GPA vs. PhDs Awarded'
    if chart_type == 'income':
        df = income_df
        x_value = '2013-2020 (total)'
        title = 'GPA vs. Research Income'
        x_label = "13'-20' Income (log scale)"
    if chart_type == 'incomeik':
        df = incomeiK_df
        x_value = '2013-2020 (total)'
        title = 'GPA vs. Research Income In-Kind'
        x_label = "13'-20' Income In-Kind (log scale)"

    gpa = results_df[results_df['Region'].isin(region)]
    metric = df[df['Region'].isin(region)]

    gpa_means = gpa.groupby(['Institution name']).agg({'GPA':'mean'}).reset_index()
    metric_totals = metric.groupby(['Institution name']).agg({x_value:'sum'}).reset_index()

    gpa_metric = gpa_means.merge(metric_totals, on='Institution name')
    gpa_metric = gpa_metric.merge(regions_mapping, on='Institution name')

    fig = px.scatter(
        gpa_metric,
        x=x_value,
        y='GPA',
        hover_name='Institution name',
        color='Region',
        log_x=True
    )

    fig.update_layout(
        title=dict(text=title, font=dict(color="#9b58b6")),
        xaxis=dict(
            title=x_label,
            color="#9b58b6",
            tickfont=dict(color="#9b58b6"),
            gridcolor='lightgrey'
            ),
        yaxis=dict(
            title="GPA",
            color="#9b58b6",
            tickfont=dict(color="#9b58b6"),
            gridcolor='lightgrey',
            range=[0,4]
            ),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        showlegend=True,
        title_font_size=18,
        font_family="Inter, sans-serif",
        margin = dict(t=50, l=35, r=35, b=10),

        legend=dict(
            x=0.65,  # Horizontal position (0 to 1)
            y=0.35,  # Vertical position (0 to 1)
            xanchor="left",  # Anchor the legend to the left
            yanchor="top",   # Anchor the legend to the top
            bgcolor='rgba(255, 255, 255, 0.7)',  # Optional: background color for the legend
            font=dict(
                size=10,  # Font size
                color="#9b58b6",  # Font color (can be any valid CSS color)
            )
        )
    )

    return fig

def generateRegionLineCharts(chart_type, region):
    if chart_type == 'phd':
        df = phd_df
        aggfunc = {
            "2013":"sum",
            "2014":"sum",
            "2015":"sum",
            "2016":"sum",
            "2017":"sum",
            "2018":"sum",
            "2019":"sum",
        }
        title = "PhDs Awarded by Region"
        hover_text = "<b>%{x}</b><br>PhDs Awarded: %{y:,}"
        x_axis_label = "PhDs Awarded"
    if chart_type == 'income':
        df = income_df
        aggfunc = {
            '2013-14': 'sum',
            '2014-15': 'sum',
            '2015-2020 (avg)': 'sum',
        }
        title = "Research Income by Region"
        hover_text="<b>%{x}</b><br>Value: £%{y:,}"
        x_axis_label = "Amount (£)"

    df = df[df["Region"].isin(region)]

    grouped_df = df.groupby(["Region"]).agg(aggfunc).reset_index()

    df_melted = grouped_df.melt(id_vars=["Region"], 
                     var_name="Year", 
                     value_name="Value")
    
    if chart_type == 'phd':
        df_melted["Year"] = df_melted["Year"].astype(int)

    fig = px.line(df_melted, 
                x="Year", 
                y="Value", 
                color="Region",  # different lines for each region
                markers=True,  # show markers at each year
                )
    
    fig.update_traces(
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.1)", font_size=12),
        hovertemplate=hover_text,
    )

    annotations = []

    colors = {trace.name: trace.line.color for trace in fig.data}

    for region in df_melted["Region"].unique():
        region_data = df_melted[df_melted["Region"] == region]
        
        # get the last point (end of the line)
        x_end, y_end = region_data["Year"].iloc[-1], region_data["Value"].iloc[-1]

        line_color = colors.get(region, "black")  # Default to black if not found

        if region == "Yorkshire and The Humber":
            region = "Yorkshire"
        
        annotations.append(dict(
            x=x_end, y=y_end + 150,
            text=region, 
            showarrow=False,
            xanchor="left", yanchor="middle",
            font=dict(size=12, color=line_color)
        ))
    
    fig.update_layout(
        title=dict(text=title, font=dict(color="#9b58b6")),
        xaxis=dict(
            title="Year",
            color="#9b58b6",
            tickfont=dict(color="#9b58b6"),
            gridcolor='lightgrey'
            ),
        yaxis=dict(
            title=dict(text=x_axis_label, font=dict(size=14)), 
            color="#9b58b6",
            tickfont=dict(color="#9b58b6"),
            gridcolor='lightgrey'
            ),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        showlegend=False,
        title_font_size=18,
        font_family="Inter, sans-serif",
        margin = dict(t=50, l=35, r=35, b=10),
        annotations = annotations
    )

    return fig

def generateRegionIncomeSankey(region):
    income_cat = {
        "UK Sources":[
            'BEIS Research Councils, The Royal Society, British Academy and The Royal Society of Edinburgh',
            'UK-based charities (open competitive process)',
            'UK-based charities (other)',
            'UK central government bodies/local authorities, health and hospital authorities',
            'Health research funding bodies',
            'UK central government tax credits for research and development expenditure',
            'UK industry, commerce and public corporations',
            'UK other sources'
        ],
        "EU Sources":[
            'EU government bodies',
            'EU-based charities (open competitive process)',
            'EU industry, commerce and public corporations',
            'EU (excluding UK) other',
        ],
        "Non-EU Sources":[
            'Non-EU-based charities (open competitive process)',
            'Non-EU industry commerce and public corporations', 
            'Non-EU other',
        ]
    }

    df = income_df
    df = df[~df["Income source"].isin(["Total income"])]
    df = df[df["Region"].isin(region)]

    df = df.groupby(['Region', 'Income source']).agg({'2013-2020 (total)':'sum'}).reset_index()

    df["Category"] = df["Income source"].map(
        {src: cat for cat, sources in income_cat.items() for src in sources}
    )

    df["Income source"] = df[
        "Income source"
        ].apply(lambda s: customwrap(s, width=45))

    all_nodes = list(set(df["Income source"]) | set(df["Category"]) | set(df["Region"]))

    # Map labels to indices
    source_indices = [all_nodes.index(src) for src in df["Income source"]]
    category_indices = [all_nodes.index(cat) for cat in df["Category"]]
    region_indices = [all_nodes.index(region) for region in df["Region"]]

    # Create source and target lists
    source = source_indices + category_indices  
    target = category_indices + region_indices  

    # Combine income values for both links
    values = list(df["2013-2020 (total)"]) + list(df["2013-2020 (total)"])

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=all_nodes,
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
        )
    ))

    fig.update_layout(
        title=dict(text="Income Sources by Region", font=dict(color="#9b58b6")),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        title_font_size=18,
        font_size=10,
        font_family="Inter, sans-serif",
        margin = dict(t=50, l=35, r=35, b=10),
    )

    return fig

def generateRegionGPADist(region):
    df = results_df
    df = df[df["Profile"] == "Overall"]
    df = df[df["Region"].isin(region)]
    data = []

    for r in region:
        df1 = df[df['Region'] == r]
        df1 = df1.groupby(['UOA name']).agg({'GPA':'mean'}).reset_index()
        data.append(df1['GPA'])
    
    fig = ff.create_distplot(
        data, 
        region,
        bin_size=.1,
        curve_type='normal',
        show_hist=False,
        show_rug=False
    )

    fig.update_layout(
        title=dict(text="Overall GPA Distribution by Region", font=dict(color="#9b58b6")),
        xaxis=dict(
            title="GPA",
            color="#9b58b6",
            tickfont=dict(color="#9b58b6"),
            gridcolor='lightgrey',
            range=[0,4],
            ),
        yaxis=dict(
            tickfont=dict(color="#9b58b6"),
            gridcolor='lightgrey'
            ),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        showlegend=True,
        title_font_size=18,
        font_family="Inter, sans-serif",
        margin = dict(t=50, l=35, r=35, b=10),

        legend=dict(
            x=0,  
            y=1,  
            xanchor="left",  # anchor the legend to the left
            yanchor="top",   # anchor the legend to the top
            bgcolor='rgba(255, 255, 255, 0.7)',
            font=dict(
                size=10,  
                color="#9b58b6", 
            )
        )
    )

    return fig