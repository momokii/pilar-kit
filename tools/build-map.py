#!/usr/bin/env python3
"""Build the Indonesia province map (SVG) for the video kit.

Source: geoBoundaries gbOpen IDN ADM1 (simplified), licence ODbL 1.0.
  https://www.geoboundaries.org/api/current/gbOpen/IDN/ADM1/
ODbL note: the SVG built here is a Derivative Database (share-alike), while a video that
merely displays it is a Produced Work and may carry any licence, provided the source is
attributed. Attribution line for the end card: "Peta: geoBoundaries (ODbL)".

Coverage caveat: the dataset represents 34 provinces (pre-2022). The four Papuan provinces
created in 2022 are still merged into Papua here; re-run this script when the source updates.

Output:
  template/assets/maps/indonesia.svg    one <path> per province, id = slug of the Indonesian name
  template/assets/maps/provinces.json   id -> Indonesian display name

Run once; re-run only when the source or the projection changes.
"""

from __future__ import annotations

import json
import math
import re
import sys
import urllib.request
from pathlib import Path

SOURCE = ("https://github.com/wmgeolab/geoBoundaries/raw/9469f09/releaseData/"
          "gbOpen/IDN/ADM1/geoBoundaries-IDN-ADM1_simplified.geojson")
CACHE = Path("/tmp/gb-idn-adm1.geojson")
OUT_DIR = Path(__file__).resolve().parent.parent / "template" / "assets" / "maps"

WIDTH = 888
PADDING = 8
TOLERANCE = 0.6
MIN_AREA = 2.0

# geoBoundaries ships English names; the account is Indonesian.
NAME_ID = {
    "Aceh": "Aceh",
    "Bali": "Bali",
    "Bangka-Belitung Islands": "Kepulauan Bangka Belitung",
    "Banten": "Banten",
    "Bengkulu": "Bengkulu",
    "Central Java": "Jawa Tengah",
    "Central Kalimantan": "Kalimantan Tengah",
    "Central Sulawesi": "Sulawesi Tengah",
    "East Java": "Jawa Timur",
    "East Kalimantan": "Kalimantan Timur",
    "East Nusa Tenggara": "Nusa Tenggara Timur",
    "Gorontalo": "Gorontalo",
    "Jakarta Special Capital Region": "DKI Jakarta",
    "Jambi": "Jambi",
    "Lampung": "Lampung",
    "Maluku": "Maluku",
    "North Kalimantan": "Kalimantan Utara",
    "North Maluku": "Maluku Utara",
    "North Sulawesi": "Sulawesi Utara",
    "North Sumatra": "Sumatera Utara",
    "Papua": "Papua",
    "Riau": "Riau",
    "Riau Islands": "Kepulauan Riau",
    "South Kalimantan": "Kalimantan Selatan",
    "South Sulawesi": "Sulawesi Selatan",
    "South Sumatra": "Sumatera Selatan",
    "Southeast Sulawesi": "Sulawesi Tenggara",
    "Special Region of Yogyakarta": "DI Yogyakarta",
    "West Java": "Jawa Barat",
    "West Kalimantan": "Kalimantan Barat",
    "West Nusa Tenggara": "Nusa Tenggara Barat",
    "West Papua": "Papua Barat",
    "West Sulawesi": "Sulawesi Barat",
    "West Sumatra": "Sumatera Barat",
}


def slug(name: str) -> str:
    value = re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-")
    return re.sub(r"-{2,}", "-", value)


def fetch() -> dict:
    if not CACHE.exists() or CACHE.stat().st_size < 100_000:
        print(f"downloading {SOURCE}")
        urllib.request.urlretrieve(SOURCE, CACHE)
    return json.loads(CACHE.read_text())


def polygons(geometry: dict) -> list[list[list[list[float]]]]:
    if geometry["type"] == "Polygon":
        return [geometry["coordinates"]]
    if geometry["type"] == "MultiPolygon":
        return geometry["coordinates"]
    return []


def project(lon: float, lat: float, lat0: float, scale: float, x0: float, y0: float) -> tuple[float, float]:
    return ((lon * math.cos(math.radians(lat0)) - x0) * scale, (y0 - lat) * scale)


def perp_distance(p, a, b) -> float:
    if a == b:
        return math.hypot(p[0] - a[0], p[1] - a[1])
    num = abs((b[0] - a[0]) * (a[1] - p[1]) - (a[0] - p[0]) * (b[1] - a[1]))
    return num / math.hypot(b[0] - a[0], b[1] - a[1])


def simplify(points: list[tuple[float, float]], tol: float) -> list[tuple[float, float]]:
    if len(points) < 3:
        return points
    stack = [(0, len(points) - 1)]
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    while stack:
        start, end = stack.pop()
        best, index = 0.0, -1
        for i in range(start + 1, end):
            d = perp_distance(points[i], points[start], points[end])
            if d > best:
                best, index = d, i
        if best > tol and index != -1:
            keep[index] = True
            stack.append((start, index))
            stack.append((index, end))
    return [p for p, k in zip(points, keep) if k]


def ring_area(points: list[tuple[float, float]]) -> float:
    total = 0.0
    for i in range(len(points)):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % len(points)]
        total += x1 * y2 - x2 * y1
    return abs(total) / 2


def main() -> int:
    data = fetch()
    features = data["features"]

    lons: list[float] = []
    lats: list[float] = []
    for feature in features:
        for poly in polygons(feature["geometry"]):
            for lon, lat, *_ in poly[0]:
                lons.append(lon)
                lats.append(lat)

    lat0 = (min(lats) + max(lats)) / 2
    lon_min, lon_max = min(lons), max(lons)
    lat_min, lat_max = min(lats), max(lats)
    span_x = (lon_max - lon_min) * math.cos(math.radians(lat0)) or 1
    span_y = (lat_max - lat_min) or 1
    scale = (WIDTH - 2 * PADDING) / span_x
    x0 = lon_min * math.cos(math.radians(lat0)) - PADDING / scale
    y0 = lat_max + PADDING / scale
    height = round(span_y * scale + 2 * PADDING, 1)

    paths: list[str] = []
    names: dict[str, str] = {}
    for feature in sorted(features, key=lambda f: (f["properties"].get("shapeName") or "")):
        english = feature["properties"].get("shapeName") or "?"
        display = NAME_ID.get(english, english)
        pid = slug(display)
        names[pid] = display

        parts: list[str] = []
        for poly in polygons(feature["geometry"]):
            for ring_index, ring in enumerate(poly):
                pts = [project(lon, lat, lat0, scale, x0, y0) for lon, lat, *_ in ring]
                pts = simplify(pts, TOLERANCE)
                if len(pts) < 3 or ring_area(pts) < (MIN_AREA if ring_index > 0 else 1.0):
                    continue
                parts.append("M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z")
        if parts:
            paths.append(f'    <path id="{pid}" d="{"".join(parts)}" />')

    svg = "\n".join([
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {height}" '
        f'width="{WIDTH}" height="{height}" role="img" aria-label="Indonesia, provinces">',
        '  <g fill="none" stroke="#1B1714" stroke-width="1.1" stroke-linejoin="round" stroke-linecap="round">',
        *paths,
        "  </g>",
        "</svg>",
        "",
    ])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    (OUT_DIR / "indonesia.svg").write_text(svg)
    (OUT_DIR / "provinces.json").write_text(json.dumps(names, indent=2, ensure_ascii=False) + "\n")
    print(f"provinces: {len(names)} | viewBox 0 0 {WIDTH} {height} | "
          f"svg {(OUT_DIR / 'indonesia.svg').stat().st_size / 1024:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
