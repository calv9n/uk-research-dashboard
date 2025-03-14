# tests/test_dashboard_components.py
import pytest
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc , html
import textwrap
from unittest.mock import patch
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from utils.dashboard_components import *

def get_data_path(filename):
    return os.path.join(project_root, 'data', filename)

@pytest.fixture
def sample_dataframe():
    return pd.DataFrame({
        "Institution name": ["Uni A", "Uni B", "Uni C", "Uni D", "Uni E"],
        "GPA": [3.5, 4.0, 3.2, 3.8, 3.6],
        "Income": [500000, 750000, 300000, 600000, 550000],
    })

@pytest.mark.parametrize(
    "input_value, expected_output",
    [
        (500, 500.0),     # Below 1,000 → rounded as is
        (999, 999.0),     # Edge case below 1,000
        (1_000, "1.0K"),  # 1,000 → converted to K
        (10_500, "10.5K"), # 10,500 → converted to K
        (1_000_000, "1.0M"), # 1M → converted to M
        (15_500_000, "15.5M"), # 15.5M → converted to M
        (1_000_000_000, "1.00B"), # 1B → converted to B
        (2_500_000_000, "2.50B"), # 2.5B → converted to B
    ]
)
def test_format_value(input_value, expected_output):
    assert format_value(input_value) == expected_output

def test_create_gpa_kpi_card():
    title = "Test KPI"
    card_id = "test-card-id"
    icon_class = "fa-chart-line"

    card = create_gpa_kpi_card(title, card_id, icon_class)

    # check if it is a dbc.Card
    assert isinstance(card, dbc.Card)

    # check if it contains a dcc.Loading
    assert isinstance(card.children, dcc.Loading)

    # check if the dcc.Loading contains dbc.CardBody
    card_body = card.children.children
    assert isinstance(card_body, dbc.CardBody)

    # check icon and check its class
    icon_element = card_body.children[0].children[0].children[0].children[0]
    assert isinstance(icon_element, html.I)
    assert icon_class in icon_element.className

    # check title and text elements
    title_element = card_body.children[0].children[0].children[1].children[0]
    text_element = card_body.children[0].children[0].children[1].children[1]
    
    # Check title text
    assert isinstance(title_element, html.H3)
    assert title_element.children == title

    # Check ID
    assert isinstance(text_element, html.H4)
    assert text_element.id == card_id  

def test_create_leaderboard(sample_dataframe):
    title = "Top Institutions"
    col = "GPA"

    leaderboard = create_leaderboard(title, sample_dataframe, col)

    # check it is a dbc.Card
    assert isinstance(leaderboard, dbc.Card)

    # check it contains dcc.Loading component
    assert isinstance(leaderboard.children, dcc.Loading)

    # check if dcc.Loading contains a dbc.CardBody
    card_body = leaderboard.children.children
    assert isinstance(card_body, dbc.CardBody)

    # check if title is present
    title_element = card_body.children[0].children[1]
    assert isinstance(title_element, html.H3)
    assert title_element.children == title

    # check if table exists
    table = card_body.children[1]
    assert isinstance(table, dbc.Table)

    # th
    table_head = table.children[0]
    assert isinstance(table_head, html.Thead)

    header_row = table_head.children
    assert isinstance(header_row, html.Tr)
    assert len(header_row.children) == 3  # Rank, Institution name, GPA
    assert header_row.children[0].children == "Rank"
    assert header_row.children[1].children == "Institution name"
    assert header_row.children[2].children == col

    # check sorting
    table_body = table.children[1]
    assert isinstance(table_body, html.Tbody)

    rows = table_body.children
    # Should not exceed 10 rows
    assert len(rows) == min(10, len(sample_dataframe))  

    sorted_df = sample_dataframe.sort_values(col, ascending=False).head(10).reset_index(drop=True)

    for i, row in enumerate(rows):
        assert isinstance(row, html.Tr)
        assert row.children[0].children == i + 1  
        assert row.children[1].children == sorted_df.iloc[i]["Institution name"]  
        assert row.children[2].children == np.round(sorted_df.iloc[i][col], 2) 

def test_customwrap():
    # normal wrapping
    text = "This is a long sentence that should be wrapped properly."
    wrapped_text = customwrap(text, width=10)
    expected = "<br>".join(textwrap.wrap(text, width=10))
    assert wrapped_text == expected

    # short string (should remain unchanged)
    short_text = "Short text"
    assert customwrap(short_text, width=20) == "Short text"

    # test exact width match (should not add <br>)
    exact_text = "This line is 30 chars long."
    assert customwrap(exact_text, width=30) == exact_text

    # input is None
    assert customwrap(None) is None

    # custom width (should break at 15 chars)
    custom_width_text = "This text should be wrapped at 15 characters."
    wrapped_custom_width = customwrap(custom_width_text, width=15)
    expected_custom_width = "<br>".join(textwrap.wrap(custom_width_text, width=15))
    assert wrapped_custom_width == expected_custom_width

