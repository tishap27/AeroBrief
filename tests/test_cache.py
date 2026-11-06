from app import cache


def test_put_get(tmp_path, monkeypatch):
    monkeypatch.setattr(cache, "DB", str(tmp_path / "t.db"))
    assert cache.get("k") is None
    cache.put("k", {"a": 1})
    assert cache.get("k") == {"a": 1}


def test_expired(tmp_path, monkeypatch):
    monkeypatch.setattr(cache, "DB", str(tmp_path / "t.db"))
    monkeypatch.setattr(cache, "TTL", -1)
    cache.put("k", {"a": 1})
    assert cache.get("k") is None