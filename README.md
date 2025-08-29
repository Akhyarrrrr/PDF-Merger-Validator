# KKN PDF Merger & Validator (3‑Way) 🚀

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)
![OS](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-informational)

Toolkit sederhana untuk mengelola ratusan PDF bertema KKN:

- ✅ **Merge 3 berkas per nomor**: `Cover` → `Pengesahan` → `Lampiran` menjadi satu berkas `Hasil/NNN.pdf` (mis. `001.pdf`).
- ♻️ **Incremental & idempotent**: aman dijalankan berulang. Output **di-skip** jika sudah up-to-date; **di-replace** jika sumber berubah. Opsi `--force` untuk rebuild semua.
- 🔎 **Validator penamaan** untuk **tiga** folder sumber (`Cover/`, `Pengesahan/`, `Lampiran/`) sesuai pola:  
  - `Cover`      ➜ `NNN - C.pdf`  
  - `Pengesahan` ➜ `NNN - P.pdf`  
  - `Lampiran`   ➜ `NNN - L.pdf`  
  (dengan `NNN` = `001..100`)
- 🛠️ **Auto-repair (opsional)**: jika terpasang `pikepdf`, skrip akan mencoba memperbaiki PDF yang “kotor/korup” saat proses merge.

> Folder **Cover/**, **Pengesahan/**, dan **Lampiran/** sengaja diabaikan oleh Git lewat `.gitignore`, jadi aman push ke GitHub tanpa mengikutsertakan data mentah. Folder `Hasil/` bisa ikut repo atau diabaikan—sesuai kebutuhanmu.

---

## Struktur Proyek

```
KKN/
├─ merge_pdf.py         # merge incremental: Cover → Pengesahan → Lampiran ➜ Hasil/NNN.pdf
├─ cek_nama_pdf.py      # validasi & laporan: nomor hilang / typo / suffix salah (C/P/L)
├─ Cover/               # (ignored) 001 - C.pdf ... 100 - C.pdf
├─ Pengesahan/          # (ignored) 001 - P.pdf ... 100 - P.pdf
├─ Lampiran/            # (ignored) 001 - L.pdf ... 100 - L.pdf
└─ Hasil/               # output hasil penggabungan (opsional di-ignore)
```

---

## Persiapan

1. Pastikan **Python 3.8+** terpasang.
2. Install dependensi minimum:
   ```bash
   pip install PyPDF2
   ```
3. (Opsional) untuk kemampuan **auto-repair** PDF:
   ```bash
   pip install pikepdf
   ```

---

## Cara Pakai

### 1) Validasi Penamaan & Kelengkapan
Jalankan:
```bash
python cek_nama_pdf.py
```
Kamu akan mendapatkan ringkasan:
- Nomor **hilang** di masing-masing folder
- File dengan **suffix salah** (mis. di `Lampiran/` tapi bernama `... - C.pdf`)
- File **typo** (spasi/maupun tanda minus tidak persis) dengan **saran rename**
- File yang polanya tidak dapat dikenali (perlu cek manual)
- Daftar nomor yang **lengkap di ketiga folder** vs. yang belum lengkap

### 2) Merge 3-Way → `Hasil/NNN.pdf`
```bash
python merge_pdf.py
```
Perilaku:
- Output `Hasil/NNN.pdf` **dibuat/diperbarui** hanya jika sumber (`C/P/L`) lebih baru.
- Jika output sudah up-to-date, akan tampil `⏩ NNN: up-to-date, dilewati.`
- Proses menulis menggunakan **file sementara di folder yang sama** lalu `replace` (aman & atomic).

**Paksa rebuild semua nomor:**
```bash
python merge_pdf.py --force
```

---

## Konvensi Penamaan

- **Cover**      : `NNN - C.pdf`  
- **Pengesahan** : `NNN - P.pdf`  
- **Lampiran**   : `NNN - L.pdf`  
- `NNN` wajib **3 digit** (`001..100`).  
- Spasi & tanda minus harus **persis** seperti di atas (ada spasi di kiri-kanan tanda minus).

---

## Troubleshooting

- **`File tidak lengkap (cek C/P/L)`**  
  Salah satu dari `C/P/L` tidak ada atau namanya tidak sesuai pola. Jalankan `cek_nama_pdf.py` untuk detail.

- **`EOF marker not found`** / PDF korup  
  File PDF terpotong/invalid. Solusi cepat:
  - Coba perbaiki otomatis dengan `pikepdf` (skrip merge akan mencoba saat append).
  - Atau perbaiki manual, mis. **Print to PDF** via viewer (Edge/Adobe), atau gunakan **qpdf**:
    ```powershell
    qpdf "Pengesahan\057 - P.pdf" "Pengesahan\057 - P.fixed.pdf"
    ```
    lalu ganti file aslinya.

- **Warning “Multiple definitions …” dari PyPDF2**  
  Itu peringatan struktur internal; biasanya aman diabaikan. README/skrip sudah meredamnya.
