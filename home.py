import streamlit as st
import pandas as pd
import numpy as np
import re

st.set_page_config(layout="wide")
steam_path = "./data/total_steam_titles.xlsx"
roblox_path = "./data/total_roblox_experiences.xlsx"
steam_charts_path = "./data/total_steam_charts.xlsx"
total_steam_charts = pd.read_excel(steam_charts_path, sheet_name=0)
steam_data = pd.read_excel(steam_path, sheet_name=0)
steam_sheet_names = pd.ExcelFile(steam_path).sheet_names

steam_data.rename(columns={'Indie Budget Dev': 'Indie Budget Dev (Found Online)'}, inplace=True)

curr_roblox_data = pd.read_excel(roblox_path, sheet_name=0, skiprows=1)
prev_roblox_data = pd.read_excel(roblox_path, sheet_name=1, skiprows=1)
roblox_sheet_names = pd.ExcelFile(roblox_path).sheet_names

# Streamlit Titel
st.title("Weekly Roblox and Steam Trends")

curr_tuesday = pd.to_datetime(steam_sheet_names[0], yearfirst=True)
# orubt*
# print(curr_tuesday)

last_tuesday = curr_tuesday - pd.DateOffset(weeks=1)
one_year_ago = curr_tuesday - pd.DateOffset(years=1)

# print("Curr_Tuesday")
# print(curr_tuesday)
# print("Last_Tuesday")
# print(last_tuesday)

st.info(body = f"🎮 Steam Data scraped on {steam_sheet_names[0]} from Global Top 100 Sellers.  \n 🏠 Roblox Data scraped on {roblox_sheet_names[0]} from Romonitor Top 50 Experiences.  \n ")


# st.warning(body="💡 Note: The next iteration will add estimated revenue/copies sold.")
st.warning(body="💡 Note: The next iteration will add estimated revenue/copies sold.")

def filter_greater_than(value):
    try:
        if int(value):
            # change this value for climbers in Game Weekly Change
            return int(value) if int(value) >= 15 else np.nan
    except:
        return np.nan
    
# def regex_number(string):
#     numbers = re.findall(r'\d+', string)
#     return numbers[0] if numbers else np.nan

def regex_number(value):
    # Ensure value is a string and non-null
    if isinstance(value, str):
        numbers = re.findall(r'\d+', value)
        return numbers[0] if numbers else np.nan  # Return the first match if found, else NaN
    return np.nan  # Return NaN if the value was not a string

# Ensure 'Game Price USD' column is consistently numeric, converting 'Free to Play' to 0 or NaN
steam_data['Game Price USD'] = pd.to_numeric(steam_data['Game Price USD'], errors='coerce').fillna(0)


steam_data["Game Ranking"] = list(steam_data.index+1)
steam_data['Game Release Date'] = pd.to_datetime(steam_data['Game Release Date'])
reordered_columns =['Game Ranking',
                    'Game',
                    'Indie',
                    'Indie Budget Dev (Found Online)',
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
                    'Game Steam Link',
                    'Estimated Revenue From Game Sales']
steam_drop_columns = ['Game Genre',
                      'Game Recent Reviews',
                      'Game Total Reviews',
                      'Game Weekly Change',
                      'Number of Appearances in Weekly Top 100']

# data processing steam
steam_data = steam_data[reordered_columns]
new_released = steam_data[(steam_data['Game Release Date'] <= curr_tuesday) & (steam_data['Game Release Date'] >= last_tuesday)].set_index(["Game Ranking"])
print(new_released["Game Release Date"])
print(new_released)
print("Curr_Tuesday")
print(curr_tuesday)
print("Last_Tuesday")
print(last_tuesday)

new_entrants = steam_data[(steam_data["Number of Appearances in Weekly Top 100"] == 1) & (steam_data["Game Weekly Change"] == "NEW")].set_index(["Game Ranking"])
steam_data['Climber Filtered'] = steam_data['Game Weekly Change'].apply(filter_greater_than)
climbers = steam_data.dropna(subset=['Climber Filtered']).set_index(["Game Ranking"])
new_released["Game Release Date"] = new_released["Game Release Date"].dt.date
new_entrants["Game Release Date"] = new_entrants["Game Release Date"].dt.date
climbers["Game Release Date"] = climbers["Game Release Date"].dt.date

