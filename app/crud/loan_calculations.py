    
def calculate_monthly_interest_rate(annual_interest_rate):
    # divide annual_interest_rate by 12 to get monthly interest, then divide by 100 to get as decimal
    return float(annual_interest_rate) / 12 / 100

def calculate_loan_monthly_payment_zero_interest(loan_amt, number_of_payments):
    return float(loan_amt) / number_of_payments

def calculate_loan_amortization(loan_amt, monthly_interest_rate, number_of_payments):
    return float(loan_amt) * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments) / ((1 + monthly_interest_rate) ** number_of_payments - 1)

def generate_loan_schedule(remaining_balance, monthly_interest_rate, monthly_payment, number_of_payments):
    # loop through each month left in the loan term to caculate monthly schedule
    schedule = []
    for month in range(1, number_of_payments + 1):
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
        schedule.append({
            "month": month,
            "remaining_balance": round(max(remaining_balance, 0), 2),
            "monthly_payment": round(monthly_payment, 2)
        })
    return schedule
