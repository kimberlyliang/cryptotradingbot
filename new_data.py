import boto3
from botocore import UNSIGNED
from botocore.config import Config
import pandas as pd
import json
import io

s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
bucket_name = "user-tweets-991943d5bae2b44ccfb0a711279c8720"

# get all objects from the s3url
response = s3.list_objects_v2(Bucket=bucket_name, Prefix="uploads/")

file_keys = [obj["Key"] for obj in response.get("Contents", []) if obj["Key"].endswith(".json")]

all_dfs = []

for file_key in file_keys:
    print(f"Processing: {file_key}")
    
    try:
        # s3 stuff 
        obj = s3.get_object(Bucket=bucket_name, Key=file_key)
        json_data = json.load(io.BytesIO(obj["Body"].read()))
        df = pd.DataFrame(json_data)

        df["source"] = file_key.split("/")[-1].replace(".json", "")

        all_dfs.append(df)
    except Exception as e:
        print(f"Error processing {file_key}: {e}")

# concatenate stuff 
if all_dfs:
    final_df = pd.concat(all_dfs, ignore_index=True)
    print("Final DataFrame shape:", final_df.shape)
    print(final_df.head())
else:
    print("No valid JSON files found in the bucket.")

print(all_dfs.head())