new_released = new_released.drop(columns=steam_drop_columns)
new_entrants = new_entrants.drop(columns=steam_drop_columns)
climbers = climbers.drop(columns=steam_drop_columns)

########################################## TOP 10 STEAM GAMES BY 24H PEAK PLAYERS ##########################################
total_steam_charts = (
    total_steam_charts.head(10)  # Select top 10 rows
    .drop(total_steam_charts.columns[:2], axis=1)  # Drop first two columns
    .sort_values(by='Peak Players', ascending=False)  # Sort by 'Peak Players' descending
    .reset_index(drop=True)  # Reset index
)
total_steam_charts.index += 1  # Make index 1-based

# Reorder columns: move the third column to the first position
columns = total_steam_charts.columns.to_list()
columns = [columns[2], columns[0], columns[1]] + columns[3:]
# Reorder columns: move 'Game Name' to the first position
columns = ['Game Name'] + [col for col in columns if col != 'Game Name']
top_10_steam_games_by_24H_peak = total_steam_charts[columns]
###################################################################################

if not total_steam_charts.empty:
    st.subheader("Top 10 Steam Games by 24H Peak Players")
    st.table(top_10_steam_games_by_24H_peak.style.format({"Peak Players": "{:,.0f}", "Current Players": "{:,.0f}", "Hours Played": "{:,.0f}"}))
else:
    st.info("No Steam Charts available.")

if not new_released.empty:
    st.subheader("Titles in Global Top 100 Sellers Released in the Past Week")
    st.dataframe(new_released.style.format({"Game Price USD": "{:,.2f}", "Estimated Revenue From Game Sales": "{:.1f}M"}))
else:
    st.info(f"There were no new titles on the top 100 released within the past week")
if not new_entrants.empty:
    st.subheader("First Time Entrant Titles in Global Top 100 Sellers")
    st.dataframe(new_entrants.style.format({"Game Price USD": "{:,.2f}", "Estimated Revenue From Game Sales": "{:.1f}M"}))
else:
    st.info(f"There were no new entrants on the top 100 charts within the last week")

if not climbers.empty:
    st.subheader("Titles Climbed >15 Ranks Since Last Week on Global Top 100 Sellers")
    st.dataframe(climbers.style.format({"Game Price USD": "{:,.2f}", "Climber Filtered": "{:.0f}", "Estimated Revenue From Game Sales": "{:.1f}M"}))
else:
    st.info(f"There were no titles that climbed >15 ranks on top 100 charts for the week of {curr_tuesday} and {last_tuesday}")

# roblox data cleaning
curr_roblox_data["Rating"] = curr_roblox_data["Rating"]*100
# # Read previous week's data
# try:
#     prev_roblox_data = pd.read_excel(roblox_path, sheet_name=1, skiprows=1)
# except:
#     prev_roblox_data = pd.DataFrame()

# def normalize_name(name):
#     # Remove content within brackets
#     name = re.sub(r'\[.*?\]', '', name)
#     # Remove spaces
#     name = name.replace(' ', '')
#     name = re.sub(r'[^a-zA-Z]', '', name)
#     # Convert to lower case
#     name = name.lower()
#     return name
# # Apply the normalization function to the experience names
# prev_roblox_data['Normalized Name'] = prev_roblox_data['Experience Name'].apply(normalize_name)
# curr_roblox_data['Normalized Name'] = curr_roblox_data['Experience Name'].apply(normalize_name)

curr_roblox_data['ID from URL'] = curr_roblox_data["Romonitor Exp ID"].apply(regex_number)
prev_roblox_data['ID from URL'] = prev_roblox_data["Romonitor Exp ID"].apply(regex_number)

