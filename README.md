# Cryptography Assignment

A collection of projects that are related to cryptography.

## Features

- Credit card number generation and validation with luhn algorithm
- Hamming code encryption and decryption for even and odd
- Hashed password cracking demonstration using brute force and dictionary attacks
- Hiding a string in another by encoding into invisible characters

## Run locally

### Prerequisite

- [Python 3.8 or 3.9](https://www.python.org/)

### Steps

Open the project root folder in terminal

Install the requirements by running

```bash
python -m pip install -r requirements.txt
```

Do the setup and run the django app

```bash
python manage.py migrate
python manage.py loaddata credit_card.json
python manage.py collectstatic
python manage.py runserver
```

Then you can open the url the server was started on
