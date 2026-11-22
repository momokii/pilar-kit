# Video kit — handoff

Self-contained handoff for any agent picking up video work on this machine. Read this file
first; it does not depend on any prior conversation. Every claim below was verified on the
machine on **2026-11-19**.

---

## 0. Start here

Open the T3 project **`video-maker`**. Its root is:

```
/home/kelanach/Public/main-linux-kelanach/code-berkah-titipan-tuhan/code/personal_prjct/video-maker
```

Start the session with that directory as the working directory. Every path in this document is
relative to it. If you are somewhere else, `cd` there before doing anything; do not scatter
video projects outside this folder.

```
video-maker/
  bin/hf                    the wrapper (canonical); ~/.local/bin/hf symlinks to it
  template/                 16:9 1920x1080 starter (6 s), passes `check`
  template-pilar/           9:16 1080x1920 pillar base (22 s), passes `check`, has a render
    compositions/           hud · hook · peta · f1 · f2 · f3 · end
  template-project/         starter for an account folder: BRIEF.md + brand/
  tools/                    build-map.py, build-dish.py, pilar-templates/, icons/
  content/BRIEF.md          the pilot account brief; content/examples/ sample dish JSON
  projects/<akun>/          one folder per account
    BRIEF.md                the account brief — read it before writing any video
    brand/                  logo, fonts, screens, music shared by every video
    dishes/<slug>.json      data + sources per dish
    <video>/                one HyperFrames project per video
  HANDOFF.md  README.md  AGENTS.md  .gitignore
```

Account folder, then video folder. The brief and the brand assets are written once per
account; `hf new <akun>/<video>` copies `brand/` into the new video as `assets/brand/`
so asset paths stay relative. The repo is a git repository since 2026-11-21; `projects/`
is production data and stays untracked.

## 1. What this gives you

Make, revise and render videos from HTML/CSS with HyperFrames.

- New account folder: `hf project <akun>` → fill `BRIEF.md` → drop assets in `brand/`.
- New video, pillar format: `hf new <akun>/<video> template-pilar` → `tools/build-dish.py`
  fills the compositions from `dishes/<slug>.json` → `hf check` → `hf render`. Agents write
  JSON, never HTML, for a new dish.
- New video, general format: `hf new <akun>/<video>` (16:9 `template/`) → edit `index.html`.
- Revision: edit the **same** project folder; earlier renders stay as history. Change data,
  re-run the builder with `--force` — never hand-edit generated text.
- Output: pillar MP4 is 1080×1920, 30 fps, 22 s; general is 1920×1080. H.264 + AAC.

## 2. State you can rely on

| Item | Location (relative to the project root) | Verified |
|---|---|---|
| Template (16:9) | `template/` | `hf check` passes (2 cosmetic warnings) |
| Template (9:16 pillar) | `template-pilar/` | `hf check --no-cache` clean: 0/0, 0 layout, 36/36 AA; render 22.000 s 1080×1920 |
| Dish builder | `tools/build-dish.py` + `tools/pilar-templates/` | rebuild of the sample is byte-identical (no drift) |
| Project starter | `template-project/` (`BRIEF.md`, `brand/README.md`) | `hf project` tested; brief not yet filled for a real product |
| Accounts | `projects/<akun>/<video>/` | `projects/petarasa/` (rendang built by hand), `v3-boxbox`, legacy `demo-e2e` |
| CLI wrapper | `bin/hf` → `~/.local/bin/hf` | pins `hyperframes@0.9.69` + Chromium; `hf --help`, template arg tested |
| Skills | `~/.agents/skills/hyperframes{,-cli,-registry}`, `media-use`, `reverse-any-video`, `style-sampling` | installed on disk |
| Agent rules | `~/.pi/agent/AGENTS.md`, `~/.config/opencode/AGENTS.md` → "Video & motion" | present |
| Browser | `~/.cache/ms-playwright/chromium-1255/chrome-linux64/chrome` | used by the wrapper |
| ffmpeg | `/usr/bin/ffmpeg` | present |

**Skills may not appear in your advertised skill list.** Registration happens when a session
starts. If they are missing from the list, read them directly:
`~/.agents/skills/hyperframes/SKILL.md`, then `hyperframes-cli`. Do not report the skill as
unavailable.

## 3. First actions, then stop

1. Read `~/.agents/skills/hyperframes/SKILL.md` (contract) and `hyperframes-cli/SKILL.md` (commands).
2. Run `hf projects`, then `cd template-pilar && hf check` to confirm the engine works.
3. **Stop and wait.** Do not create a video until the user asks for one.

Do not reinstall anything, do not run `npx hyperframes` directly, and do not download Chrome.

## 4. Commands

```bash
hf projects                        # accounts, their videos, render counts
hf project <akun>                  # projects/<akun>/ with BRIEF.md + brand/
hf new <akun>/<video> [template]   # template/ (default) or template-pilar/
hf --help                          # usage, shipped templates
cd projects/<akun>/<video>
hf check                           # gate: lint, runtime, layout, motion, contrast, audio
hf snapshot --at 0,3.2,6.5,11.5    # PNG frames to inspect before rendering
hf render --crf 20                 # → renders/<video>_<timestamp>.mp4
```

