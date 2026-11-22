# Video kit (HyperFrames)

Repo ini **kit**: mesin produksi yang dipakai ulang oleh akun-akun video. Satu akun = satu folder
di `projects/`, berisi `BRIEF.md`, `brand/`, dan satu subfolder per video. Akun mengubah datanya
sendiri; kit jarang berubah.

## Struktur

```
video-maker/
  bin/hf                     # wrapper: versi + Chromium dipaku (~/.local/bin/hf → symlink ke sini)
  template/                  # starter 16:9 1920x1080, 6 s — video produk/umum
  template-pilar/            # pilar 9:16 1080x1920, 22 s — "satu daerah, satu hidangan, tiga fakta"
    index.html               #   token + komponen baku, host scene, audio
    compositions/            #   hud · hook · peta · f1 · f2 · f3 · end
    tools/make-soundtrack.py #   bed deterministik (ffmpeg → AAC)
  template-project/          # kerangka folder akun: BRIEF.md + brand/
  tools/
    build-map.py             # geoBoundaries IDN ADM1 → template/assets/maps/ (ODbL)
    build-dish.py            # dish JSON → komposisi template-pilar
    pilar-templates/*.tmpl   # sumber scene yang diisi builder (bukan diedit tangan)
    icons/*.svg              # ikon fakta: jam, bumbu, peta, kuali, cabai, empat, bawang
  content/
    BRIEF.md                 # brief akun pilot: format, pilar, lisensi, kebijakan sumber
    examples/contoh-rendang.json  # data contoh untuk template-pilar (bukan naskah produksi)
  projects/<akun>/
    BRIEF.md                 # brief akun — dibaca sebelum menulis video apa pun
    brand/                   # logo, font, screenshot, musik (dipakai semua video)
    dishes/<slug>.json       # data + sumber per hidangan
    <video>/                 # satu proyek HyperFrames
      index.html
      compositions/
      assets/brand/          # salinan otomatis dari projects/<akun>/brand/
      renders/               # tiap render bertimestamp — riwayat revisi
```

## Alur: akun baru

```bash
hf project <akun>                   # projects/<akun>/ + BRIEF.md + brand/
# isi BRIEF.md dulu: produk/akun, audiens, palet, voice, klaim+sumber, audio, batasan, daftar video
# taruh logo/font/screenshot di projects/<akun>/brand/
```

## Alur A — video pilar (9:16, 22 s, dish JSON → komposisi)

```bash
hf new <akun>/<video> template-pilar        # salin pilar + brand akun
cd projects/<akun>/<video>
python3 ../../../tools/build-dish.py --data ../dishes/<slug>.json --dest . --force
hf check                                    # gate: lint, layout, kontras, audio, runtime
hf snapshot --at 0,3.2,4.4,6.5,11.5,16.5,20.5
hf render --crf 20                          # → renders/<video>_<timestamp>.mp4
```

`build-dish.py` menulis ulang `index.html` + tujuh scene dari JSON: nama hidangan, hook, provinsi
+ sorotan peta, tiga fakta (teks di-wrap 36 karakter, ikon dipilih field `ikon`), baris sumber, dan
atribusi peta. Agen menulis **JSON**, bukan HTML. Skema data: `content/BRIEF.md` §9.4.

Di luar folder akun, untuk mencoba cepat:

```bash
python3 tools/build-dish.py --data content/examples/contoh-rendang.json --dest /tmp/coba
cd /tmp/coba && hf check && hf render
```

## Alur B — video umum (16:9)

```bash
hf new <akun>/<video>               # template/ (default) + brand akun
cd projects/<akun>/<video>
# edit index.html
hf check && hf snapshot --at 0,3,6 && hf render --crf 18
```

## Verifikasi kit

Satu perintah, dipakai sebelum menyentuh apa pun dan setelah mengubah kit:

```bash
bin/kit-check            # pakai cache (cepat)
bin/kit-check --fresh    # ulang dari nol (~30 s)
```

