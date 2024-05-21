import requests

class BaseApiConnector:
    """
    Parameters
    ----------

    headers : string
    """

    def __init__(self, headers=None):
        self.session = requests.Session()
        self.headers = headers

    @property
    def url(self):
        """API URL"""
        raise NotImplementedError
    
    @property
    def params(self):
        """Parameters to use in API calls"""
        return None

    def _get_response(self, url, params=None, headers=None):
        """send raw HTTP request to get requests.Response from the specified url
        Parameters
        ----------
        url : str
            target URL
        params : dict or None
            parameters passed to the URL
        """
        try:
            response = self.session.get(url, params=params, headers=headers)
            response.raise_for_status()

            return response.json()

        except requests.exceptions.HTTPError as err:
            raise SystemExit(err)
        except requests.exceptions.Timeout as err:
            raise SystemExit(err)

        finally:
            self.session.close()