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
