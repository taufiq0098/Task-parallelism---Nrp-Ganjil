. Pendahuluan
Karena NRP saya 152024161 (ganjil), saya mengerjakan bagian Task Parallelism. Task parallelism adalah teknik pemrograman paralel di mana beberapa task yang berbeda secara fungsional dieksekusi secara bersamaan menggunakan thread yang berbeda-beda.
Perbedaan utamanya dengan data parallelism: kalau data parallelism menjalankan operasi yang sama ke banyak data secara serentak (cocok NRP genap), task parallelism justru menjalankan pekerjaan yang berbeda-beda secara paralel. Makanya beban tiap task tidak harus sama (uneven), yang penting bisa dijalankan secara independen.
Di praktikum ini saya mengimplementasikan 3 task yang benar-benar berbeda: image processing (manipulasi pixel), database query (agregasi data), dan file compression (buat dan zip file). Ketiganya dijalankan paralel menggunakan modul threading bawaan Python.
2. Source Code
Berikut adalah kode lengkap yang digunakan:

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
    timestamp("Task 1        : gambar dibuat (800x600 pixels)")
    # resize ke 400x300 (ambil setiap pixel ke-2)
    hasil_resize = [gambar[i][j]
                    for i in range(0, height, 2)
                    for j in range(0, width, 2)]
    timestamp("Task 1        : resize ke 400x300 selesai")
    # konversi ke grayscale: Y = 0.299R + 0.587G + 0.114B
    grayscale = [int(0.299*r + 0.587*g + 0.114*b)
                 for r, g, b in hasil_resize]
    rata = sum(grayscale) / len(grayscale)
    timestamp(f"Task 1        : grayscale selesai, avg brightness = {rata:.1f}")
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
    timestamp(f"Task 2        : loaded {len(tabel)} rows")
    # SELECT AVG(nilai) GROUP BY kategori
    grup = {"A": [], "B": [], "C": []}
    for row in tabel:
        grup[row["kategori"]].append(row["nilai"])
    hasil = {k: sum(v)/len(v) for k, v in grup.items()}
    for kat, avg in hasil.items():
        timestamp(f"Task 2        : kategori {kat} -> avg nilai = {avg:.2f}")
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
    timestamp(f"Task 3        : {len(file_list)} file sumber siap")
    # kompres semua file ke satu ZIP
    zip_path = os.path.join(tmpdir, "output.zip")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for fp in file_list:
            zf.write(fp, os.path.basename(fp))
    ukuran = os.path.getsize(zip_path)
    timestamp(f"Task 3        : ZIP selesai, ukuran = {ukuran} bytes")
timestamp("Task 3 selesai: File Compression DONE")

# ── MAIN ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("=" * 55)
    print("  TASK PARALLELISM - Taufiq Mahfudin / 152024161")
    print("  3 task BERBEDA dijalanin paralel pake threading")
    print("=" * 55)
    t1 = threading.Thread(target=proses_gambar,  name="ImageThread")
    t2 = threading.Thread(target=query_database, name="DBThread")
    t3 = threading.Thread(target=kompresi_file,  name="ZipThread")
    mulai = time.time()
    t1.start()
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
    total = time.time() - mulai
    print("=" * 55)
    print(f"  Semua task selesai! Total waktu: {total:.2f} detik")
    print("=" * 55)
