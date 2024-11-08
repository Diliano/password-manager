import boto3
from src.utils import (
    store_secret,
    list_secrets,
    retrieve_secret,
    delete_secret,
    is_valid_secret_id,
)


def run_password_manager():
    secretsmanager_client = boto3.client("secretsmanager")

    while True:
        choice = input(
            "\n> Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it: "
        )

        if not choice:
            print("\n⚠️ Invalid input.")
            continue

        if choice not in {"e", "r", "d", "l", "x"}:
            print("\n⚠️ Invalid input.")
            continue

        if choice == "e":
            while True:
                secret_id = input("\n> Secret identifier: ")
                if is_valid_secret_id(secret_id):
                    break
                else:
                    print(
                        "\n⚠️ Invalid identifier: only letters, numbers, underscores and hyphens are permitted"
                    )
                    continue

            while True:
                user_id = input("\n> User ID: ")
                if user_id:
                    break
                else:
                    print("\n⚠️ Invalid input.")
                    continue

            while True:
                password = input("\n> Password: ")
                if password:
                    break
                else:
                    print("\n⚠️ Invalid input.")
                    continue

            try:
                store_secret(secretsmanager_client, secret_id, user_id, password)
                continue
            except:
                continue

        if choice == "x":
            print("\nThank you. Goodbye")
            break


if __name__ == "__main__":
    run_password_manager()
