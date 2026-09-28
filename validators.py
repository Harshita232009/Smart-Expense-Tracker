# some validators that I made which are used in the project

from datetime import datetime


# this is the amount validator
def valid_amount(value):
    try:
        amount = float(value)
    except (TypeError, ValueError) as err:
        raise ValueError("Amount must be a number.") from err
    
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    
    return round(amount, 2)



# this the validator for date
def valid_date(value):
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
    
    except ValueError as err:
        raise ValueError("Date must use YYYY-MM-DD format.") from err


# validatr for month
def valid_month(value):
    try:
        return datetime.strptime(value, "%Y-%m").strftime("%Y-%m")
    
    except ValueError as err:
        raise ValueError("Month must use YYYY-MM format.") from err


#validate text , cant be empty and cant be greater than maxlen
def valid_text(value, field, maxlen=100):
    text = (value or "").strip()

    if not text:
        raise ValueError(f"{field} cannot be empty.")
    
    if len(text) > maxlen:
        raise ValueError(f"{field} must be at most {maxlen} characters.")
    
    return text
