import pytest
import requests
from requests.exceptions import HTTPError, Timeout
from unittest.mock import Mock, patch
from src.readers.api.base import BaseApiConnector

@patch('src.readers.api.base.requests.Session.get')
def test_get_response_successful(mock_get):
    # Mock successful response
    mock_response = Mock()
    mock_response.json.return_value = {'key': 'value'}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    connector = BaseApiConnector()
    response = connector._get_response('http://example.com/api')

    assert response == {'key': 'value'}

@patch('src.readers.api.base.requests.Session.get')
def test_get_response_http_error(mock_get):
    # Mock HTTP error response
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = HTTPError
    mock_get.return_value = mock_response

    connector = BaseApiConnector()
    with pytest.raises(SystemExit):
        connector._get_response('http://example.com/api')

@patch('src.readers.api.base.requests.Session.get')
def test_get_response_timeout_error(mock_get):
    # Mock timeout error response
    mock_response = Mock()
    mock_response.raise_for_status.side_effect = Timeout
    mock_get.return_value = mock_response

    connector = BaseApiConnector()
    with pytest.raises(SystemExit):
        connector._get_response('http://example.com/api')

def test_url_property_raises_not_implemented_error():
    connector = BaseApiConnector()
    with pytest.raises(NotImplementedError):
        _ = connector.url

def test_params_property_returns_none():
    connector = BaseApiConnector()
    assert connector.params is None

