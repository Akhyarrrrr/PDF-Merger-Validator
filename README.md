# KKN PDF Merger & Validator 🚀

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-active-success)
![OS](https://img.shields.io/badge/OS-Windows%20%7C%20macOS%20%7C%20Linux-informational)

Tool kecil untuk:
- ✅ **Menggabungkan** pasangan PDF `Cover` + `Lampiran` per nomor (mis. `001 - C.pdf` + `001 - L.pdf` ➜ `001.pdf`)
- 🔎 **Memvalidasi** penamaan file agar sesuai pola:  
  - `Cover` ➜ `NNN - C.pdf`  
  - `Lampiran` ➜ `NNN - L.pdf`  
  (dengan `NNN` = `001..100`)

> Folder **Cover/** dan **Lampiran/** sengaja diabaikan oleh Git lewat `.gitignore`, jadi kamu aman push ke GitHub tanpa mengikutsertakan data mentah.

---

## Struktur Proyek

```
KKN/
├─ merge_pdf.py         # gabung Cover + Lampiran ➜ Hasil/NNN.pdf
├─ cek_nama_pdf.py      # cek & laporkan file yang typo / hilang
├─ Cover/               # (ignored) berisi 001 - C.pdf ... 100 - C.pdf
├─ Lampiran/            # (ignored) berisi 001 - L.pdf ... 100 - L.pdf
└─ Hasil/               # (ignored) output hasil penggabungan
```

---

## Persiapan

1. **Python 3.8+** terpasang.
2. Install dependensi:
   ```bash
   pip install PyPDF2
   ```
   > (Opsional, untuk memperbaiki PDF rusak/kotor)  
   ```bash
   pip install pikepdf
   ```

---

## Cara Pakai

### 1) Cek Penamaan File (rekomendasi sebelum merge)
Jalankan:
```bash
python cek_nama_pdf.py
```
Kamu akan mendapat ringkasan:
- Nomor yang **hilang** di tiap folder
- File yang **suffix-nya salah** (mis. `C` di folder Lampiran)
- File **typo** (spasi/tanda minus/format tidak presisi) + **saran rename**
- File yang polanya tidak bisa dikenali

### 2) Gabung Cover + Lampiran ➜ Hasil/NNN.pdf
```bash
python merge_pdf.py
```
- Script akan membuat folder `Hasil/` jika belum ada.
- Output per nomor: `Hasil/001.pdf`, `Hasil/002.pdf`, dst.
- Pasangan yang tidak lengkap akan **diskip** dan dilaporkan.

> Tips: jika kamu menemui error seperti `EOF marker not found`, berarti ada PDF korup. Perbaiki dulu (contoh cepat):
> ```bash
> # perbaiki dengan pikepdf (opsional)
> python -c "import pikepdf,glob,os; os.makedirs('Lampiran_fixed',exist_ok=True); > [pikepdf.open(f).save(os.path.join('Lampiran_fixed',os.path.basename(f))) for f in glob.glob('Lampiran/*.pdf')]"
> ```

---

## Konvensi Penamaan

- **Cover**  : `NNN - C.pdf`  
- **Lampiran**: `NNN - L.pdf`  
- `NNN` wajib **3 digit** (`001..100`).  
- Spasi & tanda minus harus **persis** seperti di atas.

---

## Troubleshooting

- **`File tidak ditemukan untuk nomor XXX`** → Pastikan kedua file (`Cover` & `Lampiran`) untuk nomor itu ada dan penamaannya tepat.
- **`EOF marker not found` / PDF korup** → Coba perbaiki dengan `pikepdf` atau `qpdf`, lalu jalankan ulang.
- **Nama file tidak konsisten** → Jalankan `cek_nama_pdf.py` untuk melihat saran rename.

---

