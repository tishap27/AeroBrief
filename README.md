# AeroBrief
METAR briefing API for aviation weather.

![CI](https://github.com/tishap27/AeroBrief/actions/workflows/ci.yml/badge.svg)

A small REST API that returns live aviation weather (METAR and TAF) as clean JSON. Built with FastAPI. Responses are cached in SQLite for 5 minutes to avoid repeat calls to the upstream service.

## Endpoints
| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Service status |
| GET | `/metar/{icao}` | Latest METAR, e.g. `/metar/CYOW` (cached 5 min) |
| GET | `/taf/{icao}` | Latest TAF, e.g. `/taf/CYOW` |

Errors: `400` for an invalid ICAO code, `404` when no data exists.
Interactive API docs are served at `/docs` when the server is running.

Example response for `/metar/CYOW`:
```json
{
  "icao": "CYOW",
  "raw": "...",
  "flight_category": "VFR",
  "temp_c": 5,
  "wind_dir": 270,
  "wind_kt": 8,
  "visibility": 10
}
```

## Run locally
```
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Run with Docker
```
docker build -t aerobrief .
docker run -p 8000:8000 aerobrief
```

## Tests
```
pytest
```
Tests run on every push and pull request through GitHub Actions.

## Documentation
- [Architecture and design decisions](docs/architecture.md)
- [Requirements and test traceability](docs/requirements.md)

## Project layout
- `app/main.py`: API endpoints
- `app/cache.py`: SQLite cache with expiry
- `tests/`: unit tests
- `docs/`: architecture and requirements
- `Dockerfile`: container image
- `.github/workflows/ci.yml`: CI pipeline

## Limitations
- Single instance only: the SQLite cache is local to one container
- No rate limiting on the public endpoints yet
- Upstream failures return 404 rather than a separate error code
- The 404 case has no automated test yet (see requirements)

## Data source
Weather data comes from [aviationweather.gov](https://aviationweather.gov).
