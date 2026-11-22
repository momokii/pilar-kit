# AGENTS.md — kit video (`video-maker`)

Repo ini **kit produksi**, bukan repo konten. Kit menyediakan mesin (template, tools, brief);
akun video memakainya. Satu thread untuk kit, thread terpisah per akun — jangan dicampur.
Repo ini git sejak 2026-11-21; `projects/` adalah data produksi dan sengaja tidak di-track.

**Status (2026-11-22):** mesin siap — `bin/kit-check` hijau, `main` = tag `v0.1.1`, lisensi MIT,
repo publik. Yang sudah ada, yang belum, dan langkah pertama: `HANDOFF.md` §2–§3 dan §7.

## Peta folder

```
video-maker/                 KIT — jarang berubah
  bin/hf                     wrapper (kanonik; ~/.local/bin/hf → symlink ke sini)
  template/                  starter 16:9 1920x1080, 6 s
  template-pilar/            pilar 9:16 1080x1920, 22 s (hud/hook/peta/f1-f3/end)
  template-project/          kerangka folder akun: BRIEF.md + brand/
  tools/                     build-map.py, build-dish.py, pilar-templates/, icons/
  content/BRIEF.md           brief akun pilot; content/examples/ = data contoh
  projects/<akun>/           DATA AKUN — brief, brand, dishes/, video, renders/
```

Boleh diubah di sini: `template/`, `template-pilar/`, `template-project/`, `tools/`, `content/`,
`bin/hf`, `README.md`, `HANDOFF.md`, `AGENTS.md` ini. **Jangan** mengedit `projects/<akun>/`
(data akun, bukan kit), jangan mengunggah apa pun. Ubah wrapper `hf` hanya dengan alasan tertulis
di laporan.

## Perintah

```bash
hf projects                        # daftar akun, video, jumlah render
hf project <akun>                  # projects/<akun>/ + BRIEF.md + brand/
hf new <akun>/<video> [template]   # template/ (default) atau template-pilar/
cd projects/<akun>/<video>
python3 ../../../tools/build-dish.py --data ../dishes/<slug>.json --dest . --force
hf check                           # gate: lint, runtime, layout, motion, kontras AA, audio
hf snapshot --at 0,3.2,6.5,11.5     # PNG frame kunci — dibaca sebelum render
hf render --crf 20                 # → renders/<video>_<timestamp>.mp4
bin/kit-check                      # kesehatan kit: template + builder + git, exit 0 = sehat
```

Untuk video pilar: **tulis JSON, bukan HTML**. `build-dish.py` mengisi nama, hook, provinsi +
sorotan peta, tiga fakta, sumber, atribusi. Jangan menyunting teks hasil generate — ubah JSON,
jalankan ulang dengan `--force`. Selalu `hf`, jangan `npx hyperframes` (wrapper memaku 0.9.69).

## Lisensi aset — harga mati

| Aset | Aturan |
|---|---|
| Peta | geoBoundaries gbOpen IDN ADM1, **ODbL 1.0**. Atribusi wajib di kartu akhir: `Peta: geoBoundaries (ODbL)`. Dibangun lewat `python3 tools/build-map.py`, bukan sumber lain. Cakupan 34 provinsi (pemekaran Papua 2022 belum ada) |
| Audio | digenerate lokal & deterministik: `python3 tools/make-soundtrack.py` (ffmpeg → AAC). Tanpa musik pihak ketiga |
| Foto / gambar | **tidak ada** foto pihak ketiga, footage, atau wajah. Visual = tipografi + SVG peta + gerak |
| Font | bundel (`Inter`, `JetBrains Mono`) atau file di `assets/fonts/` lewat `@font-face` |
| Klaim | satu fakta = satu sumber tingkat 1–2 (`content/BRIEF.md` §13); klaim sengketa ditulis "diklaim" |
| Kode | MIT (`LICENSE`); aset peta tetap ODbL dan wajib diatribusikan di kartu akhir |

## Gate sebelum render

1. `hf check` → 0 error. Warning ditimbang, tidak diabaikan diam-diam.
2. `hf snapshot --at <detik>` → frame dibaca; frame 0 sudah memuat judul (thumbnail).
3. Teks bacaan ≥ 28 px di kanvas 1080, kontras WCAG AA, `<audio>` ada (`film_silent` = gagal).
4. Baru `hf render`. Laporkan path render + hasil `hf check`; render lama tetap jadi riwayat.

## Batas

- Thread kit: ubah kit, verifikasi dengan `bin/kit-check`, lalu lapor.
- Thread akun: kerjakan video akun itu; jangan mengubah kit demi satu video.
- Yang tidak bisa diverifikasi → tulis `NOT VERIFIED`. Jangan klaim selesai tanpa bukti.
