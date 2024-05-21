from datetime import datetime as dt
from src.validators.exceptions.date_validation_exception import DateValidationException


def _validate_date_format(date):

    if (date is None):
        raise DateValidationException('Date cannot be None')
    
    try:
        dt.strptime(date, "%Y-%m-%d")

    except ValueError:
        raise DateValidationException('Invalid date format. Please provide a valid date formatted as YYYY-MM-DD.')


def validate_arguments(start_date, end_date):
    _validate_date_format(start_date)
    _validate_date_format(end_date)

    if end_date < start_date:
        raise DateValidationException('Start date is greater than end date.')
    
def validate_schema(data):
    if not isinstance(data, dict) or 'base' not in data or 'rates' not in data:
        raise ValueError("Invalid data format")
    if len(data['rates']) == 0 or 'EUR' not in data['rates']:
        raise ValueError("No data found for EUR")