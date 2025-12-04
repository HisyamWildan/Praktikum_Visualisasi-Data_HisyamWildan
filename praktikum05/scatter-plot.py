# Import Library
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

# dataset utama
suhu = [20, 22, 24, 26, 28, 30, 32, 34, 36]
penjualan = [50, 60, 70, 90, 100, 110, 130, 150, 180]

# dataset tambahan (data penjualan)
penjualan_weekdays = [50, 60, 70, 80, 90, 100, 110, 120, 130]
penjualan_weekend = [60, 70, 80, 100, 110, 120, 140, 160, 200]

# data untuk analisis
data = {
    'Suhu': [20, 22, 24, 26, 28, 30, 32, 34, 36],
    'Penjualan_Coklat': [40, 45, 50, 55, 60, 65, 70, 75, 80],
    'Penjualan_Vanila': [82, 80, 78, 76, 77, 80, 82, 85, 88],
    'Penjualan_Stroberi': [55, 50, 55, 60, 65, 60, 65, 70, 72],
    'Kelembapan': [50, 65, 70, 75, 80, 85, 90, 95, 100]
}

# Konversi ke DataFrame
df = pd.DataFrame(data)

# Layout utama
option = st.sidebar.selectbox(
    "Pilih contoh scatter plot",
    (
        "Basic Scatter Plot",
        "Kustomisasi Scatter Plot",
        "Multi Scatter Plot",
        "Analisis Scatter Plot"
    )
)

# Indentitas Kelompok
st.title("Praktikum 5 - Matplotlib Scatter Plot")
st.markdown("""
Kelompok 14:
1. Fatih Mubasyir (0110222186)
2. Hisyam Wildan Alfath (0110222206) 
3. Dean Pramona (0110222163)
""")

# 1. Basic Scatter Plot
def basic_scatter():
    st.subheader("1. Basic Scatter Plot")
    fig, ax = plt.subplots()
    ax.scatter(suhu, penjualan)
    ax.set_title('Hubungan Penjualan Es Krim dengan Suhu')
    ax.set_xlabel('Suhu')
    ax.set_ylabel('Penjualan Es Krim')
    st.pyplot(fig)

# 2. Kustomisasi Scatter Plot
def custom_scatter():
    st.subheader("2. Kustomisasi Scatter Plot")
    fig, ax = plt.subplots()
    ax.scatter(suhu, penjualan, color='orange', s=100, edgecolors='black', alpha=0.7)
    ax.set_title('Hubungan Penjualan Es Krim dengan Suhu')
    ax.set_xlabel('Suhu')
    ax.set_ylabel('Penjualan Es Krim')
    ax.grid(True)
    st.pyplot(fig)

# 3. Multi Scatter Plot
def multiple_scatter():
    st.subheader("3. Multi Scatter Plot")
    fig, ax = plt.subplots()
    ax.scatter(suhu, penjualan_weekdays, color='green', label='Hari Kerja', s=80)
    ax.scatter(suhu, penjualan_weekend, color='purple', label='Akhir Pekan', s=80)
    ax.set_title('Hubungan Penjualan Es Krim dengan Suhu')
    ax.set_xlabel('Suhu (°C)')
    ax.set_ylabel('Penjualan Es Krim')
    ax.grid(True)
    st.pyplot(fig)

# 4. Analisis Scatter Plot
def scatter_3_variabel():
    st.subheader("4. Analisis Scatter Plot")
    # Opsi jenis eskrim
    jenis_eskrim = st.selectbox("Pilih jenis eskrim", ["Coklat", "Vanila", "Stroberi"])

    # Logika untuk opsi jenis eskrim berdasarkan pilihan
    if jenis_eskrim == "Coklat":
        penjualan = df["Penjualan_Coklat"]
    elif jenis_eskrim == "Vanila":
        penjualan = df["Penjualan_Vanila"]
    else:
        penjualan = df["Penjualan_Stroberi"]

    st.subheader("Data Penjualan dan Suhu")
    st.dataframe(df)

    # Scatter Plot
    fig, ax = plt.subplots()
    scatter = ax.scatter(df["Suhu"], penjualan, c=df["Kelembapan"], s=100, cmap="coolwarm", alpha=0.7)

    # Styling
    ax.set_title(f'Hubungan Penjualan {jenis_eskrim} vs Suhu dan Kelembapan')
    ax.set_xlabel('Suhu (°C)')
    ax.set_ylabel(f'Penjualan Es Krim {jenis_eskrim}')
    fig.colorbar(scatter, label='Kelembapan (%)')

    st.pyplot(fig)

    # Ringkasan hubungan
    st.subheader("Analisis Hubungan")
    st.write(f"Grafik menunjukan hubungan antara suhu, kelembapan, dan penjualan eskrim jenis **{jenis_eskrim}**")
    
# Routing berdasarkan menu sidebar
if option == "Basic Scatter Plot":
    basic_scatter()
elif option == "Kustomisasi Scatter Plot":
    custom_scatter()
elif option == "Multi Scatter Plot":
    multiple_scatter()
elif option == "Analisis Scatter Plot":
    scatter_3_variabel()