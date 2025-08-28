import os
import re
from collections import defaultdict

# --- Pengaturan folder (relatif terhadap lokasi script) ---
BASE = os.path.dirname(os.path.abspath(__file__))
FOLDER_LAMPIRAN = os.path.join(BASE, "Lampiran")
FOLDER_COVER    = os.path.join(BASE, "Cover")

# --- Parameter ---
START_NUM, END_NUM = 1, 100   # 001..100
STRICT_EXT = ".pdf"           # ekstensi yang diizinkan

# Pola nama PERSIS (harus cocok 100%)
PAT_LAMPIRAN = re.compile(r"^\d{3} - L\.pdf$", re.IGNORECASE)
PAT_COVER    = re.compile(r"^\d{3} - C\.pdf$", re.IGNORECASE)

# Pola longgar untuk memberi saran rename (ambil nomor & suffix)
PAT_RELAX = re.compile(r"(?i)(\d{1,3}).*?([CL])\.pdf$")

def scan_folder(folder, pat_exact, expected_suffix):
    """Kembalikan info cek untuk satu folder."""
    expected = {f"{i:03d}": f"{i:03d} - {expected_suffix}.pdf" for i in range(START_NUM, END_NUM + 1)}
    exists_exact = set()
    typos = []
    wrong_suffix = []
    others = []

    files = [f for f in os.listdir(folder) if f.lower().endswith(STRICT_EXT)]
    for name in files:
        if pat_exact.match(name):
            num = name[:3]
            exists_exact.add(num)
        else:
            # cek apakah suffix-nya kebalik (mis. L vs C)
            m = PAT_RELAX.search(name)
            if m:
                num = f"{int(m.group(1)):03d}"
                suf = m.group(2).upper()
                if suf != expected_suffix:
                    wrong_suffix.append((name, f"{num} - {expected_suffix}.pdf"))
                else:
                    typos.append((name, f"{num} - {expected_suffix}.pdf"))
            else:
                others.append(name)

    missing = sorted(set(expected.keys()) - exists_exact)

    return {
        "missing": missing,
        "typos": typos,                 # (nama_asli, saran_nama_baru)
        "wrong_suffix": wrong_suffix,   # (nama_asli, saran_nama_baru)
        "others": others,               # file .pdf yang tidak bisa dipahami polanya
        "count_ok": len(exists_exact),
        "count_total_pdf": len(files),
    }

def print_report(title, info):
    print(f"\n===== {title} =====")
    print(f"Total PDF: {info['count_total_pdf']} | Cocok pola: {info['count_ok']}")
    if info["missing"]:
        print(f"- Nomor HILANG ({len(info['missing'])}): " + ", ".join(info["missing"]))
    else:
        print("- Tidak ada nomor hilang.")

    if info["wrong_suffix"]:
        print(f"- Suffix SALAH ({len(info['wrong_suffix'])}):")
        for old, new in sorted(info["wrong_suffix"]):
            print(f"  • {old}  -> seharusnya: {new}")
    else:
        print("- Tidak ada suffix salah.")

    if info["typos"]:
        print(f"- TYPO/format tidak presisi ({len(info['typos'])}):")
        for old, new in sorted(info["typos"]):
            print(f"  • {old}  -> saran: {new}")
    else:
        print("- Tidak ada nama typo (yang masih benar suffix).")

    if info["others"]:
        print(f"- TIDAK TERDETEKSI polanya ({len(info['others'])}):")
        for name in sorted(info["others"]):
            print(f"  • {name}")
    else:
        print("- Tidak ada file lain yang membingungkan.")

def main():
    if not os.path.isdir(FOLDER_LAMPIRAN) or not os.path.isdir(FOLDER_COVER):
        print("Pastikan ada folder 'Lampiran' dan 'Cover' di sebelah script ini.")
        return

    lamp = scan_folder(FOLDER_LAMPIRAN, PAT_LAMPIRAN, "L")
    cov  = scan_folder(FOLDER_COVER,    PAT_COVER,    "C")

    print_report("LAMPIRAN (harus 'NNN - L.pdf')", lamp)
    print_report("COVER (harus 'NNN - C.pdf')", cov)

    # Ringkasan cepat gabungan
    miss_l = set(lamp["missing"])
    miss_c = set(cov["missing"])
    both_missing = sorted(miss_l & miss_c)
    print("\n===== RINGKASAN GABUNGAN =====")
    if both_missing:
        print(f"- Nomor yang hilang di KEDUA folder: {', '.join(both_missing)}")
    else:
        print("- Tidak ada nomor yang hilang di kedua folder sekaligus.")

if __name__ == "__main__":
    main()
