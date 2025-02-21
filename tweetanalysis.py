import json

# Load the JSON data from the file
with open('local-directory/uploads/_charlienoyes.json', 'r') as file:
    tweets_data = json.load(file)

# Set to store unique tweets based on (timestamp, text) pairs
unique_tweets = set()

# Debugging: Print the total number of entries in the JSON
print(f"Total entries in JSON: {len(tweets_data)}")

# Initialize a counter
full_text_count = 0

# Extract timestamps and text
for index, tweet in enumerate(tweets_data):
    # Debugging: Print the current tweet being processed
    print(f"Processing tweet {index + 1}: {tweet}")

    # Check if 'content' and 'itemContent' exist
    if 'content' in tweet and 'itemContent' in tweet['content']:
        tweet_content = tweet['content']['itemContent']
        
        # Check if 'tweet_results' and 'result' exist
        if 'tweet_results' in tweet_content and 'result' in tweet_content['tweet_results']:
            tweet_result = tweet_content['tweet_results']['result']
            if 'core' in tweet_result and 'user_results' in tweet_result['core']:
                user_result = tweet_result['core']['user_results']['result']
                
                # Check if 'legacy' exists
                if 'legacy' in user_result:
                    legacy = user_result['legacy']
                    
                    # Extract 'created_at' and 'full_text' (or 'description')
                    tweet_text = legacy.get('full_text', legacy.get('description', "Text not available"))
                    tweet_timestamp = legacy.get('created_at', "Timestamp not available")
                    
                    # Add to the set of unique tweets
                    unique_tweets.add((tweet_timestamp, tweet_text))

                    # Check if 'full_text' exists in the legacy dictionary
                    if 'full_text' in legacy:
                        full_text_count += 1
                else:
                    print("Legacy data not found for user result.")
            else:
                print("User results not found in tweet result.")
        else:
            print("Tweet results not found in item content.")
    else:
        print("Content or item content not found in tweet.")

# Print the unique tweets
print("\nUnique Tweets:")
for timestamp, text in unique_tweets:
    print(f"Timestamp: {timestamp}, Text: {text}")

# Debugging: Print the number of unique tweets found
print(f"\nTotal unique tweets found: {len(unique_tweets)}")

# Output the count
print(f"Number of tweets with 'full_text': {full_text_count}")
