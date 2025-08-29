import os
import re

# --- Pengaturan folder (relatif terhadap lokasi script) ---
BASE = os.path.dirname(os.path.abspath(__file__))
FOLDER_COVER      = os.path.join(BASE, "Cover")
FOLDER_PENGESAHAN = os.path.join(BASE, "Pengesahan")
FOLDER_LAMPIRAN   = os.path.join(BASE, "Lampiran")

# --- Parameter ---
START_NUM, END_NUM = 1, 100   # 001..100
STRICT_EXT = ".pdf"           # ekstensi yang diizinkan

# Pola nama PERSIS (harus cocok 100%)
PAT_COVER      = re.compile(r"^\d{3} - C\.pdf$", re.IGNORECASE)
PAT_PENGESAHAN = re.compile(r"^\d{3} - P\.pdf$", re.IGNORECASE)
PAT_LAMPIRAN   = re.compile(r"^\d{3} - L\.pdf$", re.IGNORECASE)

# Pola longgar untuk memberi saran rename (ambil nomor & suffix)
PAT_RELAX = re.compile(r"(?i)(\d{1,3}).*?([CLP])\.pdf$")

def scan_folder(folder, pat_exact, expected_suffix):
    """Kembalikan info cek untuk satu folder."""
    expected = {f"{i:03d}": f"{i:03d} - {expected_suffix}.pdf" for i in range(START_NUM, END_NUM + 1)}
    exists_exact = set()
    typos, wrong_suffix, others = [], [], []

    if not os.path.isdir(folder):
        return {
            "missing": sorted(expected.keys()),
            "typos": [], "wrong_suffix": [], "others": [],
            "count_ok": 0, "count_total_pdf": 0,
            "folder_missing": True,
        }

    files = [f for f in os.listdir(folder) if f.lower().endswith(STRICT_EXT)]
    for name in files:
        if pat_exact.match(name):
            num = name[:3]
            exists_exact.add(num)
        else:
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
        "typos": typos,
        "wrong_suffix": wrong_suffix,
        "others": others,
        "count_ok": len(exists_exact),
        "count_total_pdf": len(files),
        "folder_missing": False,
    }

def print_report(title, info):
    print(f"\n===== {title} =====")
    if info.get("folder_missing"):
        print("⚠️ Folder tidak ditemukan.")
        return
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
    cov = scan_folder(FOLDER_COVER, PAT_COVER, "C")
    pen = scan_folder(FOLDER_PENGESAHAN, PAT_PENGESAHAN, "P")
    lam = scan_folder(FOLDER_LAMPIRAN, PAT_LAMPIRAN, "L")

    print_report("COVER (harus 'NNN - C.pdf')", cov)
    print_report("PENGESAHAN (harus 'NNN - P.pdf')", pen)
    print_report("LAMPIRAN (harus 'NNN - L.pdf')", lam)

    # Ringkasan gabungan
    miss_cov = set(cov["missing"]) if not cov.get("folder_missing") else set(f"{i:03d}" for i in range(START_NUM, END_NUM + 1))
    miss_pen = set(pen["missing"]) if not pen.get("folder_missing") else set(f"{i:03d}" for i in range(START_NUM, END_NUM + 1))
    miss_lam = set(lam["missing"]) if not lam.get("folder_missing") else set(f"{i:03d}" for i in range(START_NUM, END_NUM + 1))

    all_nums = set(f"{i:03d}" for i in range(START_NUM, END_NUM + 1))
    complete = sorted(all_nums - (miss_cov | miss_pen | miss_lam))
    incomplete = sorted(all_nums - set(complete))

    print("\n===== RINGKASAN GABUNGAN =====")
    print(f"- Lengkap di KETIGA folder ({len(complete)}): {', '.join(complete) if complete else '-'}")
    print(f"- TIDAK lengkap di satu/lebih folder ({len(incomplete)}): {', '.join(incomplete) if incomplete else '-'}")

if __name__ == "__main__":
    main()
