## This file contains almost all of the helper & utility functions
## used to facilitate the dashboard's functionality.

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

with open("assets/regions.geojson") as f:
    regions_geojson = json.load(f)

def format_value(value):
    """
    Formats a numerical value into a more readable string representation.

    Depending on the size of the input value, the function returns:
    - A rounded value (1 decimal place) if the value is less than 1,000.
    - A value in thousands (rounded to 1 decimal place with a 'K' suffix) if the value is between 1,000 and 999,999.
    - A value in millions (rounded to 1 decimal place with an 'M' suffix) if the value is between 1 million and 999 million.
    - A value in billions (rounded to 2 decimal places with a 'B' suffix) if the value is 1 billion or more.

    Parameters:
    value (float or int): The numerical value to format.

    Returns:
    str: The formatted value as a string with appropriate suffix ('', 'K', 'M', or 'B').

    Example:
    >>> format_value(750)
    '750.0'

    >>> format_value(1200)
    '1.2K'

    >>> format_value(5000000)
    '5.0M'

    >>> format_value(1500000000)
    '1.50B'
    """
    if value < 1e3:
        return np.round(value,1)
    elif value < 1e6:
        return f"{value / 1e3:.1f}K"                   # Values below 1 million in thousands
    elif value < 1e9:
        return f"{value / 1e6:.1f}M"                  # Values above 1 million in millions
    else:
        return f"{value / 1e9:.2f}B"                   # values above 100 million in billions
    
def create_gpa_kpi_card(title, card_id, icon_class):
    """
    Creates a KPI card component with a title, value placeholder, and an icon.

    This function generates a Dash `dbc.Card` that displays a KPI (Key Performance Indicator) card 
    with a customizable title, a placeholder for the card's value (identified by `card_id`), 
    and a FontAwesome icon for visual representation.

    Parameters:
    title (str): The title of the KPI card.
    card_id (str): The unique identifier for the card's value. This will be used to update the value dynamically.
    icon_class (str): The FontAwesome icon class to display in the card.
    """
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

