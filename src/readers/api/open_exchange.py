from src.readers.api.base import BaseApiConnector
from datetime import datetime as dt

class OpenExchangeConnector(BaseApiConnector):
    """Get data for the given name from Eurostat."""

    def __init__(self, headers=None, app_id=None, base=None, symbols=None):
        super().__init__(headers)
        self.app_id = app_id
        self.base = base
        self.symbols = symbols

    @property
    def default_date(self):
        """Default date for reader. Defaults to current date"""
        return dt.now().strftime("%Y-%m-%d")

    @property
    def url(self):
        """API URL"""
        return "https://openexchangerates.org/api/historical/"

    @property
    def params(self):
        """Parameters to use in API calls"""
        return {
            "app_id": self.app_id,
            "base": self.base,
            "symbols": self.symbols
        }

    def extract_data(self, date=None):
        """Read data from API"""
        if date is None:
            date = self.default_date

        response = self._get_response(self.url + date + ".json",
                                        params=self.params,
                                        headers=self.headers)
        return response
