# coding: utf-8

from dataclasses import dataclass

@dataclass(frozen=True)
class Loan:
    id: str
    label: str
    amount: float
    left_to_pay: float
    must_pay_per_month: float
    currency: str
