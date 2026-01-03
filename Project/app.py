import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Bank Marketing Dashboard", layout="wide")

# =========================
# STYLE (CSS)
# =========================
st.markdown("""
<style>
/* background halus */
.stApp {
    background: linear-gradient(180deg, #f7f9fc 0%, #ffffff 60%);
}
.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}

/* Card style */
.card {
    background: #ffffff;
    border: 1px solid #eef2f7;
    border-radius: 16px;
    padding: 16px 18px;
    box-shadow: 0 6px 18px rgba(15, 23, 42, 0.06);
}
.card-title {
    font-size: 0.9rem;
    color: #64748b;
    margin-bottom: 6px;
}
.card-value {
    font-size: 1.6rem;
    font-weight: 700;
    color: #0f172a;
    line-height: 1.1;
}
.badge {
    display: inline-block;
    padding: 4px 10px;
    border-radius: 999px;
    border: 1px solid #e2e8f0;
    background: #f8fafc;
    color: #334155;
    font-size: 0.85rem;
}
.hr {
    height: 1px;
    background: #eef2f7;
    margin: 14px 0 18px 0;
}
.small-note {
    color: #64748b;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD DATA (ANTI ERROR)
# =========================
@st.cache_data
def load_data(path="bank-full.csv"):
    df = None
    for sep in [";", ","]:
        try:
            tmp = pd.read_csv(path, sep=sep)
            tmp.columns = (
                tmp.columns.astype(str)
                .str.replace("\ufeff", "", regex=False)
                .str.strip()
                .str.strip('"')
            )
            if "age" in tmp.columns:
                df = tmp
                break
        except:
            continue

    if df is None:
        st.error("Kolom 'age' tidak ditemukan. Pastikan file adalah bank-full.csv dan satu folder dengan app.py")
        st.stop()

    # cleaning numerik
    num_cols = ["age", "balance", "day", "duration", "campaign", "pdays", "previous"]
    for c in num_cols:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")

    # transformasi
    if "pdays" in df.columns:
        df["pdays_clean"] = df["pdays"].replace(-1, np.nan)

    # normalisasi target
    df["y"] = df["y"].astype(str).str.lower().str.strip()

    # urut bulan
    if "month" in df.columns:
        month_order = ["jan","feb","mar","apr","may","jun","jul","aug","sep","oct","nov","dec"]
        df["month"] = pd.Categorical(df["month"], categories=month_order, ordered=True)

    return df


df = load_data()

# Helper
def yes_rate(series: pd.Series) -> float:
    if len(series) == 0:
        return 0.0
    return (series.eq("yes").mean() * 100)

def nice_plot(ax):
    ax.grid(True, linestyle="--", linewidth=0.6, alpha=0.25)
    for spine in ["top", "right"]:
        ax.spines[spine].set_visible(False)

# =========================
# SIDEBAR FILTER
# =========================
st.sidebar.header("⚙️ Filter Data")

if st.sidebar.button("🔄 Reset Filter"):
    st.cache_data.clear()
    st.rerun()

age_min, age_max = int(df.age.min()), int(df.age.max())
age_range = st.sidebar.slider("Rentang Umur", age_min, age_max, (age_min, age_max))

job = st.sidebar.selectbox("Pekerjaan", ["Semua"] + sorted(df.job.unique().tolist()))
month = st.sidebar.selectbox("Bulan", ["Semua"] + list(df.month.cat.categories))
target = st.sidebar.selectbox("Target (y)", ["Semua", "yes", "no"])

top_n = st.sidebar.slider("Top-N Job", 5, 20, 10)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<div class='small-note'>Dataset: Bank Marketing (Moro et al., 2011)</div>",
    unsafe_allow_html=True
)

# apply filter
dff = df[(df.age >= age_range[0]) & (df.age <= age_range[1])]
if job != "Semua":
    dff = dff[dff.job == job]
if month != "Semua":
    dff = dff[dff.month == month]
if target != "Semua":
    dff = dff[dff.y == target]

# =========================
# HEADER
# =========================
st.markdown(
    """
<div class="card">
  <div style="display:flex; justify-content:space-between; gap:14px; flex-wrap:wrap;">
    <div>
      <div style="font-size:1.6rem; font-weight:800; color:#0f172a;">📊 Bank Marketing Dashboard</div>
      <div class="small-note">Eksplorasi data kampanye telemarketing untuk melihat pola pelanggan yang berlangganan deposito berjangka (y).</div>
    </div>
    <div style="display:flex; gap:8px; align-items:center; flex-wrap:wrap;">
      <span class="badge">Interactive • Streamlit</span>
      <span class="badge">45.211 baris (bank-full)</span>
      <span class="badge">≥ 5 visualisasi</span>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True
)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =========================
# KPI CARDS
# =========================
total_rows = len(dff)
rate_yes = yes_rate(dff["y"]) if total_rows else 0.0
avg_balance = float(dff["balance"].mean()) if total_rows else 0.0
median_duration = float(dff["duration"].median()) if total_rows else 0.0

