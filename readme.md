# Nigerian Tax Calculator

A simple Python tax calculator that calculates taxes based on some tax brackets.

## Tax Rules

- First ₦200,000 of salary is tax-free
- Next ₦500,000 is taxed at 10%
- Next ₦300,000 is taxed at 15%
- Any amount above ₦1,000,000 is taxed at 20%
- Bonuses are not taxed, but are included in gross pay

## How to Run

### Installation

1. Make sure you have Python installed (Python 3.6+)

2. Install pytest (only needed for running tests):
   ```
   pip install pytest
   ```

### Basic Usage

1. Save the `tax_calculator.py` file to your project directory

2. Create a simple script to use the calculator:

```python
# example.py
from decimal import Decimal
from tax_calculator import TaxRequest, calculate_tax

# Calculate tax for a salary of 800,000 with a bonus of 200,000
request = TaxRequest(salary=Decimal('800000'), bonus=Decimal('200000'))
response = calculate_tax(request)

# Display results
print(f"Salary: ₦{request.salary:,.2f}")
print(f"Bonus: ₦{request.bonus:,.2f}")
print(f"Gross Pay: ₦{response.gross_pay:,.2f}")
print(f"Tax Amount: ₦{response.tax_amount:,.2f}")
print(f"Net Pay: ₦{response.net_pay:,.2f}")
```

3. Run the example:
   ```
   python example.py
   ```

### Running Tests

Run the tests with:
```
pytest test_tax_calculator.py
```

Run with verbose output:
```
pytest test_tax_calculator.py -v
```