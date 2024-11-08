import boto3
from src.utils import (
    store_secret,
    list_secrets,
    retrieve_secret,
    delete_secret,
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

        if choice == "x":
            print("\nThank you. Goodbye")
            break


if __name__ == "__main__":
    run_password_manager()
