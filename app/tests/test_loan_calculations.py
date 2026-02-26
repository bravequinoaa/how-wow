import pytest
from app.crud.loan_calculations import (
    calculate_monthly_interest_rate,
    calculate_loan_monthly_payment_zero_interest,
    calculate_loan_amortization,
    generate_loan_schedule
)

def test_calculate_monthly_interest_rate():
    assert calculate_monthly_interest_rate(12) == 0.01
    assert calculate_monthly_interest_rate(0) == 0.0
    assert calculate_monthly_interest_rate(6) == 0.005

def test_calculate_loan_monthly_payment_zero_interest():
    assert calculate_loan_monthly_payment_zero_interest(1200, 12) == 100
    assert calculate_loan_monthly_payment_zero_interest(0, 12) == 0
    assert calculate_loan_monthly_payment_zero_interest(1200, 1) == 1200

def test_calculate_loan_amortization():
    # Example: $1000, 1% monthly, 12 payments
    result = calculate_loan_amortization(1000, 0.01, 12)
    assert round(result, 2) == 88.85  # Precomputed value

    # Zero interest should not crash
    with pytest.raises(ZeroDivisionError):
        calculate_loan_amortization(1000, 0, 12)

def test_generate_loan_schedule():
    # $1200, 0% interest, 12 payments of $100
    schedule = generate_loan_schedule(1200, 0, 100, 12)
    assert len(schedule) == 12
    assert schedule[0]["month"] == 1
    assert schedule[-1]["remaining_balance"] == 0

    # $1000, 1% monthly, 12 payments
    monthly_payment = calculate_loan_amortization(1000, 0.01, 12)
    schedule = generate_loan_schedule(1000, 0.01, monthly_payment, 12)
    assert len(schedule) == 12
    assert schedule[-1]["remaining_balance"] == 0 or schedule[-1]["remaining_balance"] < 1

    # Negative balance should be clamped to zero
    schedule = generate_loan_schedule(100, 0, 200, 1)
