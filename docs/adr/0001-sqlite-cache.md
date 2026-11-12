# ADR 0001: Cache METAR responses in SQLite

## Context
Every request to /metar called aviationweather.gov. Weather reports only change every few minutes, so most calls were repeats, and we depend on a public service we don't control.

## Decision
Store successful responses in a local SQLite file and reuse them for 5 minutes.

## Consequences
- Fewer upstream calls and faster repeat responses
- No extra infrastructure to run
- The cache is local to one instance, so several containers would not share it
- A cached report can be up to 5 minutes old
- If scale grows, replace SQLite with a shared cache such as Redis