import streamlit as st
import pandas as pd
import plotly.express as px

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")

# BATASI LEBAR DASHBOARD
st.markdown("""
    <style>
    .block-container {
        max-width: 1100px;
        margin: auto;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# =========================
# WARNA UTAMA
# =========================
ORANGE = '#ff7f0e'

# =========================
# LOAD DATA
# =========================
df = pd.read_csv('df_integrasi.csv')
df_penumpang = pd.read_csv('df_penumpang_grouped.csv')

# =========================
# PREPROCESS
# =========================
df_penumpang['periode_data'] = pd.to_datetime(df_penumpang['periode_data'])
df_penumpang['pertumbuhan'] = df_penumpang['jumlah'].pct_change()

kepadatan = df.groupby('koridor').size().reset_index(name='jumlah_halte')
halte = df.groupby('koridor')['nama_halte'].nunique().reset_index()
rute = df.groupby('koridor')['asal'].nunique().reset_index()

# =========================
# HEADER
# =========================
st.title("Dashboard TransJakarta 🚍")
st.caption("Analisis KPI Transportasi TransJakarta")

# =========================
# KPI CARDS
# =========================
col1, col2, col3 = st.columns(3)

col1.metric("Total Penumpang", f"{int(df_penumpang['jumlah'].sum()):,}")
col2.metric("Rata-rata Penumpang", f"{int(df_penumpang['jumlah'].mean()):,}")
col3.metric("Total Halte", df['nama_halte'].nunique())

st.markdown("---")

# =========================
# ROW 1 (TREND & GROWTH)
# =========================
col1, col2 = st.columns(2)

with col1:
    fig = px.line(
        df_penumpang,
        x='periode_data',
        y='jumlah',
        title='Trend Penumpang',
        markers=True,
        color_discrete_sequence=[ORANGE]
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.line(
        df_penumpang,
        x='periode_data',
        y='pertumbuhan',
        title='Pertumbuhan Penumpang',
        markers=True,
        color_discrete_sequence=[ORANGE]
    )
    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# =========================
# ROW 2 (KPI VARIASI)
# =========================
col1, col2, col3 = st.columns(3)

# Kepadatan Koridor (Horizontal Bar)
with col1:
    fig = px.bar(
        kepadatan,
        x='jumlah_halte',
        y='koridor',
        orientation='h',
        title='Kepadatan Koridor',
        color_discrete_sequence=[ORANGE]
    )
    st.plotly_chart(fig, use_container_width=True)

# Jumlah Halte per Koridor
with col2:
    fig = px.bar(
        halte,
        x='koridor',
        y='nama_halte',
        title='Jumlah Halte per Koridor',
        text='nama_halte',
        color_discrete_sequence=[ORANGE]
    )
    fig.update_traces(textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

# Jumlah Rute per Koridor
with col3:
    fig = px.line(
        rute,
        x='koridor',
        y='asal',
        title='Jumlah Rute per Koridor',
        markers=True,
        color_discrete_sequence=[ORANGE]
    )
    st.plotly_chart(fig, use_container_width=True)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("Dashboard dibuat menggunakan Streamlit & Plotly")