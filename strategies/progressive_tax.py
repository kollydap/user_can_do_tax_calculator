from decimal import Decimal
from strategies.base import TaxStrategy, TaxRequest, TaxResponse

class ProgressiveTaxStrategy(TaxStrategy):
    def calculate(self, request: TaxRequest) -> TaxResponse:
        salary = request.salary
        bonus = request.bonus
        tax_amount = Decimal('0')

        taxable = max(Decimal('0'), salary - Decimal('200000'))

        slab1 = min(taxable, Decimal('500000'))
        tax_amount += slab1 * Decimal('0.1')
        taxable -= slab1

        if taxable > 0:
            slab2 = min(taxable, Decimal('300000'))
            tax_amount += slab2 * Decimal('0.15')
            taxable -= slab2

        if taxable > 0:
            tax_amount += taxable * Decimal('0.2')

        gross = salary + bonus
        net = gross - tax_amount

        return TaxResponse(
            tax_amount=tax_amount.quantize(Decimal('0.01')),
            gross_pay=gross.quantize(Decimal('0.01')),
            net_pay=net.quantize(Decimal('0.01'))
        )
