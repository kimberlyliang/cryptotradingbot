import os
import json
import matplotlib.pyplot as plt

def plot_timestamps_histogram(directory):
    timestamps = []

    # Loop through all files in the specified directory
    
    for filename in os.listdir(directory):
        print(filename)
        # Check if the file is a JSON file
        if filename.endswith('.json'):
            with open(os.path.join(directory, filename), 'r') as file:
                data = json.load(file)
                # Loop through each entry in the JSON data
                for entry in data:
                    print(entry)
                    # Check if the entry has the expected structure
                    if 'content' in entry and 'itemContent' in entry['content']:
                        item_content = entry['content']['itemContent']
                        if 'tweet_results' in item_content and 'result' in item_content['tweet_results']:
                            tweet_result = item_content['tweet_results']['result']
                            # Assuming the timestamp is in a field named 'created_at'
                            if 'created_at' in tweet_result['core']:
                                timestamps.append(tweet_result['core']['created_at'])

    # Plotting the histogram of timestamps
    plt.hist(timestamps, bins=30)
    plt.xlabel('Timestamps')
    plt.ylabel('Frequency')
    plt.title('Histogram of Timestamps')
    plt.show()

# Example usage
plot_timestamps_histogram('/Users/kimberly/Documents/Coding_projects/cryptotradingbot/local-directory/uploads')
