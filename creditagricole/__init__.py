# coding: utf-8

"""
A list of countries where CreditAgricole is established can be found there:
https://www.credit-agricole.com/en/business-lines-and-brands/all-brands
"""

from creditagricole.api import CreditAgricole

class CreditAgricoleFrance(CreditAgricole):
    URL_PATTERN = "https://www.credit-agricole.fr/ca-{region}/particulier{endpoint}"
    KEYPAD_ENDPOINT = "/acceder-a-mes-comptes.authenticationKeypad.json"
    AUTH_ENDPOINT = "/acceder-a-mes-comptes.html/j_security_check"
    PRODUCT_ENDPOINT = "/operations/synthese/_jcr_content.produits-valorisation.json/{product_id}"
    OPERATION_ENDPOINT = "/operations/synthese/detail-comptes/jcr:content.n3.operations.json?grandeFamilleCode={product_id}&compteIdx={account_index}&idDevise={currency}&count=2147483647"

class CreditAgricoleItaly(CreditAgricole):
    def __init__(self):
        raise NotImplementedError("sorry this country is not supported yet")

class CreditAgricolePolska(CreditAgricole):
    def __init__(self):
        raise NotImplementedError("sorry this country is not supported yet")

class CreditAgricoleUkraine(CreditAgricole):
    def __init__(self):
        raise NotImplementedError("sorry this country is not supported yet")

class CreditAgricoleMaroc(CreditAgricole):
    def __init__(self):
        raise NotImplementedError("sorry this country is not supported yet")

class CreditAgricoleEgypt(CreditAgricole):
    def __init__(self):
        raise NotImplementedError("sorry this country is not supported yet")

CA_COUNTRIES = {
    "france": CreditAgricoleFrance,
    "italy": CreditAgricoleItaly,
    "polska": CreditAgricolePolska,
    "ukraine": CreditAgricoleUkraine,
    "maroc": CreditAgricoleMaroc,
    "egypt": CreditAgricoleEgypt,
}
