import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

# Define the API URL for mutual fund schemes
schemes_api_url = "https://api.mfapi.in/mf"

# Define the API URL for NAV data
nav_api_url = "https://api.mfapi.in/mf/"

# Fetch the list of mutual funds and organize it into a DataFrame
response = requests.get(schemes_api_url)

if response.status_code == 200:
    mutual_funds_data = response.json()
    df_mutual_funds = pd.DataFrame(mutual_funds_data)
    df_mutual_funds = df_mutual_funds[['schemeCode', 'schemeName']]
else:
    st.error("Error fetching mutual fund data from the API.")

# Initialize session_state to store selected mutual funds and filter keyword
if 'selected_funds' not in st.session_state:
    st.session_state.selected_funds = []
if 'filter_keyword' not in st.session_state:
    st.session_state.filter_keyword = ""

# Streamlit UI
st.title("Mutual Fund Analyzer")

# Clear existing selected funds
if st.button("Clear Selected Funds"):
    st.session_state.selected_funds = []

# Filter funds by keyword
st.session_state.filter_keyword = st.text_input("Filter Funds by Keyword")

# Select mutual funds based on the filter keyword and add them to the special list
selected_funds = st.multiselect("Select Mutual Funds", df_mutual_funds[df_mutual_funds['schemeName'].str.contains(st.session_state.filter_keyword, case=False)]['schemeName'])

if st.button("Add Selected Funds"):
    if selected_funds:
        for fund_name in selected_funds:
            scheme_code = df_mutual_funds.loc[df_mutual_funds['schemeName'] == fund_name, 'schemeCode'].values[0]
            
            # Check if the fund is not already in the list
            if not any(fund['name'] == fund_name for fund in st.session_state.selected_funds):
                st.session_state.selected_funds.append({'name': fund_name, 'code': scheme_code})
        st.success("Selected funds added to the special list.")
    else:
        st.warning("Please select at least one mutual fund.")

# Display selected funds in the special list
if st.session_state.selected_funds:
    st.subheader("Special List - Selected Mutual Funds:")
    for fund in st.session_state.selected_funds:
        st.write(f"- Name: {fund['name']}, Code: {fund['code']}")

# Fetch and display NAV data for selected funds
if st.button("Fetch NAV Data"):
    st.subheader("NAV Data for Selected Funds:")
    
    # Create a list of dictionaries to store NAV data
    nav_data_list = []
    
    for fund in st.session_state.selected_funds:
        scheme_code = fund['code']
        
        # Fetch NAV data
        response = requests.get(f"{nav_api_url}{scheme_code}")
        if response.status_code == 200:
            nav_data = response.json()
            fund_info = nav_data['meta']
            nav_list = nav_data['data']
            
            # Extract NAV for today and one year ago, converting them to float
            today_nav = float(nav_list[0]['nav'])
            one_year_ago = (datetime.now() - timedelta(days=365)).strftime('%d-%m-%Y')
            one_year_ago_nav = None
            for entry in nav_list:
                if entry['date'] == one_year_ago:
                    one_year_ago_nav = float(entry['nav'])
                    break
            
            # Calculate percentage change
            if today_nav is not None and one_year_ago_nav is not None:
                percentage_change = ((today_nav - one_year_ago_nav) / one_year_ago_nav) * 100
            else:
                percentage_change = None
            
            nav_data_list.append({'Fund Name': fund_info['scheme_name'], 'Today NAV': today_nav, '1-Year Ago NAV': one_year_ago_nav, 'Percentage Change': percentage_change})
        else:
            st.write(f"Error fetching data for fund: {fund['name']}")

    # Convert the list of dictionaries to a DataFrame
    df_nav_data = pd.DataFrame(nav_data_list)
    
    # Display NAV data in descending order of percentage change
    df_nav_data_sorted = df_nav_data.sort_values(by='Percentage Change', ascending=False)
    st.dataframe(df_nav_data_sorted)
