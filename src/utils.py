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


def list_secrets(client):
    try:
        response = client.list_secrets()

        num_secrets = len(response["SecretList"])
        secret_ids = [secret["Name"] for secret in response["SecretList"]]

        print(f"{num_secrets} secret(s) available")
        if secret_ids:
            print(f"{(", ".join(secret_ids))}")
    except ClientError as error:
        print(f"Internal error. Please try again in a few moments.")
        raise error
