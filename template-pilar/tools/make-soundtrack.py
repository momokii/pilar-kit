#!/usr/bin/env python3
"""Generate a deterministic soundtrack bed with one tick per stage change.

Usage:
  python3 tools/make-soundtrack.py --duration 16.5 --ticks 1.6,3.3,5.0,6.6,7.5,8.7,9.6,10.9,12.2 --arrival 13.4

Writes assets/soundtrack.wav, then encodes assets/soundtrack.m4a with ffmpeg.
Everything is synthesised locally: no downloads, no samples, repeatable.
"""

from __future__ import annotations

import argparse
import math
import shutil
import struct
import subprocess
import wave
from pathlib import Path

SR = 44100


def build(duration: float, ticks: list[float], arrival: float | None, bed: float) -> list[float]:
    n = int(SR * duration)
    buf = [0.0] * n

    # Deterministic low rumble: LCG noise through a one-pole low-pass.
    seed = 12345
    lp = 0.0
    for i in range(n):
        seed = (1103515245 * seed + 12345) & 0x7FFFFFFF
        white = (seed / 0x7FFFFFFF) * 2 - 1
        lp = lp * 0.995 + white * 0.005
        buf[i] += lp * bed

    def tone(t0: float, freq: float, dur: float, amp: float, decay: float) -> None:
        start = int(t0 * SR)
        for k in range(int(dur * SR)):
            i = start + k
            if i >= n:
                break
            t = k / SR
            buf[i] += amp * math.exp(-decay * t) * math.sin(2 * math.pi * freq * t)

    for t in ticks:
        if 0 <= t < duration:
            tone(t, 1180, 0.09, 0.22, 45)
    if arrival is not None and 0 <= arrival < duration:
        tone(arrival, 780, 0.22, 0.28, 14)
        tone(arrival + 0.02, 1560, 0.16, 0.10, 22)

    return buf


def write_wav(path: Path, buf: list[float]) -> None:
    peak = max((abs(v) for v in buf), default=0.0) or 1.0
    scale = 0.85 / peak
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "w") as handle:
        handle.setnchannels(1)
        handle.setsampwidth(2)
        handle.setframerate(SR)
        handle.writeframes(
            b"".join(struct.pack("<h", int(max(-1.0, min(1.0, v * scale)) * 32767)) for v in buf)
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--duration", type=float, required=True)
    parser.add_argument("--ticks", default="")
    parser.add_argument("--arrival", type=float, default=None)
    parser.add_argument("--bed", type=float, default=0.9, help="rumble level, 0 disables")
    parser.add_argument("--out", default="assets/soundtrack")
    args = parser.parse_args()

    ticks = [float(x) for x in args.ticks.split(",") if x.strip()]
    out = Path(args.out)
    buf = build(args.duration, ticks, args.arrival, args.bed)
    write_wav(out.with_suffix(".wav"), buf)

    if shutil.which("ffmpeg"):
        subprocess.run(
            ["ffmpeg", "-y", "-loglevel", "error", "-i", str(out.with_suffix(".wav")),
             "-c:a", "aac", "-b:a", "128k", str(out.with_suffix(".m4a"))],
            check=True,
        )
        print(f"wrote {out.with_suffix('.wav')} and {out.with_suffix('.m4a')}")
    else:
        print(f"wrote {out.with_suffix('.wav')} (ffmpeg not found: no .m4a)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
