import os

import pytest


@pytest.fixture
def base_url() -> str:
    url = os.environ.get("RECORDS_BASE_URL", "")
    if "integration." not in url:
        pytest.skip("integration tests run only against the integration environment")
    return url
