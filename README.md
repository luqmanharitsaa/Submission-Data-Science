#  Proyek Analisis Data: Bike Sharing Dataset

Proyek analisis data untuk mengeksplorasi faktor lingkungan, cuaca, dan pola waktu yang memengaruhi peminjaman sepeda publik, dilengkapi dengan dashboard interaktif berbasis Streamlit.

---

##  Latar Belakang & Pertanyaan Bisnis

Proyek ini bertujuan menjawab dua pertanyaan bisnis utama menggunakan framework **SMART**:
1. **Pertanyaan 1:** Bagaimana pengaruh kondisi cuaca (*weathersit*) dan musim (*season*) terhadap total rata-rata peminjaman sepeda harian sepanjang tahun 2011 hingga 2012?
2. **Pertanyaan 2:** Bagaimana pola perbedaan jumlah peminjaman sepeda per jam antara hari kerja (*workingday*) dan hari libur (*weekend/holiday*) pada tahun 2011–2012?

---

##  Struktur Direktori

```text
submission/
├── dashboard/
│   ├── dashboard.py         # Skrip antarmuka Streamlit
│   └── main_data.csv        # Dataset bersih siap pakai untuk dashboard
├── data/
│   ├── day.csv              # Data agregat harian mentah
│   └── hour.csv             # Data per jam mentah
├── notebook.ipynb           # Notebook proses data wrangling, EDA, & visualisasi
├── README.md                # Dokumentasi proyek
├── requirements.txt         # Daftar pustaka yang dibutuhkan
└── url.txt                  # Link publik dashboard di Streamlit Cloud