# Identify new entries into top 50 from previous week
old_experiences = set(prev_roblox_data['ID from URL'])
new_experiences = set(curr_roblox_data['ID from URL'])
roblox_new_entries = new_experiences - old_experiences
roblox_new_entries_df = curr_roblox_data[curr_roblox_data['ID from URL'].isin(roblox_new_entries)].sort_index().reset_index(drop=True)

# Ensure 'Release Date' is in datetime format
curr_roblox_data['Release Date'] = pd.to_datetime(curr_roblox_data['Release Date'], errors='coerce')
roblox_new_entries_df["Release Date"] = pd.to_datetime(roblox_new_entries_df["Release Date"], errors='coerce')

# Identify new releases in the past year that are in the current week's Top 50
roblox_new_releases = curr_roblox_data[curr_roblox_data['Release Date'] >= one_year_ago].sort_index().reset_index(drop=True)

# Convert 'Romonitor Ranking' columns to numeric, coercing errors to NaN
merged_roblox_data = curr_roblox_data.merge(prev_roblox_data, on='ID from URL', suffixes=('_curr', '_prev'))
merged_roblox_data['Romonitor Ranking_curr'] = pd.to_numeric(merged_roblox_data['Romonitor Ranking_curr'].str.replace('#', ''), errors='coerce')
merged_roblox_data['Romonitor Ranking_prev'] = pd.to_numeric(merged_roblox_data['Romonitor Ranking_prev'].str.replace('#', ''), errors='coerce')

# Identify experiences that jumped >15 spots in Romonitor Ranking
rank_jumps = merged_roblox_data[merged_roblox_data['Romonitor Ranking_prev'] - merged_roblox_data['Romonitor Ranking_curr'] > 15]

# Drop these columns before creating snapshot
roblox_drop_columns = ['Favourites', 'Likes', 'Dislikes','Romonitor Exp ID','ID from URL']

curr_roblox_data["Release Date"] = curr_roblox_data["Release Date"].dt.date
roblox_new_entries_df["Release Date"] = roblox_new_entries_df["Release Date"].dt.date
roblox_new_releases["Release Date"] = roblox_new_releases["Release Date"].dt.date

# curr_roblox_data.drop(columns=['ID from URL'], inplace=True)

# steam streamlit dataframes
if not curr_roblox_data.empty:
    st.subheader("Top 10 Roblox Experiences")
    st.dataframe(curr_roblox_data.head(10).drop(columns=roblox_drop_columns).style.format({"Rating": "{:,.0f}"}))
else:
    st.info(f"No Roblox Experiences... ask Alson.")

if not roblox_new_entries_df.empty:
    st.subheader("New Roblox Experience Entrants to Top 50")
    st.dataframe(roblox_new_entries_df.drop(columns=roblox_drop_columns).style.format({"Rating": "{:,.0f}"}))
else:
    st.info(f"No New Roblox Experience Entrants into the Top 50 from Last Week")

if not climbers.empty:
    st.subheader("Roblox Experiences Released in Past Year in Current Week's Top 50")
    st.dataframe(roblox_new_releases.drop(columns=roblox_drop_columns).style.format({"Rating": "{:,.0f}"}))
else:
    st.info(f"No Roblox Experiences in the Current Week's Top 50 were Released in the Past Year")

# if not rank_jumps.empty:
#     st.subheader("Roblox Experiences Jumped >15 Spots in Romonitor Ranking")
#     st.dataframe(rank_jumps[['Experience Name_curr', 'Romonitor Ranking_curr', 'Romonitor Ranking_prev']])
# else:
#     st.info("No Roblox Experiences Jumped >15 Spots in Romonitor Ranking")

# New section to share lists

# if not climbers.empty:
#     st.subheader("List of Steam Titles Climbed >15 Ranks:")
#     st.dataframe(climbers[['Game', 'Climber Filtered']])
# else:
#     st.info("No Steam Titles Climbed >15 Ranks.")

st.warning(body="If any steam game has data fields missing, it is either the steam deck or it's NSFW...", icon="⚠️")

st.write("made by your local :red[makers fund] intern")
