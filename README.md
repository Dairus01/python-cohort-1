# USDC Whale Activity Analysis

This repository analyses whether large on‑chain USDC transfers (whale activity) influence short‑term price movements.  

## Contents
* `data/` – pre‑downloaded datasets used in the notebook (`usdc_price.json` and `usdc_whale_events.csv`).
* `src/fetch_data.py` – script to fetch price data from CoinGecko and whale transaction events from Sim by Dune.  Requires API keys set in `.env`.
* `analysis.ipynb` – Jupyter Notebook performing data wrangling, time‑series analysis, visualisations and correlation analysis.
* `.env` – environment file where you should place your API keys.
* `requirements.txt` – Python dependencies.

## Running
1. Install dependencies: `pip install -r requirements.txt`.
2. Set your API keys in `.env`.
3. Run `python src/fetch_data.py` to download the latest data.
4. Open `analysis.ipynb` in Jupyter to reproduce the analysis.

## Notes
The data provided here represents a snapshot of 90 days of price and whale‑transaction history.  Use the fetch script to update it.