import streamlit as st
import pandas as pd
import numpy as np
from streamlit_autorefresh import st_autorefresh
import plotly.graph_objects as go
import plotly.express as px

# Konfigurasi halaman
st.set_page_config(page_title="Dashboard Otomatis", layout="wide")

# Ganti dengan URL direct image
st.markdown("""
    <style>
    .stApp {
        background-image: url("https://i.imgur.com/6Nwgd41.jpeg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
        color: white;
    }

    h1 {
        text-shadow: 0 0 8px #0ff;
    }

    .block-container {
        padding-top: 2rem;
        background-color: rgba(0, 0, 0, 0.6);
        border-radius: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Auto-refresh tiap 3 detik
st_autorefresh(interval=3000, limit=None, key="refresh")

# Judul
st.markdown("<h1 style='text-align: center; color: #4CAF50;'>📊 Dashboard Penjualan Real-Time</h1>", unsafe_allow_html=True)
st.markdown("---")

# Data dummy
labels = ['Produk A', 'Produk B', 'Produk C', 'Produk D', 'Produk E']
data = pd.DataFrame({
    'Produk': labels,
    'Jumlah': np.random.randint(50, 150, size=5)
})

# 🔽 Dropdown filter
selected_produk = st.selectbox("Pilih Produk:", ["Semua Produk"] + labels)

# Filter data sesuai pilihan
if selected_produk != "Semua Produk":
    filtered_data = data[data['Produk'] == selected_produk]
else:
    filtered_data = data

# Layout: 3 kolom untuk 3 grafik
col1, col2, col3 = st.columns(3)

# Grafik Bar
with col1:
    st.subheader("Grafik Batang")
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(
        x=filtered_data['Produk'],
        y=filtered_data['Jumlah'],
        marker_color='cyan',
        text=filtered_data['Jumlah'],
        textposition='outside'
    ))
    fig_bar.update_traces(
    hoverinfo='x+y',
    hovertemplate='<b>%{x}</b><br>Jumlah: %{y}',
    marker_line_color='white',
    marker_line_width=1.5
)

    fig_bar.update_layout(
        transition_duration=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        yaxis=dict(showgrid=False),
        title="Jumlah Penjualan Tiap Produk"
    )
    st.plotly_chart(fig_bar, use_container_width=True, key="bar_chart")

# Grafik Pie
with col2:
    st.subheader("Diagram Pie")
    fig_pie = px.pie(
        filtered_data, names='Produk', values='Jumlah', title="Distribusi Penjualan",
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    fig_pie.update_traces(
    hovertemplate='<b>%{label}</b><br>Jumlah: %{value}<extra></extra>',
    textinfo='label+percent',
    pull=[0.05 if i == filtered_data['Jumlah'].idxmax() else 0 for i in filtered_data.index]
)

    fig_pie.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig_pie, use_container_width=True, key="pie_chart")

# Grafik Line
with col3:
    st.subheader("Tren Penjualan (Simulasi)")
    trend_data = pd.DataFrame({
        'Waktu': pd.date_range(start='2025-04-23', periods=5, freq='H'),
        'Jumlah': np.sort(np.random.randint(50, 150, size=5)),
        'Produk': 'Produk A'
    })
    fig_line = px.line(
        trend_data, x='Waktu', y='Jumlah', markers=True,
        title=None, color_discrete_sequence=['#4CAF50'], height=350
    )
    fig_line.update_traces(
    hovertemplate='<b>%{x}</b><br>Jumlah: %{y}',
    line=dict(width=3),
    marker=dict(size=8, color='#00ffaa', line=dict(width=2, color='white'))
)

    fig_line.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white'
    )
    st.plotly_chart(fig_line, use_container_width=True, key="line_chart")

# Footer
st.markdown("---")
st.markdown("<p style='text-align:center;'>📈 Update otomatis tiap 3 detik</p>", unsafe_allow_html=True)