k1, k2, k3, k4 = st.columns(4, gap="large")
k1.markdown(f"<div class='card'><div class='card-title'>Jumlah Data (setelah filter)</div><div class='card-value'>{total_rows:,}</div></div>", unsafe_allow_html=True)
k2.markdown(f"<div class='card'><div class='card-title'>Persentase y = yes</div><div class='card-value'>{rate_yes:.2f}%</div></div>", unsafe_allow_html=True)
k3.markdown(f"<div class='card'><div class='card-title'>Rata-rata Balance (€)</div><div class='card-value'>{avg_balance:,.2f}</div></div>", unsafe_allow_html=True)
k4.markdown(f"<div class='card'><div class='card-title'>Median Durasi (detik)</div><div class='card-value'>{median_duration:,.0f}</div></div>", unsafe_allow_html=True)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =========================
# ROW 1 (Pie + Bar)
# =========================
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("1) Proporsi Target (Pie/Donut)")
    if total_rows == 0:
        st.warning("Data kosong setelah filter.")
    else:
        counts = dff["y"].value_counts().reindex(["yes", "no"]).fillna(0)
        fig, ax = plt.subplots()
        ax.pie(counts.values, labels=counts.index, autopct="%1.1f%%", startangle=90)
        centre_circle = plt.Circle((0, 0), 0.65, fc="white")
        fig.gca().add_artist(centre_circle)
        ax.axis("equal")
        ax.set_title("Proporsi y (yes/no)")
        st.pyplot(fig)

        st.info(f"Insight: Pada kondisi filter saat ini, **{rate_yes:.2f}%** nasabah berlangganan deposito (y=yes).")
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("2) Top Job berdasarkan Yes Rate (Bar)")
    if total_rows == 0:
        st.warning("Data kosong setelah filter.")
    else:
        job_rate = (
            dff.groupby("job")["y"]
            .apply(lambda x: (x == "yes").mean() * 100)
            .sort_values(ascending=False)
            .head(top_n)
        )
        fig, ax = plt.subplots()
        ax.bar(job_rate.index, job_rate.values)
        nice_plot(ax)
        ax.set_title(f"Top-{top_n} Job — Persentase y=yes")
        ax.set_ylabel("Yes rate (%)")
        ax.set_xlabel("Job")
        plt.xticks(rotation=45, ha="right")
        st.pyplot(fig)

        best_job = job_rate.index[0]
        st.info(f"Insight: Job dengan **yes rate tertinggi** adalah **{best_job}** (± **{job_rate.iloc[0]:.2f}%**).")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# ROW 2 (Line + Scatter)
# =========================
col3, col4 = st.columns(2, gap="large")

with col3:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("3) Tren y=yes per Bulan (Line)")
    if total_rows == 0:
        st.warning("Data kosong setelah filter.")
    else:
        month_rate = dff.groupby("month")["y"].apply(lambda x: (x == "yes").mean() * 100)
        fig, ax = plt.subplots()
        ax.plot(month_rate.index.astype(str), month_rate.values, marker="o")
        nice_plot(ax)
        ax.set_title("Yes rate per bulan")
        ax.set_xlabel("Month")
        ax.set_ylabel("Yes rate (%)")
        st.pyplot(fig)

        peak_idx = int(np.argmax(month_rate.values)) if len(month_rate.values) else 0
        if len(month_rate.values):
            st.info(f"Insight: Puncak yes rate terjadi pada **{month_rate.index[peak_idx]}** (± **{month_rate.values[peak_idx]:.2f}%**).")
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("4) Age vs Balance (Scatter)")
    if total_rows == 0:
        st.warning("Data kosong setelah filter.")
    else:
        sample = dff.sample(min(3500, len(dff)), random_state=1) if len(dff) > 0 else dff
        fig, ax = plt.subplots()
        ax.scatter(sample["age"], sample["balance"], alpha=0.5)
        nice_plot(ax)
        ax.set_title("Sebaran Age vs Balance (sample)")
        ax.set_xlabel("Age")
        ax.set_ylabel("Balance (€)")
        st.pyplot(fig)

        st.info("Insight: Scatter membantu melihat pola hubungan umur dan saldo. Titik yang menyebar luas menandakan variasi nasabah yang beragam.")
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='hr'></div>", unsafe_allow_html=True)

# =========================
# ROW 3 (Histogram + Heatmap)
# =========================
col5, col6 = st.columns(2, gap="large")

with col5:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("5) Distribusi Balance (Histogram)")
    if total_rows == 0:
        st.warning("Data kosong setelah filter.")
    else:
        fig, ax = plt.subplots()
        ax.hist(dff["balance"].dropna(), bins=40)
        nice_plot(ax)
        ax.set_title("Histogram Balance")
        ax.set_xlabel("Balance (€)")
        ax.set_ylabel("Frekuensi")
        st.pyplot(fig)
        st.info("Insight: Histogram menunjukkan sebaran saldo. Jika data condong ke satu sisi, berarti banyak nasabah berada pada rentang saldo tertentu.")
    st.markdown("</div>", unsafe_allow_html=True)

with col6:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.subheader("6) Korelasi Numerik (Heatmap)")
    if total_rows == 0:
        st.warning("Data kosong setelah filter.")
    else:
        num_cols = ["age", "balance", "day", "duration", "campaign", "pdays_clean", "previous"]
        corr = dff[num_cols].corr(numeric_only=True)

        fig, ax = plt.subplots()
        im = ax.imshow(corr.values)
        ax.set_title("Correlation Heatmap")
        ax.set_xticks(range(len(num_cols)))
        ax.set_yticks(range(len(num_cols)))
        ax.set_xticklabels(num_cols, rotation=45, ha="right")
        ax.set_yticklabels(num_cols)
        plt.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
        st.pyplot(fig)

        st.info("Insight: Korelasi membantu melihat hubungan linear antar variabel numerik. Nilai mendekati 1/-1 berarti hubungan kuat.")
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# DATA PREVIEW
# =========================
with st.expander("📄 Lihat Data (Preview)"):
    st.dataframe(dff.head(30), use_container_width=True)

st.caption(
    "Citation: S. Moro, R. Laureano, P. Cortez (2011). Using Data Mining for Bank Direct Marketing: An Application of the CRISP-DM Methodology. "
    "ESM'2011. http://hdl.handle.net/1822/14838"
)
