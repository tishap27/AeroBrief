
# AeroBrief requirements

| ID | Requirement | Verified by |
|----|-------------|-------------|
| REQ-1 | The service shall return the latest METAR for a valid 4-letter ICAO code | tests/test_metar.py::test_metar_success_is_cached |
| REQ-2 | The service shall reject an invalid ICAO code with HTTP 400 | tests/test_api.py::test_bad_icao |
| REQ-3 | The service shall return HTTP 404 when no weather data exists | tests/test_metar.py::test_metar_404_when_no_data |
| REQ-4 | The service shall serve repeat requests within 5 minutes from a local cache | tests/test_cache.py::test_put_get, test_expired; tests/test_metar.py::test_metar_success_is_cached |
| REQ-5 | The service shall expose a health check endpoint | tests/test_api.py::test_health |
| REQ-6 | The service shall return the latest TAF and reject invalid codes | tests/test_api.py::test_bad_icao_taf (invalid code only) |

## Known gaps
- REQ-6: the successful TAF response is not covered by an automated test
- No rate limiting on the public endpoints (issue #3)