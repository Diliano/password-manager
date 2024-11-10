import json
from botocore.exceptions import ClientError
import re


def store_secret(client, secret_id, user_id, password):
    secret_string = json.dumps({"user_id": user_id, "password": password})
    try:
        client.create_secret(Name=secret_id, SecretString=secret_string)
        print("\n✓ Secret saved.")
    except ClientError as error:
        if error.response["Error"]["Code"] == "InvalidRequestException":
            print(
                f"\n⚠️ To reuse identifier: {secret_id}, please try "
                "again in a few moments."
            )
        else:
            exception_handler(error, secret_id)


def list_secrets(client):
    try:
        response = client.list_secrets()

        num_secrets = len(response["SecretList"])
        secret_ids = [secret["Name"] for secret in response["SecretList"]]

        print(f"\n✓ {num_secrets} secret(s) available")
        if secret_ids:
            print(f"\n✓ {(", ".join(secret_ids))}")
    except ClientError as error:
        exception_handler(error)


def retrieve_secret(client, secret_id):
    try:
        response = client.get_secret_value(SecretId=secret_id)

        secret_string = json.loads(response["SecretString"])
        user_id = secret_string["user_id"]
        password = secret_string["password"]

        with open("./secret.txt", "w") as f:
            f.write(f"User ID: {user_id}, Password: {password}")

        print("\n✓ Secret stored in local file: secret.txt")
    except ClientError as error:
        exception_handler(error, secret_id)


def delete_secret(client, secret_id):
    try:
        # workaround for moto quirk that does not raise ResourceNotFoundException
        client.describe_secret(SecretId=secret_id)

        client.delete_secret(SecretId=secret_id, ForceDeleteWithoutRecovery=True)
        print(f"\n✓ Deleted secret with identifier: {secret_id}")
    except ClientError as error:
        exception_handler(error, secret_id)


def exception_handler(error, secret_id=None):
    error_code = error.response["Error"]["Code"]

    match error_code:
        case "ResourceExistsException":
            print(f"\n⚠️ Secret identifier already exists: {secret_id}")
        case "ResourceNotFoundException":
            print(f"\n⚠️ No secret found with identifier: {secret_id}")
        case _:  # default behaviour
            print("\n⚠️ Internal error. Please try again in a few moments.")
            raise error


def is_valid_secret_id(secret_id):
    regex = re.compile(r"^[\w-]+$")
    if regex.search(secret_id):
        return True
    else:
        return False
