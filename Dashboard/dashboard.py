import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Atur konfigurasi layout halaman
st.set_page_config(page_title="Bike Sharing Dashboard", layout="wide")

# 1. Load data yang sudah bersih
@st.cache_data
def load_data():
    df = pd.read_csv('Dashboard/main_data.csv')
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# 2. Sidebar Filter Rentang Tanggal
min_date = df['dteday'].min().date()
max_date = df['dteday'].max().date()

with st.sidebar:
    st.title("Filter Data")
    date_range = st.date_input(
        label="Pilih Rentang Waktu",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter data berdasarkan input tanggal
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[(df['dteday'].dt.date >= start_date) & (df['dteday'].dt.date <= end_date)]
else:
    filtered_df = df

# 3. Header & Kartu Metrik
st.title("🚲 Bike Sharing Analytics Dashboard")
st.markdown("Analisis performa peminjaman sepeda harian dan pola jam sibuk.")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Peminjaman", value=f"{filtered_df['cnt'].sum():,}")
with col2:
    st.metric("Pengguna Kasual", value=f"{filtered_df['casual'].sum():,}")
with col3:
    st.metric("Pengguna Terdaftar", value=f"{filtered_df['registered'].sum():,}")

st.markdown("---")

# 4. Visualisasi Pertanyaan 1 (Pengaruh Musim & Cuaca)
st.subheader("1. Pengaruh Musim dan Cuaca Terhadap Peminjaman Sepeda")

# Agregasi data harian dari data filtered_df
daily_agg = filtered_df.groupby(['dteday', 'season', 'weathersit'])['cnt'].sum().reset_index()

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(16, 6))

colors_season = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
season_order = daily_agg.groupby('season')['cnt'].mean().sort_values(ascending=False).index
sns.barplot(
    x='season', y='cnt', data=daily_agg, order=season_order,
    palette=colors_season, ax=ax[0], errorbar=None
)
ax[0].set_title('Rata-rata Peminjaman per Musim', fontsize=14, weight='bold')
ax[0].set_xlabel(None)
ax[0].set_ylabel('Rata-rata Unit Harian')

colors_weather = ["#72BCD4", "#D3D3D3", "#D3D3D3"]
weather_order = daily_agg.groupby('weathersit')['cnt'].mean().sort_values(ascending=False).index
sns.barplot(
    x='weathersit', y='cnt', data=daily_agg, order=weather_order,
    palette=colors_weather, ax=ax[1], errorbar=None
)
ax[1].set_title('Rata-rata Peminjaman per Cuaca', fontsize=14, weight='bold')
ax[1].set_xlabel(None)
ax[1].set_ylabel(None)

st.pyplot(fig)

st.markdown("---")

# 5. Visualisasi Pertanyaan 2 (Pola Jam Sibuk)
st.subheader("2. Pola Peminjaman per Jam: Hari Kerja vs Hari Libur")

hourly_trend = filtered_df.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()
hourly_trend['workingday'] = hourly_trend['workingday'].map({1: 'Hari Kerja', 0: 'Hari Libur / Akhir Pekan'})

fig2, ax2 = plt.subplots(figsize=(12, 5))
sns.lineplot(
    data=hourly_trend, x='hr', y='cnt', hue='workingday',
    palette=['#FF6F61', '#1F77B4'], linewidth=2.5, marker='o', ax=ax2
)
ax2.set_title('Rata-rata Peminjaman per Jam', fontsize=14, weight='bold')
ax2.set_xlabel('Jam (00:00 - 23:00)')
ax2.set_ylabel('Rata-rata Unit')
ax2.set_xticks(range(0, 24))
ax2.grid(axis='y', linestyle='--', alpha=0.6)

st.pyplot(fig2)