import json
import os
import pandas as pd
from datetime import datetime

run = True

# List of specific JSON files to process
json_files = [
    "CoinDeskMarkets.json",
    "BloombergAsia.json",
    "BoredApeYC.json",
    "MarioNawfal.json",
    "CNBC.json",
    "CoinDesk.json",
    "BBCWorld.json",
    "DecryptMedia.json",
    "BBCNews.json",
    "ArweaveEco.json",
    "Aptos.json",
    "CurveCap.json",
    "Consensys.json",
    "MarketWatch.json",
    "DeGodsNFT.json",
    "Azuki.json",
    "Meter_IO.json",
    "Cardano.json",
    "IvanOnTech.json",
    "Bancor.json",
    "GordonGoner.json",
    "MetaMaskSupport.json",
    "BBCBreaking.json",
    "FT.json",
    "BrendanPedersen.json",
    "0xMarcB.json",
    "CharlotteFang77.json",
    "ABC.json",
    "BillAckman.json",
    "GnosisDAO.json",
    "MinaProtocol.json",
    "CryptoGarga.json",
    "2dcapital1.json",
    "AxieInfinity.json",
    "MihailoBjelic.json",
    "AptosLabs.json",
    "DLNewsInfo.json",
    "0xPolygonEco.json",
    "BitcoinMagazine.json",
    "AcalaNetwork.json",
    "Celo.json",
    "Neo_Blockchain.json",
    "Dune.json",
    "ETHGlobal.json",
    "0xPolygonDeFi.json",
    "CathieDWood.json",
    "ABCWorldNews.json",
    "BackTheBunny.json",
    "MantaNetwork.json",
    "Fxhedgers.json"
]

# Directory containing the JSON files
directory_path = "/Users/kimberly/Documents/Coding_projects/cryptotradingbot/local-directory/uploads/"

# Create a DataFrame to hold the tweets
start_date = datetime(2024, 3, 1)
time_range = pd.date_range(start=start_date, periods=24, freq='H')  # Use 'h' instead of 'H'
df = pd.DataFrame(index=time_range)

# Set to hold valid tweet times for quick lookup
valid_times = set(df.index)

if run:
    # Iterate over each specified file
    for filename in json_files:
        file_path = os.path.join(directory_path, filename)
        print(f"Processing file: {filename}")  # Debugging line

        # Load the JSON data from the file
        try:
            with open(file_path, "r") as file:
                tweets_data = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading {filename}: {e}")
            continue  # Skip to the next file if there's an error

        # Dictionary to hold tweet texts for each time
        tweet_texts = {time: [] for time in valid_times}

        # Iterate through each tweet
        for tweet in tweets_data:
            try:
                print("Processing tweet:", tweet)  # Debugging line
                # Check if 'content' and 'itemContent' exist
                if 'content' in tweet and 'itemContent' in tweet['content']:
                    item_content = tweet['content']['itemContent']
                    # Check if 'tweet_results' and 'result' exist
                    if 'tweet_results' in item_content and 'result' in item_content['tweet_results']:
                        tweet_result = item_content['tweet_results']['result']
                        # Check if 'legacy' exists
                        if 'legacy' in tweet_result:
                            legacy = tweet_result['legacy']
                            # Use the full_text from the current tweet
                            full_text = legacy.get('full_text', '')
                            created_at = legacy.get('created_at', '')

                            # Convert created_at to a datetime object
                            tweet_time = pd.to_datetime(created_at)

                            # Debugging: Print the tweet time and full text
                            print(f"Tweet time: {tweet_time}, Full text: {full_text}")

                            # Check if the tweet time is valid
                            if tweet_time in valid_times:
                                tweet_texts[tweet_time].append(full_text)  # Collect tweet texts
                            else:
                                print(f"Tweet time {tweet_time} not in valid times.")  # Debugging line
            except Exception as e:
                print(f"Error processing tweet: {e}")  # Log the error

        # Slot the collected tweet texts into the DataFrame
        # Use the filename without the .json extension as the column name
        column_name = os.path.splitext(filename)[0]
        for time, texts in tweet_texts.items():
            if texts:  # Only if there are texts to add
                df.at[time, column_name] = ' '.join(texts)  # Join texts into a single string

# Output the DataFrame
print("\nDataFrame of Tweets:")
print(df.fillna(''))  # Fill NaN with empty strings for better readability

# Check if DataFrame has any columns
if df.empty or df.columns.empty:
    print("Warning: The DataFrame is empty or has no columns.")
else:
    print("DataFrame columns:", df.columns.tolist())