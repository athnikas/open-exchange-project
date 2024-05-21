import pytest
from unittest.mock import Mock, patch

from datetime import datetime
from src.readers.api.open_exchange import OpenExchangeConnector

def test_default_date_property():
    connector = OpenExchangeConnector()
    current_date = datetime.now().strftime("%Y-%m-%d")
    assert connector.default_date == current_date

def test_url_property():
    connector = OpenExchangeConnector()
    assert connector.url == "https://openexchangerates.org/api/historical/"

def test_params_property():
    connector = OpenExchangeConnector(app_id="test_id", base="USD", symbols=["EUR","GBP"])
    expected_params = {
        "app_id": "test_id",
        "base": "USD",
        "symbols": ["EUR","GBP"]
    }
    assert connector.params == expected_params

@patch('src.readers.api.open_exchange.OpenExchangeConnector._get_response')
def test_extract_data(mock_get):
    # Mock response data

    mock_response_data = {'example_key': 'example_value'}

    # Configure mock _get_response method
    mock_get.return_value = mock_response_data

    # Instantiate the OpenExchangeConnector
    connector = OpenExchangeConnector(headers={'header_key': 'header_value'}, app_id='app_id', base='USD', symbols='EUR')

    # Call extract_data without providing a date
    response = connector.extract_data()

    # Assert that _get_response was called with the correct URL and parameters
    mock_get.assert_called_once_with(
        "https://openexchangerates.org/api/historical/" + connector.default_date + ".json",
        params={"app_id": 'app_id', "base": 'USD', "symbols": 'EUR'},
        headers={'header_key': 'header_value'}
    )

    # Assert that extract_data returns the response received from _get_response
    assert response == mock_response_data
 
@patch('src.readers.api.open_exchange.OpenExchangeConnector._get_response')
def test_extract_data_specific_date(mock_get):
    # Mock response data

    mock_response_data = {'example_key': 'example_value'}

    # Configure mock _get_response method
    mock_get.return_value = mock_response_data

    # Instantiate the OpenExchangeConnector
    connector = OpenExchangeConnector(headers={'header_key': 'header_value'}, app_id='app_id', base='USD', symbols='EUR')

    # Call extract_data with a specific date
    specific_date = "2024-05-20"
    response = connector.extract_data(date=specific_date)

    # Assert that _get_response was called with the correct URL and parameters for the specific date
    mock_get.assert_called_with(
        "https://openexchangerates.org/api/historical/" + specific_date + ".json",
        params={"app_id": 'app_id', "base": 'USD', "symbols": 'EUR'},
        headers={'header_key': 'header_value'}
    )

    # Assert that extract_data returns the response received from _get_response
    assert response == mock_response_data