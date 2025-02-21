import requests
import pandas as pd
from dotenv import load_dotenv
import os


load_dotenv()
api_key = os.getenv('API_KEY')

list_of_coins = ['official-trump', 'dogwifcoin', 'ai16z', 'would', 'jeff-3', 'fartgirl', 'kekius-maximus', 'mother-iggy', 'woman-yelling-at-cat', 'elonia-trump', 'popcat']

df = pd.DataFrame()


for coin in list_of_coins: 
    url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range'
    print(url)

    params = {  
    'vs_currency': 'usd', 
    'from': '1709269200',
    'to': '1739941200',
    'x-cg-demo-api-key': api_key
    }
    
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        
        prices = data['prices']
        market_caps = data['market_caps']
        total_volumes = data['total_volumes']
        
        coin_df = pd.DataFrame({
            'date': [pd.to_datetime(price[0], unit='ms') for price in prices],
            f'{coin}_price': [price[1] for price in prices],
            f'{coin}_market_cap': [market_cap[1] for market_cap in market_caps],
            f'{coin}_total_volume': [total_volume[1] for total_volume in total_volumes]
        })
        
        if df.empty:
            df = coin_df
        else:
            df = pd.merge(df, coin_df, on='date', how='outer')
    else:
        print(f"Error: {response.status_code}")

print(df)
