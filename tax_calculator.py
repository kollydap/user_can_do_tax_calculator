from decimal import Decimal
from dataclasses import dataclass
from typing import Optional


@dataclass
class TaxRequest:
    """
    Class to hold the input data for tax calculation.
    
    Attributes:
        salary (Decimal): The base salary amount in Naira
        bonus (Decimal, optional): Any bonus amount in Naira, defaults to 0
    """
    salary: Decimal
    bonus: Decimal = Decimal('0')
    
    def __post_init__(self):
        """Validate and convert inputs to Decimal if needed."""
        if not isinstance(self.salary, Decimal):
            self.salary = Decimal(str(self.salary))
        
        if not isinstance(self.bonus, Decimal):
            self.bonus = Decimal(str(self.bonus))
            
        if self.salary < 0:
            raise ValueError("Salary cannot be negative")
        if self.bonus < 0:
            raise ValueError("Bonus cannot be negative")


@dataclass
class TaxResponse:
    """
    Class to hold the result of tax calculation.
    
    Attributes:
        tax_amount (Decimal): The calculated tax amount
        gross_pay (Decimal): The total gross pay (salary + bonus)
        net_pay (Decimal): The net pay after tax deduction
    """
    tax_amount: Decimal
    gross_pay: Decimal
    net_pay: Decimal


def calculate_tax(request: TaxRequest) -> TaxResponse:
    """
    Calculate tax based on the following rules:
    - First ₦200,000 of salary is tax-free
    - Next ₦500,000 is taxed at 10%
    - Next ₦300,000 is taxed at 15%
    - Any amount above ₦1,000,000 is taxed at 20%
    - Bonuses are not taxed, but are included in gross pay
    
    Args:
        request (TaxRequest): The tax calculation request with salary and bonus
        
    Returns:
        TaxResponse: Object containing tax amount, gross pay, and net pay
        
    Raises:
        TypeError: If input is not a valid TaxRequest
    """
    if not isinstance(request, TaxRequest):
        raise TypeError("Input must be a TaxRequest object")
    
    salary = request.salary
    bonus = request.bonus
    tax_amount = Decimal('0')
    
    # First ₦200,000 is tax-free
    taxable_amount = max(Decimal('0'), salary - Decimal('200000'))
    
    # ₦500,000 is taxed at 10%
    tax_bracket_1 = min(taxable_amount, Decimal('500000'))
    tax_amount += tax_bracket_1 * Decimal('0.1')
    taxable_amount -= tax_bracket_1
    
    if taxable_amount > 0:
        # ₦300,000 is taxed at 15%
        tax_bracket_2 = min(taxable_amount, Decimal('300000'))
        tax_amount += tax_bracket_2 * Decimal('0.15')
        taxable_amount -= tax_bracket_2
        
        if taxable_amount > 0:
            # Any amount above ₦1,000,000 is taxed at 20%
            tax_amount += taxable_amount * Decimal('0.2')
    
    # Calculate gross and net pay
    gross_pay = salary + bonus
    net_pay = gross_pay - tax_amount
    
    return TaxResponse(
        tax_amount=tax_amount.quantize(Decimal('0.01')),
        gross_pay=gross_pay.quantize(Decimal('0.01')),
        net_pay=net_pay.quantize(Decimal('0.01'))
    )