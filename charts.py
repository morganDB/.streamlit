"""
charts.py
Fungsi-fungsi untuk membuat grafik menggunakan Plotly.

Grafik yang digunakan:
- Bar chart
- Line chart
- Pie / donut chart
- Histogram

Tidak menggunakan boxplot dan heatmap agar lebih mudah dipahami saat presentasi.
"""

import pandas as pd
import plotly.express as px

# Pemetaan warna fakultas ITK
FAKULTAS_COLOR_MAP = {
    "Fakultas Rekayasa dan Teknologi Industri": "#EF4444",   # merah
    "Fakultas Pembangunan Berkelanjutan": "#22C55E",        # hijau
    "Fakultas Sains dan Teknologi Informasi": "#3B82F6",    # biru
}


# ==============================
# Grafik untuk halaman Ringkasan
# ==============================

def chart_tren_bulanan_status(df_pinjam: pd.DataFrame):
    """
    Grafik batang bertumpuk jumlah peminjaman per bulan berdasarkan status peminjaman.
    """
    df = df_pinjam.copy()
    if df.empty:
        return None

    df["bulan"] = df["tgl_pinjam"].dt.to_period("M").astype(str)
    per_bulan_status = (
        df.groupby(["bulan", "status_peminjaman"])
          .size()
          .reset_index(name="jumlah")
    )

    fig = px.bar(
        per_bulan_status,
        x="bulan",
        y="jumlah",
        color="status_peminjaman",
        barmode="stack",
        title="Perkembangan peminjaman per bulan berdasarkan status",
    )
    fig.update_layout(
        xaxis_title="Bulan",
        yaxis_title="Jumlah peminjaman",
    )
    return fig


def chart_peminjaman_per_fakultas(df_pinjam: pd.DataFrame):
    """
    Grafik batang jumlah peminjaman per fakultas.
    """
    df = df_pinjam.copy()
    if "nama_fakultas" not in df.columns:
        return None, pd.DataFrame()

    per_fak = (
        df.groupby("nama_fakultas")
          .size()
          .reset_index(name="jumlah")
          .sort_values("jumlah", ascending=False)
    )

    if per_fak.empty:
        return None, per_fak

    fig = px.bar(
        per_fak,
        x="nama_fakultas",
        y="jumlah",
        color="nama_fakultas",
        color_discrete_map=FAKULTAS_COLOR_MAP,
        title="Peminjaman per fakultas",
    )
    fig.update_layout(
        xaxis_title="Fakultas",
        yaxis_title="Jumlah peminjaman",
        showlegend=False,
    )
    return fig, per_fak


