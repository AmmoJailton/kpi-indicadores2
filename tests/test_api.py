from fastapi.testclient import TestClient

from innovation_api import __version__
from innovation_api.api.create_api import create_api

fast_api = create_api()
client = TestClient(fast_api)


def test_search_get_info():
    route = "/"
    response = client.get(f"{route}")
    assert response.status_code == 200
    assert list(response.json().keys()) == ["statusCode", "version", "env", "Status"]
    assert response.json()["statusCode"] == 201
    assert response.json()["version"] == f"{__version__}"
