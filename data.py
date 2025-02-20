import boto3
import requests

# Ensure you have the correct credentials
aws_access_key_id = 'YOUR_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_SECRET_ACCESS_KEY'
aws_session_token = 'YOUR_SESSION_TOKEN'  # Only if using temporary credentials

s3 = boto3.client(
    "s3",
    aws_access_key_id=aws_access_key_id,
    aws_secret_access_key=aws_secret_access_key,
    aws_session_token=aws_session_token  # Include this line if using temporary credentials
)

bucket_name = "user-tweets-991943d5bae2b44ccfb0a711279c8720"

# List objects in the bucket
try:
    response = s3.list_objects_v2(Bucket=bucket_name)
    
    # Print available files
    if "Contents" in response:
        for obj in response["Contents"]:
            print(obj["Key"])  # Prints file names
    else:
        print("No files found in bucket.")
except Exception as e:
    print(f"Error occurred: {e}")

url = "https://user-tweets-991943d5bae2b44ccfb0a711279c8720.s3.us-east-1.amazonaws.com/your_file.json"  # Replace with your specific file
response = requests.get(url)

if response.status_code == 200:
    data = response.json()  # Assuming the file is in JSON format
    print(data)
else:
    print(f"Failed to retrieve data: {response.status_code}")
