#!/usr/bin/env python3
"""Build one pillar video (9:16, 22 s, "satu daerah · satu hidangan · tiga fakta").

The kit's engine: `template-pilar/` is a runnable sample, and this script rewrites its
compositions from a dish JSON, so no agent ever hand-edits HTML for a new dish.

Usage:
  python3 tools/build-dish.py --data content/examples/petarasa-rendang.json --dest /tmp/probe
  hf new petarasa/<slug> template-pilar
  python3 tools/build-dish.py --data projects/petarasa/dishes/<slug>.json \
                              --dest projects/petarasa/<slug>

Data (content/BRIEF.md §9.4, extended by the account's dish files):
  id, edisi, provinsi, provinsi_id, nama, hook,
  fakta[]: {teks, ikon, sumber, tingkat}   # exactly three, one claim each
  sumber[], kartu_akhir.sumber_baris[], atribusi_peta, catatan

Rules enforced here, so `hf check` starts from a valid frame:
  - exactly three facts, one line of text each (wrapped to 36 chars, max 3 lines)
  - province slug must exist in template/assets/maps/provinces.json
  - map attribution always rendered on the end card
"""

from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATES = ROOT / "tools" / "pilar-templates"
ICONS = ROOT / "tools" / "icons"
BASE_TEMPLATE = ROOT / "template-pilar"
MAPS = ROOT / "template" / "assets" / "maps"

DURATION = 22
BEATS = {"hook": 2.5, "peta": 2.5, "f1": 5.0, "f2": 5.0, "f3": 4.6, "end": 2.4}
ZOOM_SCALE = 3.6
ZOOM_TARGET = (540.0, 700.0)  # where the highlighted province lands on the 1080x1920 canvas
FACT_LINE = 36  # characters per line at 38 px mono, 888 px column
FACT_LINES = 3


def fail(message: str) -> "None":
    print(f"build-dish: {message}", file=sys.stderr)
    raise SystemExit(2)


def wrap(text: str) -> list[str]:
    """Greedy wrap; explicit newlines in the data win over the measured width."""
    lines: list[str] = []
    for paragraph in text.split("\n"):
        words, line = paragraph.split(), ""
        for word in words:
            candidate = f"{line} {word}".strip()
            if len(candidate) <= FACT_LINE or not line:
                line = candidate
            else:
                lines.append(line)
                line = word
        if line:
            lines.append(line)
    return lines


def fact_html(text: str) -> str:
    lines = wrap(text)
    if len(lines) > FACT_LINES:
        fail(f"fact too long for three lines ({len(lines)}): {text!r}")
    return "<br/>".join(html.escape(line, quote=False) for line in lines)


# Measured on Inter 800 with -0.03em tracking: a glyph advances ~0.50 em, and the
# last glyph of a 24-char name at 84 px ended 10.8 px past the canvas edge.
CHAR_EM = 0.52
HERO_SIZES = (150, 118, 96, 84, 72, 64)
SMALL_SIZES = (96, 84, 72, 64, 56)
COLUMN = 888


def fit(text: str, sizes: tuple[int, ...], max_lines: int = 2) -> tuple[int, list[str]]:
    """Largest size at which the text wraps into max_lines inside the 888 px column."""
    words = text.split()
    for size in sizes:
        limit = int(COLUMN / (CHAR_EM * size)) - 1
        lines: list[str] = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            if len(candidate) <= limit or not current:
                current = candidate
            else:
                lines.append(current)
                current = word
        if current:
            lines.append(current)
        if len(lines) <= max_lines:
            return size, lines
    size = sizes[-1]
    limit = int(COLUMN / (CHAR_EM * size)) - 1
    lines, current = [], ""
    for word in words:
        candidate = f"{current} {word}".strip()
        if len(candidate) <= limit or not current:
            current = candidate
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return size, lines


def name_lines(name: str, sizes: tuple[int, ...]) -> tuple[int, str, int]:
    """Size plus markup: one line stays nowrap, two lines wrap inside the column."""
    size, lines = fit(name, sizes)
    markup = "<br/>".join(
        "".join(f'<span class="ch">{"&nbsp;" if ch == " " else html.escape(ch)}</span>' for ch in line)
        for line in lines
    )
    return size, markup, len(lines)


def map_index() -> tuple[dict[str, str], float, float]:
    """id -> path d, plus the SVG viewBox width/height it belongs to."""
    svg = (MAPS / "indonesia.svg").read_text()
    view = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if not view:
        fail("template/assets/maps/indonesia.svg has no viewBox")
    paths = dict(re.findall(r'<path id="([^"]+)" d="([^"]+)"\s*/>', svg))
    if not paths:
        fail("no province paths found — run python3 tools/build-map.py")
    return paths, float(view.group(1)), float(view.group(2))


