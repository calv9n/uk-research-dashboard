# tests/test_data_loading.py
import pytest
import pandas as pd
import os
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

def get_data_path(filename):
    return os.path.join(project_root, 'data', filename)

def test_csv_files_exist():
    """Test that all required CSV files exist."""
    required_files = [
        'income_cleaned.csv',
        'incomeik_cleaned.csv',
        'phd_awarded_cleaned.csv',
        'regions.csv',
        'results_cleaned.csv'
    ]

    
    for file_name in required_files:
        file_path = get_data_path(file_name)
        assert os.path.exists(file_path), f"Required file {file_path} does not exist"

def test_load_income_data():
    """Test loading income data."""
    df = pd.read_csv(get_data_path('income_cleaned.csv'))
    
    # Check basic properties of the dataframe
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_load_income_in_kind_data():
    """Test loading income in kind data."""
    df = pd.read_csv(get_data_path('incomeik_cleaned.csv'))
    
    # Check basic properties of the dataframe
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_load_phd_data():
    """Test loading phd data."""
    df = pd.read_csv(get_data_path('phd_awarded_cleaned.csv'))
    
    # Check basic properties of the dataframe
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_load_results_data():
    """Test loading results data."""
    df = pd.read_csv(get_data_path('results_cleaned.csv'))
    
    # Check basic properties of the dataframe
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_load_region_data():
    """Test loading region data."""
    df = pd.read_csv(get_data_path('regions.csv'))
    
    # Check basic properties of the dataframe
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_data_consistency():
    """Test for data consistency across related files."""
    regions_df = pd.read_csv(get_data_path('regions.csv'))

    files = [
        'income_cleaned.csv',
        'incomeik_cleaned.csv',
        'phd_awarded_cleaned.csv',
        'results_cleaned.csv'
    ]

    for f in files:
        df = pd.read_csv(get_data_path('income_cleaned.csv'))
    
        # Check that Region in income data exist in regions data
        if 'Region' in df.columns and 'Region' in regions_df.columns:
            df_regions = set(df['Region'].unique())
            master_regions = set(regions_df['Region'].unique())
            assert df_regions.issubset(master_regions), "Income data contains region IDs not in regions master data"

def test_regions_size():
    """Test that regions.csv size is as expected"""
    regions_df = pd.read_csv(get_data_path('regions.csv'))

    assert (regions_df.shape[0]) == 157, "Number of rows in regions.csv is not as expected (157)"