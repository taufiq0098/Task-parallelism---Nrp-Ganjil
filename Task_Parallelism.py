import threading
import time
import os
import math
import zipfile
import tempfile

# NRP: 152024161 (Ganjil) -> Task Parallelism
# Nama: Taufiq Mahfudin

def timestamp(pesan):
    t = time.strftime("%H:%M:%S")
    print(f"[{t}] {pesan}")


# ── TASK 1: Image Processing ──────────────────────────────
# simulasi resize + grayscale conversion dari pixel matrix
def proses_gambar():
    timestamp("Task 1 mulai : Image Processing")

    # buat dummy image 800x600 (pixel RGB)
    width, height = 800, 600
    gambar = [[(i % 256, (i+j) % 256, j % 256)
               for j in range(width)]
              for i in range(height)]
    timestamp("Task 1        : gambar dibuat (800x600 pixels)")

    # resize ke 400x300 (ambil setiap pixel ke-2)
    hasil_resize = [gambar[i][j]
                    for i in range(0, height, 2)
                    for j in range(0, width, 2)]
    timestamp("Task 1        : resize ke 400x300 selesai")

    # konversi ke grayscale: Y = 0.299R + 0.587G + 0.114B
    grayscale = [int(0.299*r + 0.587*g + 0.114*b)
                 for r, g, b in hasil_resize]
    rata = sum(grayscale) / len(grayscale)
    timestamp(f"Task 1        : grayscale selesai, avg brightness = {rata:.1f}")
    timestamp("Task 1 selesai: Image Processing DONE")


# ── TASK 2: Database Query (simulasi pake list) ───────────
# simulasi fetch + aggregate data tanpa library eksternal
def query_database():
    timestamp("Task 2 mulai : Database Query")

    # buat "tabel" dummy berisi 50.000 baris
    tabel = [{"id": i,
              "nilai": (i * 37 + 13) % 100,
              "kategori": ["A","B","C"][i % 3]}
             for i in range(50000)]
    timestamp(f"Task 2        : loaded {len(tabel)} rows")

    # SELECT AVG(nilai) GROUP BY kategori
    grup = {"A": [], "B": [], "C": []}
    for row in tabel:
        grup[row["kategori"]].append(row["nilai"])

    hasil = {k: sum(v)/len(v) for k, v in grup.items()}
    for kat, avg in hasil.items():
        timestamp(f"Task 2        : kategori {kat} -> avg nilai = {avg:.2f}")

    timestamp("Task 2 selesai: Database Query DONE")


# ── TASK 3: File Compression ──────────────────────────────
# beneran bikin file terus zip menggunakan zipfile
def kompresi_file():
    timestamp("Task 3 mulai : File Compression")

    tmpdir = tempfile.mkdtemp()
    file_list = []

    # bikin 5 file teks dummy
    for i in range(5):
        path = os.path.join(tmpdir, f"data_{i}.txt")
        with open(path, "w") as f:
            # tiap file isi 1000 baris angka
            for j in range(1000):
                f.write(f"baris {j}: nilai = {math.sin(j + i):.6f}\n")
        file_list.append(path)

    timestamp(f"Task 3        : {len(file_list)} file sumber siap")

    # kompres semua file ke satu ZIP
    zip_path = os.path.join(tmpdir, "output.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp in file_list:
            zf.write(fp, os.path.basename(fp))

    ukuran = os.path.getsize(zip_path)
    timestamp(f"Task 3        : ZIP selesai, ukuran = {ukuran} bytes")
    timestamp("Task 3 selesai: File Compression DONE")


# ── MAIN ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  TASK PARALLELISM - Taufiq Mahfudin / 152024161")
    print("  3 task BERBEDA dijalanin paralel pake threading")
    print("=" * 55)

    t1 = threading.Thread(target=proses_gambar,  name="ImageThread")
    t2 = threading.Thread(target=query_database, name="DBThread")
    t3 = threading.Thread(target=kompresi_file,  name="ZipThread")

    mulai = time.time()

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    total = time.time() - mulai
    print("=" * 55)
    print(f"  Semua task selesai! Total waktu: {total:.2f} detik")
    print("=" * 55)