def chart_peminjaman_per_kategori(df_pinjam: pd.DataFrame):
    """
    Donut chart peminjaman berdasarkan kategori buku.
    """
    df = df_pinjam.copy()
    if "kategori_buku" not in df.columns:
        return None, pd.DataFrame()

    per_kat = (
        df.groupby("kategori_buku")
          .size()
          .reset_index(name="jumlah")
          .sort_values("jumlah", ascending=False)
    )

    if per_kat.empty:
        return None, per_kat

    fig = px.pie(
        per_kat,
        names="kategori_buku",
        values="jumlah",
        hole=0.4,
        title="Peminjaman per kategori buku",
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig, per_kat


def chart_durasi_rata_per_fakultas(df_pinjam: pd.DataFrame):
    """
    Grafik batang rata-rata durasi peminjaman per fakultas.
    """
    df = df_pinjam.copy()
    df = df[df["durasi_peminjaman"].notna()]

    if df.empty or "nama_fakultas" not in df.columns:
        return None, pd.DataFrame()

    durasi_fak = (
        df.groupby("nama_fakultas")["durasi_peminjaman"]
          .mean()
          .reset_index(name="rata_durasi")
          .sort_values("rata_durasi", ascending=False)
    )

    if durasi_fak.empty:
        return None, durasi_fak

    fig = px.bar(
        durasi_fak,
        x="nama_fakultas",
        y="rata_durasi",
        color="nama_fakultas",
        color_discrete_map=FAKULTAS_COLOR_MAP,
        title="Rata-rata durasi peminjaman per fakultas",
    )
    fig.update_layout(
        xaxis_title="Fakultas",
        yaxis_title="Rata-rata durasi (hari)",
        showlegend=False,
    )
    return fig, durasi_fak


# ==============================
# Grafik untuk halaman Peminjaman
# ==============================

def chart_peminjaman_per_status(df_filtered: pd.DataFrame):
    """
    Grafik batang distribusi jumlah peminjaman per status peminjaman.
    """
    df = df_filtered.copy()
    if "status_peminjaman" not in df.columns:
        return None, pd.DataFrame()

    per_status = (
        df.groupby("status_peminjaman")
          .size()
          .reset_index(name="jumlah")
    )

    if per_status.empty:
        return None, per_status

    fig = px.bar(
        per_status,
        x="status_peminjaman",
        y="jumlah",
        color="status_peminjaman",
        title="Peminjaman per status peminjaman",
    )
    fig.update_layout(
        xaxis_title="Status peminjaman",
        yaxis_title="Jumlah peminjaman",
        showlegend=False,
    )
    return fig, per_status


def chart_top5_judul(df_filtered: pd.DataFrame):
    """
    Grafik batang horizontal untuk lima judul buku dengan frekuensi peminjaman tertinggi.
    """
    df = df_filtered.copy()
    if "judul" not in df.columns:
        return None, pd.DataFrame()

    top_judul = (
        df.groupby("judul")
          .size()
          .reset_index(name="jumlah")
          .sort_values("jumlah", ascending=False)
          .head(5)
    )

    if top_judul.empty:
        return None, top_judul

    fig = px.bar(
        top_judul,
        x="jumlah",
        y="judul",
        orientation="h",
        color="jumlah",
        title="Lima judul buku dengan peminjaman tertinggi",
    )
    fig.update_layout(
        xaxis_title="Jumlah peminjaman",
        yaxis_title="Judul buku",
        showlegend=False,
    )
    fig.update_yaxes(autorange="reversed")
    return fig, top_judul


def chart_hist_durasi(df_filtered: pd.DataFrame):
    """
    Histogram distribusi durasi peminjaman.
    Lebih mudah dijelaskan daripada boxplot.
    """
    df = df_filtered.copy()
    df = df[df["durasi_peminjaman"].notna()]

    if df.empty:
        return None

    fig = px.histogram(
        df,
        x="durasi_peminjaman",
        nbins=10,
        title="Distribusi durasi peminjaman",
    )
    fig.update_layout(
        xaxis_title="Durasi peminjaman (hari)",
        yaxis_title="Jumlah peminjaman",
    )
    return fig


# ==============================
# Grafik untuk halaman Anggota
# ==============================

def chart_anggota_per_status(df_anggota: pd.DataFrame):
    """
    Grafik batang jumlah anggota per status keanggotaan.
    """
    df = df_anggota.copy()
    if "status_anggota" not in df.columns:
        return None

    per_status = (
        df.groupby("status_anggota")
          .size()
          .reset_index(name="jumlah")
    )

    fig = px.bar(
        per_status,
        x="status_anggota",
        y="jumlah",
        color="status_anggota",
        title="Jumlah anggota per status",
    )
    fig.update_layout(
        xaxis_title="Status anggota",
        yaxis_title="Jumlah anggota",
        showlegend=False,
    )
    return fig


def chart_anggota_per_fakultas(df_anggota: pd.DataFrame):
    """
    Grafik batang jumlah anggota per fakultas.
    """
    df = df_anggota.copy()
    if "nama_fakultas" not in df.columns:
        return None

    per_fak = (
        df.groupby("nama_fakultas")
          .size()
          .reset_index(name="jumlah")
          .sort_values("jumlah", ascending=False)
    )

    fig = px.bar(
        per_fak,
        x="nama_fakultas",
        y="jumlah",
        color="nama_fakultas",
        color_discrete_map=FAKULTAS_COLOR_MAP,
        title="Jumlah anggota per fakultas",
    )
    fig.update_layout(
        xaxis_title="Fakultas",
        yaxis_title="Jumlah anggota",
        showlegend=False,
    )
    return fig


# ==============================
# Grafik untuk halaman Buku
# ==============================

def chart_buku_per_kategori(df_buku: pd.DataFrame):
    """
    Grafik batang horizontal jumlah buku per kategori.
    """
    df = df_buku.copy()
    if "kategori_buku" not in df.columns:
        return None

    per_kat = (
        df.groupby("kategori_buku")
          .size()
          .reset_index(name="jumlah")
          .sort_values("jumlah", ascending=False)
    )

    fig = px.bar(
        per_kat,
        x="jumlah",
        y="kategori_buku",
        orientation="h",
        color="kategori_buku",
        title="Jumlah buku per kategori",
    )
    fig.update_layout(
        xaxis_title="Jumlah buku",
        yaxis_title="Kategori buku",
        showlegend=False,
    )
    fig.update_yaxes(autorange="reversed")
    return fig


def chart_buku_per_status(df_buku: pd.DataFrame):
    """
    Donut chart komposisi status koleksi buku (Tersedia, Dipinjam, Hilang, Rusak).
    """
    df = df_buku.copy()
    if "status_buku" not in df.columns:
        return None

    per_status = (
        df.groupby("status_buku")
          .size()
          .reset_index(name="jumlah")
    )

    fig = px.pie(
        per_status,
        names="status_buku",
        values="jumlah",
        hole=0.4,
        title="Komposisi status koleksi buku",
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def chart_buku_per_tahun(df_buku: pd.DataFrame):
    """
    Grafik garis jumlah buku per tahun terbit.
    """
    df = df_buku.copy()
    if "tahun_terbit" not in df.columns:
        return None

    per_tahun = (
        df.groupby("tahun_terbit")
          .size()
          .reset_index(name="jumlah")
          .sort_values("tahun_terbit")
    )

    fig = px.line(
        per_tahun,
        x="tahun_terbit",
        y="jumlah",
        markers=True,
        title="Jumlah buku per tahun terbit",
    )
    fig.update_layout(
        xaxis_title="Tahun terbit",
        yaxis_title="Jumlah buku",
    )
    return fig
