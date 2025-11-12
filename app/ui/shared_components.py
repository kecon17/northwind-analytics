"""
Shared UI components for the Streamlit dashboard pages.
Manages session state for filters.
"""
import streamlit as st
import pandas as pd
from datetime import date

def create_download_button(df: pd.DataFrame, filename: str):
    """Creates a Streamlit download button for a DataFrame."""
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name=f"{filename}.csv",
        mime="text/csv",
    )

def get_quarter_options(sales_data: pd.DataFrame) -> dict:
    """Generates a dictionary of quarter-based date ranges."""
    sales_data['YearQuarter'] = sales_data['OrderDate'].dt.to_period('Q').astype(str)
    quarters = sorted(sales_data['YearQuarter'].unique())
    
    options = {"Full History": (sales_data['OrderDate'].min().date(), sales_data['OrderDate'].max().date())}
    for q in quarters:
        period = pd.Period(q)
        options[q] = (period.start_time.date(), period.end_time.date())
    return options

def initialize_state(sales_data: pd.DataFrame):
    """Initializes session state for filters if they don't exist."""
    if 'start_date' not in st.session_state:
        st.session_state.start_date = sales_data['OrderDate'].min().date()
        st.session_state.end_date = sales_data['OrderDate'].max().date()
        st.session_state.selected_regions = sorted(sales_data['Region'].unique())
        st.session_state.selected_countries = sorted(sales_data['Country'].unique())
        st.session_state.selected_categories = sorted(sales_data['CategoryName'].unique())

def render_sidebar(sales_data: pd.DataFrame) -> pd.DataFrame:
    """Renders the sidebar controls and returns the filtered DataFrame."""
    initialize_state(sales_data)

    st.sidebar.header("Dashboard Controls")

    # --- Quarter-based Date Selector ---
    quarter_options = get_quarter_options(sales_data)
    selected_quarter = st.sidebar.selectbox(
        "Select Timeframe",
        options=list(quarter_options.keys()),
        index=0 
    )
    st.session_state.start_date, st.session_state.end_date = quarter_options[selected_quarter]

    # --- Region Filter (Event-Driven) ---
    user_selected_regions = st.sidebar.multiselect(
        'Select Regions',
        options=sorted(sales_data['Region'].unique()),
        default=st.session_state.selected_regions
    )
    if user_selected_regions != st.session_state.selected_regions:
        st.session_state.selected_regions = user_selected_regions
        new_available_countries = sorted(sales_data[sales_data['Region'].isin(user_selected_regions)]['Country'].unique())
        st.session_state.selected_countries = new_available_countries
        st.rerun()

    # --- Country Filter (Event-Driven) ---
    available_countries = sorted(sales_data[sales_data['Region'].isin(st.session_state.selected_regions)]['Country'].unique())
    user_selected_countries = st.sidebar.multiselect(
        'Select Countries',
        options=available_countries,
        default=st.session_state.selected_countries
    )
    if user_selected_countries != st.session_state.selected_countries:
        st.session_state.selected_countries = user_selected_countries
        st.rerun()
    
    # --- Category Filter (Event-Driven) ---
    user_selected_categories = st.sidebar.multiselect(
        'Select Product Categories',
        options=sorted(sales_data['CategoryName'].unique()),
        default=st.session_state.selected_categories
    )
    if user_selected_categories != st.session_state.selected_categories:
        st.session_state.selected_categories = user_selected_categories
        st.rerun()

    # --- Reset Button ---
    if st.sidebar.button("Reset All Filters"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    # --- Final Data Filtering ---
    filtered_data = sales_data[
        (sales_data['Region'].isin(st.session_state.selected_regions)) &
        (sales_data['Country'].isin(st.session_state.selected_countries)) &
        (sales_data['CategoryName'].isin(st.session_state.selected_categories)) &
        (sales_data['OrderDate'].dt.date >= st.session_state.start_date) &
        (sales_data['OrderDate'].dt.date <= st.session_state.end_date)
    ]
    
    return filtered_data