def create_leaderboard(title, df, col):
    th = 'Institution name'
    td_data_col = 'Institution name'

    if (col == 'Income') or (col == 'Income In-Kind'):
        col_name = '2013-2020 (total)'
    else:
        col_name = col

    return dbc.Card(
    dcc.Loading(  
        dbc.CardBody(  
            [
                html.Div(
                    [
                        html.I( 
                            className=f"fas fa-ranking-star card-icon", style={'margin-right':'10px'}
                        ),
                        html.H3(title, className="card-title", style={'font-size':'18px'}),
                    ],
                    className="d-flex align-items-center",  
                ),
                
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
                                        html.Td(np.round(row[col_name], 2) if col_name == "GPA" or col_name == "FTE staff" else format_value(row[col_name])),
                                    ]
                                )
                                for i, row in df.sort_values(col_name, ascending=False).head(10).reset_index(drop=True).iterrows()
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
    style={'border-top-right-radius':'0', 'border-top-left-radius':'0', 'padding-left':'1rem', 'padding-right':'1rem'},

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

## General Utility Functions
def customwrap(s, width=30):
    if (s != None):
        return "<br>".join(textwrap.wrap(s,width=width))
    else:
        return None

def returnUoAOptions():
    options = [
        {'label': "All Units of Assessment", 'value': "All"}
        ] + [
        {'label': col, 'value': col}
        for col in sorted(
            results_df["UOA name"].unique()
        )
        ]
    return options

## Visualisation Generation for Institution Overview page
def generateIncomeChart(type, ins, uoa, reg):
    df = income_df
    # agg functions
    agg_func_dict = {
        '2013-14': 'sum',
        '2014-15': 'sum',
        '2015-2020 (avg)': 'sum',
    }

    if type == 'ins':
        if (uoa == "All"):
            df_filtered = income_df.loc[(income_df["Institution name"] == ins) 
                                & (income_df['Income source'] == "Total income")
                                ].agg(agg_func_dict)
        else:
            df_filtered = income_df.loc[(income_df["Institution name"] == ins) 
                                & (income_df['Income source'] == "Total income")
                                & (income_df["UOA name"] == uoa)].agg(agg_func_dict)
    elif type == 'reg':
        df = income_df[(income_df['Region'] == reg) &(income_df['Income source'] == 'Total income')]
        if uoa != 'All':
            df = df[df['UOA name'] == uoa]
        df_filtered = df.agg(agg_func_dict)
    else:
        df = income_df[income_df['Income source'] != 'Total income']
        if uoa != 'All':
            df = income_df[income_df['UOA name'] == uoa]
        df_filtered = df.agg(agg_func_dict)
    
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
        hovertemplate="<b>%{x}</b><br>Value: £%{y:,}<extra></extra>",
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

def generatePhdChartAndKPICard(type, ins, uoa, reg):
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
    
    if type == 'ins':
        if (uoa == "All"):
            df_agg = phd_df.loc[(phd_df["Institution name"] == ins)].agg(agg_func_dict)
        else:
            df_agg = phd_df.loc[(phd_df["Institution name"] == ins) &
                                    (phd_df["UOA name"] == uoa)].agg(agg_func_dict)
    elif type == 'reg':
        df = phd_df[phd_df['Region'] == reg]
        if (uoa != 'All'):
            df = df[df['UOA name'] == uoa]
        df_agg = df.agg(agg_func_dict)
    else:
        df = phd_df
        if uoa != 'All':
            df = phd_df[phd_df['UOA name'] == uoa]
        df_agg = df.agg(agg_func_dict)
    
    total_phds = df_agg['Total']

    df_agg = df_agg.drop('Total')         # removing 'Total' value - not needed for plots

    df_agg = df_agg.rename({
        '2013':"13'",
        '2014':"14'",
        '2015':"15'",
        '2016':"16'",
        '2017':"17'",
        '2018':"18'",
        '2019':"19'",
    })

    phd_awarded_chart = px.line(df_agg,
                                markers=True)

    phd_awarded_chart.update_traces(
        marker_color="#800080",
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.1)", font_size=12),
        hovertemplate="<b>%{x}</b><br>PhDs Awarded: %{y}<extra></extra>",
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

    phd_kpi_card = generateKPICard(
        "PhDs Awarded",
        format_value(total_phds),
        "2013-2019 (Total)",
        'phds',
        "Number of research doctoral degrees awarded by the institution for academic years 2013-14 to 2018-19"
    ) 

    return phd_awarded_chart, phd_kpi_card

def generateIncomeCategoryChartAndKPICard(type, uni, uoa, reg):
    if type == 'ins':
        if (uoa == 'All'):
            df = income_df.loc[
                (income_df["Institution name"] == uni) &
                (income_df["Income source"] != "Total income")
            ]
        else:
            df = income_df.loc[
                (income_df["Institution name"] == uni) &
                (income_df["Income source"] != "Total income") &
                (income_df["UOA name"] == uoa)
            ]
        # copy of income df to filter
        income_filter_agg = df.groupby('Income source')\
                                    .agg({'2013-2020 (total)':'sum'})\
                                    .reset_index()\
                                    .sort_values(by="2013-2020 (total)",ascending=False)
    elif type == 'reg':
        # filtering df by region and to exclude total income 
        df = income_df.loc[
            (income_df['Income source'] != 'Total income') &
            (income_df['Region'] == reg)
        ]
        if (uoa != 'All'):
            # filter by uoa
            df = df[df['UOA name'] == uoa]
        income_filter_agg = df.groupby(['Region', 'Income source'])\
                                    .agg({'2013-2020 (total)':'sum'})\
                                    .reset_index()\
                                    .sort_values(by='2013-2020 (total)', ascending=False)
    else:
        df = income_df[income_df['Income source'] != 'Total income']
        if uoa != 'All':
            df = df[df['UOA name'] == uoa]
        income_filter_agg = df.groupby('Income source').agg({'2013-2020 (total)':'sum'}).reset_index()

    income_filter_agg.loc[:,'Income source'] = income_filter_agg['Income source'].apply(customwrap)
    
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
        hovertemplate='%{label}<br>Total funding: £%{value}<br><extra></extra>',
        texttemplate="%{label}<br><br>£%{value}",
    )

    inc_kpi_card = generateKPICard(
        "Research Income",
        f'£{format_value(int(total_income))}',
        "2013-2020 (Total)",
        'income',
        "Research income (non-in-kind) received for the selected UoA from 2013-2020."
    )  

    return income_cat_chart, inc_kpi_card

def generateKPICard(title, value, subtitle, icon_id, tooltip):
    return html.Div([
        html.H1(title, className='subtitle-medium-18-color'),
        html.H1(value, className="ranking-title-color"),
        html.Div([
            html.H3(subtitle, className='subtitle-small-color'),
            html.Span(
                html.I(className="fa fa-info-circle info-icon", id=f"{icon_id}-info-icon"),
                style={"margin": "0px 0px 8px 8px", "cursor": "pointer", "color": "#0d6efd"},
            ),
        ], className="d-flex align-items-center justify-content-center"),
        dbc.Tooltip(
            tooltip,
            target=f"{icon_id}-info-icon",
            placement="right",  
        ),
    ])

def generateStaffFTEKPICard(type, uni, uoa, reg):
    if type == 'ins':
        if (uoa == 'All'):
            df = results_df.loc[
                (results_df["Institution name"] == uni) & 
                 (results_df['Profile'] == 'Overall')
            ]
        else:
            df = results_df.loc[
                (results_df["Institution name"] == uni) &
                (results_df["UOA name"] == uoa) &
                (results_df['Profile'] == 'Overall')
            ]
    elif type == 'reg':
        df = results_df[(results_df['Region'] == reg) &
                        (results_df['Profile'] == 'Overall')]
        if uoa != 'All':
            df = df[df['UOA name'] == uoa]
    else:
        if uoa != 'All':
            df = results_df[(results_df['UOA name'] == uoa)&
                            (results_df['Profile'] == 'Overall')]
        else:
            df = results_df[results_df["Profile"] == "Overall"]
    
    # check if any multiple submissions
    df = df.groupby('UOA name').agg({'FTE staff':'sum'})
    
    total = df['FTE staff'].sum()

    fte_kpi_card = generateKPICard(
        "Staff FTE",
        format_value(total),
        "2013-2019 (Total)",
        'fte',
        "Full-time equivalent of all staff with significant responsibility for research."
    )

    return fte_kpi_card

def generateInKindKPICard(type, uni, uoa, reg):
    df = incomeiK_df[incomeiK_df['Income source'] != 'Total income']

    if type == 'ins':
        if (uoa == 'All'):
            df = df.loc[
                (df["Institution name"] == uni)
            ]
        else:
            df = df.loc[
                (df["Institution name"] == uni) &
                (df["UOA name"] == uoa)
            ]
    elif type == 'reg':
        df = df[df['Region'] == reg]
        if uoa != 'All':
            df = df[df['UOA name'] == uoa]
    else:
        if uoa != 'All':
            df = df[df["UOA name"] == uoa]
    
    total = df['2013-2020 (total)'].sum()

    ik_kpi_card = generateKPICard(
        "Income In-Kind",
        f'£{format_value(int(total))}',
        "2013-2020 (Total)",
        'in-kind',
        "Non-monetary resources received to support research actvities (e.g. staff resource, time allocated to use equipment, spaces, etc.)"
    )

    return ik_kpi_card

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

def generateRankingCards(type, uni, uoa):
    if (type == 'reg') or (type == 'nat'):
        return ['', '']
    
    results_overall = results_df[results_df["Profile"] == "Overall"]

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

## Visualisation Generation for Regional Overview page
def generateRegionScatterPlots(chart_type, region, uoa, gpa_profile):
    if chart_type == 'phd':
        df = phd_df
        x_value = 'Total'
        x_label = 'PhDs Awarded (log scale)'
        title = f'{gpa_profile} GPA vs. PhDs Awarded'
    if chart_type == 'income':
        df = income_df
        x_value = '2013-2020 (total)'
        title = f'{gpa_profile} GPA vs. Income'
        x_label = "13'-20' Income (log scale)"
    if chart_type == 'incomeik':
        df = incomeiK_df
        x_value = '2013-2020 (total)'
        title = f'{gpa_profile} GPA vs. Income In-Kind'
        x_label = "13'-20' Income In-Kind (log scale)"

    if uoa != 'All':
        gpa = results_df[(results_df['Region'].isin(region)) &
                         (results_df['UOA name'] == uoa) & 
                         (results_df['Profile'] == gpa_profile)]
        metric = df[(df['Region'].isin(region)) &
                    (df['UOA name'] == uoa)]
    else:
        gpa = results_df[results_df['Region'].isin(region) &
                         (results_df['Profile'] == gpa_profile)]
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
            title=f"{gpa_profile} GPA",
            color="#9b58b6",
            tickfont=dict(color="#9b58b6"),
            gridcolor='lightgrey',
            range=[0,4.1]
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

def generateRegionLineCharts(chart_type, region, uoa):
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
        x_axis_label = "PhDs Awarded"
    if chart_type == 'income':
        df = income_df[income_df['Income source'] != 'Total income']
        aggfunc = {
            '2013-14': 'sum',
            '2014-15': 'sum',
            '2015-2020 (avg)': 'sum',
        }
        title = "Research Income by Region"
        x_axis_label = "Amount (£)"

    df = df[df["Region"].isin(region)]

    if uoa != 'All':
        df = df[df['UOA name'] == uoa]

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
            x=x_end, y=y_end + 0.01*y_end,
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

def generateRegionIncomeSankey(region, uoa):
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

    category_colors = {
        "UK Sources": "rgba(166, 206, 227, 0.6)",        
        "EU Sources": "rgba(178, 223, 138, 0.6)",        
        "Non-EU Sources": "rgba(255, 164, 140, 0.6)",    
    }

    #darker shades of category_colors for the nodes
    node_colors = {
        "UK Sources": "#7198ac",        
        "EU Sources": "#7ca857",        
        "Non-EU Sources": "#c08c00",    
    }

    df = income_df
    df = df[~df["Income source"].isin(["Total income"])]
    df = df[df["Region"].isin(region)]

    if uoa != 'All':
        df = df[df['UOA name'] == uoa]

    df = df.groupby(['Region', 'Income source']).agg({'2013-2020 (total)':'sum'}).reset_index()

    df["Category"] = df["Income source"].map(
        {src: cat for cat, sources in income_cat.items() for src in sources}
    )

    all_nodes = list(set(df["Income source"]) | set(df["Category"]) | set(df["Region"]))

    # map labels to indices
    source_indices = [all_nodes.index(src) for src in df["Income source"]]
    category_indices = [all_nodes.index(cat) for cat in df["Category"]]

    # create source and target lists
    source = source_indices  
    target = category_indices  
    values = list(df["2013-2020 (total)"]) 

    flow_colors_individual = [category_colors[df["Category"].iloc[i]] for i in range(len(source_indices))]

    aggregated_flows = df.groupby(['Category', 'Region'])['2013-2020 (total)'].sum().reset_index()

    # map the indices for aggregated flows (Category → Region)
    agg_source_indices = [all_nodes.index(cat) for cat in aggregated_flows['Category']]
    agg_target_indices = [all_nodes.index(reg) for reg in aggregated_flows['Region']]
    agg_values = list(aggregated_flows['2013-2020 (total)'])

    flow_colors_aggregated = [category_colors[cat] for cat in aggregated_flows["Category"]]

    # update the source, target, and values to reflect the aggregated flows
    source += agg_source_indices
    target += agg_target_indices
    values += agg_values
    flow_colors = flow_colors_individual + flow_colors_aggregated

    node_color_list = []
    for node in all_nodes:
        if node in income_cat["UK Sources"] or node == "UK Sources":
            node_color_list.append(node_colors["UK Sources"])  # Darker shade for nodes
        elif node in income_cat["EU Sources"] or node == "EU Sources":
            node_color_list.append(node_colors["EU Sources"])  # Darker shade for nodes
        elif node in income_cat["Non-EU Sources"] or node == "Non-EU Sources":
            node_color_list.append(node_colors["Non-EU Sources"])  # Darker shade for nodes
        elif node in region:
            node_color_list.append('#e59b59')
        else:
            node_color_list.append("gray")
    
    wrapped_labels = [customwrap(label, width=40) for label in all_nodes]

    fig = go.Figure(go.Sankey(
        node=dict(
            pad=20,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=wrapped_labels,
            color=node_color_list,
            hovertemplate='Amount of funding by %{label}: £%{value:,.2f}<extra></extra>'
        ),
        link=dict(
            source=source,
            target=target,
            value=values,
            color=flow_colors,
            hovertemplate="Flow from %{source.label} → %{target.label}: £%{value:,.2f}<extra></extra>"
        )
    ))

    fig.update_layout(
        title=dict(text="Income Sources by Region", font=dict(color="#9b58b6")),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        title_font_size=18,
        font_size=12,
        font_family="Inter, sans-serif",
        margin = dict(t=50, l=35, r=35, b=10),
    )

    return fig

def generateRegionGPADist(region, uoa, gpa_profile):
    df = results_df[(results_df["Profile"] == gpa_profile) &
                    (results_df["Region"].isin(region))]
    data = []

    if uoa != 'All':
        df = df.groupby('Region').agg({'GPA':'mean'}).reset_index()
        df['GPA'] = np.round(df['GPA'],2)
        fig = px.bar(
            df,
            x='Region',
            y='GPA',
            text='GPA',
            color='Region',
        )

        fig.update_layout(
            title=dict(text=f"{gpa_profile} GPA Comparison", font=dict(color="#9b58b6")),
            xaxis=dict(
                title="Region",
                color="#9b58b6",
                tickfont=dict(color="#9b58b6"),
                ),
            yaxis=dict(
                title=f"{gpa_profile} GPA",
                color="#9b58b6",
                tickfont=dict(color="#9b58b6"),
                range=[0,4],
                ),
            plot_bgcolor="rgba(0, 0, 0, 0)",
            showlegend=False,
            title_font_size=18,
            font_family="Inter, sans-serif",
            margin = dict(t=50, l=35, r=35, b=10),
        )

    else:
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
            title=dict(text=f"{gpa_profile} GPA Distribution by Region", font=dict(color="#9b58b6")),
            xaxis=dict(
                title=f"{gpa_profile} GPA",
                color="#9b58b6",
                tickfont=dict(color="#9b58b6"),
                gridcolor='lightgrey',
                range=[0,4],
                ),
            yaxis=dict(
                title = 'Density',
                color="#9b58b6",
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

## TBC
def generateMap(df, data):

    if data == "Staff FTE":
        color = "FTE staff"
    if data in ["Overall GPA", 'Outputs GPA', 'Environment GPA', 'Impact GPA']:
        color = "GPA"
    if data == 'PhDs Awarded':
        color = 'Total'
    if data in ['Income', 'Income In-Kind']:
        color = '2013-2020 (total)'

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
        title=f"Regional Comparison of {data}",
    )

    map_graph.update_layout(
        title=dict(text=f"Regional Comparison of {data}", font=dict(color="#9b58b6")),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        showlegend=False,
        title_font_size=18,
        font_family="Inter, sans-serif",
        margin = dict(t=40, l=10, r=10, b=10),
    )
    
    return map_graph

def generateDataFrameForMap(data, uoa):
    if (data == "Overall GPA"):
        df = results_df[results_df["Profile"] == "Overall"]
        agg_func_dict = {
            "GPA":"mean"
        }
    elif (data == "Outputs GPA"):    
        df = results_df[results_df["Profile"] == "Outputs"]
        agg_func_dict = {
            "GPA":"mean"
        }
    elif (data == "Environment GPA"):
        df = results_df[results_df["Profile"] == "Environment"]
        agg_func_dict = {
            "GPA":"mean"
        }
    else:
        df = results_df[results_df["Profile"] == "Impact"]
        agg_func_dict = {
            "GPA":"mean"
        }

    if (data == "Staff FTE"):
        df = results_df[results_df["Profile"] == "Overall"]
        agg_func_dict = {
            "FTE staff":'sum'
        }
    if data == "PhDs Awarded":
        df = phd_df
        agg_func_dict = {
            'Total':'sum'
        }
        
    if data == "Income":
        df = income_df[income_df['Income source'] != 'Total income']
        agg_func_dict = {
            '2013-2020 (total)':'sum'
        }
        
    if data == "Income In-Kind":
        df = incomeiK_df[incomeiK_df['Income source'] != 'Total income']
        agg_func_dict = {
            '2013-2020 (total)':'sum'
        }
    
    if uoa != "All":
        df = df[df['UOA name'] == uoa]
    
    df = df.groupby("Region").agg(agg_func_dict).reset_index()

    return df

