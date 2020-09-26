"""
Habitica API calls functionality wrapper for requests.
"""

import time

import requests


def _validate_headers(headers):
    """
    Raise a ValueError if headers don't match Habitica API spec.
    """
    if ("x-api-user" not in headers or "x-api-key" not in headers
            or "x-client" not in headers):
        raise ValueError("Habitica request without correct headers "
                         "encountered.")


def _handle_retry(request_func):
    """
    A wrapper for adding retry functionality to requests.

    If the server responds with status 429, i.e. the rate limit has been
    exceeded, and retry is set to True, the request is remade after the
    required cooldown period.
    """
    def _wrapper(url, headers, retry=True, **kwargs):
        """
        :url: URL to make the request to
        :headers: Headers used with the request. Must match Habitica API
                  specifications.
        :retry: True if request should be remade if API call rate limit was
                exceeded.
        """
        _validate_headers(headers)
        response = request_func(url, headers, **kwargs)
        if response.status_code == 429 and retry:
            time.sleep(float(response.headers["Retry-After"]))
            response = request_func(url, headers=headers, **kwargs)
        response.raise_for_status()
        return response
    return _wrapper


@_handle_retry
def get(url, headers, **kwargs):
    """
    Make a get request to Habitica API using requests, allowing retry.

    :url: URL to make the request to
    :headers: Headers used with the request. Must match Habitica API
              specifications.
    :retry: True if request should be remade if API call rate limit was
            exceeded.
    """
    return requests.get(url, headers=headers, **kwargs)


@_handle_retry
def put(url, headers, data=None, **kwargs):
    """
    Make a put request to Habitica API using requests, allowing retry.

    :url: URL to make the request to
    :headers: Headers used with the request. Must match Habitica API
              specifications.
    :data: Data to be sent to the server
    :retry: True if request should be remade if API call rate limit was
            exceeded.
    """
    return requests.put(url, headers=headers, data=data, **kwargs)


@_handle_retry
def post(url, headers, **kwargs):
    """
    Make a post request to Habitica API using requests, allowing retry.

    :url: URL to make the request to
    :headers: Headers used with the request. Must match Habitica API
              specifications.
    :retry: True if request should be remade if API call rate limit was
            exceeded.
    """
    return requests.post(url, headers=headers, **kwargs)
