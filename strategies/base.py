from abc import ABC, abstractmethod
from decimal import Decimal
from dataclasses import dataclass

@dataclass
class TaxRequest:
    salary: Decimal
    bonus: Decimal

@dataclass
class TaxResponse:
    tax_amount: Decimal
    gross_pay: Decimal
    net_pay: Decimal

class TaxStrategy(ABC):
    @abstractmethod
    def calculate(self, request: TaxRequest) -> TaxResponse:
        pass
