import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import streamlit as st

# ─── Page config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 12px;
        padding: 20px;
        color: white;
        text-align: center;
    }
    .metric-value { font-size: 2rem; font-weight: 800; }
    .metric-label { font-size: 0.9rem; opacity: 0.85; margin-top: 4px; }
    .section-header {
        background: linear-gradient(90deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 1.4rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Load data ───────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("dashboard/main_data.csv", parse_dates=[
        "order_purchase_timestamp",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ])
    df["review_score"] = df["review_score"].astype(int)
    return df

df = load_data()

# ─── Sidebar filters ─────────────────────────────────────────────────────────
st.sidebar.image("https://img.icons8.com/color/96/shopping-cart.png", width=80)
st.sidebar.title("🔍 Filter Data")

years = sorted(df["year"].dropna().unique().astype(int).tolist())
selected_years = st.sidebar.multiselect("Tahun", years, default=years)

all_cats = sorted(df["product_category_name_english"].dropna().unique().tolist())
selected_cats = st.sidebar.multiselect(
    "Kategori Produk (Grafik 1)",
    all_cats,
    default=all_cats[:20],
    help="Pilih kategori yang ingin ditampilkan"
)
top_n = st.sidebar.slider("Tampilkan Top-N Kategori", 5, 20, 10)

review_range = st.sidebar.select_slider(
    "Rentang Skor Review (Grafik 2)",
    options=[1, 2, 3, 4, 5],
    value=(1, 5)
)

# ─── Filter dataframe ─────────────────────────────────────────────────────────
filtered = df[df["year"].isin(selected_years)].copy()
if selected_cats:
    filtered_rev = filtered[filtered["product_category_name_english"].isin(selected_cats)]
else:
    filtered_rev = filtered.copy()
filtered_del = filtered[filtered["review_score"].between(review_range[0], review_range[1])]

# ─── Title ────────────────────────────────────────────────────────────────────
st.title("🛒 E-Commerce Public Dataset — Dashboard Analisis")
st.markdown("**Nama:** Dini Naily Farchati &nbsp;|&nbsp; **Dataset:** Olist E-Commerce Brazil")
st.divider()

# ─── KPI Metrics ─────────────────────────────────────────────────────────────
total_orders   = filtered["order_id"].nunique()
total_revenue  = filtered["revenue"].sum()
avg_delivery   = filtered["delivery_days"].mean()
avg_review     = filtered["review_score"].mean()

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("📦 Total Pesanan", f"{total_orders:,}")
with c2:
    st.metric("💰 Total Revenue", f"R$ {total_revenue/1e6:.2f}M")
with c3:
    st.metric("🚚 Rata-rata Pengiriman", f"{avg_delivery:.1f} hari")
with c4:
    st.metric("⭐ Rata-rata Review", f"{avg_review:.2f} / 5")

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# PERTANYAAN 1
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 📊 Pertanyaan 1")
st.markdown("**Kategori produk apa yang menghasilkan total revenue tertinggi, dan bagaimana tren revenue bulanannya selama 2017–2018?**")

cat_revenue = (
    filtered_rev.groupby("product_category_name_english")["revenue"]
    .sum()
    .sort_values(ascending=False)
)
top10 = cat_revenue.head(top_n)

monthly_rev = (
    filtered_rev.groupby("month")["revenue"]
    .sum()
    .reset_index()
    .sort_values("month")
)
monthly_rev = monthly_rev[monthly_rev["month"] >= "2017-01"]

col1, col2 = st.columns([1.1, 1])

with col1:
    st.markdown(f"#### 🏆 Top {top_n} Kategori berdasarkan Revenue")
    fig1, ax1 = plt.subplots(figsize=(7, top_n * 0.55 + 1))
    colors = ["#27ae60" if i == 0 else "#95a5a6" for i in range(top_n)]
    bars = ax1.barh(top10.index[::-1], top10.values[::-1] / 1e6,
                    color=colors[::-1], edgecolor="white")
    ax1.set_xlabel("Total Revenue (Juta R$)", fontsize=10)
    ax1.set_title(f"Top {top_n} Kategori berdasarkan Revenue\n({', '.join(map(str, selected_years))})",
                  fontsize=11, fontweight="bold")
    ax1.spines["top"].set_visible(False)
    ax1.spines["right"].set_visible(False)
    for bar, val in zip(bars, top10.values[::-1]):
        ax1.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height() / 2,
                 f"R${val/1e6:.2f}M", va="center", fontsize=8)
    plt.tight_layout()
    st.pyplot(fig1)

with col2:
    st.markdown("#### 📈 Tren Revenue Bulanan (2017–2018)")
    fig2, ax2 = plt.subplots(figsize=(7, 4.5))
    x = range(len(monthly_rev))
    ax2.plot(x, monthly_rev["revenue"] / 1e6, color="#2980b9",
             linewidth=2.5, marker="o", markersize=4)
    ax2.fill_between(x, monthly_rev["revenue"] / 1e6, alpha=0.12, color="#2980b9")
    ticks = list(range(0, len(monthly_rev), 3))
    ax2.set_xticks(ticks)
    ax2.set_xticklabels(
        [monthly_rev["month"].iloc[i] for i in ticks], rotation=45, ha="right", fontsize=8
    )
    ax2.set_ylabel("Revenue (Juta R$)", fontsize=10)
    ax2.set_title("Tren Revenue Bulanan (2017–2018)", fontsize=11, fontweight="bold")
    ax2.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f"))
    ax2.spines["top"].set_visible(False)
    ax2.spines["right"].set_visible(False)
    if len(monthly_rev) > 0:
        peak_i = (monthly_rev["revenue"] / 1e6).idxmax()
        ax2.annotate(
            f'Puncak: R${monthly_rev["revenue"].max()/1e6:.2f}M\n({monthly_rev["month"].iloc[peak_i]})',
            xy=(list(x)[list(monthly_rev.index).index(peak_i)], monthly_rev["revenue"].max() / 1e6),
            xytext=(list(x)[list(monthly_rev.index).index(peak_i)] + 1.5,
                    monthly_rev["revenue"].max() / 1e6 - 0.1),
            arrowprops=dict(arrowstyle="->", color="navy"), fontsize=8, color="navy"
        )
    plt.tight_layout()
    st.pyplot(fig2)

with st.expander("💡 Insight Pertanyaan 1"):
    st.info(
        "**health_beauty** adalah kategori dengan revenue tertinggi, diikuti watches_gifts dan bed_bath_table. "
        "Tren bulanan menunjukkan pertumbuhan konsisten di 2017 dengan puncak di November 2017 (~R$1,15M), "
        "kemungkinan dipicu momen belanja akhir tahun. Revenue stabil di kisaran R$0,8M–1,0M sepanjang 2018."
    )

st.divider()

# ══════════════════════════════════════════════════════════════════════════════
# PERTANYAAN 2
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("## 🚚 Pertanyaan 2")
st.markdown("**Apakah durasi pengiriman berpengaruh terhadap skor review pelanggan pada pesanan berstatus *delivered* sepanjang 2016–2018?**")

palette_map = {1: "#e74c3c", 2: "#e67e22", 3: "#f1c40f", 4: "#2ecc71", 5: "#27ae60"}
scores = sorted(filtered_del["review_score"].unique())
palette = [palette_map[s] for s in scores]

avg_days = filtered_del.groupby("review_score")["delivery_days"].mean()

col3, col4 = st.columns(2)

with col3:
    st.markdown("#### 📊 Rata-rata Durasi Pengiriman per Skor Review")
    fig3, ax3 = plt.subplots(figsize=(6, 4.5))
    bars3 = ax3.bar(avg_days.index, avg_days.values,
                    color=[palette_map.get(s, "#888") for s in avg_days.index],
                    edgecolor="white", width=0.6)
    ax3.set_xlabel("Skor Review (1=Sangat Buruk, 5=Sangat Baik)", fontsize=10)
    ax3.set_ylabel("Rata-rata Durasi Pengiriman (Hari)", fontsize=10)
    ax3.set_title("Rata-rata Durasi Pengiriman\nper Skor Review", fontsize=11, fontweight="bold")
    ax3.spines["top"].set_visible(False)
    ax3.spines["right"].set_visible(False)
    for bar, val in zip(bars3, avg_days.values):
        ax3.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.2,
                 f"{val:.1f} hari", ha="center", fontsize=9, fontweight="bold")
    if 1 in avg_days.index and 5 in avg_days.index:
        ax3.annotate(
            f'Skor 1 rata-rata {avg_days[1]/avg_days[5]:.1f}x\nlebih lambat dari skor 5',
            xy=(1, avg_days[1]),
            xytext=(2.5, avg_days[1] - 2),
            arrowprops=dict(arrowstyle="->", color="red"), fontsize=9, color="red"
        )
    plt.tight_layout()
    st.pyplot(fig3)

