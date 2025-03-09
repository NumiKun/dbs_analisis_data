import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

@st.cache
def load_data():
    df1 = pd.read_csv('data/data_1.csv')
    df2 = pd.read_csv('data/data_2.csv')
    return df1, df2

df1, df2 = load_data()

merged_df = pd.merge(df1, df2, on=['year', 'month', 'day', 'hour', 'station'], suffixes=('_df1', '_df2'), how='outer')

num_cols = ['PM2.5_df1', 'PM10_df1', 'SO2_df1', 'NO2_df1', 'CO_df1', 'O3_df1', 
            'TEMP_df1', 'PRES_df1', 'DEWP_df1', 'RAIN_df1', 'WSPM_df1',
            'PM2.5_df2', 'PM10_df2', 'SO2_df2', 'NO2_df2', 'CO_df2', 'O3_df2', 
            'TEMP_df2', 'PRES_df2', 'DEWP_df2', 'RAIN_df2', 'WSPM_df2']
merged_df[num_cols] = merged_df[num_cols].interpolate(method='linear')

st.title('Dashboard Kualitas Udara')
st.write("""
    Dashboard ini menunjukkan analisis tren polusi udara (PM2.5, PM10) serta statistik deskriptif dari data kualitas udara.
""")

station_selected = st.selectbox("Pilih Stasiun Pemantauan", options=['Tiantan', 'Shunyi'])

pollutant_selected = st.selectbox("Pilih Polutan", options=['PM2.5', 'PM10'])

year_range = st.slider("Pilih Rentang Tahun", 2013, 2017, (2013, 2017))

filtered_data = merged_df[(merged_df['station'] == station_selected) & 
                          (merged_df['year'] >= year_range[0]) & 
                          (merged_df['year'] <= year_range[1])]

st.subheader(f"Tren Polusi Udara ({pollutant_selected}) di Stasiun {station_selected}")
pollutant_column = f"{pollutant_selected}_df1" if station_selected == "Tiantan" else f"{pollutant_selected}_df2"
yearly_pollutant = filtered_data.groupby('year').agg({pollutant_column: 'mean'}).reset_index()

fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(yearly_pollutant['year'], yearly_pollutant[pollutant_column], label=f'{pollutant_selected} {station_selected}', marker='o', linestyle='-', color='blue')

ax.set_title(f"Tren Polusi Udara ({pollutant_selected}) di Stasiun {station_selected} ({year_range[0]}-{year_range[1]})", fontsize=16)
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Konsentrasi Polusi (µg/m³)", fontsize=12)
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.subheader("Statistik Deskriptif")

filtered_data_renamed = filtered_data.rename(columns={
    'PM2.5_df1': 'PM2.5 Tiantan', 
    'PM10_df1': 'PM10 Tiantan', 
    'PM2.5_df2': 'PM2.5 Shunyi', 
    'PM10_df2': 'PM10 Shunyi'
})

st.write(filtered_data_renamed[['PM2.5 Tiantan', 'PM10 Tiantan', 'PM2.5 Shunyi', 'PM10 Shunyi']].describe())

st.subheader(f"Korelasi antara {pollutant_selected} dan Faktor Cuaca di Stasiun {station_selected}")

pollutant_column = f'PM2.5_df1' if station_selected == "Tiantan" else f'PM2.5_df2'
weather_columns = ['TEMP', 'PRES', 'DEWP', 'RAIN', 'WSPM']
weather_columns = [f'{col}_df1' if station_selected == "Tiantan" else f'{col}_df2' for col in weather_columns]

correlation_data = filtered_data[[pollutant_column] + weather_columns].corr()

fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(correlation_data, annot=True, cmap='coolwarm', vmin=-1, vmax=1, ax=ax)
ax.set_title(f'Korelasi antara PM2.5 dan Faktor Cuaca di Stasiun {station_selected}')
st.pyplot(fig)

st.write(correlation_data[pollutant_column].sort_values(ascending=False))
