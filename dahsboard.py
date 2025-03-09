#INI KODE MILIK MUHAMAD TEGAR WIJAYA 
#MEMULAI MENERJAKAN PADA TANGGAL 7 MARET 20:30 WIB SAMPAI 8 MARET 15:23
#MOHON UNTUK DI CEK TERIMAKASIH

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
df_day = pd.read_csv("day.csv")  
df_hour = pd.read_csv("hour.csv")  
st.header("PERTANYAAN")
st.subheader("1. Pengaruh suhu terhadap penyewaan sepeda")
st.subheader("2. Jumlah sepeda berdasarkan musim")

st.title("Dashboard Analisis Bike Sharing")

# Sidebar untuk filter
st.sidebar.header("Filter Data")

# Filter berdasarkan musim
season_mapping = {1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"}
selected_season = st.sidebar.selectbox("Pilih Musim", options=["Semua"] + list(season_mapping.values()))

# Filter berdasarkan cuaca
weather_mapping = {1: "Cerah", 2: "Mendung", 3: "Hujan Ringan", 4: "Hujan Lebat"}
selected_weather = st.sidebar.selectbox("Pilih Cuaca", options=["Semua"] + list(weather_mapping.values()))

# Filter berdasarkan tanggal
min_date = pd.to_datetime(df_day["dteday"].min()).date()
max_date = pd.to_datetime(df_day["dteday"].max()).date()
selected_date = st.sidebar.date_input("Pilih Rentang Tanggal", [min_date, max_date], min_value=min_date, max_value=max_date)

# Konversi kolom tanggal
df_day["dteday"] = pd.to_datetime(df_day["dteday"])

# Terapkan filter
filtered_df = df_day.copy()
if selected_season != "Semua":
    season_key = list(season_mapping.keys())[list(season_mapping.values()).index(selected_season)]
    filtered_df = filtered_df[filtered_df["season"] == season_key]

if selected_weather != "Semua":
    weather_key = list(weather_mapping.keys())[list(weather_mapping.values()).index(selected_weather)]
    filtered_df = filtered_df[filtered_df["weathersit"] == weather_key]

selected_date = [pd.to_datetime(selected_date[0]), pd.to_datetime(selected_date[1])]
filtered_df = filtered_df[(filtered_df["dteday"] >= selected_date[0]) & (filtered_df["dteday"] <= selected_date[1])]

# Menampilkan data hasil filter dalam tabel
st.subheader("Data Penyewaan Sepeda (Setelah Filter)")
st.dataframe(filtered_df)

# Visualisasi 1: Pengaruh Suhu terhadap Penyewaan Sepeda
st.subheader("Pengaruh Suhu terhadap Penyewaan Sepeda")
fig, ax = plt.subplots(figsize=(10, 5))
sns.scatterplot(x=filtered_df["temp"], y=filtered_df["cnt"], ax=ax)
ax.set_xlabel("Suhu")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Pengaruh Suhu terhadap Penyewaan Sepeda")
st.pyplot(fig)

# Visualisasi 2: Jumlah Penyewaan Sepeda Berdasarkan Musim
st.subheader("Jumlah Penyewaan Sepeda Berdasarkan Musim")
fig, ax = plt.subplots(figsize=(8, 5))
sns.barplot(x=filtered_df["season"], y=filtered_df["cnt"], ax=ax)
ax.set_xlabel("Musim")
ax.set_ylabel("Jumlah Penyewaan")
ax.set_title("Jumlah Penyewaan Sepeda Berdasarkan Musim")
st.pyplot(fig)

# Visualisasi 3: Pola Penyewaan Sepeda per Jam (jika tersedia)
if "hr" in df_hour.columns:
    st.subheader("Pola Penyewaan Sepeda per Jam")
    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(x=df_hour["hr"], y=df_hour["cnt"], ax=ax)
    ax.set_xlabel("Jam")
    ax.set_ylabel("Jumlah Penyewaan")
    ax.set_title("Pola Penyewaan Sepeda sepanjang Hari")
    st.pyplot(fig)

st.write("**Kesimpulan:**")
st.write("- Penyewaan sepeda meningkat seiring kenaikan suhu.")
st.write("- Musim panas (season 3) memiliki jumlah penyewaan tertinggi.")
st.write("- Pola penyewaan tinggi saat jam kerja (pagi & sore).")