with col4:
    st.markdown("#### 📦 Distribusi Durasi Pengiriman per Skor Review")
    fig4, ax4 = plt.subplots(figsize=(6, 4.5))
    groups = [
        filtered_del[filtered_del["review_score"] == s]["delivery_days"].dropna()
        for s in range(review_range[0], review_range[1] + 1)
    ]
    labels = list(range(review_range[0], review_range[1] + 1))
    bp = ax4.boxplot(
        groups, labels=labels, patch_artist=True,
        medianprops=dict(color="black", linewidth=2),
        showfliers=False
    )
    for patch, score in zip(bp["boxes"], labels):
        patch.set_facecolor(palette_map.get(score, "#888"))
        patch.set_alpha(0.7)
    ax4.set_xlabel("Skor Review", fontsize=10)
    ax4.set_ylabel("Durasi Pengiriman (Hari)", fontsize=10)
    ax4.set_title("Distribusi Durasi Pengiriman\nper Skor Review", fontsize=11, fontweight="bold")
    ax4.spines["top"].set_visible(False)
    ax4.spines["right"].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig4)

# Summary table
st.markdown("#### 📋 Ringkasan Statistik per Skor Review")
summary = (
    filtered_del.groupby("review_score")["delivery_days"]
    .agg(["mean", "median", "count"])
    .round(1)
    .rename(columns={"mean": "Rata-rata (hari)", "median": "Median (hari)", "count": "Jumlah Pesanan"})
)
st.dataframe(summary.style.background_gradient(subset=["Rata-rata (hari)"], cmap="RdYlGn_r"), use_container_width=True)

