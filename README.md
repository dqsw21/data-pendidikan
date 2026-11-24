# Data Pendidikan

Website untuk mengolah, menganalisis, memvisualisasikan, dan memprediksi data pendidikan berdasarkan data historis. Aplikasi dikembangkan menggunakan Django, Python, Pandas, NumPy, JavaScript, dan integrasi Gemini AI.

## Tentang Proyek

Data Pendidikan merupakan platform yang dirancang untuk membantu pengguna memahami perkembangan indikator pendidikan melalui penyajian data, analisis statistik, visualisasi grafik, dan prediksi.

Data yang tersedia diolah menjadi informasi yang lebih mudah dipahami, sehingga pengguna dapat melihat perkembangan indikator pendidikan, membandingkan jenjang pendidikan, serta memahami perubahan data dari tahun ke tahun.

Selain pengolahan data, sistem juga mengintegrasikan Gemini AI untuk memberikan interpretasi terhadap hasil analisis dan prediksi.

## Tujuan

- Menyajikan data pendidikan dalam bentuk yang lebih informatif.
- Mempermudah eksplorasi dataset pendidikan.
- Menampilkan perkembangan indikator pendidikan dari tahun ke tahun.
- Membandingkan data berdasarkan jenjang pendidikan dan wilayah.
- Melakukan analisis statistik terhadap indikator pendidikan.
- Menghasilkan prediksi berdasarkan data historis.
- Membantu memahami hasil analisis dan prediksi melalui AI.

## Teknologi

| Teknologi | Penggunaan |
|---|---|
| Python | Bahasa pemrograman utama |
| Django | Framework aplikasi web dan backend |
| Pandas | Pengolahan dataset |
| NumPy | Perhitungan numerik |
| SQLite | Database aplikasi |
| HTML | Struktur halaman |
| CSS | Desain dan tampilan |
| JavaScript | Interaksi dan pengelolaan grafik |
| Chart.js | Visualisasi data |
| Google Gemini AI | Interpretasi analisis dan prediksi |
| python-dotenv | Pengelolaan konfigurasi environment |
| WhiteNoise | Pengelolaan static files |
| Gunicorn | Server WSGI |

## Struktur Proyek

