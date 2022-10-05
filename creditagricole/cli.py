# coding: utf-8

import os
import argparse
from getpass import getpass

from creditagricole.api import CreditAgricole
from creditagricole import CA_COUNTRIES

def parse_cli() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Welcome to the Credit Agricole utility')

    parser.add_argument('--country', choices=CA_COUNTRIES.keys(), help="the country you're in")
    parser.add_argument('--region', help="the region of the Credit Agricole you're affiliated to")

    args = parser.parse_args()
    return args

def main() -> None:
    args = parse_cli()

    try:
        user_id = os.environ["CA_USER_ID"]
    except KeyError:
        user_id = input("User ID: ")

    try:
        pin_code = os.environ["CA_PIN_CODE"]
    except KeyError:
        pin_code = getpass("Pin code: ")

    ca = CA_COUNTRIES[args.country](args.region) # type: CreditAgricole
    ca.login(user_id, pin_code)

    print("Accounts:")
    for account in ca.accounts:
        print(account)
    print()

    print("Loans:")
    for loan in ca.loans:
        print(loan)
    print()

    print("Insurances:")
    for insurance in ca.insurances:
        print(insurance)
