import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Konfigurasi Halaman
st.set_page_config(
    page_title="Bike Sharing Insights Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Custom CSS untuk mempercantik kartu metrik & container
st.markdown("""
    <style>
    .metric-card {
        background-color: #F8F9FA;
        border-radius: 10px;
        padding: 15px 20px;
        border-left: 5px solid #1E88E5;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .metric-title { font-size: 14px; color: #6C757D; margin-bottom: 5px; font-weight: 500; }
    .metric-value { font-size: 26px; color: #212529; font-weight: 700; }
    </style>
""", unsafe_allow_html=True)

# 1. Load Data dengan path fleksibel
@st.cache_data
def load_data():
    current_dir = os.path.dirname(__file__)
    file_path = os.path.join(current_dir, 'main_data.csv')
    df = pd.read_csv(file_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

df = load_data()

# 2. Sidebar Filter
with st.sidebar:
    st.image("https://images.unsplash.com/photo-1507035895480-2b3156c31fc8?auto=format&fit=crop&w=400&q=80", use_container_width=True)
    st.title("⚙️ Filter Analisis")
    
    min_date = df['dteday'].min().date()
    max_date = df['dteday'].max().date()
    
    date_range = st.date_input(
        label="Rentang Waktu:",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

# Filter Dataset
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = df[(df['dteday'].dt.date >= start_date) & (df['dteday'].dt.date <= end_date)]
else:
    filtered_df = df

# 3. Header Utama
st.title("🚲 Bike Sharing Performance Dashboard")
st.caption("Eksplorasi tren peminjaman sepeda publik, pengaruh kondisi cuaca, serta dinamika komuter harian.")

st.markdown("<br>", unsafe_allow_html=True)

# 4. Ringkasan Kartu Metrik
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-title">Total Peminjaman</div>
        <div class="metric-value">{filtered_df['cnt'].sum():,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #43A047;">
        <div class="metric-title">Pengguna Member (Registered)</div>
        <div class="metric-value">{filtered_df['registered'].sum():,}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #FB8C00;">
        <div class="metric-title">Pengguna Kasual (Casual)</div>
        <div class="metric-value">{filtered_df['casual'].sum():,}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    daily_avg = int(filtered_df.groupby('dteday')['cnt'].sum().mean()) if not filtered_df.empty else 0
    st.markdown(f"""
    <div class="metric-card" style="border-left-color: #8E24AA;">
        <div class="metric-title">Rata-rata Peminjaman/Hari</div>
        <div class="metric-value">{daily_avg:,}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. Navigasi Tab Analisis
tab1, tab2 = st.tabs(["🌦️ Pengaruh Faktor Lingkungan", "⏰ Pola Jam Sibuk & Hari Kerja"])

with tab1:
    st.subheader("Pengaruh Musim dan Kondisi Cuaca")
    st.info("Visualisasi ini membandingkan rata-rata unit harian yang dipinjam berdasarkan musim dan tingkat keparahan cuaca.")
    
    daily_agg = filtered_df.groupby(['dteday', 'season', 'weathersit'])['cnt'].sum().reset_index()
    
    col_plot1, col_plot2 = st.columns(2)
    
    with col_plot1:
        fig1, ax1 = plt.subplots(figsize=(7, 4.5))
        season_order = daily_agg.groupby('season')['cnt'].mean().sort_values(ascending=False).index
        
        # Palet biru kontras (dari navy pekat sampai biru medium, tidak ada warna pucat)
        colors_season = ["#0D47A1", "#1976D2", "#2196F3", "#64B5F6"]
        
        sns.barplot(
            x='season', y='cnt', data=daily_agg, order=season_order,
            palette=colors_season, ax=ax1, errorbar=None
        )
        ax1.set_title("Rata-rata Peminjaman per Musim", fontsize=12, weight='bold', pad=12)
        ax1.set_xlabel(None)
        ax1.set_ylabel("Unit Peminjaman Harian")
        sns.despine(top=True, right=True)
        st.pyplot(fig1)

    with col_plot2:
        fig2, ax2 = plt.subplots(figsize=(7, 4.5))
        weather_order = daily_agg.groupby('weathersit')['cnt'].mean().sort_values(ascending=False).index
        
        # Palet hijau tegas (4 variasi warna kontras untuk 4 kondisi cuaca)
        colors_weather = ["#1B5E20", "#2E7D32", "#388E3C", "#66BB6A"]
        
        sns.barplot(
            x='weathersit', y='cnt', data=daily_agg, order=weather_order,
            palette=colors_weather, ax=ax2, errorbar=None
        )
        ax2.set_title("Rata-rata Peminjaman per Kondisi Cuaca", fontsize=12, weight='bold', pad=12)
        ax2.set_xlabel(None)
        ax2.set_ylabel(None)
        sns.despine(top=True, right=True)
        st.pyplot(fig2)

with tab2:
    st.subheader("Dinamika Peminjaman Jam Sibuk (Hari Kerja vs Hari Libur)")
    st.info("Pola mobilitas komuter menunjukkan 2 puncak aktivitas (rush hour) saat hari kerja dibandingkan pola stabil saat hari libur.")
    
    hourly_trend = filtered_df.groupby(['hr', 'workingday'])['cnt'].mean().reset_index()
    hourly_trend['workingday'] = hourly_trend['workingday'].map({1: 'Hari Kerja (Workingday)', 0: 'Hari Libur / Weekend'})
    
    fig3, ax3 = plt.subplots(figsize=(12, 4.5))
    sns.lineplot(
        data=hourly_trend, x='hr', y='cnt', hue='workingday',
        palette=['#E53935', '#1E88E5'], linewidth=2.5, marker='o', ax=ax3
    )
    ax3.set_title("Rata-rata Volume Sepeda per Jam", fontsize=12, weight='bold', pad=12)
    ax3.set_xlabel("Jam (00:00 - 23:00)")
    ax3.set_ylabel("Rata-rata Unit")
    ax3.set_xticks(range(0, 24))
    ax3.grid(axis='y', linestyle='--', alpha=0.5)
    sns.despine(top=True, right=True)
    ax3.legend(title=None, frameon=True)
    
    st.pyplot(fig3)