import pandas as pd
from dash import dcc, html
import dash_bootstrap_components as dbc
import textwrap
import plotly.express as px
import plotly.graph_objects as go

# read in datasets
results_df = pd.read_csv('data/results_cleaned.csv')
income_df = pd.read_csv('data/income_cleaned.csv')
incomeiK_df = pd.read_csv('data/incomeiK_cleaned.csv')
phd_df = pd.read_csv('data/phd_awarded_cleaned.csv')

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

## Helper Functions
def customwrap(s, width=30):
    if (s != None):
        return "<br>".join(textwrap.wrap(s,width=width))
    else:
        return None

def generateIncomeChart(uni, uoa, df, inkind=False):
    # agg functions
    if (inkind):
        agg_func = {
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
        agg_func = {
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
                            ].agg(agg_func)
    else:
        df_filtered = df.loc[(df["Institution name"] == uni) 
                            & (df['Income source'] == col_name)
                            & (df["UOA name"] == uoa)].agg(agg_func)
        

    # graph cards
    if (inkind):
        chart = px.line(df_filtered,
                        title=title,
                        markers=True,)
    else:
        chart = px.bar(df_filtered,
                        text_auto=True,
                        title=title,)
    

    chart.update_traces(
        marker_color="#800080",
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.1)", font_size=12),
        hovertemplate="<b>%{x}</b><br>Value: £%{y:,}",
    )

    chart.update_layout(
        xaxis_title="Year",
        yaxis_title="Amount (£)",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=35, r=35, t=60, b=40),
        showlegend=False,
        title_font_size=18,
        font_family="Inter, sans-serif",
    )

    return chart

def generatePhdChart(uni, uoa):
    agg_func = {
            '2013': 'sum',
            '2014': 'sum',
            '2016': 'sum',
            '2017': 'sum',
            '2018': 'sum',
            '2019': 'sum',
        }
    
    if (uoa == "All"):
        df_filtered = phd_df.loc[(phd_df["Institution name"] == uni)].agg(agg_func)
    else:
        df_filtered = phd_df.loc[(phd_df["Institution name"] == uni) &
                                 (phd_df["UOA name"] == uoa)].agg(agg_func)


    phd_awarded_chart = px.line(df_filtered,
                                markers=True,
                                title=f"Total PhDs Awarded")

    phd_awarded_chart.update_traces(
        marker_color="#800080",
        hoverlabel=dict(bgcolor="rgba(255, 255, 255, 0.1)", font_size=12),
        hovertemplate="<b>%{x}</b><br>PhDs Awarded: %{y}",
    )

    phd_awarded_chart.update_layout(
        xaxis_title="Year",
        yaxis_title="# of PhD degrees awarded",
        plot_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=35, r=35, t=60, b=40),
        showlegend=False,
        title_font_size=18,
        font_family="Inter, sans-serif",
    )

    return phd_awarded_chart

def generateIncomeCategoryChart(uni, uoa):

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
                                    .agg({'2013-2020 (avg)':'sum'})\
                                    .reset_index()\
                                    .sort_values(by="2013-2020 (avg)",ascending=False)

    # defining the treemap chart
    income_cat_chart = go.Figure(go.Treemap(
                    labels=["Average annual income"] + income_filter_agg['Income source'].tolist(),
                    parents=[""] + (len(income_filter_agg)) * ["Average annual income"],
                    values=[0] + income_filter_agg['2013-2020 (avg)'].tolist(),
                    marker_colorscale = ["#FFFFFF", "#800080"],
                ))
    

    income_cat_chart.update_layout(
        margin = dict(t=50, l=25, r=25, b=25),
        title="Research Income Sources (£avg/yr)",
        title_font_size=18,
        font_family="Inter, sans-serif",
        font_size=14,
    )
    
    income_cat_chart.update_traces(
        hovertemplate='%{label}<br>Avg funding: £%{value}/yr<br>',
        texttemplate="%{label}<br><br>£%{value}",
    )

    return income_cat_chart

def generateIncomeInKindPieChart(uni, uoa):
    if (uoa == 'All'):
        income_filtered = incomeiK_df.loc[
            (incomeiK_df["Institution name"] == uni) &
            (incomeiK_df["Income source"] != "Total income")
        ]
    else:
        income_filtered = incomeiK_df.loc[
            (incomeiK_df["Institution name"] == uni) &
            (incomeiK_df["Income source"] != "Total income") &
            (incomeiK_df["UOA name"] == uoa)
        ]

    incomeik_pie_chart = go.Figure(
        data=[
            go.Pie(
                labels=income_filtered['Income source'],
                values=income_filtered['2013-2020 (avg)'],
            )
        ]
    )

    incomeik_pie_chart.update_traces(
        marker=dict(colors=["#800080", "#bc8bd0"]),
        hole=0.7,
        textposition= "outside",
        texttemplate="%{label}<br>%{percent}",
        hovertemplate='%{label}<br>Avg funding: £%{value}/yr<br>',
    )

    incomeik_pie_chart.update_layout(
        margin = dict(t=50, l=25, r=25, b=25),
        showlegend = False,
    )

    incomeik_pie_chart.add_annotation(
        x=0.5,
        y=0.5,
        align="center",
        xref="paper",
        yref="paper",
        showarrow=False,
        font_size=18,
        font_family="Inter, sans-serif",
        text="Research In-Kind Income<br>Sources (£avg/yr)",
    )

    return incomeik_pie_chart