# Weekly Roblox and Steam Trends

This Streamlit application displays weekly trends for Roblox and Steam games. It highlights new releases, first-time entrants, and games that have climbed significantly in the rankings over the past week. 

Data for Steam Titles is scraped weekly from the global top 100 sellers list on steamstore.
Data for Roblox Experiences is scraped from the top experiences on RoMonitor (scraping top 50).
This repository does not include the code for the scrapers themselves, just the public visualizations.

## Installation

To run this application, you need to have Python installed. Follow the steps below to set up the project:

1. Clone this repository:
    ```bash
    git clone <repository-url>
    cd <repository-directory>
    ```

2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Data Preparation

Ensure you have an Excel file named `total_steam_titles.xlsx` in the `./data/` directory. The Excel file should contain the most recent relevant game data.

## Running the Application

To start the Streamlit application, run the following command:
```bash
streamlit run app.py
