# Video kit (HyperFrames)

Satu produk = satu folder. Di dalamnya: satu `BRIEF.md`, satu folder `brand/` berisi aset
bersama, dan satu subfolder per video. Revisi mengedit folder video yang sama, bukan membuat
project baru.

## Struktur

```
~/Public/main-linux-kelanach/code-berkah-titipan-tuhan/code/personal_prjct/video-maker/
  template/              # salinan awal untuk video baru (jangan diedit langsung)
    index.html           # komposisi: HTML + CSS + timeline GSAP
    assets/              # audio, gambar, media
    tools/make-soundtrack.py
  template-project/      # salinan awal untuk folder produk
    BRIEF.md             # kerangka project brief
    brand/README.md      # aturan aset brand
  projects/
    <produk>/
      BRIEF.md           # brief produk — dibaca sebelum menulis video apa pun
      brand/             # logo, font, screenshot, musik (dipakai semua video)
      <video>/
        index.html
        assets/brand/    # salinan otomatis dari projects/<produk>/brand/
        renders/         # tiap render tersimpan bertimestamp — riwayat revisi
```

## Alur membuat video baru

```bash
hf project <produk>                 # buat projects/<produk>/ + BRIEF.md + brand/
# isi BRIEF.md dulu: produk, audiens, palet, voice, klaim, audio, batasan, daftar video
# taruh logo/font/screenshot di projects/<produk>/brand/

hf new <produk>/<video>             # salin template + brand → projects/<produk>/<video>
cd /home/kelanach/Public/main-linux-kelanach/code-berkah-titipan-tuhan/code/personal_prjct/video-maker/projects/<produk>/<video>
# edit index.html sesuai brief
hf check                            # gate: kontras, type floor, audio, runtime
hf snapshot --at 0,3,6              # lihat frame kunci sebelum render
hf render --crf 18                  # hasil: renders/<video>_<timestamp>.mp4
```

Isi semua produk dan video: `hf projects`.

## Alur revisi (tanpa membuat ulang)

1. Semua permintaan revisi dikerjakan di folder video yang sama.
2. Ubah hanya elemen yang diminta — setiap clip punya `id` stabil (`#headline`, `#n-browser`, `#bubble`, …).
3. Ubah palette/logo/font? Edit `projects/<produk>/BRIEF.md` + `brand/`, salin ulang ke video (`cp -a ../../brand/. assets/brand/`), lalu render ulang.
3. `hf snapshot --at <detik>` untuk membandingkan frame sebelum/sesudah.
4. `hf render` lagi → file baru muncul di `renders/`, render lama tetap ada sebagai riwayat.
5. Untuk membandingkan dua varian sekaligus: `hf compare` (lihat `hf compare --help`).

## Aturan yang sudah divalidasi tool

- Teks bacaan **≥ 28 px** pada kanvas 1080 px (di bawah itu ditandai `text_below_floor`).
- Kontras teks lolos **WCAG AA** (`check` menjalankan 149 pemeriksaan).
- Setiap clip punya `id` → `studio_missing_editable_id` hilang.
- Sertakan audio (`<audio data-start data-duration data-track-index>`); tanpa itu muncul `film_silent`.
- `data-layout-ignore` hanya untuk label tekstur (eyebrow, tag kecil), bukan teks yang harus dibaca.

## Catatan teknis

- Browser: memakai Chromium Playwright yang sudah ada lewat `HYPERFRAMES_BROWSER_PATH`
  (wrapper `hf` mengaturnya). Tanpa itu, HyperFrames mengunduh Chrome sendiri ±150 MB.
- Versi: `hyperframes@0.9.69` (pre-1.0). Warning `nested_structure_needs_subcomposition`
  dan `timeline_track_too_dense` hanya soal ergonomi Studio, bukan kebenaran render.
- Audio dibuat deterministik oleh `tools/make-soundtrack.py` (bed rendah + tick per tahap),
  lalu di-encode ke AAC oleh ffmpeg.
