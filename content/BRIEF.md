# Brief akun — makanan khas Nusantara (headless, TikTok → IG Reels)

Draf kerja, 2026-11-19. Pilot berbahasa Indonesia, diproduksi dengan kit HyperFrames di folder ini.

---

## 1. Batasan yang menentukan format

Video dibuat dari HTML + SVG, **bukan rekaman kamera**. Artinya:

- Tidak ada footage masakan, tidak ada wajah, tidak ada suara orang.
- Keindahan harus datang dari **tipografi, peta, dan gerak** — bukan dari foto.
- Semua klaim kuliner butuh sumber; tanpa itu akun ini jadi sumber hoaks rasa.

Batasan ini bukan hambatan, justru pembeda: mayoritas konten makanan bersaing di footage. Akun ini
bersaing di **informasi yang tersusun rapi**.

## 2. Niche yang diusulkan

**"Satu daerah, satu hidangan, tiga fakta."**

Setiap video: satu hidangan khas, satu provinsi di peta, tiga fakta singkat (asal-usul, bahan kunci,
satu catatan budaya atau cara makan), dan satu baris sumber.

Kenapa ini:

- **Bahan tidak habis.** 38 provinsi, ratusan hidangan bernama; belum termasuk jajanan pasar dan
  varian daerah. Pada 1 video/hari, ini bertahun-tahun.
- **Audiens lebar.** Bukan penggemar teknologi; semua orang punya daerah dan akan berkomentar
  "daerahku mana".
- **Visual khas.** Peta Indonesia yang bergerak + tipografi tebal adalah tanda tangan yang sulit
  ditiru akun footage.
- **Skalabel.** Satu template, satu file data per hidangan; batch 10 video dalam satu duduk.

Alternatif pilar (dipakai setelah pilot terbukti):

| Pilar | Isi | Kenapa |
|---|---|---|
| **Bumbu** | satu bumbu per video: asal, aroma, pasangan | sangat unik, hampir tak tergarap |
| **Harga pasar** | rincian biaya seporsi | data-driven, gampang diperbarui |
| **Cara makan** | aturan sajian (dipakai tangan, daun, kuah terpisah) | konten budaya, bukan resep |

## 3. Sistem desain

| Elemen | Aturan |
|---|---|
| Kanvas | 1080×1920, 30 fps, 15–22 detik |
| Warna | latar krem `#F4EFE6`, tinta `#1B1714`, satu aksen cabai `#C8402F`, satu kuning kunyit `#E0A32E` |
| Tipografi | satu keluarga sans tebal untuk nama hidangan (72–96 px), satu mono untuk fakta (34–38 px) |
| Peta | satu SVG Indonesia, sorotan provinsi per video, garis batas tipis, tanpa label kecil |
| Gerak | tiga primitif: peta zoom-in halus, kartu fakta masuk satu per satu, garis bawah tumbuh |
| Intro | 0,5 s: nama provinsi + nomor seri |
| Outro | 1,2 s: handle + "sumber di komentar" |
| Audio | satu bed gamelan-modern yang dibuat lokal (deterministik) + satu SFX "tok" per fakta |
| Caption | teks Indonesia di layar, maksimal 2 baris; selalu ada karena banyak ditonton tanpa suara |

Aturan isi: **tiga fakta, bukan lebih.** Satu klaim per fakta. Sumber ditulis di kartu akhir dan di
komentar pertama (bukan di caption, agar tidak memotong teks).

## 4. Struktur tiap video

```
0.0–2.0   hook: "Ini bukan rendang yang kamu kira." / "Satu provinsi, satu hidangan."
2.0–7.0   peta: sorot provinsi, nama hidangan muncul
7.0–16.0  tiga fakta, satu per satu, masing-masing 1 baris + satu ikon bahan
16.0–20.0 kartu penutup: asal + sumber + handle
```

## 5. Alur produksi

```
content/dishes/<provinsi>-<slug>.json    # nama, provinsi, 3 fakta, bahan kunci, sumber
        ↓  (agen menulis data, bukan HTML)
projects/makanan/<slug>/index.html       # dari satu template
        ↓  hf check  (kontras, type floor, audio)
        ↓  hf render --crf 20
renders/<slug>_<timestamp>.mp4
```

## 6. Pilot 10 video (2 minggu, lintas pulau)

