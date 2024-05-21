import pytest
from src.validators.validators import _validate_date_format, validate_arguments, validate_schema
from src.validators.exceptions.date_validation_exception import DateValidationException


def test_validate_date_format():
    # Valid date format
    assert _validate_date_format("2024-05-19") is None

    # Invalid date format
    with pytest.raises(DateValidationException):
        _validate_date_format("2024/05/19")

    # Invalid date format
    with pytest.raises(DateValidationException):
        _validate_date_format("2024-13-01")

    # Invalid date format
    with pytest.raises(DateValidationException):
        _validate_date_format("random_string")    


def test_validate_arguments():
    assert validate_arguments('2024-05-01', "2024-05-10") is None

    with pytest.raises(DateValidationException):
        validate_arguments('2024-05-20', '2024-05-01')        

    with pytest.raises(DateValidationException):
        validate_arguments(None, None)          

def test_valid_data():
    data = {'base': 'USD', 'rates': {'EUR': 0.85, 'GBP': 0.77}}
    validate_schema(data)

def test_invalid_data_type():
    data = 'invalid data'
    with pytest.raises(ValueError):
        validate_schema(data)

def test_missing_key():
    data = {'base': 'USD', 'some_other_key': 'some_value'}
    with pytest.raises(ValueError):
        validate_schema(data)

def test_empty_rates():
    data = {'base': 'USD', 'rates': {}}
    with pytest.raises(ValueError):
        validate_schema(data)

def test_missing_EUR_rate():
    data = {'base': 'USD', 'rates': {'GBP': 0.77}}
    with pytest.raises(ValueError):
        validate_schema(data)