import boto3
import requests

s3 = boto3.client("s3")

bucket_name = "user-tweets-991943d5bae2b44ccfb0a711279c8720"

# List objects in the bucket
response = s3.list_objects_v2(Bucket=bucket_name)

# Print available files
if "Contents" in response:
    for obj in response["Contents"]:
        print(obj["Key"])  # Prints file names
else:
    print("No files found in bucket.")

url = "https://user-tweets-991943d5bae2b44ccfb0a711279c8720.s3.us-east-1.amazonaws.com/your_file.json"  # Replace with your specific file
response = requests.get(url)

if response.status_code == 200:
    data = response.json()  # Assuming the file is in JSON format
    print(data)
else:
    print(f"Failed to retrieve data: {response.status_code}")
