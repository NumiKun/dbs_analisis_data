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
    Dashboard ini menunjukkan analisis tren polusi udara (PM2.5, PM10) serta korelasi antara faktor cuaca dan kualitas udara.
""")

st.subheader("Tren Polusi Udara (PM2.5 dan PM10) di Stasiun Tiantan dan Shunyi")
tiantan_data = merged_df[merged_df['station'] == 'Tiantan']
shunyi_data = merged_df[merged_df['station'] == 'Shunyi']

tiantan_yearly = tiantan_data.groupby('year').agg({'PM2.5_df1': 'mean', 'PM10_df1': 'mean'}).reset_index()
shunyi_yearly = shunyi_data.groupby('year').agg({'PM2.5_df2': 'mean', 'PM10_df2': 'mean'}).reset_index()

fig, ax = plt.subplots(figsize=(14, 7))
ax.plot(tiantan_yearly['year'], tiantan_yearly['PM2.5_df1'], label='PM2.5 Tiantan', marker='o', linestyle='-', color='blue')
ax.plot(tiantan_yearly['year'], tiantan_yearly['PM10_df1'], label='PM10 Tiantan', marker='s', linestyle='--', color='red')
ax.plot(shunyi_yearly['year'], shunyi_yearly['PM2.5_df2'], label='PM2.5 Shunyi', marker='o', linestyle='-', color='green')
ax.plot(shunyi_yearly['year'], shunyi_yearly['PM10_df2'], label='PM10 Shunyi', marker='s', linestyle='--', color='orange')

ax.set_title("Tren Polusi Udara (PM2.5 dan PM10) di Stasiun Tiantan dan Shunyi (2013-2017)", fontsize=16)
ax.set_xlabel("Tahun", fontsize=12)
ax.set_ylabel("Konsentrasi Polusi (µg/m³)", fontsize=12)
ax.legend()
ax.grid(True)

st.pyplot(fig)

st.subheader("Korelasi antara PM2.5 dan Variabel Cuaca")
correlation = merged_df[['PM2.5_df1', 'TEMP_df1', 'PRES_df1', 'DEWP_df1', 'RAIN_df1', 'WSPM_df1']].corr()

fig, ax = plt.subplots(figsize=(10, 8))
sns.heatmap(correlation, annot=True, cmap='coolwarm', center=0, cbar_kws={'label': 'Korelasi'}, ax=ax)
st.pyplot(fig)

st.subheader("Statistik Deskriptif")
st.write(merged_df[['PM2.5_df1', 'PM10_df1', 'PM2.5_df2', 'PM10_df2']].describe())
