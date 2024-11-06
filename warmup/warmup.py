import boto3

# Creates an S3 bucket.

client = boto3.client("s3")
bucket_name = "nc-password-manager-warm-up-bucket"

client.create_bucket(
    Bucket=bucket_name, CreateBucketConfiguration={"LocationConstraint": "eu-west-2"}
)

# Loads two text files to the bucket.

with open("./warmup/text1.txt", "rb") as f:
    client.put_object(Bucket=bucket_name, Key="text1.txt", Body=f)

with open("./warmup/text2.txt", "rb") as f:
    client.put_object(Bucket=bucket_name, Key="text2.txt", Body=f)

# Prints a listing of the files, saving the filenames in a readable list.

response = client.list_objects_v2(Bucket=bucket_name)

filenames = [content["Key"] for content in response["Contents"]]

print(filenames)

# Reads one of the files and prints it to the console.

response = client.get_object(Bucket=bucket_name, Key="text1.txt")

print(response["Body"].read().decode("utf-8"))

# Deletes the files in the bucket.

client.delete_objects(
    Bucket=bucket_name, Delete={"Objects": [{"Key": "text1.txt"}, {"Key": "text2.txt"}]}
)

# Deletes the bucket.

client.delete_bucket(Bucket=bucket_name)

# Checks that the bucket is deleted by listing the available buckets (there should be none).

response = client.list_buckets()

print(response["Buckets"])
