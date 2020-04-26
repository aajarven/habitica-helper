"""
Miscellaneous small utility functions.
"""

import requests

def get_dict_from_api(header, url):
    """
    Get data dict for API call represented by the given url.

    :header: HTTP header required when making Habitica API calls
    :url: URL for API get request
    :returns: Dict containing the data

    :raises: HTTPError if the request was bad
    """
    response = requests.get(url, headers=header)
    response.raise_for_status()
    return response.json()["data"]
