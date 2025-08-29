import os
import argparse
import tempfile
import logging
import warnings
from PyPDF2 import PdfMerger

# ==== (opsional) redam warning "Multiple definitions..." dari PyPDF2 ====
logging.getLogger("PyPDF2").setLevel(logging.ERROR)
warnings.filterwarnings("ignore", category=UserWarning, module="PyPDF2")

# ==== Argumen CLI ====
parser = argparse.ArgumentParser(
    description="Merge Cover -> Pengesahan -> Lampiran secara incremental."
)
parser.add_argument(
    "--force", action="store_true", help="Rebuild semua output meski sudah up-to-date"
)
args = parser.parse_args()

# ==== Folder ====
base_folder = os.path.dirname(os.path.abspath(__file__))
cover_folder = os.path.join(base_folder, "Cover")
pengesahan_folder = os.path.join(base_folder, "Pengesahan")
lampiran_folder = os.path.join(base_folder, "Lampiran")
output_folder = os.path.join(base_folder, "Hasil")
os.makedirs(output_folder, exist_ok=True)

# (opsional) fallback perbaikan jika pikepdf tersedia
try:
    import pikepdf

    HAS_PIKEPDF = True
except Exception:
    HAS_PIKEPDF = False


def newest_mtime(paths):
    try:
        return max(os.path.getmtime(p) for p in paths)
    except Exception:
        return None


def append_with_repair(merger, path):
    """Append PDF. Jika gagal & pikepdf ada, coba perbaiki dulu."""
    try:
        merger.append(path)
        return True
    except Exception:
        if not HAS_PIKEPDF:
            return False
        try:
            # simpan fixed file di folder output juga (satu drive)
            fixed = os.path.join(
                output_folder, "." + os.path.basename(path) + ".fixed.pdf"
            )
            with pikepdf.open(path) as pdf:
                pdf.save(fixed)
            merger.append(fixed)
            # bersihkan file fixed setelah selesai (akan dihapus manual opsional)
            return True
        except Exception:
            return False


for i in range(1, 101):
    nomor = f"{i:03d}"
    cover = os.path.join(cover_folder, f"{nomor} - C.pdf")
    pengesahan = os.path.join(pengesahan_folder, f"{nomor} - P.pdf")
    lampiran = os.path.join(lampiran_folder, f"{nomor} - L.pdf")
    out = os.path.join(output_folder, f"{nomor}.pdf")

    sources = [cover, pengesahan, lampiran]
    if not all(os.path.exists(p) for p in sources):
        print(f"⚠️  {nomor}: file tidak lengkap (cek C/P/L).")
        continue

    # Skip kalau output sudah >= terbaru dari sumber (kecuali --force)
    src_mtime = newest_mtime(sources)
    if os.path.exists(out) and not args.force:
        out_mtime = os.path.getmtime(out)
        if src_mtime is not None and out_mtime >= src_mtime:
            print(f"⏩ {nomor}: up-to-date, dilewati.")
            continue

    # Tulis ke file sementara di folder output (satu drive) → replace atomic
    tmp_out = os.path.join(output_folder, f".{nomor}.tmp.pdf")
    merger = PdfMerger(strict=False)
    ok = True
    for p in [cover, pengesahan, lampiran]:
        if not append_with_repair(merger, p):
            ok = False
            print(f"❌ {nomor}: gagal append {os.path.basename(p)}")
            break

    if ok:
        try:
            # tulis ke file sementara (same directory to avoid WinError 17)
            with open(tmp_out, "wb") as ftmp:
                merger.write(ftmp)
            merger.close()
            os.replace(tmp_out, out)  # atomic replace di drive yang sama
            print(f"✅ {nomor}: dibuat/diperbarui -> {out}")
        except Exception as e:
            try:
                merger.close()
            except:
                pass
            try:
                if os.path.exists(tmp_out):
                    os.remove(tmp_out)
            except:
                pass
            print(f"❌ {nomor}: gagal menulis output ({e})")
    else:
        try:
            merger.close()
        except:
            pass
        try:
            if os.path.exists(tmp_out):
                os.remove(tmp_out)
        except:
            pass
        print(f"❌ {nomor}: merge batal, output lama (jika ada) dipertahankan.")
