# <product> — video project brief

Fill this in **before** the first composition. Agents read this file before writing any
video in this folder; it is the single source of truth for look, tone, claims and audio.
Write it in Indonesian or English — the agent follows whatever you use.

Last updated: <YYYY-MM-DD> · Owner: <name>

## 1. Product

- **Name:**
- **One line** (what it is, for whom):
- **Stage:** idea / prototype / beta / live
- **Repo or app path:**
- **Where it runs:** web / mobile / desktop / CLI

## 2. Audience

- **Primary audience:**
- **What they already know:**
- **What must be true after watching** (one sentence each, max 3):
  1.
  2.

## 3. Brand

- **Palette** (hex — these become `var(--bg)`, `var(--panel)`, `var(--text)`, `var(--muted)`, `var(--accent)`):
  - background: `#`
  - surface: `#`
  - text: `#`
  - muted: `#`
  - accent: `#`
- **Type:** family · files in `brand/fonts/`
- **Logo:** `brand/logo.svg` (light on dark / dark on light — say which)
- **Real screens to show:** `brand/screens/`
- **Never use** (colours, stock imagery, phrases, faces):

## 4. Voice

- **Tone, three adjectives:**
- **Words we use:**
- **Words we never use:**
- **On-screen copy language:** id / en / both
- **Reading level / max words per frame:**

## 5. Claims & facts

Every number on screen must trace to a source here. No source, no number.

| Claim shown on screen | Source | Date | Still true? |
|---|---|---|---|
|  |  |  |  |

- **Things we must not claim:**
- **Legal / compliance wording required:**

## 6. Audio

- **Music mood:** (calm / driving / ambient / none)
- **Sound on visible actions:** yes / no
- **Narration:** yes / no — if yes, voice: <name or TTS>
- **Silence allowed** when: <e.g. silent social autoplay variant>

## 7. Constraints

- **Aspect ratios:** 16:9 1920×1080 (default) · 9:16 1080×1920 · 1:1
- **Max duration per video:**
- **Reading text floor:** 28 px on a 1080 canvas — enforced by `hf check`, not negotiable
- **Contrast:** WCAG AA — enforced by `hf check`
- **Captions:** none / burned into frames / sidecar `.srt`
- **Title visible at frame 0:** yes (social players use it as the thumbnail)
- **Delivery:** local `renders/` only / needs share link / needs publish

## 8. Videos in this project

One row per video. Folder name is the path under this project folder; run
`hf new <product>/<video>` to create it.

| # | folder | goal | duration | ratio | status | latest render |
|---|---|---|---|---|---|---|
| 1 | `onboarding/` |  |  | 16:9 | brief | — |

Status ladder: `brief` → `script` → `build` → `checked` → `rendered` → `approved`.
A video is only `rendered` when a fresh file exists in `<video>/renders/`.

## 9. Open questions

- [ ]
