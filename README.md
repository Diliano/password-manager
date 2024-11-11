# Password Manager

Password Manager provides a command-line interface (CLI) to securely store, retrieve, list, and delete secrets in AWS Secrets Manager.

## Project Structure

- **src/**: Contains the main project code.
- **test/**: Holds all test cases for the application.
- **Makefile**: Automates setup, testing, and code quality checks.
- **.github/workflows/password-manager.yml**: CI pipeline configuration for GitHub Actions.

## Features

- **Secret Storage**: Store user IDs and passwords securely in AWS Secrets Manager.
- **Secret Retrieval**: Retrieve secrets and store them locally in a `secret.txt` file.
- **Secret Deletion**: Delete secrets by identifier.
- **Listing Secrets**: List all secrets stored in AWS Secrets Manager.

## Technologies and Tools Used

- **Python**: The primary language used throughout.
- **AWS Secrets Manager**: For securely managing and retrieving secrets (mocked in tests with Moto).
- **Boto3**: AWS SDK for Python to interact with AWS Secrets Manager.
- **Moto**: A library that mocks AWS services for local testing without actual AWS calls.
- **Pytest**: For unit and integration testing.
- **Flake8**: For linting and enforcing code style.
- **Black**: For code formatting.
- **GitHub Actions**: For continuous integration, running automated tests and checks on every push.
- **Make**: For task automation, managing environment setup, tests, and code checks.

## Requirements

- Python 3.12
- AWS account (for AWS Secrets Manager access)

## Setup

### Create Virtual Environment & Install Dependencies
1. Run the following command to set up the environment:
   ```bash
   make requirements
   ```

2. Install development tools:
   ```bash
   make dev-setup
   ```

## Usage

To start the password manager CLI:
```bash
python src/password_manager.py
```

## Makefile Commands

- **Environment Setup**
  - `make create-environment`: Creates a virtual environment.
  - `make requirements`: Installs project dependencies.

- **Development Setup**
  - `make dev-setup`: Installs `black`, `flake8`, and `coverage` tools.
  
- **Testing & Code Quality**
  - `make run-black`: Formats code with Black.
  - `make run-flake8`: Lints code with Flake8.
  - `make unit-test`: Runs all tests.
  - `make check-coverage`: Runs tests with coverage reporting.
  - `make run-checks`: Executes all checks: formatting, linting, tests, and coverage.

## CI/CD

This project uses GitHub Actions to automate testing on each push to the `main` branch. The workflow:
1. Checks out the code.
2. Sets up Python.
3. Installs dependencies and tools.
4. Runs `make run-checks` to ensure code quality and test coverage.

