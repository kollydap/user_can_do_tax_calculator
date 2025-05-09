from decimal import Decimal
from strategies.base import TaxStrategy, TaxRequest, TaxResponse

class NoTaxStrategy(TaxStrategy):
    def calculate(self, request: TaxRequest) -> TaxResponse:
        gross = request.salary + request.bonus
        return TaxResponse(
            tax_amount=Decimal('0.00'),
            gross_pay=gross,
            net_pay=gross
        )
