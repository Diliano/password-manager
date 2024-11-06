# AWS-Powered Password Manager

In this sprint, you will create a simple command-line application to store and retrieve passwords. The passwords will be stored in AWS Secrets Manager. Accessing your AWS account (with your Access Key ID and Secret Key) will be considered sufficient authorisation to retrieve the passwords.

## Outline

The application should allow you to:

- store a user ID and password as a secret in secretsmanager
- list all the stored secrets
- retrieve a secret - the resulting user ID and password should not be printed out but should be stored in a file.
- delete a secret

An example workflow:

```
# Assuming you have authenticated to an AWS account...
python password_manager.py
> Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:
y
> Invalid input. Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:
l
> 0 secret(s) available
> Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:
e
> Secret identifier:
Missile_Launch_Codes
> UserId:
bidenj
> Password:
Pa55word
> Secret saved.
> Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:
l
> 1 secret(s) available
  Missile_Launch_Codes
> Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:
r
> Specify secret to retrieve:
Missile_Launch_Codes
> Secrets stored in local file secrets.txt
> Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:
d
> Specify secret to delete:
Missile_Launch_Codes
> Deleted
> Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:
x
> Thank you. Goodbye.

# In the shell:
cat secrets.txt
UserId: bidenj
Password: Pa55word
```

## Components

### Utility functions to cover the user options:

#### Store Secret

- accepts secret_identifier, user_id and password
- stores the secret using the arguments provided
- display confirmation message

- unit testing

- possible errors: identifier already exists

#### List Secrets

- displays number of secrets available
- if more than 0, display their identifiers

- unit testing

#### Retrieve Secret

- accepts secret_identifier 
- writes the associated user_id and password to a file
- displays confirmation message

- unit testing

- possible errors: secret_identifier does not exist

#### Delete Secret

- accepts secret_identifier
- deletes the secret_identifer, associated user_id and password
- displays confirmation message

- unit testing

- possible errors: secret_identifier does not exist

### Main function to handle the user interface

#### Password Manager

- displays a menu with options for user action
- each action is mapped to a utility function + an additional exit option to leave the interface
- displays the result of actions that are mapped to a utility function OR an exit message if the relevant option is chosen

- integration testing

- possible errors: invalid user input (invalid selection or no input), any errors from the utility functions
