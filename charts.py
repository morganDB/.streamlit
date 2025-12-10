"""
charts.py
Modul berisi fungsi-fungsi pembuat grafik menggunakan Plotly.
Setiap fungsi menerima DataFrame dan mengembalikan objek figure.
"""

import plotly.express as px
import pandas as pd

# =====================================================================
# PALET WARNA & FUNGSI BANTU LAYOUT
# =====================================================================

# Warna brand gelap (dipakai sedikit untuk aksen)
BRAND_DARK = ["#2A004E", "#500073", "#C62300", "#F14A00"]

# Versi lebih terang / kontras supaya kelihatan di background gelap
BRAND_BRIGHT = [
    "#C4B5FD",  # ungu muda
    "#8B5CF6",  # ungu terang
    "#FB923C",  # oranye muda
    "#F97316",  # oranye terang
]

# Gradien ungu → oranye buat continuous color (misal pakai "jumlah")
BRAND_GRADIENT = ["#C4B5FD", "#8B5CF6", "#FB923C", "#F97316"]


def apply_common_layout(fig, title: str | None = None):
    """
    Terapkan layout standar supaya semua grafik konsisten
    dengan tema ungu-oranye dan background gelap.
    """
    if title:
        fig.update_layout(title=title)

    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",   # transparan, ikut tema Streamlit
        paper_bgcolor="rgba(0,0,0,0)",
        font_color="#F9FAFB",           # teks putih lembut
        title_font=dict(size=18, color="#F9FAFB"),
        legend=dict(
            bgcolor="rgba(15,23,42,0.85)",
            bordercolor="rgba(148,163,184,0.4)",
            borderwidth=1,
            font=dict(color="#E5E7EB"),
        ),
        xaxis=dict(
            gridcolor="rgba(148,163,184,0.18)",
            zerolinecolor="rgba(148,163,184,0.35)",
            linecolor="rgba(148,163,184,0.45)",
            tickfont=dict(color="#E5E7EB"),
            title_font=dict(color="#F9FAFB"),
        ),
        yaxis=dict(
            gridcolor="rgba(148,163,184,0.18)",
            zerolinecolor="rgba(148,163,184,0.35)",
            linecolor="rgba(148,163,184,0.45)",
            tickfont=dict(color="#E5E7EB"),
            title_font=dict(color="#F9FAFB"),
        ),
        margin=dict(t=60, r=20, b=60, l=70),
    )
    return fig


# =====================================================================
# GRAFIK UNTUK HALAMAN RINGKASAN / PEMINJAMAN
# =====================================================================

def chart_tren_bulanan_status(df_pinjam: pd.DataFrame):
    """
    Grafik batang bertumpuk (stacked bar) jumlah peminjaman per bulan
    berdasarkan status peminjaman (Sedang dipinjam / Selesai / dll).
    """
    df = df_pinjam.copy()
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
        color_discrete_sequence=BRAND_BRIGHT,
        labels=dict(bulan="Bulan", jumlah="Jumlah peminjaman",
                    status_peminjaman="Status peminjaman"),
    )
    apply_common_layout(
        fig, "Perkembangan peminjaman per bulan berdasarkan status"
    )
    return fig


def chart_peminjaman_per_fakultas(df_pinjam: pd.DataFrame):
    """
    Grafik batang jumlah peminjaman per fakultas.
    Mengembalikan fig dan data agregat per_fak untuk insight tambahan.
    """
    per_fak = (
        df_pinjam
        .groupby("nama_fakultas")
        .size()
        .reset_index(name="jumlah")
        .sort_values("jumlah", ascending=False)
    )

    fig = px.bar(
        per_fak,
        x="nama_fakultas",
        y="jumlah",
        color="nama_fakultas",
        color_discrete_sequence=BRAND_BRIGHT,
        labels=dict(nama_fakultas="Fakultas", jumlah="Jumlah peminjaman"),
    )
    apply_common_layout(fig, "Peminjaman per fakultas")
    fig.update_xaxes(tickangle=-20)
    return fig, per_fak


