import httpx
from fastapi import FastAPI, HTTPException

app = FastAPI(title="AeroBrief")
API = "https://aviationweather.gov/api/data/metar"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/metar/{icao}")
async def metar(icao: str):
    icao = icao.upper()
    if not (len(icao) == 4 and icao.isalpha()):
        raise HTTPException(400, "ICAO must be 4 letters")
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get(API, params={"ids": icao, "format": "json"})
    if r.status_code != 200 or not r.json():
        raise HTTPException(404, f"No METAR for {icao}")
    m = r.json()[0]
    return {
        "icao": icao,
        "raw": m.get("rawOb"),
        "flight_category": m.get("fltCat"),
        "temp_c": m.get("temp"),
        "wind_dir": m.get("wdir"),
        "wind_kt": m.get("wspd"),
        "visibility": m.get("visib"),
    }

@app.get("/taf/{icao}")
async def taf(icao: str):
    icao = icao.upper()
    if not (len(icao) == 4 and icao.isalpha()):
        raise HTTPException(400, "ICAO must be 4 letters")
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.get("https://aviationweather.gov/api/data/taf",
                        params={"ids": icao, "format": "json"})
    if r.status_code != 200 or not r.json():
        raise HTTPException(404, f"No TAF for {icao}")
    return {"icao": icao, "raw": r.json()[0].get("rawTAF")}