| # | Provinsi | Hidangan | Sudut |
|---|---|---|---|
| 1 | Sumatera Barat | Rendang | yang diklaim Malaysia vs yang tercatat |
| 2 | Sulawesi Selatan | Coto Makassar | kuah tanpa santan |
| 3 | Jawa Tengah | Gudeg | manis yang bukan gula |
| 4 | Papua | Papeda | bukan bubur biasa |
| 5 | Nusa Tenggara Timur | Se'i | asap, bukan panggang |
| 6 | Kalimantan Selatan | Ketupat kandangan | ikan haruan |
| 7 | Bali | Lawar | kelapa bakar |
| 8 | Aceh | Mie Aceh | dua jenis mie |
| 9 | Maluku | Papeda ikan kuah kuning | pala & cengkih |
| 10 | Jawa Barat | Karedok | sayur mentah |

Metrik yang dilihat: tahan 2 detik pertama, rasio selesai, simpan, dan komentar "daerahku mana".

## 7. Risiko dan cara menanganinya

| Risiko | Penanganan |
|---|---|
| Klaim budaya salah / diperdebatkan | setiap video wajib satu sumber; klaim diperdebatkan ditulis sebagai "diklaim", bukan fakta |
| Visual terasa sama setelah 30 video | tiga pilar berbeda tata letak; rotasi peta zoom, close-up bahan, dan kartu harga |
| Hak cipta | tidak memakai foto atau musik pihak lain; peta SVG buatan sendiri, audio digenerate lokal |
| Nama akun salah eja | handle pendek, tanpa angka dan tanpa plesetan |

## 8. Keputusan yang masih terbuka

1. Nama/handle: usulan `PetaRasa`, `SepiringNusantara`, `Bumbu`.
2. Gaya peta: siluet penuh Indonesia, atau hanya bentuk provinsi yang disorot.
3. Sumber kanonik: buku/ensiklopedia kuliner, situs pemerintah daerah, atau arsip budaya.
4. Durasi default: 15 s (cepat, retensi tinggi) atau 22 s (cukup untuk tiga fakta).

---

## 9. Yang belum ada di brief versi pertama (dan sekarang dilengkapi)

Brief sebelumnya baru menjawab *apa* dan *kenapa*. Untuk konsistensi, masih kurang enam hal yang
menentukan "jati diri" secara teknis. Berikut tambahannya.

### 9.1 Grid dan safe area

- Kanvas 1080×1920. Margin kiri-kanan 96 px, atas 160 px, bawah 220 px (area UI TikTok).
- Semua teks berada di dalam satu kolom 888 px. Tidak ada elemen yang menyentuh tepi.
- Peta menempati area 96–1400 px vertikal, boleh keluar margin horizontal (bleed) — hanya peta.

### 9.2 Skala tipografi (tetap, tidak boleh improvisasi)

| Peran | Ukuran | Berat | Line-height |
|---|---|---|---|
| Nama hidangan | 96 px | 800 | 1.0 |
| Subjudul / hook | 44 px | 600 | 1.15 |
| Fakta | 38 px | 500 | 1.35 |
| Label provinsi / edisi | 28 px | 600 (mono, tracking +0.08em) | 1.2 |
| Sumber | 24 px | 400 (mono) | 1.3 |

Tidak ada teks di bawah 24 px. Tidak ada lebih dari dua ukuran berbeda dalam satu frame kecuali
nama hidangan.

### 9.3 Waktu dan easing (tabel gerak)

| Aksi | Durasi | Easing |
|---|---|---|
| Hook masuk | 0.35 s | power2.out |
| Peta zoom ke provinsi | 1.2 s | power2.inOut |
| Nama hidangan masuk | 0.45 s | power3.out |
| Kartu fakta masuk | 0.30 s | power2.out, delay 0.08 s antar kartu |
| Garis aksen tumbuh | 0.40 s | power1.out |
| Outro | 0.60 s | power2.in |

Total: 15 s (3 fakta × 3.5 s) atau 22 s (3 fakta × 5 s + peta lebih lama). Tidak ada easing
`back`, tidak ada bounce, tidak ada rotasi.

### 9.4 Skema data satu hidangan

```json
{
  "id": "rendang",
  "edisi": 1,
  "provinsi": "Sumatera Barat",
  "nama": "Rendang",
  "hook": "Ini bukan rendang yang kamu kira.",
  "fakta": [
    { "teks": "Dimasak 6–8 jam sampai kuah habis, bukan 'berkuah'.", "ikon": "jam" },
    { "teks": "Daging, santan, dan 20+ bumbu; tanpa pengawet.", "ikon": "bumbu" },
    { "teks": "Diklaim Malaysia sejak 2009; tercatat di Minang sejak abad ke-16.", "ikon": "peta" }
  ],
  "sumber": "…",
  "catatan": "klaim budaya ditulis sebagai 'diklaim', bukan fakta"
}
```

Agen menulis JSON ini, bukan HTML. Template membaca JSON lewat build script sederhana.

### 9.5 Konvensi penomoran dan identitas

