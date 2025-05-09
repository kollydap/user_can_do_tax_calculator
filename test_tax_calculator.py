import pytest
from decimal import Decimal
from tax_calculator import TaxRequest, TaxResponse, calculate_tax


def test_tax_free_amount():
    """Test case where salary is below the tax-free threshold."""
    request = TaxRequest(salary=Decimal('150000'))
    response = calculate_tax(request)
    
    assert response.tax_amount == Decimal('0')
    assert response.gross_pay == Decimal('150000')
    assert response.net_pay == Decimal('150000')


def test_first_bracket():
    """Test case where salary falls in the first tax bracket."""
    request = TaxRequest(salary=Decimal('400000'))
    response = calculate_tax(request)
    
    # First 200,000 is tax-free, next 200,000 is taxed at 10%
    expected_tax = Decimal('20000')  # (400000 - 200000) * 0.1
    
    assert response.tax_amount == expected_tax
    assert response.gross_pay == Decimal('400000')
    assert response.net_pay == Decimal('380000')


def test_second_bracket():
    """Test case where salary falls in the second tax bracket."""
    request = TaxRequest(salary=Decimal('800000'))
    response = calculate_tax(request)
    
    # First 200,000 is tax-free
    # Next 500,000 is taxed at 10% = 50,000
    # Remaining 100,000 is taxed at 15% = 15,000
    expected_tax = Decimal('65000')  # 50000 + 15000
    
    assert response.tax_amount == expected_tax
    assert response.gross_pay == Decimal('800000')
    assert response.net_pay == Decimal('735000')


def test_third_bracket():
    """Test case where salary falls in the highest tax bracket."""
    request = TaxRequest(salary=Decimal('1200000'))
    response = calculate_tax(request)
    
    # First 200,000 is tax-free
    # Next 500,000 is taxed at 10% = 50,000
    # Next 300,000 is taxed at 15% = 45,000
    # Remaining 200,000 is taxed at 20% = 40,000
    expected_tax = Decimal('135000')  # 50000 + 45000 + 40000
    
    assert response.tax_amount == expected_tax
    assert response.gross_pay == Decimal('1200000')
    assert response.net_pay == Decimal('1065000')


def test_with_bonus():
    """Test case with both salary and bonus."""
    request = TaxRequest(salary=Decimal('900000'), bonus=Decimal('100000'))
    response = calculate_tax(request)
    
    # First 200,000 is tax-free
    # Next 500,000 is taxed at 10% = 50,000
    # Remaining 200,000 is taxed at 15% = 30,000
    expected_tax = Decimal('80000')  # 50000 + 30000
    expected_gross = Decimal('1000000')  # 900000 + 100000
    expected_net = Decimal('920000')  # 1000000 - 80000
    
    assert response.tax_amount == expected_tax
    assert response.gross_pay == expected_gross
    assert response.net_pay == expected_net


def test_with_string_inputs():
    """Test case with string inputs that should be converted to Decimal."""
    request = TaxRequest(salary="500000", bonus="50000")
    response = calculate_tax(request)
    
    # First 200,000 is tax-free
    # Next 300,000 is taxed at 10% = 30,000
    expected_tax = Decimal('30000')
    expected_gross = Decimal('550000')  # 500000 + 50000
    expected_net = Decimal('520000')  # 550000 - 30000
    
    assert response.tax_amount == expected_tax
    assert response.gross_pay == expected_gross
    assert response.net_pay == expected_net


def test_edge_cases():
    """Test edge cases like zero salary."""
    request = TaxRequest(salary=Decimal('0'), bonus=Decimal('100000'))
    response = calculate_tax(request)
    
    assert response.tax_amount == Decimal('0')
    assert response.gross_pay == Decimal('100000')
    assert response.net_pay == Decimal('100000')


def test_rounding():
    """Test rounding to two decimal places."""
    request = TaxRequest(salary=Decimal('200100.50'))
    response = calculate_tax(request)
    
    # 100.50 is taxed at 10% = 10.05
    expected_tax = Decimal('10.05')
    
    assert response.tax_amount == expected_tax
    assert response.gross_pay == Decimal('200100.50')
    assert response.net_pay == Decimal('200090.45')


def test_error_handling():
    """Test error handling for invalid inputs."""
    # Test negative salary
    with pytest.raises(ValueError, match="Salary cannot be negative"):
        TaxRequest(salary=Decimal('-100'))
    
    # Test negative bonus
    with pytest.raises(ValueError, match="Bonus cannot be negative"):
        TaxRequest(salary=Decimal('100'), bonus=Decimal('-50'))
    
    # Test invalid input type
    with pytest.raises(TypeError, match="Input must be a TaxRequest object"):
        calculate_tax("invalid input")


def test_exactTaxBoundaries():
    """Test exact tax bracket boundaries."""
    # Exactly at the tax-free threshold
    request1 = TaxRequest(salary=Decimal('200000'))
    response1 = calculate_tax(request1)
    assert response1.tax_amount == Decimal('0')
    
    # Exactly at the first bracket boundary
    request2 = TaxRequest(salary=Decimal('700000'))  # 200K tax-free + 500K at 10%
    response2 = calculate_tax(request2)
    assert response2.tax_amount == Decimal('50000')  # 500K * 10%
    
    # Exactly at the second bracket boundary
    request3 = TaxRequest(salary=Decimal('1000000'))  # 200K tax-free + 500K at 10% + 300K at 15%
    response3 = calculate_tax(request3)
    assert response3.tax_amount == Decimal('95000')  # 50000 + 45000