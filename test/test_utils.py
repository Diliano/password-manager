from src.utils import (
    store_secret,
    list_secrets,
    retrieve_secret,
    delete_secret,
    is_valid_secret_id,
)
import pytest
from moto import mock_aws
import os
import boto3
from botocore.exceptions import ClientError


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


class TestStoreSecret:
    def test_stores_secret_in_secretsmanager(self, mock_secretsmanager, capsys):
        # Arrange
        test_secret_id = "Top_Secret_Secret"
        test_user_id = "Secret User"
        test_password = "Secret password"
        # Act
        store_secret(mock_secretsmanager, test_secret_id, test_user_id, test_password)

        captured = capsys.readouterr()
        output = captured.out

        response = mock_secretsmanager.list_secrets()
        # Assert
        assert "✓ Secret saved." in output

        assert response["SecretList"][0]["Name"] == test_secret_id

    def test_provides_informative_message_if_secret_id_already_exists(
        self, mock_secretsmanager, capsys
    ):
        # Arrange
        test_secret_id = "Top_Secret_Secret"
        test_user_id = "Secret User"
        test_password = "Secret password"
        # Act
        store_secret(mock_secretsmanager, test_secret_id, test_user_id, test_password)
        _ = capsys.readouterr()  # ignore output

        store_secret(mock_secretsmanager, test_secret_id, test_user_id, test_password)
        captured = capsys.readouterr()
        output = captured.out
        # Assert
        assert "⚠️ Secret identifier already exists: Top_Secret_Secret" in output


class TestListSecrets:
    def test_confirms_if_there_are_no_secrets_stored(self, mock_secretsmanager, capsys):
        # Act
        list_secrets(mock_secretsmanager)
        captured = capsys.readouterr()
        output = captured.out
        # Assert
        assert "✓ 0 secret(s) available" in output

    def test_displays_number_of_secrets_with_secret_ids(
        self, mock_secretsmanager, capsys
    ):
        # Arrange
        test_secret_id = "Top_Secret_Secret"
        test_user_id = "Secret User"
        test_password = "Secret password"

        store_secret(mock_secretsmanager, test_secret_id, test_user_id, test_password)
        _ = capsys.readouterr()  # ignore output
        # Act
        list_secrets(mock_secretsmanager)
        captured = capsys.readouterr()
        output = captured.out
        # Assert
        assert "✓ 1 secret(s) available" in output
        assert "✓ Top_Secret_Secret" in output

    def test_handles_multiple_stored_secrets(self, mock_secretsmanager, capsys):
        # Arrange
        test_secret_id = "Top_Secret_Secret"
        test_secret_id_2 = "Even_More_Top_Secret_Secret"
        test_user_id = "Secret User"
        test_password = "Secret password"

        store_secret(mock_secretsmanager, test_secret_id, test_user_id, test_password)
        store_secret(mock_secretsmanager, test_secret_id_2, test_user_id, test_password)
        _ = capsys.readouterr()  # ignore output
        # Act
        list_secrets(mock_secretsmanager)
        captured = capsys.readouterr()
        output = captured.out
        # Assert
        assert "✓ 2 secret(s) available" in output
        assert "✓ Top_Secret_Secret, Even_More_Top_Secret_Secret" in output

    def test_list_secrets_client_error(self, mock_secretsmanager, monkeypatch, capsys):
        # Arrange
        error_response = {"Error": {"Code": "InternalServiceError"}}
        operation_name = "ListSecrets"

        def mock_list_secrets(*args, **kwargs):
            raise ClientError(error_response, operation_name)

        monkeypatch.setattr(mock_secretsmanager, "list_secrets", mock_list_secrets)
        # Act
        list_secrets(mock_secretsmanager)
        captured = capsys.readouterr()
        output = captured.out
        # Assert
        assert "⚠️ Internal error. Please try again later." in output


class TestRetrieveSecret:
    def test_retrieves_secret_writes_to_file(self, mock_secretsmanager, capsys):
        # Arrange
        test_secret_id = "Top_Secret_Secret"
        test_user_id = "Secret User"
        test_password = "Secret password"

        store_secret(mock_secretsmanager, test_secret_id, test_user_id, test_password)
        _ = capsys.readouterr()  # ignore output
        # Act
        retrieve_secret(mock_secretsmanager, test_secret_id)
        captured = capsys.readouterr()
        output = captured.out
        # Assert
        assert "✓ Secret stored in local file: secret.txt" in output

        with open("./secret.txt") as f:
            assert f.read() == "User ID: Secret User, Password: Secret password"

    def test_provides_informative_message_if_secret_id_does_not_exist(
        self, mock_secretsmanager, capsys
    ):
        # Act
        retrieve_secret(mock_secretsmanager, "Not_A_Real_Secret")
        captured = capsys.readouterr()
        output = captured.out
        # Assert
        assert "⚠️ No secret found with identifier: Not_A_Real_Secret" in output


class TestDeleteSecret:
    def test_deletes_secret(self, mock_secretsmanager, capsys):
        # Arrange
        test_secret_id = "Top_Secret_Secret"
        test_user_id = "Secret User"
        test_password = "Secret password"

        store_secret(mock_secretsmanager, test_secret_id, test_user_id, test_password)
        _ = capsys.readouterr()  # ignore output
        # Act
        num_secrets_before_delete = len(
            mock_secretsmanager.list_secrets()["SecretList"]
        )

        delete_secret(mock_secretsmanager, test_secret_id)
        captured = capsys.readouterr()
        output = captured.out

        num_secrets_after_delete = len(mock_secretsmanager.list_secrets()["SecretList"])
        # Assert
        assert "✓ Deleted secret with identifier: Top_Secret_Secret" in output

        assert num_secrets_before_delete == 1
        assert num_secrets_after_delete == 0

    def test_provides_message_if_secret_id_does_not_exist(
        self, mock_secretsmanager, capsys
    ):
        # Act
        delete_secret(mock_secretsmanager, "Not_A_Real_Secret")
        captured = capsys.readouterr()
        output = captured.out
        # Assert
        assert "⚠️ No secret found with identifier: Not_A_Real_Secret" in output


class TestIsValidSecretId:
    def test_confirms_a_valid_secret_id(self):
        # Arrange
        test_input = "Top_Secret_Secret"
        # Act
        result = is_valid_secret_id(test_input)
        # Assert
        assert result is True

        # Arrange
        test_input = "secret-101"
        # Act
        result = is_valid_secret_id(test_input)
        # Assert
        assert result is True

    def test_confirms_if_invalid_secret_id(self):
        # Arrange
        test_input = "Top_Secret?"
        # Act
        result = is_valid_secret_id(test_input)
        # Assert
        assert result is False

        # Arrange
        test_input = ""
        # Act
        result = is_valid_secret_id(test_input)
        # Assert
        assert result is False