def chart_peminjaman_per_kategori(df_pinjam: pd.DataFrame):
    """
    Donut chart peminjaman berdasarkan kategori buku.
    """
    per_kat = (
        df_pinjam
        .groupby("kategori_buku")
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
        hole=0.55,
        color="kategori_buku",
        color_discrete_sequence=BRAND_BRIGHT,
    )
    apply_common_layout(fig, "Peminjaman per kategori buku")
    fig.update_traces(
        textinfo="percent+label",
        textposition="inside",
        textfont=dict(color="#0F172A", size=12),
    )
    return fig, per_kat


def chart_durasi_rata_per_fakultas(df_pinjam: pd.DataFrame):
    """
    Grafik batang rata-rata durasi peminjaman per fakultas.
    """
    df = df_pinjam.copy()
    df = df[df["durasi_peminjaman"].notna()]

    if df.empty:
        return None, df

    durasi_fak = (
        df.groupby("nama_fakultas")["durasi_peminjaman"]
        .mean()
        .reset_index(name="rata_durasi")
        .sort_values("rata_durasi", ascending=False)
    )

    fig = px.bar(
        durasi_fak,
        x="nama_fakultas",
        y="rata_durasi",
        color="nama_fakultas",
        color_discrete_sequence=BRAND_BRIGHT,
        labels=dict(
            nama_fakultas="Fakultas",
            rata_durasi="Rata-rata durasi (hari)",
        ),
    )
    apply_common_layout(fig, "Rata-rata durasi peminjaman per fakultas")
    fig.update_xaxes(tickangle=-20)
    return fig, durasi_fak


def chart_hist_durasi(df_pinjam: pd.DataFrame):
    """
    Histogram sederhana untuk distribusi durasi peminjaman.
    Mudah dibaca: sumbu X = hari, sumbu Y = jumlah transaksi.
    """
    df = df_pinjam.copy()
    df = df[df["durasi_peminjaman"].notna()]

    if df.empty:
        return None

    fig = px.histogram(
        df,
        x="durasi_peminjaman",
        nbins=10,
        color_discrete_sequence=[BRAND_BRIGHT[2]],
        labels=dict(durasi_peminjaman="Durasi peminjaman (hari)"),
    )
    apply_common_layout(fig, "Distribusi durasi peminjaman")
    fig.update_yaxes(title_text="Jumlah peminjaman")
    return fig


def chart_peminjaman_per_status(df_filtered: pd.DataFrame):
    """
    Grafik batang jumlah peminjaman per status (Dipinjam, Selesai, Hilang, Rusak, dst.).
    """
    per_status = (
        df_filtered
        .groupby("status_peminjaman")
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
        color_discrete_sequence=BRAND_BRIGHT,
        labels=dict(
            status_peminjaman="Status peminjaman",
            jumlah="Jumlah peminjaman",
        ),
    )
    apply_common_layout(fig, "Peminjaman per status peminjaman")
    return fig, per_status


def chart_top5_judul(df_filtered: pd.DataFrame):
    """
    Grafik batang horizontal untuk lima judul buku
    dengan frekuensi peminjaman tertinggi.
    """
    top_judul = (
        df_filtered.groupby("judul")
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
        color_continuous_scale=BRAND_GRADIENT,
        labels=dict(jumlah="Jumlah peminjaman", judul="Judul buku"),
    )
    apply_common_layout(fig, "Lima judul buku dengan peminjaman tertinggi")
    # Supaya judul paling banyak di atas
    fig.update_layout(coloraxis_showscale=False)
    fig.update_yaxes(autorange="reversed")
    return fig, top_judul


# =====================================================================
# GRAFIK UNTUK HALAMAN ANGGOTA
# =====================================================================

