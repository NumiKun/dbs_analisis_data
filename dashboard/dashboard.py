import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Membaca data
@st.cache
def load_data():
    df1 = pd.read_csv('path_to_data_1.csv')
    df2 = pd.read_csv('path_to_data_2.csv')
    return df1, df2

# Membaca data
df1, df2 = load_data()

# Menggabungkan data
merged_df = pd.merge(df1, df2, on=['year', 'month', 'day', 'hour', 'station'], suffixes=('_df1', '_df2'), how='outer')

# Melakukan interpolasi dan imputasi
num_cols = ['PM2.5_df1', 'PM10_df1', 'SO2_df1', 'NO2_df1', 'CO_df1', 'O3_df1', 
            'TEMP_df1', 'PRES_df1', 'DEWP_df1', 'RAIN_df1', 'WSPM_df1',
            'PM2.5_df2', 'PM10_df2', 'SO2_df2', 'NO2_df2', 'CO_df2', 'O3_df2', 
            'TEMP_df2', 'PRES_df2', 'DEWP_df2', 'RAIN_df2', 'WSPM_df2']
merged_df[num_cols] = merged_df[num_cols].interpolate(method='linear')

# Menampilkan judul dan deskripsi dashboard
st.title('Dashboard Kualitas Udara')
st.write("""
    Dashboard ini menunjukkan analisis tren polusi udara (PM2.5, PM10) serta korelasi antara faktor cuaca dan kualitas udara.
""")

# 1. Menambahkan Fitur Interaktif - Pemilihan Stasiun
station_selected = st.selectbox("Pilih Stasiun Pemantauan", options=['Tiantan', 'Shunyi'])

# 2. Menambahkan Fitur Interaktif - Pemilihan Polutan
pollutant_selected = st.selectbox("Pilih Polutan", options=['PM2.5', 'PM10'])

# 3. Menambahkan Fitur Interaktif - Slider untuk Rentang Tahun
year_range = st.slider("Pilih Rentang Tahun", 2013, 2017, (2013, 2017))

# Filter Data Berdasarkan Stasiun dan Rentang Tahun
filtered_data = merged_df[(merged_df['station'] == station_selected) & 
                          (merged_df['year'] >= year_range[0]) & 
                          (merged_df['year'] <= year_range[1])]

# 4. Menampilkan Tren Polusi Udara PM2.5 dan PM10 Berdasarkan Pilihan Polutan
st.subheader(f"Tren Polusi Udara ({pollutant_selected}) di Stasiun {station_selected}")
pollutant_column = f"{pollutant_selected}_df1" if station_selected == "Tiantan" else f"{pollutant_selected}_df2"
yearly_pollutant = filtered_data.groupby('year').agg({pollutant_column: 'mean'}).reset_index()

# Plotting tren PM2.5 atau PM10
fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(yearly_pollutant['year'], yearly_pollutant[pollutant_column], label=f'{pollutant_selected} {station_selected}', marker='o', linestyle='-', color='blue')

# Menambahkan elemen visualisasi
ax.set_title(f"Tren Polusi Udara ({pollutant_selected}) di Stasiun {station_selected} ({year_range[0]}-{year_range[1]})", fontsize=16)
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Konsentrasi Polusi (µg/m³)", fontsize=12)
ax.legend()
ax.grid(True)

# Menampilkan grafik
st.pyplot(fig)

# 5. Korelasi antara PM2.5 dan Faktor Cuaca
st.subheader("Korelasi antara PM2.5 dan Variabel Cuaca")
# Menghitung korelasi
correlation = merged_df[['PM2.5_df1', 'TEMP_df1', 'PRES_df1', 'DEWP_df1', 'RAIN_df1', 'WSPM_df1']].corr()

# Visualisasi heatmap korelasi
fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, cbar_kws={'label': 'Korelasi'}, ax=ax)
st.pyplot(fig)

# 6. Menampilkan statistik deskriptif
st.subheader("Statistik Deskriptif")
st.write(filtered_data[['PM2.5_df1', 'PM10_df1', 'PM2.5_df2', 'PM10_df2']].describe())
