import os
import requests
import json
import pandas as pd

# Load API keys from environment variables
CG_API_KEY = os.getenv('CG_API_KEY')
SIM_API_KEY = os.getenv('SIM_API_KEY')

TOKEN_ID = 'usd-coin'  # CoinGecko token id
VS_CURRENCY = 'usd'
DAYS = 90  # number of days of historical data

TOKEN_ADDRESS = '0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48'  # USDC contract on Ethereum
CHAIN_ID = '1'

def fetch_coingecko_price(output_path):
    """
    Fetch historical price data for USDC from the public CoinGecko API and save to JSON.
    """
    url = f'https://api.coingecko.com/api/v3/coins/{TOKEN_ID}/market_chart'
    params = {'vs_currency': VS_CURRENCY, 'days': DAYS}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    with open(output_path, 'w') as f:
        json.dump(data, f)
    print(f'Saved price data to {output_path}')

def fetch_sim_whale_data(output_csv, limit_holders=50, tx_threshold=100000):
    """
    Retrieve whale transaction events (> tx_threshold USDC) from Sim.
    The function queries the top token holders and then fetches their activities.
    The results are written to a CSV with columns: datetime, value_token, wallet.
    """
    headers = {'X-Sim-Api-Key': SIM_API_KEY}
    # Get top token holders
    holders_url = f'https://api.sim.dune.com/v1/evm/token-holders/{CHAIN_ID}/{TOKEN_ADDRESS}'
    resp = requests.get(holders_url, headers=headers, params={'limit': limit_holders})
    resp.raise_for_status()
    holders = resp.json().get('holders', [])
    wallets = [h['wallet_address'] for h in holders]

    events = []
    threshold_units = tx_threshold * (10 ** 6)  # USDC has 6 decimals
    for wallet in wallets:
        act_url = f'https://api.sim.dune.com/v1/evm/activity/{wallet}'
        params = {'chain_ids': CHAIN_ID, 'limit': 200}
        r = requests.get(act_url, headers=headers, params=params)
        if r.status_code != 200:
            continue
        for tx in r.json().get('activity', []):
            if tx.get('token_address', '').lower() == TOKEN_ADDRESS.lower():
                value = int(tx['value'])
                if value >= threshold_units:
                    token_amount = value / (10 ** 6)
                    events.append({
                        'datetime': tx['block_time'],
                        'value_token': token_amount,
                        'wallet': wallet
                    })
    df = pd.DataFrame(events)
    df.to_csv(output_csv, index=False)
    print(f'Saved whale events to {output_csv}')

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    fetch_coingecko_price(os.path.join('data', 'usdc_price.json'))
    fetch_sim_whale_data(os.path.join('data', 'usdc_whale_events.csv'))