\`\`\`text
data-pendidikan/
├── config/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── dashboard/
│   ├── migrations/
│   ├── templatetags/
│   ├── ai_interpreter.py
│   ├── ai_service.py
│   ├── analysis_engine.py
│   ├── data_processor.py
│   ├── dataset_processor.py
│   ├── predictor.py
│   ├── province_predictor.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── tests.py
├── data/
│   ├── Data_TahunAjar_2023-2024.csv
│   ├── Data_TahunAjar_2024-2025.csv
│   └── Data_TahunAjar_2025-2026.csv
├── static/
│   ├── css/
│   └── js/
├── templates/
│   ├── base.html
│   └── dashboard/
├── staticfiles/
├── .env
├── .gitignore
├── manage.py
├── requirements.txt
└── db.sqlite3
\`\`\`

## Fitur Utama

### 1. Landing Page

Halaman awal website yang memperkenalkan platform Data Pendidikan serta memberikan gambaran indikator dan informasi yang tersedia.

Landing page menampilkan gambaran data pendidikan, indikator utama, dan informasi perkembangan data antarperiode.

### 2. Dashboard

Dashboard berfungsi sebagai halaman utama untuk melihat gambaran data pendidikan.

Informasi yang disajikan meliputi:

- Peserta didik baru.
- Jumlah peserta didik.
- Jumlah lulusan.
- Peserta didik mengulang.
- Persentase peserta didik mengulang.
- Jumlah putus sekolah.
- Persentase putus sekolah.
- Perbandingan data antarperiode.

### 3. Eksplorasi Dataset

Fitur eksplorasi dataset digunakan untuk melihat data pendidikan yang tersedia secara lebih terperinci.

Pengguna dapat mengeksplorasi informasi dataset yang digunakan oleh sistem untuk memahami isi dan kondisi data sebelum melakukan analisis lebih lanjut.

### 4. Analisis Pendidikan

Fitur analisis digunakan untuk mengetahui kondisi dan perubahan indikator pendidikan berdasarkan tahun yang dipilih.

Analisis mencakup:

- Ringkasan 9 indikator pendidikan.
- Rata-rata nilai indikator.
- Median.
- Nilai tertinggi dan terendah.
- Kecamatan dengan nilai tertinggi dan terendah.
- Analisis berdasarkan jenjang pendidikan.
- Perbandingan perubahan tahunan.
- Perubahan nilai indikator antarperiode.
- Daftar perubahan terbesar dan terkecil.

Indikator yang dianalisis terdiri dari tiga kategori pada masing-masing jenjang SMA, MA, dan SMK:

| Kategori | Jenjang |
|---|---|
| Mengulang | SMA, MA, SMK |
| Putus Sekolah | SMA, MA, SMK |
| Lulusan | SMA, MA, SMK |

Total terdapat 9 indikator yang digunakan dalam proses analisis.

### 5. Prediksi Pendidikan Tingkat Kecamatan

Sistem prediksi kecamatan menggunakan data historis untuk menghasilkan perkiraan indikator pendidikan pada tahun mendatang.

Prediksi mencakup:

- Angka mengulang SMA.
- Angka putus sekolah SMA.
- Angka lulusan SMA.
- Angka mengulang MA.
- Angka putus sekolah MA.
- Angka lulusan MA.
- Angka mengulang SMK.
- Angka putus sekolah SMK.
- Angka lulusan SMK.

Prediksi tersedia untuk tahun 2026, 2027, dan 2028.

#### Metode Prediksi

Sistem menggunakan pendekatan Local Trend yang mempertimbangkan perubahan data aktual antarperiode.

Proses prediksi juga menggunakan:

- Perubahan nilai historis.
- Perkembangan indikator dari tahun ke tahun.
- Student Growth Assumption.
- Dynamic Indicator Interaction.
- Pembatasan nilai indikator sesuai kategorinya.
- Stability Score untuk melihat kestabilan data historis.

#### Local Trend

Metode Local Trend menggunakan perubahan nilai historis sebagai dasar untuk memperkirakan nilai pada tahun berikutnya.

Prediksi dilakukan secara bertahap berdasarkan perkembangan data aktual dan perubahan antarperiode.

#### Student Growth Assumption

Pada indikator lulusan, sistem menggunakan asumsi pertumbuhan peserta didik secara moderat sebagai bagian dari perhitungan prediksi.

Asumsi ini merupakan komponen perhitungan model, bukan data pertumbuhan aktual.

#### Dynamic Indicator Interaction

Prediksi indikator lulusan juga mempertimbangkan perubahan indikator mengulang dan putus sekolah yang berkaitan dengan jenjang pendidikan tersebut.

### 6. Prediksi Pendidikan Tingkat Provinsi

Sistem prediksi provinsi menyediakan visualisasi data aktual dan hasil prediksi untuk jenjang SMA dan SMK.

Indikator yang digunakan:

- Lulusan.
- Mengulang.
- Putus sekolah.

Hasil prediksi ditampilkan dalam bentuk grafik yang membandingkan data aktual dengan data prediksi.

Grafik juga menampilkan informasi jumlah dan persentase indikator berdasarkan jumlah peserta didik.

#### Linear Forecast

Metode Linear Forecast menggunakan tren linear dari data historis untuk memperkirakan nilai pada tahun mendatang.

Perhitungan dilakukan berdasarkan hubungan antara waktu dan nilai historis indikator.

#### Trend, Momentum, dan Damped Acceleration

Metode ini digunakan untuk menghasilkan proyeksi perkembangan berdasarkan:

- Perubahan historis.
- Tren perubahan terbaru.
- Momentum perkembangan.
- Percepatan perubahan.
- Peredaman tren secara bertahap.
- Fluktuasi terkontrol.

Tujuannya adalah menghasilkan proyeksi yang mempertimbangkan perubahan sebelumnya tanpa mempertahankan pertumbuhan atau penurunan secara berlebihan.

### 7. Interpretasi Gemini AI

Aplikasi mengintegrasikan Gemini AI untuk membantu menjelaskan data dan hasil prediksi dalam bahasa Indonesia yang lebih mudah dipahami.

Interpretasi AI tersedia untuk:

- Analisis dashboard.
- Hasil prediksi tingkat kecamatan.
- Grafik prediksi tingkat provinsi.

AI digunakan sebagai pendukung interpretasi, bukan sebagai pengganti perhitungan utama sistem.

AI diarahkan untuk:

- Menggunakan data yang tersedia.
- Menjelaskan perubahan indikator.
- Membandingkan data jika tersedia.
- Membedakan data aktual dengan data prediksi.
- Menjelaskan tren naik, turun, atau stabil.
- Tidak mengarang angka maupun penyebab perubahan.
- Menyampaikan keterbatasan apabila data tidak mencukupi.

## Modul Backend

### views.py

Mengelola request pengguna, menyiapkan data, menjalankan proses yang diperlukan, dan mengirimkan hasil kepada template website.

### data_processor.py

Mengelola dataset utama untuk proses analisis dan visualisasi.

Fungsinya mencakup pembacaan dataset, konversi kolom numerik, serta penyediaan data indikator berdasarkan tahun.

### dataset_processor.py

Mengelola dataset tahun ajaran untuk prediksi tingkat provinsi.

Modul ini membaca beberapa dataset tahun ajaran, menggabungkan data, mengolah nilai numerik, serta menyiapkan informasi berdasarkan provinsi dan jenjang pendidikan.

### analysis_engine.py

Menjalankan proses analisis indikator pendidikan berdasarkan tahun yang dipilih.

Modul ini menghasilkan ringkasan statistik, informasi per jenjang, data kecamatan, serta perbandingan perubahan antarperiode.

### predictor.py

Menangani perhitungan prediksi pendidikan tingkat kecamatan.

Modul ini mengolah data historis, menghitung tren, menghasilkan proyeksi indikator, dan menyusun informasi hasil prediksi.

### province_predictor.py

Menangani prediksi pendidikan tingkat provinsi.

Modul ini menyediakan perhitungan Linear Forecast serta metode prediksi berdasarkan tren, momentum, dan percepatan yang diredam.

### ai_service.py

Menghubungkan aplikasi dengan layanan Gemini AI.

Modul ini mengelola permintaan AI, konfigurasi API Key, pilihan model, timeout, logging, dan penanganan kesalahan.

Sistem menyediakan beberapa model alternatif sebagai mekanisme fallback apabila model yang digunakan mengalami kegagalan.

### ai_interpreter.py

Mengelola prompt dan proses interpretasi AI untuk data dashboard, prediksi kecamatan, dan grafik prediksi provinsi.

## Dataset

Dataset disimpan dalam folder `data/`.

File yang digunakan:

- `Data_TahunAjar_2023-2024.csv`
- `Data_TahunAjar_2024-2025.csv`
- `Data_TahunAjar_2025-2026.csv`

Dataset digunakan untuk menyediakan data historis yang menjadi dasar pengolahan, analisis, visualisasi, dan prediksi.

## Template

Template HTML disimpan dalam folder `templates/`.

| File | Fungsi |
|---|---|
| `base.html` | Kerangka utama website |
| `landing.html` | Halaman landing |
| `home.html` | Dashboard |
| `dataset.html` | Eksplorasi dataset |
| `analysis.html` | Analisis pendidikan |
| `prediction.html` | Prediksi pendidikan |
| `model_info.html` | Informasi sistem prediksi |
| `about.html` | Informasi website |

## Static Files

### CSS

Folder `static/css/` berisi file untuk mengatur tampilan website, layout, animasi konten, efek entrance, dan transisi halaman.

File utama:

- `style.css`
- `content-motion.css`
- `entrance.css`
- `page-transition.css`

### JavaScript

Folder `static/js/` berisi script interaksi frontend dan visualisasi.

File utama:

- `charts.js`
- `province_prediction.js`
- `content-motion.js`
- `page-transition.js`

Folder `dashboard/static/js/` juga berisi script untuk pengelolaan interpretasi AI dashboard dan prediksi.

### Staticfiles

Folder `staticfiles/` merupakan hasil pengumpulan static files melalui Django Collectstatic dan digunakan sesuai konfigurasi pengelolaan aset statis aplikasi.

## Database

Aplikasi menggunakan SQLite melalui Django ORM.

Database disimpan pada:

\`\`\`text
db.sqlite3
\`\`\`

### PredictionHistory

Model `PredictionHistory` digunakan untuk menyimpan riwayat prediksi.

Data yang disimpan meliputi:

- Kecamatan.
- Tahun prediksi.
- Tahun data.
- Hasil prediksi dalam format JSON.
- Waktu pembuatan prediksi.

Riwayat disusun berdasarkan waktu pembuatan terbaru.

## Cache

Aplikasi menggunakan cache lokal Django untuk menyimpan hasil interpretasi AI.

Cache memiliki waktu penyimpanan 24 jam untuk membantu mengurangi permintaan AI yang berulang dan meningkatkan efisiensi penggunaan layanan.

## Instalasi

### Persyaratan

- Python
- pip
- Git

### Clone Repository

\`\`\`bash
git clone https://github.com/namelles12/data-pendidikan.git
cd data-pendidikan
\`\`\`

### Membuat Virtual Environment

\`\`\`bash
python3 -m venv .venv
\`\`\`

### Mengaktifkan Virtual Environment

\`\`\`bash
source .venv/bin/activate
\`\`\`

### Instal Dependency

\`\`\`bash
pip install -r requirements.txt
\`\`\`

## Konfigurasi Environment

Aplikasi menggunakan file `.env` untuk menyimpan konfigurasi lingkungan.

Konfigurasi yang digunakan:

- `DJANGO_SECRET_KEY`
- `DJANGO_DEBUG`
- `DJANGO_ALLOWED_HOSTS`
- `DJANGO_CSRF_TRUSTED_ORIGINS`
- `GEMINI_API_KEY_1`
- `GEMINI_API_KEY_2`

Contoh:

\`\`\`env
DJANGO_SECRET_KEY=isi_secret_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=
GEMINI_API_KEY_1=isi_api_key
GEMINI_API_KEY_2=isi_api_key
\`\`\`

Sesuaikan konfigurasi dengan lingkungan yang digunakan.

Jangan mengunggah API Key, Secret Key, maupun informasi sensitif ke repository publik.

## Menjalankan Aplikasi

### Memeriksa Konfigurasi Django

\`\`\`bash
python manage.py check
\`\`\`

### Migrasi Database

\`\`\`bash
python manage.py migrate
\`\`\`

### Menjalankan Server Development

\`\`\`bash
python manage.py runserver
\`\`\`

## Perintah Django

| Perintah | Fungsi |
|---|---|
| `python manage.py check` | Memeriksa konfigurasi Django |
| `python manage.py runserver` | Menjalankan server development |
| `python manage.py migrate` | Menerapkan perubahan database |
| `python manage.py makemigrations` | Membuat migration |
| `python manage.py collectstatic` | Mengumpulkan static files |
| `python manage.py createsuperuser` | Membuat administrator |

## Alur Sistem

\`\`\`text
Dataset Pendidikan
       |
       v
Pembacaan Dataset
       |
       v
Pengolahan dan Persiapan Data
       |
       v
+---------------------------+
|                         |
v                         v
Analisis Statistik    Mesin Prediksi
|                         |
v                         v
Visualisasi Data     Hasil Prediksi
                          |
                          v
                    Interpretasi AI
                          |
                          v
                    Informasi Website
\`\`\`

## Keamanan

Hal yang perlu diperhatikan dalam pengembangan dan deployment:

- Menjaga Secret Key Django.
- Menjaga API Key Gemini.
- Tidak mengunggah file `.env` ke repository publik.
- Menggunakan `DEBUG=False` pada lingkungan produksi.
- Mengatur `ALLOWED_HOSTS` sesuai kebutuhan.
- Memeriksa konfigurasi keamanan Django sebelum deployment.

## Batasan Sistem

Hasil analisis dan prediksi merupakan informasi yang dihasilkan dari dataset dan metode perhitungan yang digunakan.

Prediksi bukan data aktual. Hasil prediksi dapat berbeda dari kondisi yang terjadi di masa mendatang karena dipengaruhi oleh kualitas dataset, perubahan kondisi pendidikan, serta keterbatasan metode perhitungan.

Interpretasi Gemini AI digunakan sebagai pendukung pemahaman data dan tetap perlu diperiksa berdasarkan data yang tersedia.

## Pengembangan Selanjutnya

Pengembangan dapat mencakup:

- Peningkatan metode prediksi.
- Pengembangan analisis statistik.
- Penambahan indikator pendidikan.
- Peningkatan visualisasi.
- Optimasi proses pengolahan data.
- Peningkatan kualitas interpretasi AI.
- Pengujian dan validasi hasil prediksi.
- Peningkatan pengalaman pengguna.

---

**Data Pendidikan**  
Platform pengolahan, analisis, visualisasi, dan prediksi data pendidikan.
