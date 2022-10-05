# Python Credit Agricole

**DISCLAIMER : I AM NOT AFFILIATED TO THE CREDIT AGRICOLE IN ANY WAY, THIS IS AN UNOFFICIAL LIBRARY**

I'm looking for help to support other countries. I only have access to a french account.

This library has been made in a way that it should be easy to add support for other countries.

To do so, simply add API endpoints to `creditagricole/__init__.py`.

## Installation

```
$ pip install credit-agricole
```

## Usage

There's a command line tool that will allow you to have a brief summary of your bank
account :

```
$ creditagricole --help
usage: creditagricole [-h] [--country {france,italy,polska,ukraine,maroc,egypt}] [--region REGION]

Welcome to the Credit Agricole utility

options:
  -h, --help            show this help message and exit
  --country {france,italy,polska,ukraine,maroc,egypt}
                        the country you're in
  --region REGION       the region of the Credit Agricole you're affiliated to
```

For example you can run `creditagricole --country france --region aquitaine`.

But to be fair, this command line is not really useful.

This repo only contains the API to communicate with the Credit Agricole website, if
you want to get valuable insights about your bank accounts, head over to the [Work In Progress]().


## The API

```python
from creditagricole import CreditAgricoleFrance

ca = CreditAgricoleFrance("aquitaine") # pass the region of your affiliated Credit Agricole

user_id = input("User ID: ")
pin_code = getpass("Pin code: ")

ca.login(user_id, pin_code)

for account in ca.accounts:
    print(account)

    for operation in account.operations:
        print(operation)
```