def chart_anggota_per_status(df_anggota_view: pd.DataFrame):
    """
    Grafik batang jumlah anggota per status keanggotaan.
    """
    per_status = (
        df_anggota_view
        .groupby("status_anggota")
        .size()
        .reset_index(name="jumlah")
    )

    fig = px.bar(
        per_status,
        x="status_anggota",
        y="jumlah",
        color="status_anggota",
        color_discrete_sequence=BRAND_BRIGHT,
        labels=dict(status_anggota="Status anggota", jumlah="Jumlah anggota"),
    )
    apply_common_layout(fig, "Jumlah anggota per status")
    return fig


def chart_anggota_per_fakultas(df_anggota_view: pd.DataFrame):
    """
    Grafik batang jumlah anggota per fakultas.
    (lebih mudah dibaca dibanding treemap).
    """
    per_fak = (
        df_anggota_view
        .groupby("nama_fakultas")
        .size()
        .reset_index(name="jumlah")
        .sort_values("jumlah", ascending=False)
    )

    fig = px.bar(
        per_fak,
        x="nama_fakultas",
        y="jumlah",
        color="nama_fakultas",
        color_discrete_sequence=BRAND_BRIGHT,
        labels=dict(nama_fakultas="Fakultas", jumlah="Jumlah anggota"),
    )
    apply_common_layout(fig, "Jumlah anggota per fakultas")
    fig.update_xaxes(tickangle=-20)
    return fig


# =====================================================================
# GRAFIK UNTUK HALAMAN BUKU
# =====================================================================

def chart_buku_per_kategori(df_buku_view: pd.DataFrame):
    """
    Grafik batang horizontal jumlah judul per kategori buku.
    """
    per_kat = (
        df_buku_view
        .groupby("kategori_buku")
        .size()
        .reset_index(name="jumlah")
        .sort_values("jumlah", ascending=True)
    )

    fig = px.bar(
        per_kat,
        x="jumlah",
        y="kategori_buku",
        orientation="h",
        color="kategori_buku",
        color_discrete_sequence=BRAND_BRIGHT,
        labels=dict(kategori_buku="Kategori buku", jumlah="Jumlah judul"),
    )
    apply_common_layout(fig, "Jumlah buku per kategori")
    fig.update_yaxes(autorange="reversed")
    return fig


def chart_buku_per_tahun(df_buku_view: pd.DataFrame):
    """
    Grafik garis jumlah buku per tahun terbit.
    """
    per_tahun = (
        df_buku_view
        .groupby("tahun_terbit")
        .size()
        .reset_index(name="jumlah")
        .sort_values("tahun_terbit")
    )

    fig = px.line(
        per_tahun,
        x="tahun_terbit",
        y="jumlah",
        markers=True,
        color_discrete_sequence=[BRAND_BRIGHT[1]],
        labels=dict(tahun_terbit="Tahun terbit", jumlah="Jumlah judul"),
    )
    apply_common_layout(fig, "Jumlah buku per tahun terbit")
    return fig

def chart_buku_per_status(df_buku_view: pd.DataFrame):
    """
    Grafik batang jumlah buku per status (Tersedia, Dipinjam, Hilang, Rusak).
    Kolom status bisa bernama 'status_buku' atau 'status', fungsi ini
    otomatis menyesuaikan.
    """
    # Deteksi nama kolom status di DataFrame
    if "status_buku" in df_buku_view.columns:
        status_col = "status_buku"
    elif "status" in df_buku_view.columns:
        status_col = "status"
    else:
        # Kalau tidak ada kolom status sama sekali, kembalikan None
        return None

    per_status = (
        df_buku_view
        .groupby(status_col)
        .size()
        .reset_index(name="jumlah")
        .sort_values("jumlah", ascending=False)
    )

    fig = px.bar(
        per_status,
        x=status_col,
        y="jumlah",
        color=status_col,
        color_discrete_sequence=BRAND_BRIGHT,
        labels={
            status_col: "Status buku",
            "jumlah": "Jumlah buku"
        },
    )
    apply_common_layout(fig, "Jumlah buku per status")
    fig.update_xaxes(title_text="Status buku")
    fig.update_yaxes(title_text="Jumlah buku")
    return fig