def path_center(d: str) -> tuple[float, float]:
    nums = [float(v) for v in re.findall(r"-?\d+\.?\d*", d)]
    xs, ys = nums[0::2], nums[1::2]
    return (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2


def map_svg(province_id: str, paths: dict[str, str], vb_w: float, vb_h: float) -> tuple[str, float, float, float]:
    if province_id not in paths:
        near = ", ".join(sorted(k for k in paths if province_id[:4] in k) or list(paths)[:6])
        fail(f"unknown provinsi_id {province_id!r}; check template/assets/maps/provinces.json (e.g. {near})")

    cx, cy = path_center(paths[province_id])
    body = "".join(
        f'    <path id="{pid}" d="{d}" />' for pid, d in sorted(paths.items()) if pid != province_id
    )
    svg = "\n".join([
        f'<svg id="map-svg" viewBox="0 0 {vb_w:g} {vb_h:g}">',
        '  <g fill="none" stroke="#1B1714" stroke-width="1.1" stroke-linejoin="round" stroke-linecap="round">',
        body,
        f'    <path id="{province_id}" d="{paths[province_id]}" fill="#C8402F" />',
        "  </g>",
        f'  <circle id="p2-ping" cx="{cx:.1f}" cy="{cy:.1f}" r="18" fill="none" stroke="#C8402F" stroke-width="5"/>',
        "</svg>",
    ])

    # the scene draws the map 1080 px wide, so viewBox units scale by 1080/vb_w
    k = 1080.0 / vb_w
    tx = ZOOM_TARGET[0] - ZOOM_SCALE * cx * k
    ty = ZOOM_TARGET[1] - ZOOM_SCALE * cy * k
    return svg, tx, ty, vb_h * k


def icon_svg(ikon: str) -> str:
    path = ICONS / f"{ikon}.svg"
    if not ikon or not path.exists():
        # a wrong icon must never ship silently
        print(f"build-dish: warning: ikon {ikon!r} not in tools/icons/, using 'bumbu'", file=sys.stderr)
        path = ICONS / "bumbu.svg"
    return path.read_text().strip()


def render(template_name: str, tokens: dict[str, str]) -> str:
    text = (TEMPLATES / f"{template_name}.html.tmpl").read_text()
    for key, value in tokens.items():
        text = text.replace("{{" + key + "}}", str(value))
    leftover = re.findall(r"\{\{([A-Z0-9_]+)\}\}", text)
    if leftover:
        fail(f"{template_name}: unfilled tokens {sorted(set(leftover))}")
    return text


def source_rows(data: dict) -> str:
    rows = (data.get("kartu_akhir") or {}).get("sumber_baris") or []
    if not rows:
        rows = [
            f"{s.get('sitasi', '')[:52]}"
            for s in (data.get("sumber") or [])
            if isinstance(s, dict)
        ][:3]
    if not rows:
        fail("no sources: kartu_akhir.sumber_baris or sumber[] is required")
    out = []
    for index, row in enumerate(rows[:3]):
        label = "Sumber" if index == 0 else ""
        out.append(
            f'      <div class="row"><span class="k">{label}</span>'
            f"<span>{html.escape(str(row), quote=False)}</span></div>"
        )
    return "\n".join(out)


def identity(data: dict, data_path: Path, args: argparse.Namespace) -> tuple[str, str]:
    account = ""
    parts = data_path.resolve().parts
    if "projects" in parts:
        index = parts.index("projects")
        if index + 1 < len(parts):
            account = parts[index + 1]
    seri = args.seri or data.get("seri") or (account.capitalize() if account else "Edisi")
    handle = args.handle or data.get("handle") or (f"@{account}" if account else "@contoh")
    return seri, handle


def main() -> int:
    parser = argparse.ArgumentParser(description="dish JSON -> pillar video")
    parser.add_argument("--data", required=True, help="dish JSON (content/BRIEF.md §9.4)")
    parser.add_argument("--dest", required=True, help="project folder to write into")
    parser.add_argument("--seri", default="", help="HUD series name (default: account folder)")
    parser.add_argument("--handle", default="", help="end-card handle (default: @account)")
    parser.add_argument("--from-template", default="", help="copy this template when dest is missing")
    parser.add_argument("--force", action="store_true", help="overwrite an existing project")
    args = parser.parse_args()

    data_path = Path(args.data).expanduser()
    if not data_path.exists():
        fail(f"no such dish JSON: {data_path}")
    data = json.loads(data_path.read_text())

    facts = data.get("fakta") or []
    if len(facts) != 3:
        fail(f"exactly three facts are required, got {len(facts)}")
    for field in ("nama", "provinsi", "provinsi_id"):
        if not data.get(field):
            fail(f"dish JSON is missing {field!r}")


    paths, vb_w, vb_h = map_index()
    svg, zoom_x, zoom_y, map_height = map_svg(data["provinsi_id"], paths, vb_w, vb_h)
    seri, handle = identity(data, data_path, args)
    hero, hero_markup, hero_lines = name_lines(data["nama"], HERO_SIZES)
    small, small_markup, _ = name_lines(data["nama"], SMALL_SIZES)
    handle_size, _ = fit(handle, SMALL_SIZES, max_lines=1)
    # the hook lockup moves up when the headword needs two lines, so the rule and the
    # lead never collide with it
    hook_top = 660 if hero_lines == 1 else 560
    hook_rule = hook_top + int(hero * 1.05 * hero_lines) + 30
    hook_sub = hook_rule + 70

    tokens = {
        "SERI": html.escape(seri, quote=False),
        "EDITION": f"{int(data.get('edisi', 1)):03d}",
        "PROVINCE": html.escape(data["provinsi"], quote=False),
        "DISH": html.escape(data["nama"], quote=False),
        "HOOK": html.escape(data.get("hook", ""), quote=False),
        "HANDLE": html.escape(handle, quote=False),
        "NAME_CHARS": hero_markup,
        "NAME_CHARS_SM": small_markup,
        "NAME_WRAP_CLASS": " wrap" if "<br/>" in small_markup else "",
        "NAME_SIZE": hero,
        "NAME_SIZE_SM": small,
        "HANDLE_SIZE": handle_size,
        "HOOK_TOP": hook_top,
        "HOOK_RULE_TOP": hook_rule,
        "HOOK_SUB_TOP": hook_sub,
        "DURATION": DURATION,
        "MAP_SVG": svg,
        "MAP_HEIGHT": f"{map_height:.1f}",
        "ZOOM_X": f"{zoom_x:.1f}",
        "ZOOM_Y": f"{zoom_y:.1f}",
        "ZOOM_SCALE": ZOOM_SCALE,
        "SOURCE_ROWS": source_rows(data),
        "ATRIBUSI": html.escape(data.get("atribusi_peta", "geoBoundaries (ODbL)"), quote=False),
    }

    # every check that can fail runs before the filesystem is touched
    fact_tokens_list = []
    for index, fact in enumerate(facts, start=1):
        fact_tokens = dict(tokens)
        fact_tokens.update({
            "FACT_N": index,
            "FACT_INDEX": f"{index:02d}",
            "FACT_TEXT": fact_html(fact.get("teks", "")),
            "ICON_SVG": icon_svg(fact.get("ikon", "")),
        })
        fact_tokens_list.append(fact_tokens)

    dest = Path(args.dest).expanduser()
    seeded = False
    if not dest.exists():
        source = Path(args.from_template) if args.from_template else BASE_TEMPLATE
        if not (source / "index.html").exists():
            fail(f"cannot seed {dest}: no template at {source}")
        shutil.copytree(source, dest)
        shutil.rmtree(dest / "renders", ignore_errors=True)
        shutil.rmtree(dest / ".hyperframes", ignore_errors=True)
        seeded = True
        print(f"seeded {dest} from {source.relative_to(ROOT) if source.is_relative_to(ROOT) else source}")
    elif not args.force:
        fail(f"{dest} already exists — pass --force to regenerate its compositions")

    (dest / "compositions").mkdir(exist_ok=True)
    written = []
    written.append((dest / "index.html", render("index", tokens)))
    for scene in ("hud", "hook", "peta", "end"):
        written.append((dest / "compositions" / f"{scene}.html", render(scene, tokens)))
    for index, fact_tokens in enumerate(fact_tokens_list, start=1):
        written.append((dest / "compositions" / f"f{index}.html", render("fakta", fact_tokens)))

    for path, text in written:
        path.write_text(text)

    # assets the sample ships with: the map source of truth and the generated bed
    (dest / "assets" / "maps").mkdir(parents=True, exist_ok=True)
    for name in ("indonesia.svg", "provinces.json"):
        target = dest / "assets" / "maps" / name
        if not target.exists():
            shutil.copy2(MAPS / name, target)
    bed = dest / "assets" / "soundtrack.m4a"
    if not bed.exists() and (BASE_TEMPLATE / "assets" / "soundtrack.m4a").exists():
        bed.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(BASE_TEMPLATE / "assets" / "soundtrack.m4a", bed)

    print(
        f"{data['nama']} · {data['provinsi']} · edisi {tokens['EDITION']} -> {dest}\n"
        f"  {len(written)} files, {DURATION} s, 1080x1920, highlight={data['provinsi_id']}, "
        f"zoom {zoom_x:.1f}/{zoom_y:.1f} @{ZOOM_SCALE}" + (" (seeded)" if seeded else "")
        + f"\n  next: cd {dest} && hf check && hf snapshot --at 0,3.2,6.5,11.5,16.5,20.5"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
