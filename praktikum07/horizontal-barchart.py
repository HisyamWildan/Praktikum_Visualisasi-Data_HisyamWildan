import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Judul
st.title("Praktikum 7 Visualisasi Data")
st.subheader("Horizontal Bar Chart & Stacked Horizontal Bar Chart")

# Indentitas Kelompok
st.markdown("""
Kelompok 14:
1. Fatih Mubasyir (0110222186)
2. Hisyam Wildan Alfath (0110222206) 
3. Dean Pramona (0110222163)
""")

# Dataset
brands = ["Brand A", "Brand B", "Brand C", "Brand D"]
sales_2023 = [350, 420, 300, 200]
sales_2024 = [300, 450, 320, 300]

# Atur posisi Y
y = np.arange(len(brands))
bar_width = 0.4

kategori = st.selectbox(
    "Pilih Kategori Visualisasi",
    ['Basic Chart', 'Kustomisasi Chart', 'Multiple Chart']
)

# Basic bar chart
if kategori == 'Basic Chart':
    st.subheader("Horizontal Bar Chart Sederhana")
    fig1, ax1 = plt.subplots() # Canvas dan axis grafik

    # Grafik batang horizontal
    ax1.set_yticks(y)
    ax1.set_yticklabels(brands)
    ax1.set_title('Horizontal Bar Chart - 2023')
    ax1.set_xlabel('Jumlah Penjualan')
    ax1.set_ylabel('Merk')
    ax1.barh(y, sales_2023, color='skyblue')
    st.pyplot(fig1)

    # Stacked
    st.subheader("Stacked Horizontal Bar Chart Sederhana")
    fig2, ax2, = plt.subplots() # Canvas dan axis grafik

    # Grafik batang horizontal
    ax2.set_yticks(y)
    ax2.set_yticklabels(brands)
    ax2.set_title('StackedHorizontal Bar Chart - 2023')
    ax2.set_xlabel('Jumlah Penjualan')
    ax2.set_ylabel('Merk')
    ax2.barh(y, sales_2023, color='skyblue', label='2023')
    ax2.barh(y, sales_2024, left=sales_2023, color='lightgreen', label='2024')
    ax2.legend()
    st.pyplot(fig2)

# Kustomisasi bar chart
elif kategori == 'Kustomisasi Chart':
    st.subheader("Kustomisasi Horizontal Bar Chart")
    fig3, ax3 = plt.subplots() # Canvas dan axis grafik

    # Grafik batang horizontal
    ax3.set_yticks(y)
    ax3.set_yticklabels(brands)
    ax3.set_title('Kustom Horizontal Bar Chart - 2023')
    ax3.set_xlabel('Jumlah Penjualan')
    ax3.set_ylabel('Merk')
    ax3.barh(y, sales_2023, color='lightblue', edgecolor='black')
    ax3.grid(axis='x', linestyle='--', alpha=0.6)

    # Label nilai
    for i, v in enumerate(sales_2023):
        ax3.text(v + 5, i, str(v), va='center')

    st.pyplot(fig3)

    # Stacked
    st.subheader("Kustomisasi Stacked Horizontal Bar Chart")
    fig4, ax4, = plt.subplots() # Canvas dan axis grafik

    # Grafik batang horizontal
    ax4.set_yticks(y)
    ax4.set_yticklabels(brands)
    ax4.set_title('Kustomisasi Stacked Horizontal Bar Chart - 2023')
    ax4.set_xlabel('Jumlah Penjualan')
    ax4.set_ylabel('Merk')
    ax4.barh(y, sales_2023, color='skyblue', edgecolor='black', label='2023')
    ax4.barh(y, sales_2024, left=sales_2023, color='salmon', edgecolor='black', label='2024')
    ax4.grid(axis='x', linestyle='--', alpha=0.6)
    st.pyplot(fig4)

# Multiple bar chart
elif kategori == 'Multiple Chart':
    st.subheader("Multiple Horizontal Bar Chart")
    fig5, ax5, = plt.subplots() # Canvas dan axis grafik

    # Grafik batang horizontal
    ax5.set_yticks(y)
    ax5.set_yticklabels(brands)
    ax5.set_title('Multiple Horizontal Bar Chart - 2023')
    ax5.set_xlabel('Jumlah Penjualan')
    ax5.set_ylabel('Merk')
    ax5.barh(y - bar_width/2, sales_2023, height=bar_width, label='2023')
    ax5.barh(y + bar_width/2, sales_2024, height=bar_width, label='2024')
    ax5.grid(axis='x', linestyle='--', alpha=0.6)
    ax5.legend()
    st.pyplot(fig5)

    # Stacked
    st.subheader("Multiple Stacked Horizontal Bar Chart")
    fig6, ax6, = plt.subplots() # Canvas dan axis grafik

    # Grafik batang horizontal
    ax6.set_yticks(y)
    ax6.set_yticklabels(brands)
    ax6.set_title('Multiple Stacked Horizontal Bar Chart - 2023')
    ax6.set_xlabel('Jumlah Penjualan')
    ax6.set_ylabel('Merk')
    ax6.barh(y, sales_2023, label='2023')
    ax6.barh(y, sales_2024, left=sales_2023, label='2024')
    ax6.grid(axis='x', linestyle='--', alpha=0.6)
    ax6.legend()
    st.pyplot(fig6)