- Setiap video punya `edisi` berurutan (001, 002, …) yang tampil di frame pertama dan kartu akhir.
- Handle muncul di kartu akhir saja, bukan di tengah video.
- Satu video = satu provinsi. Tidak pernah dua hidangan dalam satu video.

### 9.6 QA sebelum publish (checklist wajib)

- [ ] `hf check` lolos (kontras, type floor, audio)
- [ ] tiga fakta, tidak lebih
- [ ] setiap klaim punya sumber; klaim sengketa ditulis "diklaim"
- [ ] tidak ada foto/musik pihak ketiga
- [ ] frame 0 sudah menampilkan judul (thumbnail)
- [ ] render baru ada di `renders/` dan dicatat

## 10. Sampel dan alur persetujuan

Sampel dibuat **sebelum** template dibangun, supaya arah visual disetujui dulu:

1. **Frame sampel** (3 buah): cover, satu beat fakta, kartu akhir — PNG 1080×1920.
2. **Satu video utuh** (Rendang, 18–22 s) dari template sementara.
3. Anda menilai: palet, tipografi, peta, tempo.
4. Revisi sampai setuju, baru template pilar difinalkan dan 10 naskah pilot ditulis.

Tanpa persetujuan sampel, template tidak dibangun — ini yang mencegah 50 video salah arah.

## 11. Aset peta (prasyarat sampel)

Peta adalah tanda tangan visual, jadi lisensinya harus jelas sebelum dipakai:

- opsi A: SVG Indonesia dari sumber domain publik / CC0, disederhanakan jadi siluet;
- opsi B: silhouette dibuat sendiri dari data batas wilayah publik;
- opsi C: tanpa peta penuh — hanya bentuk provinsi yang disorot (lebih aman lisensi, lebih bersih).

Sampel berikut memakai opsi C sementara, sampai pilihan Anda ditetapkan.

---

## 12. Keputusan (2026-11-19)

| Keputusan | Nilai | Catatan |
|---|---|---|
| Peta | **geoBoundaries gbOpen IDN ADM1** (ODbL 1.0) | 34 provinsi, termasuk Kalimantan Utara. Atribusi di kartu akhir: `Peta: geoBoundaries (ODbL)` |
| Catatan cakupan | 34 provinsi, bukan 38 | dataset belum memuat pemekaran Papua 2022 (Papua Selatan, Papua Tengah, Papua Pegunungan, Papua Barat Daya). Perbarui `tools/build-map.py` saat sumber menyusul |
| Durasi | **22 s** | 3 fakta × 5 s + peta 3 s + hook/outro |
| Nama | `petarasa` | ketersediaan handle **belum terverifikasi** (lihat §13) |

## 13. Kebijakan sumber (harga mati)

"Sumber kanonik" = daftar tertutup rujukan yang boleh dikutip. Fakta di luar daftar ini tidak
dipublicasikan, walau terdengar benar.

| Tingkat | Boleh dipakai | Contoh |
|---|---|---|
| 1 | Dokumen resmi negara / lembaga | Kemendikbud (warisan budaya), BPS, arsip daerah, UNESCO |
| 2 | Karya akademik / ensiklopedia tepercaya | jurnal, buku kuliner bereputasi, Ensiklopedia Indonesia |
| 3 | Media besar dengan penyebutan sumber primer | hanya jika mengutip tingkat 1–2 secara eksplisit |
| — | **tidak boleh** | blog pribadi, konten AI generatif, forum, "kata orang" |

Aturan penulisan:

1. Setiap fakta wajib punya satu rujukan tingkat 1 atau 2. Tanpa itu, fakta dibuang.
2. Klaim yang diperdebatkan (asal-usul, klaim negara lain) ditulis "diklaim", bukan sebagai fakta.
3. Baris sumber di kartu akhir memuat nama lembaga, bukan URL panjang.
4. Sumber lengkap disimpan di file JSON hidangan (`sumber[]`) dan ditempel di komentar pertama.
5. Jika satu hidangan tidak punya cukup rujukan, hidangan itu tidak diproduksi. Kejujuran lebih
   penting daripada jumlah video.

## 14. Struktur kerja: kit vs akun

`video-maker/` adalah **kit** (template, tools, brief). Akun adalah **workspace terpisah**:

```
video-maker/                     kit — jarang berubah
  template/  tools/  content/BRIEF.md

petarasa/                        akun — berubah setiap hari
  dishes/<provinsi>-<slug>.json  data + sumber
  projects/<slug>/               komposisi per video
  renders/                       riwayat render
  publish/                       caption, hashtag, catatan unggah
  BRAND.md                       ringkasan token desain
```

Satu thread = satu akun, dibuka di folder akun. Thread di `video-maker` hanya untuk mengubah kit.