Yang diperiksa: kedua template lengkap, `hf check` lolos di `template/` dan `template-pilar/`,
sampel pilar identik dengan output builder (tidak ada drift `tools/pilar-templates`), builder
menolak data salah **sebelum** menulis apa pun, dan repo git tidak melacak `projects/`,
`renders/`, atau `.hyperframes/`. Exit 0 hanya kalau semua lolos.

## Alur revisi (tanpa membuat ulang)

1. Semua permintaan revisi dikerjakan di folder video yang sama.
2. Ubah hanya elemen yang diminta — setiap clip punya `id` stabil (`#headline`, `#f1-def`, `#p2-name`).
3. Ubah data (nama, fakta, sumber)? Edit `dishes/<slug>.json` lalu jalankan ulang `build-dish.py
   --force`; jangan menyunting teks hasil generate.
4. Ubah palette/logo/font? Edit `BRIEF.md` + `brand/`, salin ke video (`cp -a ../../brand/. assets/brand/`), render ulang.
5. `hf snapshot --at <detik>` untuk membandingkan frame sebelum/sesudah.
6. `hf render` lagi → file baru di `renders/`, render lama tetap jadi riwayat.
7. Bandingkan dua varian: `hf compare` (lihat `hf compare --help`).

## Aturan yang sudah divalidasi tool

- Teks bacaan **≥ 28 px** pada kanvas 1080 px (di bawah itu ditandai `text_below_floor`).
- Kontras teks lolos **WCAG AA** (`check` mengaudit tiap frame sampel; `template-pilar` 36/36).
- Setiap clip punya `id` → `studio_missing_editable_id` hilang.
- Audio wajib (`<audio data-start data-duration data-track-index>`); tanpa itu muncul `film_silent`.
- `data-layout-ignore` hanya untuk elemen dekoratif (ikon, bingkai), bukan teks yang harus dibaca.
- Teks sengaja diletakkan di grid selebar 96 px margin: bawa `data-layout-allow-safe-zone` supaya
  audit zona aman TikTok/Reels/Shorts tidak salah lapor. Ini keputusan desain, bukan pelanggaran.

## Lisensi

Kode dan skrip di repo ini **MIT** (lihat `LICENSE`; teks kanonik, tanpa tambahan, supaya GitHub
mendeteksinya). Aset punya aturannya sendiri dan tidak tertimpa lisensi kode:

| Aset | Lisensi | Kewajiban |
|---|---|---|
| Peta (`template/assets/maps/`, turunan geoBoundaries) | **ODbL 1.0** | atribusi `Peta: geoBoundaries (ODbL)` di kartu akhir setiap video |
| Font di `assets/fonts/` | lisensi upstream masing-masing | jangan di-redistribusi di luar repo ini |
| Audio (`tools/make-soundtrack.py`) | MIT | digenerate lokal, tidak ada sampel pihak ketiga |
| Data akun (`projects/`) | bukan bagian repo | tidak pernah di-commit |

## Catatan teknis

- Browser: memakai Chromium Playwright lewat `HYPERFRAMES_BROWSER_PATH` (diatur `hf`). Tanpa itu
  HyperFrames mengunduh Chrome sendiri ±150 MB.
- Versi: `hyperframes@0.9.69` (pre-1.0). `template/` masih memicu warning
  `nested_structure_needs_subcomposition` + `timeline_track_too_dense` (ergonomi Studio, bukan
  kebenaran render); `template-pilar/` sudah bersih karena memakai sub-komposisi.
- Audio dibuat deterministik oleh `tools/make-soundtrack.py` (bed rendah + tick per tahap), lalu
  di-encode ke AAC oleh ffmpeg. Satu trek 22 s dipakai semua video pilar.
- Peta: `tools/build-map.py` membangun ulang `template/assets/maps/` dari geoBoundaries (ODbL 1.0).
  Cakupan 34 provinsi — pemekaran Papua 2022 belum ada di dataset.
