import streamlit as st
import pandas as pd
import numpy as np
import re

st.set_page_config(layout="wide")
steam_path = "./data/total_steam_titles.xlsx"
roblox_path = "./data/total_roblox_experiences.xlsx"
steam_data = pd.read_excel(steam_path, sheet_name=0)
steam_sheet_names = pd.ExcelFile(steam_path).sheet_names
curr_roblox_data = pd.read_excel(roblox_path, sheet_name=0, skiprows=1)
roblox_sheet_names = pd.ExcelFile(roblox_path).sheet_names

# Streamlit Titel
st.title("Weekly Roblox and Steam Trends")

curr_tuesday = pd.to_datetime(steam_sheet_names[0], yearfirst=True)
last_tuesday = curr_tuesday - pd.DateOffset(weeks=1)
one_year_ago = curr_tuesday - pd.DateOffset(years=1)

st.info(body = f"Steam Data scraped on {steam_sheet_names[0]} from Global Top 100 Sellers.  \n Roblox Data scraped on {roblox_sheet_names[0]} from Romonitor Top 50 Experiences.",
        icon="🎮")


def filter_greater_than(value):
    try:
        if int(value):
            # change this value for climbers in Game Weekly Change
            return int(value) if int(value) >= 15 else np.nan
    except:
        return np.nan

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
steam_drop_columns = ['Game Genre',
                      'Game Recent Reviews',
                      'Game Total Reviews',
                      'Game Weekly Change',
                      'Number of Appearances in Weekly Top 100']

# data processing steam
steam_data = steam_data[reordered_columns]
new_released = steam_data[(steam_data['Game Release Date'] <= curr_tuesday) & (steam_data['Game Release Date'] >= last_tuesday)].set_index(["Game Ranking"])
new_entrants = steam_data[(steam_data["Number of Appearances in Weekly Top 100"] == 1) & (steam_data["Game Weekly Change"] == "NEW")].set_index(["Game Ranking"])
steam_data['Climber Filtered'] = steam_data['Game Weekly Change'].apply(filter_greater_than)
climbers = steam_data.dropna(subset=['Climber Filtered']).set_index(["Game Ranking"])
new_released["Game Release Date"] = new_released["Game Release Date"].dt.date
new_entrants["Game Release Date"] = new_entrants["Game Release Date"].dt.date
climbers["Game Release Date"] = climbers["Game Release Date"].dt.date

new_released = new_released.drop(columns=steam_drop_columns)
new_entrants = new_entrants.drop(columns=steam_drop_columns)
climbers = climbers.drop(columns=steam_drop_columns)


# steam streamlit dataframes
if not new_released.empty:
    st.subheader("Titles in Global Top 100 Sellers Released in the Past Week")
    st.dataframe(new_released)
else:
    st.info(f"There were no new titles on the top 100 released within the week of {curr_tuesday} and {last_tuesday}")
if not new_entrants.empty:
    st.subheader("First Time Entrant Titles in Global Top 100 Sellers")
    st.dataframe(new_entrants)
else:
    st.info(f"There were no new entrants on the top 100 charts for the week of {curr_tuesday} and {last_tuesday}")

if not climbers.empty:
    st.subheader("Titles Climbed >15 Ranks Since Last Week on Global Top 100 Sellers")
    st.dataframe(climbers)
else:
    st.info(f"There were no titles that climbed >15 ranks on top 100 charts for the week of {curr_tuesday} and {last_tuesday}")


# roblox data cleaning
curr_roblox_data["Rating"] = curr_roblox_data["Rating"]*100
# Read previous week's data
try:
    prev_roblox_data = pd.read_excel(roblox_path, sheet_name=1, skiprows=1)
except:
    prev_roblox_data = pd.DataFrame()

def normalize_name(name):
    # Remove content within brackets
    name = re.sub(r'\[.*?\]', '', name)
    # Remove spaces
    name = name.replace(' ', '')
    # Convert to lower case
    name = name.lower()
    return name
# Apply the normalization function to the experience names
prev_roblox_data['Normalized Name'] = prev_roblox_data['Experience Name'].apply(normalize_name)
curr_roblox_data['Normalized Name'] = curr_roblox_data['Experience Name'].apply(normalize_name)

# Identify new entries into top 50 from previous week
if not prev_roblox_data.empty:
    old_experiences = set(prev_roblox_data['Normalized Name'])
    new_experiences = set(curr_roblox_data['Normalized Name'])
    roblox_new_entries = new_experiences - old_experiences
    roblox_new_entries_df = curr_roblox_data[curr_roblox_data['Experience Name'].isin(roblox_new_entries)].sort_index().reset_index(drop=True)

else:
    roblox_new_entries_df = pd.DataFrame()

# Identify new releases in the past year that are in the current week's Top 50
roblox_new_releases = curr_roblox_data[curr_roblox_data['Release Date'] >= one_year_ago].sort_index().reset_index(drop=True)

# Drop these columns before creating snapshot
roblox_drop_columns = ['Favourites', 'Likes', 'Dislikes', 'Normalized Name']

curr_roblox_data["Release Date"] = curr_roblox_data["Release Date"].dt.date
roblox_new_entries_df["Release Date"] = roblox_new_entries_df["Release Date"].dt.date
roblox_new_releases["Release Date"] = roblox_new_releases["Release Date"].dt.date

# steam streamlit dataframes
if not curr_roblox_data.empty:
    st.subheader("Top 10 Roblox Experiences")
    st.dataframe(curr_roblox_data.head(10).drop(columns=roblox_drop_columns))
else:
    st.info(f"No Roblox Experiences...contact helen about data?")

if not roblox_new_entries_df.empty:
    st.subheader("New Roblox Experience Entrants to Top 50")
    st.dataframe(roblox_new_entries_df.drop(columns=roblox_drop_columns))
else:
    st.info(f"No New Roblox Experience Entrants into the Top 50 from Last Week")

if not climbers.empty:
    st.subheader("Roblox Experiences Released in Past Year in Current Week's Top 50")
    st.dataframe(roblox_new_releases.drop(columns=roblox_drop_columns))
else:
    st.info(f"No Roblox Experiences in the Current Week's Top 50 were Released in the Past Year")
