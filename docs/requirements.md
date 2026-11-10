# AeroBrief requirements

| ID | Requirement | Verified by |
|----|-------------|-------------|
| REQ-1 | The service shall return the latest METAR for a valid 4-letter ICAO code | Manual check (/metar/CYOW) |
| REQ-2 | The service shall reject an invalid ICAO code with HTTP 400 | tests/test_api.py::test_bad_icao |
| REQ-3 | The service shall return HTTP 404 when no weather data exists | Not yet tested |
| REQ-4 | The service shall serve repeat requests within 5 minutes from a local cache | tests/test_cache.py::test_put_get, test_expired |
| REQ-5 | The service shall expose a health check endpoint | tests/test_api.py::test_health |
| REQ-6 | The service shall return the latest TAF and reject invalid codes | tests/test_api.py::test_bad_icao_taf |

## Known gaps
- REQ-3 has no automated test (upstream calls need mocking)
- No rate limiting on the public endpoints