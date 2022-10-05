# coding: utf-8

from dataclasses import dataclass

@dataclass(frozen=True)
class Insurance:
    label: str
    status: str
    description: str
    max_amount: float
    currency: str
