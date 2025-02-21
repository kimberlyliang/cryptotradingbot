import requests
import pandas as pd
from dotenv import load_dotenv
import os
import numpy as np


load_dotenv()
api_key = os.getenv('API_KEY')

list_of_coins = ['official-trump', 'dogwifcoin', 'ai16z', 'would', 'jeff-3', 'fartgirl', 'kekius-maximus', 'mother-iggy', 'woman-yelling-at-cat', 'elonia-trump', 'popcat']

df = pd.DataFrame()
api = False

for coin in list_of_coins: 
    url = f'https://api.coingecko.com/api/v3/coins/{coin}/market_chart/range'
    print(url)

    params = {  
    'vs_currency': 'usd', 
    'from': '1709269200',
    'to': '1739941200',
    'x-cg-demo-api-key': api_key
    }
    if api:
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

# Create a list of coin names to check against the tweets
coin_names = ['official-trump', 'dogwifcoin', 'ai16z', 'would', 'jeff-3', 'fartgirl', 
              'kekius-maximus', 'mother-iggy', 'woman-yelling-at-cat', 'elonia-trump', 
              'popcat', 'CoinDeskMarkets', 'BloombergAsia', 'BoredApeYC', 'MarioNawfal', 
              'CNBC', 'CoinDesk', 'BBCWorld', 'DecryptMedia', 'BBCNews', 'ArweaveEco', 
              'BillAckman', 'CathieDWood']

# After populating df, add a check
print("DataFrame before counting occurrences:")
print(df.head())  # Display the first few rows of df

# Check if 'date' column exists
if 'date' not in df.columns:
    print("Error: 'date' column not found in DataFrame.")
else:
    # Initialize a DataFrame to hold the counts
    counts_df = pd.DataFrame(index=df['date'])

    # Count occurrences of each coin name in the tweets DataFrame
    for coin in coin_names:
        counts_df[f'{coin}_count'] = df.apply(
            lambda row: row.astype(str).str.lower().str.contains(coin.lower(), case=False).any(), axis=1
        ).astype(int)

    # Merge the counts DataFrame with the existing DataFrame
    df = pd.merge(df, counts_df, on='date', how='outer')

print(df)


# algorithm
# Compute cumulative sentiment (S(t)) by summing tweet counts for each coin
sentiment_cols = [col for col in df.columns if '_count' in col]
df['cumulative_sentiment'] = df[sentiment_cols].sum(axis=1)

# Debugging: Check the cumulative_sentiment column
print("Cumulative Sentiment Column:")
print(df['cumulative_sentiment'])

# Check for NaN values in cumulative_sentiment
if df['cumulative_sentiment'].isnull().all():
    print("Error: 'cumulative_sentiment' column contains only NaN values.")
else:
    # Find maximum sentiment timestamp (T_s)
    T_s = df.loc[df['cumulative_sentiment'].idxmax(), 'date']

# Find maximum price timestamp (T_p) by identifying peak prices for each coin
price_cols = [col for col in df.columns if '_price' in col]
df['max_price'] = df[price_cols].max(axis=1)

# Debugging: Check the max_price column
print("Max Price Column:")
print(df['max_price'])

# Check for NaN values in max_price
if df['max_price'].isnull().all():
    print("Error: 'max_price' column contains only NaN values.")
    T_p = None  # Set T_p to None if max_price is all NaN
else:
    # Find maximum price timestamp (T_p)
    T_p = df.loc[df['max_price'].idxmax(), 'date']

# Check if T_p is defined before using it
if T_p is not None and 'cumulative_sentiment' in df.columns:
    # Compute ΔT_o = T_p - T_s
    df['ΔT_o'] = (T_p - T_s).days
else:
    print("Error: T_p is not defined or cumulative_sentiment column is missing.")

# Compute entry condition γ using cumulative probability
df['cumulative_probability'] = df['cumulative_sentiment'].cumsum() / df['cumulative_sentiment'].sum()

# Compute trading execution based on f'(x) = β ± ϵ
β = 0.8  # Example beta value
ϵ = 0.05  # Small error term
# Compute first derivative for optimal trading conditions
df['trade_execution'] = np.abs(df['sentiment_derivative']) >= (β * df['cumulative_sentiment'].max() / 10)
df['trade_entry'] = df['sentiment_derivative'] > 0
df['rolling_sentiment'] = df['cumulative_sentiment'].rolling(window=5, min_periods=1).mean()
df['sentiment_derivative'] = df['rolling_sentiment'].diff()
df['trade_execution'] = np.abs(df['sentiment_derivative']) >= (β * df['rolling_sentiment'].max() / 10)


df['trade_execution'] = np.abs(df['sentiment_derivative']) >= (β - ϵ)

# Display updated DataFrame