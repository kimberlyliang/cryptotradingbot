import boto3
from botocore.config import Config
from botocore import UNSIGNED
import matplotlib.pyplot as plt

# Initialize S3 client without authentication (for public bucket)
s3 = boto3.client("s3", config=Config(signature_version=UNSIGNED))
bucket_name = "user-tweets-991943d5bae2b44ccfb0a711279c8720"

# List objects in the 'uploads/' folder
response = s3.list_objects_v2(Bucket=bucket_name, Prefix="uploads/")

# Extract all filenames
file_keys = [obj["Key"] for obj in response.get("Contents", [])]
print(len(file_keys))
# Print all filenames and their lengths
#for file_key in file_keys:
    # Get the file size from the response
   #file_size = next((obj["Size"] for obj in response.get("Contents", []) if obj["Key"] == file_key), 0)
    # print(f"{file_key}: {file_size} bytes")

# Prepare data for sorting
file_sizes_with_keys = [(file_key, next((obj["Size"] for obj in response.get("Contents", []) if obj["Key"] == file_key), 0)) for file_key in file_keys]

# Sort by file size in descending order and get top 50
top_contributors = sorted(file_sizes_with_keys, key=lambda x: x[1], reverse=True)[:50]

# Print top 50 contributors
print("Top 50 Contributors:")
for file_key, file_size in top_contributors:
    print(f"{file_key}: {file_size} bytes")

# Prepare data for histogram (top 50 contributors)
top_file_keys = [file_key for file_key, _ in top_contributors]
top_file_sizes = [file_size for _, file_size in top_contributors]

# Plotting the histogram for top 50 contributors
plt.figure(figsize=(10, 6))
plt.bar(top_file_keys, top_file_sizes, color='blue')
plt.xlabel('File Names')
plt.ylabel('File Sizes (bytes)')
plt.title('Top 50 File Sizes in uploads/ Folder')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()