@pytest.fixture
def mock_income_df():
    data = {
        'Institution name': ['Institution A', 'Institution A', 'Institution B', 'Institution B'],
        'Income source': ['Total income', 'Total income', 'Total income', 'Total income'],
        'UOA name': ['UOA 1', 'UOA 2', 'UOA 1', 'UOA 2'],
        'Region': ['Region 1', 'Region 2', 'Region 1', 'Region 2'],
        '2013-14': [1000, 2000, 1500, 2500],
        '2014-15': [1100, 2100, 1600, 2600],
        '2015-2020 (avg)': [1200, 2200, 1700, 2700]
    }
    return pd.DataFrame(data)

def test_generateIncomeChart_by_institution(mock_income_df):
    # Patching income_df in utils.dashboard_components
    with patch('utils.dashboard_components.income_df', mock_income_df):
        # call with different params
        chart = generateIncomeChart(type='ins', ins='Institution A', uoa='All', reg='')

        # chart type is plotly.go.Figure
        assert isinstance(chart, go.Figure)

        # chart title
        assert chart.layout.title.text == "Research Income"
        
        # x-axis title 
        assert chart.layout.xaxis.title.text == "Year"
        
        # y-axis title 
        assert chart.layout.yaxis.title.text == "Amount (£)"

        # line data matches expected mock data
        assert chart.data[0]['type'] == 'scatter'
        assert chart.data[0]['mode'] == 'lines+markers'
        assert chart.data[0]['hovertemplate'] == "<b>%{x}</b><br>Value: £%{y:,}<extra></extra>"

def test_generateIncomeChart_by_region(mock_income_df):
    with patch('utils.dashboard_components.income_df', mock_income_df):
        chart = generateIncomeChart(type='reg', ins='', uoa='UOA 1', reg='Region 1')

        # chart type is plotly.go.Figure
        assert isinstance(chart, go.Figure)
        
        # x,y axis titles
        assert chart.layout.xaxis.title.text == "Year"
        assert chart.layout.yaxis.title.text == "Amount (£)"
        
        # check data plotted
        assert len(chart.data) > 0  # make sure chart has data

def test_generateIncomeChart_by_type(mock_income_df):
    with patch('utils.dashboard_components.income_df', mock_income_df):
        chart = generateIncomeChart(type='other', ins='', uoa='UOA 1', reg='Region 1')

        # chart type is plotly.go.Figure
        assert isinstance(chart, go.Figure)
        
        # x,y axis titles
        assert chart.layout.xaxis.title.text == "Year"
        assert chart.layout.yaxis.title.text == "Amount (£)"
        
        # check data plotted
        assert len(chart.data) > 0  # make sure chart has data

# mock phd_df
@pytest.fixture
def mock_phd_df():
    data = {
        'Institution name': ['Institution A', 'Institution A', 'Institution B', 'Institution B'],
        'UOA name': ['UOA 1', 'UOA 2', 'UOA 1', 'UOA 2'],
        'Region': ['Region 1', 'Region 2', 'Region 1', 'Region 2'],
        '2013': [50, 60, 40, 70],
        '2014': [55, 65, 45, 75],
        '2015': [60, 70, 50, 80],
        '2016': [65, 75, 55, 85],
        '2017': [70, 80, 60, 90],
        '2018': [75, 85, 65, 95],
        '2019': [80, 90, 70, 100],
        'Total': [455, 530, 385, 595]
    }
    return pd.DataFrame(data)

def test_generatePhdChartAndKPICard_by_institution(mock_phd_df):
    with patch('utils.dashboard_components.phd_df', mock_phd_df):
        # call function with different params
        chart, kpi_card = generatePhdChartAndKPICard(type='ins', ins='Institution A', uoa='All', reg='')

        assert isinstance(chart, go.Figure)

        # chart layout
        assert chart.layout.title.text == "PhDs Awarded"
        assert chart.layout.xaxis.title.text == "Year"
        assert chart.layout.yaxis.title.text == "PhDs awarded"
        
        # chart data 
        assert len(chart.data) > 0  # make sure chart contains data

def test_generatePhdChartAndKPICard_by_region(mock_phd_df):
    with patch('utils.dashboard_components.phd_df', mock_phd_df):
        # call function with different params
        chart, kpi_card = generatePhdChartAndKPICard(type='reg', ins='', uoa='UOA 1', reg='Region 1')

        assert isinstance(chart, go.Figure)

        # chart layout
        assert chart.layout.title.text == "PhDs Awarded"
        assert chart.layout.xaxis.title.text == "Year"
        assert chart.layout.yaxis.title.text == "PhDs awarded"
        
        # chart data 
        assert len(chart.data) > 0  # make sure chart contains data

def test_generateKPICard():
    # sample input
    title = "Total Income"
    value = "£500,000"
    subtitle = "2013-2020 (Total)"
    icon_id = "income"
    tooltip = "This represents the total income for the institution over the specified period."

    card = generateKPICard(title, value, subtitle, icon_id, tooltip)

    # check div element
    assert isinstance(card, html.Div)  

    # check title H1
    h1_elements = [child for child in card.children if isinstance(child, html.H1)]
    assert len(h1_elements) == 2  # 2 H1 tags
    assert h1_elements[0].children == title  # 1) title
    assert h1_elements[1].children == value  # 2) value
