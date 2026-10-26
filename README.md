# Bike Sharing Dashboard

Proyek analisis data untuk mempelajari faktor cuaca, musim, dan jam sibuk yang memengaruhi peminjaman sepeda publik, dilengkapi dengan dashboard interaktif Streamlit. Projek ini menjadi tahap akhir dari kelas Belajar Fundamental Analisa Data yang di laksanakan oleh Dicoding sebagai bentuk Submission untuk tugas akhir. Data yang digunakan bersumber dari Kelas tersebut.

## Pertanyaan Analisis

1. Bagaimana pengaruh kondisi cuaca (*weathersit*) dan musim (*season*) terhadap rata-rata peminjaman sepeda harian sepanjang tahun 2011 hingga 2012?
2. Bagaimana pola perbedaan jumlah peminjaman sepeda per jam antara hari kerja (*workingday*) dan hari libur (*weekend/holiday*)?

## Struktur Folder

```text
submission/
├── dashboard/
│   ├── dashboard.py         # Skrip dashboard Streamlit
│   └── main_data.csv        # Data bersih siap pakai
├── data/
│   ├── day.csv              # Data harian mentah
│   └── hour.csv             # Data per jam mentah
├── notebook.ipynb           # Notebook analisis data
├── README.md                # Dokumentasi proyek
├── requirements.txt         # Daftar library Python
└── url.txt                  # Link dashboard di Streamlit Cloud

```

## Setup Environment

Pilih salah satu cara setup di bawah ini:

### 1. Menggunakan Anaconda / Conda

```bash
conda create --name main-ds python=3.9 -y
conda activate main-ds
pip install -r requirements.txt

```

### 2. Menggunakan Terminal / PowerShell (venv)

```bash
# Buat virtual environment
python -m venv env

# Aktifkan environment
# Untuk Windows (PowerShell / CMD):
.\env\Scripts\activate
# Untuk macOS / Linux:
source env/bin/activate

# Install semua library yang dibutuhkan
pip install -r requirements.txt

```

## Menjalankan Dashboard

Buka terminal di folder utama proyek (`submission`), lalu jalankan perintah ini:

```bash
streamlit run dashboard/dashboard.py

```

Setelah perintah dijalankan, dashboard bakal otomatis kebuka di browser kamu pada alamat `http://localhost:8501`.

