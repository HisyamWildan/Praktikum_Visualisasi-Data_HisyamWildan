import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bank Marketing Dashboard", layout="wide")

# =========================
# Sitasi dataset (wajib)
# =========================
DATASET_CITATION = (
    "Moro, S., Laureano, R., & Cortez, P. (2011). Using Data Mining for Bank Direct Marketing: "
    "An Application of the CRISP-DM Methodology. In Proceedings of the European Simulation and "
    "Modelling Conference (ESM'2011), pp. 117–121."
)

MONTH_ORDER = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]

@st.cache_data
def load_csv_semicolon(path: str) -> pd.DataFrame:
    # bank-full.csv biasanya pakai delimiter ;
    return pd.read_csv(path, sep=",")

def preprocess(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # pastikan tipe data numerik
    numeric_cols = ["age","balance","day","duration","campaign","pdays","previous"]
    for c in numeric_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # rapihin target y
    if "y" in df.columns:
        df["y"] = df["y"].astype(str).str.lower()

    # month jadi kategori berurutan
    if "month" in df.columns:
        df["month"] = df["month"].astype(str).str.lower()
        df["month"] = pd.Categorical(df["month"], categories=MONTH_ORDER, ordered=True)

    return df

def pct_yes(series_y: pd.Series) -> float:
    if len(series_y) == 0:
        return 0.0
    return float((series_y.astype(str).str.lower() == "yes").mean() * 100)

def insight_top(series: pd.Series, label: str) -> str:
    vc = series.value_counts(dropna=False)
    if len(vc) == 0:
        return f"Tidak ada data untuk {label}."
    top_k = str(vc.index[0])
    top_v = int(vc.iloc[0])
    pct = (vc.iloc[0] / vc.sum()) * 100 if vc.sum() else 0
    return f"Mayoritas **{label}** adalah **{top_k}** sebanyak **{top_v}** data (± **{pct:.1f}%**)."

def donut(series: pd.Series, title: str):
    counts = series.value_counts(dropna=False)
    fig, ax = plt.subplots()
    ax.pie(counts.values, labels=counts.index.astype(str), autopct="%1.1f%%", startangle=90)
    centre = plt.Circle((0, 0), 0.60, fc="white")
    fig.gca().add_artist(centre)
    ax.set_title(title)
    ax.axis("equal")
    return fig

# =========================
# Header
# =========================
st.title("📞 Dashboard Bank Marketing (Direct Marketing Campaign)")
st.caption(
    "Dashboard interaktif untuk eksplorasi data kampanye telepon bank dan analisis peluang nasabah berlangganan deposito (target: y)."
)

with st.expander("📌 Sitasi Dataset (wajib dicantumkan)"):
    st.write(DATASET_CITATION)

# =========================
# Load Data
# =========================
st.sidebar.header("📂 Sumber Data")

default_path = "bank-full.csv"
path = st.sidebar.text_input("Path file CSV", value=default_path)

try:
    df_raw = load_csv_semicolon(path)
except Exception as e:
    st.error(
        f"Gagal membaca file: {e}\n\n"
        "Pastikan file ada di folder yang sama dengan app.py, misalnya: bank-full.csv"
    )
    st.stop()

df = preprocess(df_raw)

# =========================
# Data Cleaning (ringan)
# =========================
# Hapus baris yang targetnya kosong (kalau ada)
if "y" in df.columns:
    df = df.dropna(subset=["y"])

# =========================
# Sidebar Filters (Interaktif)
# =========================
st.sidebar.header("🔎 Filter Interaktif")

def multiselect(col_name: str, label: str):
    if col_name not in df.columns:
        return None
    opts = sorted(df[col_name].dropna().astype(str).unique().tolist())
    return st.sidebar.multiselect(label, options=opts, default=[])

y_filter = st.sidebar.selectbox("Filter Target (y)", options=["all"] + (sorted(df["y"].unique().tolist()) if "y" in df.columns else []))

job_filter = multiselect("job", "Job")
marital_filter = multiselect("marital", "Marital")
edu_filter = multiselect("education", "Education")
contact_filter = multiselect("contact", "Contact")
poutcome_filter = multiselect("poutcome", "Poutcome")
month_filter = multiselect("month", "Month")

def range_slider(col: str, label: str):
    if col not in df.columns:
        return None
    s = df[col].dropna()
    if len(s) == 0:
        return None
    mn, mx = float(s.min()), float(s.max())
    return st.sidebar.slider(label, mn, mx, (mn, mx))

age_range = range_slider("age", "Rentang Age")
balance_range = range_slider("balance", "Rentang Balance (€)")
duration_range = range_slider("duration", "Rentang Duration (detik)")

# apply filters
f = df.copy()

if "y" in f.columns and y_filter != "all":
    f = f[f["y"] == y_filter]

if job_filter and "job" in f.columns:
    f = f[f["job"].astype(str).isin(job_filter)]

if marital_filter and "marital" in f.columns:
    f = f[f["marital"].astype(str).isin(marital_filter)]

if edu_filter and "education" in f.columns:
    f = f[f["education"].astype(str).isin(edu_filter)]

if contact_filter and "contact" in f.columns:
    f = f[f["contact"].astype(str).isin(contact_filter)]

if poutcome_filter and "poutcome" in f.columns:
    f = f[f["poutcome"].astype(str).isin(poutcome_filter)]

if month_filter and "month" in f.columns:
    f = f[f["month"].astype(str).isin(month_filter)]

if age_range and "age" in f.columns:
    f = f[(f["age"] >= age_range[0]) & (f["age"] <= age_range[1])]

if balance_range and "balance" in f.columns:
    f = f[(f["balance"] >= balance_range[0]) & (f["balance"] <= balance_range[1])]

if duration_range and "duration" in f.columns:
    f = f[(f["duration"] >= duration_range[0]) & (f["duration"] <= duration_range[1])]

# =========================
# KPI (Ringkasan)
# =========================
st.subheader("📌 Ringkasan (Setelah Filter)")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Jumlah data", f"{len(f):,}")

if "y" in f.columns:
    c2.metric("Subscription Rate (y=yes)", f"{pct_yes(f['y']):.2f}%")
else:
    c2.metric("Subscription Rate (y=yes)", "N/A")

if "duration" in f.columns and len(f):
    c3.metric("Rata-rata duration (detik)", f"{f['duration'].mean():.1f}")
else:
    c3.metric("Rata-rata duration (detik)", "N/A")

if "campaign" in f.columns and len(f):
    c4.metric("Rata-rata campaign (kontak)", f"{f['campaign'].mean():.2f}")
else:
    c4.metric("Rata-rata campaign (kontak)", "N/A")

with st.expander("🔍 Preview Data (Top 50)"):
    st.dataframe(f.head(50), use_container_width=True)

st.markdown("---")
st.subheader("📊 Visualisasi (Minimal 5 Jenis)")

# =========================
# VIS 1: Donut (Pie/Donut)
# =========================
colA, colB = st.columns(2)

with colA:
    st.markdown("### 1) Distribusi Target (Donut Chart)")
    if "y" in f.columns and len(f):
        fig = donut(f["y"], "Distribusi y (Subscribe Deposito)")
        st.pyplot(fig, clear_figure=True)
        st.info(insight_top(f["y"], "target y"))
    else:
        st.warning("Kolom 'y' tidak tersedia atau data kosong.")

# =========================
# VIS 2: Bar Chart (Top Job)
# =========================
with colB:
    st.markdown("### 2) Top-10 Job (Bar Chart)")
    if "job" in f.columns and len(f):
        vc = f["job"].value_counts().head(10)
        fig, ax = plt.subplots()
        ax.bar(vc.index.astype(str), vc.values)
        ax.set_title("Top-10 Job")
        ax.set_xlabel("Job")
        ax.set_ylabel("Jumlah")
        ax.tick_params(axis="x", rotation=45)
        st.pyplot(fig, clear_figure=True)
        st.info(insight_top(f["job"], "job"))
    else:
        st.warning("Kolom 'job' tidak tersedia atau data kosong.")

# =========================
# VIS 3: Line Chart (Rate by Month)
# =========================
st.markdown("### 3) Tren Subscription Rate per Bulan (Line Chart)")
if all(c in f.columns for c in ["month", "y"]) and len(f):
    tmp = f.groupby("month")["y"].apply(lambda s: (s == "yes").mean() * 100)
    tmp = tmp.reindex(MONTH_ORDER)
    fig, ax = plt.subplots()
    ax.plot(tmp.index.astype(str), tmp.values, marker="o")
    ax.set_title("Subscription Rate (%) per Month")
    ax.set_xlabel("Month")
    ax.set_ylabel("Rate (%)")
    ax.tick_params(axis="x", rotation=45)
    st.pyplot(fig, clear_figure=True)

    if tmp.notna().any():
        st.info(f"Bulan dengan rate tertinggi: **{tmp.idxmax()}** (± **{tmp.max():.2f}%**).")
else:
    st.warning("Butuh kolom 'month' dan 'y'.")

# =========================
# VIS 4: Histogram (Duration)
# =========================
st.markdown("### 4) Distribusi Duration Telepon (Histogram)")
if "duration" in f.columns and len(f):
    fig, ax = plt.subplots()
    ax.hist(f["duration"].dropna(), bins=30)
    ax.set_title("Histogram Duration (detik)")
    ax.set_xlabel("Duration (detik)")
    ax.set_ylabel("Frekuensi")
    st.pyplot(fig, clear_figure=True)

    med = float(f["duration"].median())
    st.info(f"Median duration: **{med:.1f} detik**. Data duration biasanya condong (banyak panggilan singkat).")
else:
    st.warning("Kolom 'duration' tidak tersedia atau data kosong.")

# =========================
# VIS 5: Boxplot (Balance by y)
# =========================
st.markdown("### 5) Balance berdasarkan Target y (Boxplot)")
if all(c in f.columns for c in ["balance", "y"]) and len(f):
    yes = f.loc[f["y"] == "yes", "balance"].dropna()
    no = f.loc[f["y"] == "no", "balance"].dropna()

    fig, ax = plt.subplots()
    ax.boxplot([no, yes], labels=["no", "yes"], showfliers=False)
    ax.set_title("Boxplot Balance (€) berdasarkan y")
    ax.set_xlabel("y")
    ax.set_ylabel("Balance (€)")
    st.pyplot(fig, clear_figure=True)

    if len(yes) and len(no):
        st.info(
            f"Median balance y=yes: **{np.median(yes):.1f}** | "
            f"y=no: **{np.median(no):.1f}** → ada indikasi profil balance berbeda."
        )
else:
    st.warning("Butuh kolom 'balance' dan 'y'.")

# =========================
# VIS 6: Scatter (Duration vs Balance) - tambahan (biar lebih kaya)
# =========================
st.markdown("### 6) Hubungan Duration vs Balance (Scatter Plot)")
if all(c in f.columns for c in ["duration", "balance", "y"]) and len(f):
    plot_df = f.dropna(subset=["duration", "balance", "y"]).copy()
    if len(plot_df) > 9000:
        plot_df = plot_df.sample(9000, random_state=42)

    fig, ax = plt.subplots()
    for label in ["no", "yes"]:
        sub = plot_df[plot_df["y"] == label]
        ax.scatter(sub["duration"], sub["balance"], alpha=0.5, label=label)

    ax.set_title("Scatter: Duration vs Balance (dibedakan oleh y)")
    ax.set_xlabel("Duration (detik)")
    ax.set_ylabel("Balance (€)")
    ax.legend(title="y")
    st.pyplot(fig, clear_figure=True)

    st.info("Secara visual, titik y=yes sering muncul pada duration yang lebih tinggi → durasi lebih panjang bisa terkait peluang subscribe.")
else:
    st.warning("Butuh kolom 'duration', 'balance', dan 'y'.")

# =========================
# VIS 7: Heatmap Korelasi (Heatmap)
# =========================
st.markdown("### 7) Korelasi Variabel Numerik (Heatmap)")
num_cols = [c for c in ["age","balance","day","duration","campaign","pdays","previous"] if c in f.columns]
if len(num_cols) >= 2 and len(f):
    corr = f[num_cols].corr(numeric_only=True)

    fig, ax = plt.subplots()
    im = ax.imshow(corr.values)
    ax.set_xticks(range(len(num_cols)))
    ax.set_yticks(range(len(num_cols)))
    ax.set_xticklabels(num_cols, rotation=45, ha="right")
    ax.set_yticklabels(num_cols)
    ax.set_title("Heatmap Korelasi (Pearson)")
    plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    st.pyplot(fig, clear_figure=True)

    corr_abs = corr.abs().copy()
    np.fill_diagonal(corr_abs.values, 0)
    max_idx = np.unravel_index(np.argmax(corr_abs.values), corr_abs.shape)
    a, b = num_cols[max_idx[0]], num_cols[max_idx[1]]
    st.info(f"Korelasi absolut terbesar (selain diagonal): **{a}** vs **{b}** (r ≈ **{corr.loc[a,b]:.2f}**).")
else:
    st.warning("Kolom numerik tidak cukup atau data kosong.")

# =========================
# Kesimpulan singkat (buat tugas)
# =========================
st.markdown("---")
st.subheader("🧾 Kesimpulan Singkat (Auto)")
if "y" in f.columns and len(f):
    rate = pct_yes(f["y"])
    st.write(
        f"- Dari data terfilter saat ini, subscription rate (y=yes) sekitar **{rate:.2f}%**.\n"
        f"- Visualisasi menunjukkan perbedaan karakteristik pada beberapa kategori (job/education/contact) dan pola bulanan.\n"
        f"- Durasi telepon cenderung tidak merata (banyak panggilan singkat), dan durasi lebih panjang sering terlihat pada y=yes.\n"
        f"- Korelasi antar variabel numerik umumnya tidak ekstrem, tapi ada pasangan variabel yang lebih dominan dibanding lainnya.\n"
    )
else:
    st.write("- Tidak dapat membuat kesimpulan karena data kosong atau kolom y tidak tersedia.")

st.caption("Dashboard dibuat dengan Streamlit | Sitasi dataset: " + DATASET_CITATION)