import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(layout="wide")
steam_data = pd.read_excel("./data/total_steam_titles.xlsx", sheet_name=0)
st.title("Weekly Roblox and Steam Trends")

curr_tuesday = pd.to_datetime("2024-07-23", yearfirst=True)
last_tuesday = pd.to_datetime("2024-07-16", yearfirst=True)

def filter_greater_than(value):
    try:
        if int(value):
            # change this value for climbers in Game Weekly Change
            return int(value) if int(value) >= 15 else np.nan
    except:
        return np.nan
    
steam_data["Game Total Reviews"] = steam_data["Game Total Reviews"].fillna(0)
steam_data["Game Recent Reviews"] = steam_data["Game Recent Reviews"].fillna(0)

for index, row in steam_data.iterrows():
    if row["Game Total Reviews"] == 0 and row["Game Recent Reviews"] > 0:
        steam_data.at[index, "Game Total Reviews"] = row["Game Recent Reviews"]
        steam_data.at[index, "Game Recent Reviews"] = 0

steam_data["Game Ranking"] = list(steam_data.index+1)
steam_data['Game Release Date'] = pd.to_datetime(steam_data['Game Release Date'])
reordered_columns =['Game Ranking',
                    'Game',
                    'Game Developer',
                    'Game Publisher',
                    'Game Price USD',
                    'Game Release Date',
                    'Game Genre',
                    'Game Recent Reviews',
                    'Game Total Reviews',
                    'Game Description',
                    'Game Weekly Change',
                    'Number of Appearances in Weekly Top 100',
                    'Game Steam Link']

steam_data = steam_data[reordered_columns]

new_released = steam_data[(steam_data['Game Release Date'] <= curr_tuesday) & (steam_data['Game Release Date'] >= last_tuesday)].set_index(["Game Ranking"])
new_entrants = steam_data[(steam_data["Number of Appearances in Weekly Top 100"] == 1) & (steam_data["Game Weekly Change"] == "NEW")].set_index(["Game Ranking"])

steam_data['Climber Filtered'] = steam_data['Game Weekly Change'].apply(filter_greater_than)
climbers = steam_data.dropna(subset=['Climber Filtered']).set_index(["Game Ranking"])

new_released["Game Release Date"] = new_released["Game Release Date"].dt.date
new_entrants["Game Release Date"] = new_entrants["Game Release Date"].dt.date
climbers["Game Release Date"] = climbers["Game Release Date"].dt.date

if not new_released.empty:
    st.subheader("Titles in Global Top 100 Sellers Released in the Past Week")
    st.dataframe(new_released)
else:
    st.error(f"There were no new titles on the top 100 released within the week of {curr_tuesday} and {last_tuesday}")
if not new_entrants.empty:
    st.subheader("First Time Entrant Titles in Global Top 100 Sellers")
    st.dataframe(new_entrants)
else:
    st.error(f"There were no new entrants on the top 100 charts for the week of {curr_tuesday} and {last_tuesday}")

if not climbers.empty:
    st.subheader("Titles Climbed >15 Ranks Since Last Week on Global Top 100 Sellers")
    st.dataframe(climbers)
else:
    st.error(f"There were no titles that climbed >15 ranks on top 100 charts for the week of {curr_tuesday} and {last_tuesday}")





