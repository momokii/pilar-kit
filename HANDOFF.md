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
  template/                 starter composition (6 s), passes `check`
  template-project/         starter for a product folder: BRIEF.md + brand/
  projects/<product>/       one folder per product
    BRIEF.md                the project brief — read it before writing any video
    brand/                  logo, fonts, screens, music shared by every video
    <video>/                one HyperFrames project per video
  HANDOFF.md  README.md  .gitignore
```

Product folder, then video folder. The brief and the brand assets are written once per
product; `hf new <product>/<video>` copies `brand/` into the new video as `assets/brand/`
so asset paths stay relative.

## 1. What this gives you

Make, revise and render videos from HTML/CSS with HyperFrames.

- New product folder: `hf project <product>` → fill `BRIEF.md` → drop assets in `brand/`.
- New video: `hf new <product>/<video>` → read the brief → edit `index.html` → `hf check` → `hf render`.
- Revision: edit the **same** project folder; earlier renders stay as history.
- Output: MP4, 1920×1080, 30 fps, H.264 + AAC.

## 2. State you can rely on

| Item | Location (relative to the project root) | Verified |
|---|---|---|
| Template | `template/` | `hf check` passes |
| Project starter | `template-project/` (`BRIEF.md`, `brand/README.md`) | `hf project` tested; brief not yet filled for a real product |
| Projects | `projects/<product>/<video>/` | `projects/demo-e2e/` is the legacy flat project, 3 renders |
| CLI wrapper | `~/.local/bin/hf` | pins `hyperframes@0.9.69` + Chromium |
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
2. Run `hf projects`, then `cd projects/demo-e2e && hf check` to confirm the toolchain works.
3. **Stop and wait.** Do not create a video until the user asks for one.

Do not reinstall anything, do not run `npx hyperframes` directly, and do not download Chrome.

## 4. Commands

```bash
hf projects                        # products, their videos, render counts
hf project <product>               # projects/<product>/ with BRIEF.md + brand/
hf new <product>/<video>           # copy template → projects/<product>/<video>, brand included
cd projects/<product>/<video>
hf check                           # gate: contrast AA, type floor, audio, runtime, layout
hf snapshot --at 0,3,6             # PNG frames to inspect before rendering
hf render --crf 18                 # → renders/<video>_<timestamp>.mp4
hf transcribe <audio> --to srt     # caption sidecar (needs an ASR model; untested here)
python3 tools/make-soundtrack.py --duration 16.5 --ticks 1.6,3.3 --arrival 13.4
```

Brief first: `hf project <product>` creates `projects/<product>/BRIEF.md`. Fill it (product,
audience, palette, voice, claims with sources, audio, constraints, the video list) before the
first composition; every video in that product folder is written against it. Keep the status
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

## 6. Revisions

Revisions edit the existing project, never a new one.

1. Change only the requested elements; target stable ids (`#headline`, `#card`, `#bubble`).
2. `hf snapshot --at <seconds>` to compare before and after.
3. `hf render` again; the new file lands in `renders/` beside the previous one.
4. Report the new file path and the `hf check` result.

## 7. Known gaps

| Gap | Status |
|---|---|
| Scenes live in one file, not `compositions/` sub-compositions | `check` warns `nested_structure_needs_subcomposition`; cosmetic for rendering |
| Caption generation from speech | `hf transcribe --to srt` exists, never executed here; needs an ASR model download |
| 9:16 (1080×1920) variant | not built yet |
| `timeline_track_too_dense` warning | cosmetic; Studio ergonomics only |
| Brief flow | `hf project` + `BRIEF.md` scaffolded and tested; not yet filled for a real product |
| `projects/demo-e2e/` | legacy flat project (no product folder); kept as the toolchain smoke test |
| Git | folder is not a repository yet; `.gitignore` is prepared and covers nested `renders/` |

## 8. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `Check failed` with `text_below_floor` | reading text under 28 px | raise the size, or add `data-layout-ignore` to label text only |
| `film_silent` | no `<audio>` clip | add one; generate with `tools/make-soundtrack.py` |
| `first_frame_empty` | intro animates from opacity 0 at t=0 | keep the title visible at frame 0 |
| Chrome download starts | wrapper bypassed | use `hf`, not `npx hyperframes` |
| `studio_missing_editable_id` | clip without `id` | add a stable `id` |
| `hf new` fails on `<product>/<video>` | parent folder missing | `hf new` creates it; `hf project <product>` first to get the brief |

## 9. Reporting

When you finish, state: **project path, render path, `hf check` outcome (errors/warnings), and any
`NOT VERIFIED` item.** A video is not "ready" without a fresh `hf render` result in `renders/`.
