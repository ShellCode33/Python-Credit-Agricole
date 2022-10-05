# coding: utf-8

"""
This Command Line Interface only aims to showcase how this library can be used.
It doesn't do anything useful.
"""

import os
import argparse
from getpass import getpass

from creditagricole.api import CreditAgricole, CreditAgricoleException
from creditagricole import CA_COUNTRIES

def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Welcome to the Credit Agricole utility')

    parser.add_argument('--country', choices=CA_COUNTRIES.keys(), help="the country you're in")
    parser.add_argument('--region', help="the region of the Credit Agricole you're affiliated to")

    args = parser.parse_args()
    return args

def summary(country: str, region: str) -> None:
    ca = CA_COUNTRIES[country](region) # type: CreditAgricole

    try:
        user_id = os.environ["CA_USER_ID"]
    except KeyError:
        user_id = input("User ID: ")

    try:
        pin_code = os.environ["CA_PIN_CODE"]
    except KeyError:
        pin_code = getpass("Pin code: ")

    ca.login(user_id, pin_code)
    print()

    print("LOANS")
    print("-" * 50)
    for loan in ca.loans:
        print(loan)
    print()

    print("INSURANCES")
    print("-" * 50)
    for insurance in ca.insurances:
        print(insurance)
    print()

    print("ACCOUNTS")
    print("-" * 50)

    for account in ca.accounts:
        print(account)
        print()

        print("Last transactions:")
        for operation in account.operations[:5]:
            print(operation)

        print("-" * 50)

def main() -> None:
    args = parse_cli()

    try:
        summary(args.country, args.region)
    except CreditAgricoleException as cae:
        print(f"[ERROR] {cae}")
