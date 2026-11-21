# AGENTS.md — kit video (`video-maker`)

Repo ini **kit produksi**, bukan repo konten. Kit menyediakan mesin (template, tools, brief);
akun video memakainya. Satu thread untuk kit, thread terpisah per akun — jangan dicampur.

## Peta folder

```
video-maker/                 KIT — jarang berubah
  template/                  komposisi starter 16:9; `hf check` harus lolos
  template-project/          kerangka folder akun: BRIEF.md + brand/
  tools/                     skrip deterministik (build-map.py)
  content/BRIEF.md           brief akun pilot: format, pilar, lisensi, kebijakan sumber
  projects/<akun>/           DATA AKUN — brief, brand, komposisi, renders/
  README.md  HANDOFF.md      struktur & status terpasang
```

Boleh diubah di sini: `template/`, `template-project/`, `tools/`, `content/`, `README.md`,
`HANDOFF.md`, `AGENTS.md` ini. **Jangan** mengedit `projects/<akun>/` (data akun, bukan kit),
jangan mengunggah apa pun, dan jangan mengubah wrapper `~/.local/bin/hf` tanpa menyebut alasannya
di laporan.

## Perintah

```bash
hf projects                    # daftar akun/produk, videonya, jumlah render
hf project <akun>              # projects/<akun>/ + BRIEF.md + brand/
hf new <akun>/<video>          # salin template (+ brand/) → projects/<akun>/<video>
cd projects/<akun>/<video>
hf check                       # gate: lint, runtime, layout, motion, kontras AA, audio
hf snapshot --at 0,3,6         # PNG frame kunci — dibaca sebelum render
hf render --crf 20             # → renders/<video>_<timestamp>.mp4
```

Selalu `hf`, jangan `npx hyperframes`: wrapper memaku versi 0.9.69 + Chromium lokal.

## Lisensi aset — harga mati

| Aset | Aturan |
|---|---|
| Peta | geoBoundaries gbOpen IDN ADM1, **ODbL 1.0**. Atribusi wajib di kartu akhir: `Peta: geoBoundaries (ODbL)`. Dibangun ulang lewat `python3 tools/build-map.py`, bukan sumber lain. Cakupan 34 provinsi (pemekaran Papua 2022 belum ada) |
| Audio | digenerate lokal & deterministik: `python3 tools/make-soundtrack.py` (ffmpeg → AAC). Tanpa musik pihak ketiga |
| Foto / gambar | **tidak ada** foto pihak ketiga, footage, atau wajah. Visual = tipografi + SVG peta + gerak |
| Font | hanya file di `assets/fonts/`, didaftarkan lewat `@font-face` |
| Klaim | satu fakta = satu sumber tingkat 1–2 (`content/BRIEF.md` §13); klaim sengketa ditulis "diklaim" |

## Gate sebelum render

1. `hf check` → 0 error. Warning ditimbang, tidak diabaikan diam-diam.
2. `hf snapshot --at <detik>` → frame dibaca; frame 0 sudah memuat judul (thumbnail).
3. Teks bacaan ≥ 28 px di kanvas 1080, kontras WCAG AA, `<audio>` ada (`film_silent` = gagal).
4. Baru `hf render`. Laporkan path render + hasil `hf check`; render lama tetap jadi riwayat.

## Batas

- Thread kit: ubah kit, verifikasi (`hf projects`, `cd template && hf check`), lalu lapor.
- Thread akun: kerjakan video akun itu; jangan mengubah kit demi satu video.
- Yang tidak bisa diverifikasi → tulis `NOT VERIFIED`. Jangan klaim selesai tanpa bukti.
