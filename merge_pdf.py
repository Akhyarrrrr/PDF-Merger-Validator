import os
from PyPDF2 import PdfMerger

# Path folder relatif terhadap lokasi script
base_folder = os.path.dirname(os.path.abspath(__file__))
cover_folder = os.path.join(base_folder, "Cover")
lampiran_folder = os.path.join(base_folder, "Lampiran")
output_folder = os.path.join(base_folder, "Hasil")

os.makedirs(output_folder, exist_ok=True)

# Loop dari 001 sampai 100
for i in range(1, 101):
    nomor = str(i).zfill(3)  # jadi '001', '002', dst.

    cover_file = os.path.join(cover_folder, f"{nomor} - C.pdf")
    lampiran_file = os.path.join(lampiran_folder, f"{nomor} - L.pdf")
    output_file = os.path.join(output_folder, f"{nomor}.pdf")

    if os.path.exists(cover_file) and os.path.exists(lampiran_file):
        merger = PdfMerger()
        merger.append(cover_file)     # cover dulu
        merger.append(lampiran_file)  # lalu lampiran
        merger.write(output_file)
        merger.close()
        print(f"✅ Berhasil gabung: {output_file}")
    else:
        print(f"⚠️ File tidak ditemukan untuk nomor {nomor}")