with st.expander("💡 Insight Pertanyaan 2"):
    st.info(
        "Terdapat hubungan negatif yang jelas antara durasi pengiriman dan skor review. "
        "Pesanan dengan skor review 5 rata-rata tiba dalam **10,2 hari**, "
        "sedangkan skor 1 rata-rata memerlukan **20,8 hari** — 2x lebih lama. "
        "Ini mengkonfirmasi bahwa kecepatan pengiriman adalah driver utama kepuasan pelanggan."
    )

st.divider()

# ─── Conclusion & Recommendation ─────────────────────────────────────────────
st.markdown("## ✅ Conclusion & Recommendation")

col5, col6 = st.columns(2)
with col5:
    st.success(
        "**Kesimpulan 1:** `health_beauty` adalah kategori revenue tertinggi (>R$1,44 juta). "
        "Tren bulanan memuncak di November 2017 (~R$1,15M). Revenue stabil di 2018 di kisaran R$0,8–1,0M per bulan."
    )
    st.success(
        "**Kesimpulan 2:** Durasi pengiriman berpengaruh signifikan terhadap skor review. "
        "Pengiriman ≤10 hari → skor 5; >20 hari → skor 1. Korelasi negatif kuat dikonfirmasi dari data."
    )
with col6:
    st.warning(
        "**Rekomendasi Action Item:**\n\n"
        "1. 📦 Optimalkan logistik & stok untuk kategori **health_beauty**, **watches_gifts**, dan **bed_bath_table** "
        "terutama menjelang bulan **November–Desember**.\n\n"
        "2. ⏱️ Tetapkan **SLA maksimal 10 hari** untuk seluruh pesanan agar kepuasan pelanggan terjaga di level skor 5.\n\n"
        "3. 🚨 Buat sistem **early warning** jika estimasi pengiriman melebihi 12 hari agar tim operasional "
        "dapat mengambil tindakan proaktif sebelum pelanggan kecewa."
    )

st.caption("Dashboard dibuat dengan Streamlit | Data: Olist E-Commerce Public Dataset (2016–2018)")
