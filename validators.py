"""Input validation functions shared by the menu and services."""

from datetime import datetime


def valid_amount(value):
    """Convert a positive number to float, or raise ValueError."""
    try:
        amount = float(value)
    except (TypeError, ValueError) as error:
        raise ValueError("Amount must be a number.") from error
    if amount <= 0:
        raise ValueError("Amount must be greater than zero.")
    return round(amount, 2)


def valid_date(value):
    """Validate and return a date in YYYY-MM-DD format."""
    try:
        return datetime.strptime(value, "%Y-%m-%d").strftime("%Y-%m-%d")
    except ValueError as error:
        raise ValueError("Date must use YYYY-MM-DD format.") from error


def valid_month(value):
    """Validate and return a month in YYYY-MM format."""
    try:
        return datetime.strptime(value, "%Y-%m").strftime("%Y-%m")
    except ValueError as error:
        raise ValueError("Month must use YYYY-MM format.") from error


def valid_text(value, field_name, maximum=100):
    """Return non-empty trimmed text with a reasonable length limit."""
    text = (value or "").strip()
    if not text:
        raise ValueError(f"{field_name} cannot be empty.")
    if len(text) > maximum:
        raise ValueError(f"{field_name} must be at most {maximum} characters.")
    return text