Pillar videos, outside the project folder:

```bash
python3 tools/build-dish.py --data <dish.json> --dest <project> [--force] \
        [--seri <name>] [--handle @<akun>]
python3 tools/build-map.py                # rebuild assets/maps from geoBoundaries (ODbL)
python3 tools/make-soundtrack.py --duration 22 --ticks 5,10,15 --arrival 19.6   # run in a video

bin/kit-check                     # prove the kit still builds: templates, drift, git hygiene
```

Brief first: `hf project <akun>` creates `projects/<akun>/BRIEF.md`. Fill it (account,
audience, palette, voice, claims with sources, audio, constraints, the video list) before the
first composition; every video in that account folder is written against it. Keep the status
column in the brief in step with `renders/`.

## 5. Authoring contract (from the skill)

1. Every timed element: `class="clip"`, `data-start`, `data-duration`, and a stable `id`.
2. One paused GSAP timeline, registered as `window.__timelines["<data-composition-id>"] = tl`.
3. No `Date.now()`, unseeded `Math.random()`, timers, network fetches, or `repeat: -1`.
4. Never tween `display`, `visibility`, or `autoAlpha` on a `.clip`.
5. Never animate `left/top/width/height`; animate transforms (e.g. `scaleX`).
6. Reading text ≥ **28 px** on a 1080 canvas; label text carries `data-layout-ignore`.
7. Non-bundled fonts need `@font-face` to a file in `assets/fonts/` (template uses `FilmMono`).
8. Asset paths are relative: `assets/...`.
9. Include an `<audio>` clip with `id`, `data-start`, `data-duration`, `data-track-index`;
   otherwise `check` reports `film_silent`.
10. Frame 0 should already show the title — social players use it as the thumbnail.
11. Pillar videos: one scene per file in `compositions/`, mounted with `data-composition-src`
    (host id = scene root id = `window.__timelines` key). Tokens, components and the beat map
    live in `index.html` only; never animate `left/top/width/height`.
12. Text that deliberately sits in the brand grid (96 px margins) carries
    `data-layout-allow-safe-zone`; icons and frames carry `data-layout-ignore`.

## 6. Revisions

Revisions edit the existing project, never a new one.

1. Change only the requested elements; target stable ids (`#headline`, `#card`, `#bubble`).
2. `hf snapshot --at <seconds>` to compare before and after.
3. `hf render` again; the new file lands in `renders/` beside the previous one.
4. Report the new file path and the `hf check` result.

## 7. Known gaps

| Gap | Status |
|---|---|
| Per-dish diagrams (bowl comparison, odometer, ingredient grid) | **content, not kit.** `template-pilar` gives the reusable base (three fact beats with an icon from `tools/icons/`). Rich per-dish diagrams stay in the account (see `projects/petarasa/rendang/compositions/f1..f3.html`) and are not promoted |
| Caption generation from speech | **not applicable by design**: audio is a generated bed + ticks, there is no narration, so `hf transcribe --to srt` is never used. Captions are on-screen text (`content/BRIEF.md` §3, §15). NOT VERIFIED if narration is added later |
| Pilar card variants (pilar bumbu, harga pasar, cara makan) | not built; only the peta/tiga-fakta pillar exists |
| Province coverage | 34 provinces; the four Papuan provinces created in 2022 are still merged into Papua in the geoBoundaries release. Re-run `tools/build-map.py` when the source updates |
| `template/` (16:9) lint warnings | `nested_structure_needs_subcomposition` + `timeline_track_too_dense` remain; cosmetic for rendering, kept because the starter is one 6 s scene on purpose |
| `hf compare` / `hf preview` per video | not exercised here |
| Consumers of the builder | only the kit sample; `projects/petarasa/rendang` was hand-built before the builder existed and was not regenerated (account data, not touched) |

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Check failed` with `text_below_floor` | reading text under 28 px | raise the size, or add `data-layout-ignore` to label text only |
| `film_silent` | no `<audio>` clip | add one; generate with `tools/make-soundtrack.py` |
| `first_frame_empty` | intro animates from opacity 0 at t=0 | keep the title visible at frame 0 |
| Chrome download starts | wrapper bypassed | use `hf`, not `npx hyperframes` |
| `studio_missing_editable_id` | clip without `id` | add a stable `id` |
| `hf new` fails on `<akun>/<video>` | parent folder missing | `hf new` creates it; `hf project <akun>` first to get the brief |
| `build-dish: unknown provinsi_id` | slug not in the map | use the slug from `template/assets/maps/provinces.json` (e.g. `sumatera-barat`), not the display name |
| `build-dish: fact too long` | fact wraps past three lines at 36 chars | shorten the fact; the builder refuses rather than overflow |
| `build-dish: exactly three facts` | more or fewer than three | a pillar video is one province, one dish, three facts |
| `outside_safe_zone` warnings | brand grid is wider than the modelled TikTok zone | keep `data-layout-allow-safe-zone` on text that the brand grid deliberately places there |

## 9. Reporting

When you finish, state: **project path, render path, `hf check` outcome (errors/warnings), and any
`NOT VERIFIED` item.** A video is not "ready" without a fresh `hf render` result in `renders/`.
