# coding: utf-8

"""
This module is in charge of communicating with CreditAgricole's API.
"""

from requests import Session
from enum import IntEnum
from typing import List, Tuple

from creditagricole.account import Account
from creditagricole.insurance import Insurance
from creditagricole.loan import Loan

class ProductType(IntEnum):
    ACCOUNTS = 1
    AVAILABLE_SAVINGS_ACCOUNTS = 3
    LOANS = 4
    INSURANCES = 5
    OTHER_SAVINGS_ACCOUNTS = 7

class CreditAgricoleException(Exception):
    "Thrown when something unexpected happened"

class CreditAgricole:

    URL_PATTERN: str

    KEYPAD_ENDPOINT: str
    AUTH_ENDPOINT: str
    PRODUCT_ENDPOINT: str

    def __init__(self, region: str):
        """
        Parameters
        ----------
        region: str
            Credit Agricole's region you belong to (not sure this exists in all countries)
        """

        self._session = Session()
        self._region = region

    def _keypad_challenge(self, pin_code: str) -> Tuple[str, str]:
        """
        Parameters
        ----------
        pin_code: str
            Basically your password account.

        Notes
        -----
        JSON returned by the keypad API looks like this:
        {'keyLayout': ['9', '2', '3', '4', '5', '1', '0', '7', '8', '6'], 'keypadId': 'f3b22955-d5a1-42a0-127f-b352b4d7cbe0'}
        """
        keypad_url = type(self).URL_PATTERN.format(region=self._region,
                                                   endpoint=type(self).KEYPAD_ENDPOINT)
        keypad_json = self._session.post(keypad_url).json()

        key_layout = keypad_json["keyLayout"]
        uuid = keypad_json["keypadId"] # type: str
        secret = [] # type: List[str]

        for digit in pin_code:
            pos = key_layout.index(digit)

            if pos == -1:
                # Just in case, should never happen
                raise CreditAgricoleException(f"{digit} not found in key layout: {key_layout}")

            secret.append(str(pos))

        return uuid, ",".join(secret)

    def _get_product(self, product_type: ProductType):
        product_endpoint = type(self).PRODUCT_ENDPOINT.format(product_id=product_type)
        product_url = type(self).URL_PATTERN.format(region=self._region,
                                                    endpoint=product_endpoint)

        resp = self._session.get(product_url)

        if resp.status_code != 200:
            raise CreditAgricoleException(f"PRODUCT_ENDPOINT returned error "
                                          f"{resp.status_code} with content: {resp.content}")

        return resp.json()

    def login(self, user_id: str, pin_code: str):
        """
        Parameters
        ----------
        user_id: str
            User identifier, in France this is the bank account number.

        pin_code: str
            The pin code to access your account.
        """

        try:
            int(user_id)
            int(pin_code)
        except ValueError:
            raise CreditAgricoleException("user id and pin code are expected to "
                                          "be composed only of digits")
        keypad_uuid, secret = self._keypad_challenge(pin_code)

        auth_url = type(self).URL_PATTERN.format(region=self._region,
                                                 endpoint=type(self).AUTH_ENDPOINT)

        resp = self._session.post(auth_url, data={
            "keypadId": keypad_uuid,
            "j_username": user_id,
            "j_password": secret,
            "j_validate": "true",
        })

        if resp.status_code != 200:
            raise CreditAgricoleException("bad credentials")

    @property
    def accounts(self) -> List[Account]:
        accounts = [] # type: List[Account]

        for product_type in [ProductType.ACCOUNTS,
                             ProductType.AVAILABLE_SAVINGS_ACCOUNTS,
                             ProductType.OTHER_SAVINGS_ACCOUNTS]:
            accounts_json = self._get_product(product_type)

            for entry in accounts_json:
                # TBC : are JSON entries names the same for other countries ?
                accounts.append(Account(
                    id=entry["numeroCompte"],
                    owner=" ".join(entry["libellePartenaire"].split()),
                    balance=entry["solde"],
                    currency=entry["libelleDevise"],
                    label=entry["libelleProduit"],
                ))

        return accounts

    @property
    def loans(self) -> List[Loan]:
        loans = [] # type: List[Loan]
        loans_json = self._get_product(ProductType.LOANS)

        for entry in loans_json:
            repay_period_label = entry["libellePeriodicite"].lower()

            if repay_period_label != "mensuel":
                raise TypeError("dont know what to do, expected loan to be a "
                                f"monthly repay, got {repay_period_label}, "
                                "please open a GitLab issue")

            loans.append(Loan(
                id=entry["numeroCredit"],
                label=entry["libelleProduit"],
                amount=entry["montantInitial"],
                left_to_pay=entry["montantRestantDu"],
                must_pay_per_month=entry["montantEcheance"],
                currency=entry["libelleDevise"],
            ))

        return loans

    @property
    def insurances(self) -> List[Insurance]:
        insurances = [] # type: List[Insurance]
        insurances_json = self._get_product(ProductType.INSURANCES)

        for entry in insurances_json:
            insurances.append(Insurance(
                label=entry["libelleProduit"],
                status=entry["statutContrat"],
                description=entry["description"],
                max_amount=entry["capitalGaranti"],
                currency=entry["libelleDevise"],
            ))

        return insurances
