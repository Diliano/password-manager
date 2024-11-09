from src.password_manager import run_password_manager
from moto import mock_aws
import boto3
import pytest
import os


@pytest.fixture(scope="function")
def aws_credentials():
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "eu-west-2"


@pytest.fixture(scope="function")
def mock_secretsmanager(aws_credentials):
    with mock_aws():
        yield boto3.client("secretsmanager")


def test_store_list_retrieve_delete_secret(mock_secretsmanager, capsys, monkeypatch):
    # Arrange
    user_inputs = iter(
        [
            "e",  # Choose 'entry'
            "Top_Secret_Secret",  # Enter secret identifier
            "Secret User",  # Enter user ID
            "Secret password",  # Enter password
            "l",  # Choose 'list secrets'
            "r",  # Choose 'retrieve secret'
            "Top_Secret_Secret",  # Enter secret identifier to retrieve
            "d",  # Choose 'delete secret'
            "Top_Secret_Secret",  # Enter secret identifier to delete
            "x",  # Choose 'exit'
        ]
    )

    monkeypatch.setattr("builtins.input", lambda input: next(user_inputs))
    # Act
    run_password_manager()

    captured = capsys.readouterr()
    output = captured.out
    # Assert
    assert "✓ Secret saved." in output
    assert "✓ 1 secret(s) available" in output
    assert "✓ Secret stored in local file: secret.txt" in output

    with open("secret.txt") as f:
        content = f.read()
    assert content == "User ID: Secret User, Password: Secret password"

    assert "✓ Deleted secret with identifier: Top_Secret_Secret" in output
    assert "Thank you. Goodbye" in output
