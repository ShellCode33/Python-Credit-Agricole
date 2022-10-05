# coding: utf-8

from dataclasses import dataclass

from typing import List

@dataclass(frozen=True)
class Operation:
    label: str
    description: List[str]
    amount: float

@dataclass(frozen=True)
class Account:
    id: str
    owner: str
    balance: float
    currency: str
    label: str

    @property
    def operations(self) -> List[Operation]:
        raise NotImplemented

    @property
    def cards(self):
        raise NotImplemented
