import os
import pytest
import requests

BASE_URL = os.environ.get("API_BASE_URL", "https://dummyjson.com")

VALID_USERNAME = "emilys"
VALID_PASSWORD = "emilyspass"


@pytest.fixture(scope="session")
def api_base_url() -> str:
    return BASE_URL


@pytest.fixture(scope="session")
def session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"Content-Type": "application/json"})
    yield s
    s.close()
