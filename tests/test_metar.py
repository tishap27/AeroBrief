import httpx
from fastapi.testclient import TestClient

from app import cache
from app.main import app

client = TestClient(app)

SAMPLE = [{"rawOb": "CYOW 101500Z 27008KT 15SM CLR 05/M02 A3012",
           "fltCat": "VFR", "temp": 5, "wdir": 270, "wspd": 8, "visib": 10}]


class FakeResponse:
    def __init__(self, status=200, data=None):
        self.status_code = status
        self._data = data if data is not None else []

    def json(self):
        return self._data


def test_metar_404_when_no_data(tmp_path, monkeypatch):
    monkeypatch.setattr(cache, "DB", str(tmp_path / "t.db"))

    async def fake_get(self, url, params=None):
        return FakeResponse(200, [])

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)
    assert client.get("/metar/CYOW").status_code == 404


def test_metar_success_is_cached(tmp_path, monkeypatch):
    monkeypatch.setattr(cache, "DB", str(tmp_path / "t.db"))
    calls = {"n": 0}

    async def fake_get(self, url, params=None):
        calls["n"] += 1
        return FakeResponse(200, SAMPLE)

    monkeypatch.setattr(httpx.AsyncClient, "get", fake_get)
    first = client.get("/metar/CYOW")
    second = client.get("/metar/CYOW")
    assert first.status_code == 200
    assert first.json()["flight_category"] == "VFR"
    assert second.json() == first.json()
    assert calls["n"] == 1  # second request came from the cache