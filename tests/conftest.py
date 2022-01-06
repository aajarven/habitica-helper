"""
Shared fixtures
"""

import pytest


@pytest.fixture(autouse=True)
def prevent_online_requests(monkeypatch):
    """
    Patch urlopen so that all non-patched requests raise an error.
    """
    def urlopen_error(self, method, url, *args, **kwargs):
        raise RuntimeError(
                f"Requests are not allowed, but a test attempted a {method} "
                f"request to {self.scheme}://{self.host}{url}")

    monkeypatch.setattr(
        "urllib3.connectionpool.HTTPConnectionPool.urlopen", urlopen_error
    )
