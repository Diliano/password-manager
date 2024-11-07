import json
from botocore.exceptions import ClientError


def store_secret(client, secret_id, user_id, password):
    secret_string = json.dumps({"user_id": user_id, "password": password})
    try:
        client.create_secret(Name=secret_id, SecretString=secret_string)
        print("Secret saved.")
    except ClientError as error:
        if error.response["Error"]["Code"] == "ResourceExistsException":
            print(f"Secret identifier already exists: {secret_id}")
        else:
            print(f"Internal error. Please try again in a few moments.")
            raise error