3. Penjelasan Kode
a. Fungsi timestamp(pesan)
Fungsi helper yang dipanggil di setiap step tiap task. Tugasnya nampilin waktu sekarang (format HH:MM:SS) dan pesan yang dikirim. Penting supaya bisa keliatan urutan dan timing eksekusi antar task secara real-time di terminal.
b. Task 1 — proses_gambar()
Mengimplementasikan pipeline image processing sederhana tanpa library eksternal. Pertama dibuat dummy image berukuran 800x600 pixel dalam format RGB (tuple per pixel). Kemudian dilakukan resize ke 400x300 dengan cara mengambil setiap pixel ke-2 secara horizontal dan vertikal (downsampling). Terakhir setiap pixel dikonversi ke nilai grayscale menggunakan rumus luminance standar: Y = 0.299R + 0.587G + 0.114B. Hasil akhirnya dihitung rata-rata brightness seluruh gambar.
c. Task 2 — query_database()
Mensimulasikan operasi database tanpa library eksternal. Dibuat tabel berisi 50.000 baris data dengan kolom id, nilai (0-99), dan kategori (A/B/C). Kemudian dilakukan operasi yang setara dengan SELECT AVG(nilai) GROUP BY kategori — data dikelompokkan per kategori lalu dihitung rata-rata nilainya. Ini menunjukkan task yang melibatkan iterasi data besar bisa dijalankan paralel tanpa saling mengganggu.
d. Task 3 — kompresi_file()
Melakukan kompresi file yang sesungguhnya menggunakan modul zipfile bawaan Python. Pertama dibuat 5 file teks di folder temporary, masing-masing berisi 1000 baris data numerik hasil fungsi sin(). Setelah semua file siap, kelima file dikompres ke dalam satu arsip ZIP menggunakan algoritma DEFLATE. Ukuran file ZIP hasil kompresi ditampilkan sebagai verifikasi.
e. Bagian Main
Di bagian main, tiga Thread object dibuat — masing-masing membawa satu fungsi task yang berbeda. Setelah .start() dipanggil untuk ketiganya, ketiga thread langsung berjalan secara bersamaan. .join() dipakai supaya program utama menunggu sampai semua thread selesai sebelum mencetak total waktu. Dengan cara ini 3 pekerjaan yang berbeda bisa selesai jauh lebih cepat dibanding dijalankan satu per satu.
4. Output Program
Berikut hasil output nyata ketika program dieksekusi. Log dari Task 1, 2, dan 3 saling interleave — misalnya Task 3 sudah selesai sementara Task 1 masih berjalan. Ini membuktikan ketiga task benar-benar berjalan secara paralel:

5. Analisis Output
Ada beberapa hal yang bisa diamati dari output di atas yang membuktikan task parallelism bekerja:

Pertama, ketiga task start di waktu yang sama. Semua Task 1, 2, dan 3 muncul di timestamp [04:11:32] yang sama. Ini karena .start() dipanggil berurutan sangat cepat sehingga ketiga thread langsung aktif hampir bersamaan.
Kedua, log antar task saling interleave. Task 3 sudah selesai (DONE) sementara Task 1 masih di tahap awal dan Task 2 baru selesai load data. Urutan ini tidak mungkin terjadi kalau programnya sequential — ini bukti konkret parallelism berjalan.
Ketiga, tiap task mengerjakan hal yang benar-benar berbeda. Task 1 melakukan komputasi matematika pada array pixel, Task 2 melakukan iterasi dan agregasi data tabel, Task 3 melakukan operasi I/O file dan kompresi. Inilah yang membedakan task parallelism dari data parallelism.
Keempat, efisiensi waktu. Total eksekusi paralel hanya 0.41 detik. Jika dijalankan sequential (berurutan), estimasinya sekitar 1.2 detik. Ini menunjukkan speedup nyata dari paralelisasi.
6. Kesimpulan
Task parallelism berhasil diimplementasikan menggunakan modul threading Python. Tiga task dengan karakteristik berbeda — komputasi piksel, agregasi data, dan kompresi file — dieksekusi secara paralel dan terbukti berjalan bersamaan berdasarkan interleaving output yang teramati.
Task parallelism paling tepat digunakan ketika program memiliki beberapa pekerjaan yang independen dan berbeda jenis, sehingga tidak perlu menunggu satu selesai dulu sebelum memulai yang lain. Hasilnya program bisa lebih efisien dalam memanfaatkan resources CPU yang tersedia.
