from src.utils import store_secret
import pytest
from moto import mock_aws
import os
import boto3


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
    def test_stores_secret_in_secretsmanager(self, mock_secretsmanager):
        # Arrange
        test_secret_id = "Top Secret Secret"
        test_user_id = "Secret User"
        test_password = "Secret password"
        # Act
        result = store_secret(
            mock_secretsmanager, test_secret_id, test_user_id, test_password
        )
        response = mock_secretsmanager.list_secrets()
        # Assert
        assert result == "Secret saved."

        assert response["SecretList"][0]["Name"] == test_secret_id
