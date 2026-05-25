import streamlit as st
import pandas as pd
import numpy as np
import joblib

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="SmartPick – Prediksi Harga HP",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="collapsed", # Mengubah default sidebar menjadi tertutup
)

# ─────────────────────────────────────────────
# CUSTOM CSS (ENHANCED UI/UX)
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Space+Mono:wght@400;700&display=swap');

html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

/* Background utama aplikasi */
.stApp {
    background: radial-gradient(circle at top left, #1e1b4b, #0f0c29, #1a1a2e);
    color: #e8eaf6;
}

/* Sidebar Styling - Disembunyikan secara visual jika tidak dipakai */
[data-testid="stSidebar"] {
    background: rgba(15, 12, 41, 0.6) !important;
    backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255,255,255,0.05);
}

/* Hero Box (Header) dengan efek glow */
.hero-box {
    background: linear-gradient(135deg, rgba(99,102,241,0.1), rgba(168,85,247,0.05));
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 24px;
    padding: 2.5rem;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 8px 32px rgba(99, 102, 241, 0.15);
    backdrop-filter: blur(8px);
}
.hero-title {
    font-family: 'Space Mono', monospace;
    font-size: 2.8rem;
    font-weight: 800;
    background: linear-gradient(90deg, #818cf8, #c084fc, #f472b6, #818cf8);
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: gradient-move 3s linear infinite;
    margin: 0 0 0.5rem 0;
}
@keyframes gradient-move {
    0% { background-position: 0% center; }
    100% { background-position: 200% center; }
}
.hero-sub { color: #94a3b8; font-size: 1rem; margin: 0; letter-spacing: 0.5px;}

/* Animasi Result Card */
@keyframes pulse-glow {
    0% { box-shadow: 0 0 0 0 rgba(168,85,247,0.4); }
    70% { box-shadow: 0 0 0 15px rgba(168,85,247,0); }
    100% { box-shadow: 0 0 0 0 rgba(168,85,247,0); }
}
.result-card {
    border-radius: 20px;
    padding: 2rem;
    margin: 1.2rem 0;
    text-align: center;
    border: 1px solid;
    animation: pulse-glow 2.5s infinite;
    backdrop-filter: blur(10px);
}
.result-murah    { background: linear-gradient(135deg, rgba(34,197,94,0.1), rgba(34,197,94,0.02)); border-color: rgba(34,197,94,0.5); }
.result-menengah { background: linear-gradient(135deg, rgba(59,130,246,0.1), rgba(59,130,246,0.02)); border-color: rgba(59,130,246,0.5); }
.result-mahal    { background: linear-gradient(135deg, rgba(251,146,60,0.1), rgba(251,146,60,0.02)); border-color: rgba(251,146,60,0.5); }
.result-premium  { background: linear-gradient(135deg, rgba(168,85,247,0.1), rgba(168,85,247,0.02)); border-color: rgba(168,85,247,0.5); }

.result-label { font-family:'Space Mono',monospace; font-size:1rem; letter-spacing:.15em; margin:0 0 .5rem 0; opacity:.8; }
.result-class { font-size:2.5rem; font-weight:800; margin:0; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }
.result-range { font-size:1.1rem; opacity:.8; margin:.5rem 0 0 0; }

/* Interaktif Hover pada HP Card */
.hp-card {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.hp-card:hover {
    transform: translateY(-6px) scale(1.01);
    box-shadow: 0 12px 30px rgba(99, 102, 241, 0.15);
    border-color: rgba(99,102,241,0.5);
    background: rgba(255,255,255,0.05);
}
.hp-name  { font-size:1.15rem; font-weight:800; margin:0 0 .3rem 0; color:#f8fafc; }
.hp-brand { font-size:.8rem; color:#818cf8; font-weight:700; letter-spacing:.08em; text-transform:uppercase; }
.hp-price { font-size:1.1rem; font-weight:700; color:#34d399; margin:.6rem 0 .4rem 0; }
.hp-desc  { font-size:.85rem; color:#cbd5e1; margin:.4rem 0 .8rem 0; line-height: 1.5; }
.hp-spec  { display:flex; flex-wrap:wrap; gap:.5rem; margin-top:.8rem; }
.spec-badge {
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 8px;
    padding: .3rem .6rem;
    font-size:.78rem;
    color:#c7d2fe;
    font-family:'Space Mono',monospace;
    transition: all 0.2s ease;
}
.hp-card:hover .spec-badge {
    background: rgba(99,102,241,0.2);
}

/* Custom Button Streamlit Prediksi Harga */
div.stButton > button:first-child {
    background: linear-gradient(90deg, #6366f1, #a855f7, #ec4899);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.6rem;
    font-family: 'Space Mono', monospace;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.05em;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(168, 85, 247, 0.3);
}
div.stButton > button:first-child:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(168, 85, 247, 0.5);
    background: linear-gradient(90deg, #4f46e5, #9333ea, #db2777);
    color: white;
}

/* Utils & Progress Bars */
.conf-bar-wrap { margin:.4rem 0 .8rem 0; }
.conf-label    { font-size:.85rem; color:#cbd5e1; margin-bottom:.3rem; font-weight:500;}
.conf-bar-bg   { background:rgba(255,255,255,0.05); border-radius:99px; height:10px; overflow:hidden; box-shadow: inset 0 1px 3px rgba(0,0,0,0.3); }
.conf-bar-fill { height:10px; border-radius:99px; transition: width 1s ease-in-out; }

.tip-box {
    background: linear-gradient(135deg, rgba(251,191,36,0.1), rgba(251,191,36,0.02));
    border: 1px solid rgba(251,191,36,0.3);
    border-radius: 12px;
    padding: 1rem 1.2rem;
    font-size:.88rem;
    color:#fde68a;
    margin-top:1.5rem;
    line-height: 1.5;
}
.sec-header {
    font-family:'Space Mono',monospace;
    font-size:.85rem;
    letter-spacing:.15em;
    color:#94a3b8;
    text-transform:uppercase;
    margin:1.8rem 0 1rem 0;
    font-weight: 700;
}
.input-header {
    font-size:1.1rem;
    color:#e0e7ff;
    margin-bottom: 0.5rem;
    font-weight: 600;
}
.custom-divider { border:none; border-top:1px solid rgba(255,255,255,0.08); margin:1.8rem 0; }
.block-container { padding-top:1.5rem !important; }
label { color:#cbd5e1 !important; font-size:.88rem !important; }

/* Pill selector styling */
div[data-testid="stSelectbox"] > div { border-radius: 10px; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# LOAD MODEL & DATA
# ─────────────────────────────────────────────
@st.cache_resource
def load_model():
    try:
        return joblib.load("smartphone_model.pkl")
    except FileNotFoundError:
        return None

@st.cache_data
def load_recommendations():
    return pd.read_csv("hp_rekomendasi.csv")

model  = load_model()
df_rec = load_recommendations()


# ─────────────────────────────────────────────
# MAPPING TABEL (Umum → Teknis)
# ─────────────────────────────────────────────

# RAM: pilihan umum → nilai MB
RAM_OPTIONS = {
    "1 GB":  1024,
    "2 GB":  2048,
    "3 GB":  3072,
    "4 GB":  3998,
}

# Penyimpanan → int_memory (GB, max dataset 64)
STORAGE_OPTIONS = {
    "16 GB": 16,
    "32 GB": 32,
    "64 GB": 64,
}

# Kamera belakang → pc (MP, max dataset 20)
REAR_CAM_OPTIONS = {
    "8 MP  – Standar":  8,
    "12 MP – Bagus":   12,
    "16 MP – Sangat Bagus": 16,
    "20 MP – Pro":     20,
}

# Kamera depan → fc (MP, max dataset 19)
FRONT_CAM_OPTIONS = {
    "2 MP  – Standar": 2,
    "5 MP  – Bagus":   5,
    "8 MP  – Selfie Pro": 8,
    "13 MP – Ultra Selfie": 13,
}

# Baterai → battery_power (dataset range 501–1998)
BATTERY_OPTIONS = {
    "Kecil  (~1000 mAh)":  1000,
    "Sedang (~1500 mAh)":  1500,
    "Besar  (~2000 mAh)":  1998,
}

# Konektivitas → nilai teknis
CONN_LABELS = {
    "4G LTE":      "four_g",
    "Bluetooth":   "blue",
    "Dual SIM":    "dual_sim",
    "WiFi":        "wifi",
    "Touch Screen":"touch_screen",
}

# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────
LABEL_INFO = {
    0: {"name":"Murah",    "range":"Rp 500.000 – Rp 2.000.000", "emoji":"💚", "css":"result-murah",    "color":"#22c55e"},
    1: {"name":"Menengah", "range":"Rp 2.000.000 – Rp 4.000.000","emoji":"💙", "css":"result-menengah","color":"#3b82f6"},
    2: {"name":"Mahal",    "range":"Rp 4.000.000 – Rp 7.000.000","emoji":"🧡", "css":"result-mahal",   "color":"#fb923c"},
    3: {"name":"Premium",  "range":"Rp 7.000.000+",              "emoji":"💜", "css":"result-premium", "color":"#a855f7"},
}

def fmt_harga(val):
    return f"Rp {val:,.0f}".replace(",",".")

def conf_bar(label, prob, color):
    pct = prob * 100
    st.markdown(f"""
    <div class="conf-bar-wrap">
        <div class="conf-label">{label} — {pct:.1f}%</div>
        <div class="conf-bar-bg">
            <div class="conf-bar-fill" style="width:{pct}%;background:{color};"></div>
        </div>
    </div>""", unsafe_allow_html=True)

def hp_card(row):
    specs  = [f"💾 RAM {row['ram_gb']} GB", f"📦 {row['penyimpanan_gb']} GB",
              f"📷 {row['kamera_mp']} MP",  f"🔋 {row['baterai_mah']} mAh",
              f"📺 {row['layar_inch']}\""]
    badges = "".join(f'<span class="spec-badge">{s}</span>' for s in specs)
    harga  = f"{fmt_harga(row['harga_min'])} – {fmt_harga(row['harga_max'])}"
    st.markdown(f"""
    <div class="hp-card">
        <div class="hp-brand">{row['merek']}</div>
        <div class="hp-name">{row['nama_hp']}</div>
        <div class="hp-price">{harga}</div>
        <div class="hp-desc">{row['deskripsi']}</div>
        <div class="hp-spec">{badges}</div>
    </div>""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# MAIN CONTENT & INPUT FORM
# ─────────────────────────────────────────────
st.markdown("""
<div class="hero-box">
    <p class="hero-title">📱 SmartPick</p>
    <p class="hero-sub">Prediksi kelas harga smartphone & rekomendasi HP terbaik berdasarkan spesifikasi kamu</p>
</div>
""", unsafe_allow_html=True)

if model is None:
    st.error("""
    ⚠️ **Model belum ditemukan!**

    Pastikan file `smartphone_model.pkl` ada di folder yang sama dengan `app.py`.  
    Jalankan notebook Google Colab terlebih dahulu untuk menghasilkan file tersebut.
    """)
    st.stop()

# --- BAGIAN INPUT DI HALAMAN UTAMA ---
st.markdown('<p class="sec-header">⚙️ Tentukan Spesifikasi HP Kamu</p>', unsafe_allow_html=True)

# Menggunakan 3 kolom agar input terlihat rapi dan proporsional
col_perf, col_cam, col_bat = st.columns(3, gap="large")

with col_perf:
    st.markdown('<p class="input-header">⚡ Performa</p>', unsafe_allow_html=True)
    sel_ram     = st.selectbox("Kapasitas RAM", list(RAM_OPTIONS.keys()), index=1)
    sel_storage = st.selectbox("Penyimpanan Internal", list(STORAGE_OPTIONS.keys()), index=1)

with col_cam:
    st.markdown('<p class="input-header">📷 Kamera</p>', unsafe_allow_html=True)
    sel_rear  = st.selectbox("Kamera Utama (Belakang)", list(REAR_CAM_OPTIONS.keys()), index=1)
    sel_front = st.selectbox("Kamera Selfie (Depan)", list(FRONT_CAM_OPTIONS.keys()), index=1)

with col_bat:
    st.markdown('<p class="input-header">🔋 Baterai</p>', unsafe_allow_html=True)
    sel_battery = st.selectbox("Kapasitas Baterai", list(BATTERY_OPTIONS.keys()), index=1)

st.markdown('<br>', unsafe_allow_html=True)
st.markdown('<p class="input-header">📶 Fitur Konektivitas</p>', unsafe_allow_html=True)

# Toggle diurutkan menyamping
conn_cols = st.columns(5)
conn_vals = {}
defaults  = {"4G LTE": True, "Bluetooth": True, "Dual SIM": True,
             "WiFi": True, "Touch Screen": True}

for i, label in enumerate(CONN_LABELS):
    with conn_cols[i]:
        conn_vals[label] = st.toggle(label, value=defaults[label])

st.markdown('<br>', unsafe_allow_html=True)
predict_btn = st.button("🔍 Prediksi Harga", use_container_width=True, type="primary")

st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)

# Jika tombol belum diklik, tampilkan metrik info di bawah form
if not predict_btn:
    st.info("👆 Tentukan spesifikasi HP yang kamu inginkan pada form di atas, lalu klik **Prediksi Harga**.")
    col_m1, col_m2, col_m3 = st.columns(3)
    col_m1.metric("🌲 Algoritma", "Random Forest")
    col_m2.metric("📊 Dataset Latih", "2.000 Baris Data")
    col_m3.metric("🏷️ Kelas Harga", "4 Kategori")
    st.stop()


# ─────────────────────────────────────────────
# KONVERSI INPUT UMUM → FITUR TEKNIS MODEL
# ─────────────────────────────────────────────
ram_mb     = RAM_OPTIONS[sel_ram]
storage_gb = STORAGE_OPTIONS[sel_storage]
rear_mp    = REAR_CAM_OPTIONS[sel_rear]
front_mp   = FRONT_CAM_OPTIONS[sel_front]
battery    = BATTERY_OPTIONS[sel_battery]

four_g      = int(conn_vals["4G LTE"])
blue        = int(conn_vals["Bluetooth"])
dual_sim    = int(conn_vals["Dual SIM"])
wifi        = int(conn_vals["WiFi"])
touch_screen= int(conn_vals["Touch Screen"])

# Fitur teknis tersembunyi → nilai median dari dataset training
clock_speed = 1.5
n_cores     = 4
m_dep       = 0.5
mobile_wt   = 141
sc_h        = 12
sc_w        = 5
talk_time   = 11
three_g     = 1          
px_height   = 700        
px_width    = 1300

# Susun array fitur
input_data = np.array([[
    battery, blue, clock_speed, dual_sim,
    front_mp, four_g, storage_gb, m_dep, mobile_wt, n_cores,
    rear_mp, px_height, px_width, ram_mb, sc_h, sc_w, talk_time,
    three_g, touch_screen, wifi
]])

FEATURE_NAMES = [
    "battery_power","blue","clock_speed","dual_sim","fc","four_g",
    "int_memory","m_dep","mobile_wt","n_cores","pc","px_height",
    "px_width","ram","sc_h","sc_w","talk_time","three_g","touch_screen","wifi"
]

df_input   = pd.DataFrame(input_data, columns=FEATURE_NAMES)
prediction = model.predict(df_input)[0]
proba      = model.predict_proba(df_input)[0]
info       = LABEL_INFO[prediction]


# ─────────────────────────────────────────────
# TAMPILKAN HASIL PREDIKSI
# ─────────────────────────────────────────────
st.markdown('<p class="sec-header">🎯 Hasil Prediksi & Analisis Model</p>', unsafe_allow_html=True)

col_res, col_conf = st.columns([1, 1], gap="large")

with col_res:
    st.markdown(f"""
    <div class="result-card {info['css']}">
        <p class="result-label">PREDIKSI KELAS HARGA</p>
        <p class="result-class">{info['emoji']} {info['name']}</p>
        <p class="result-range">{info['range']}</p>
    </div>
    """, unsafe_allow_html=True)

    # Ringkasan pilihan user
    st.markdown('<p class="sec-header" style="margin-top:1rem;">Spesifikasi Pilihanmu</p>', unsafe_allow_html=True)
    fitur_aktif = [k for k, v in conn_vals.items() if v]
    summary = pd.DataFrame({
        "Spesifikasi": ["RAM", "Penyimpanan", "Kamera Utama", "Kamera Selfie",
                        "Baterai", "Fitur Aktif"],
        "Pilihan": [
            sel_ram, sel_storage,
            sel_rear.split("–")[0].strip(),
            sel_front.split("–")[0].strip(),
            sel_battery.split("(")[1].replace(")","").strip(),
            ", ".join(fitur_aktif) if fitur_aktif else "—"
        ]
    })
    st.dataframe(summary, hide_index=True, use_container_width=True)

with col_conf:
    st.markdown('<p class="sec-header" style="margin-top:0;">Tingkat Kepercayaan Model</p>', unsafe_allow_html=True)
    for i, p in enumerate(proba):
        inf = LABEL_INFO[i]
        conf_bar(f"{inf['emoji']} {inf['name']}", p, inf['color'])

    best_conf = proba[prediction] * 100
    if best_conf >= 80:
        st.success(f"✅ Model sangat yakin: **{best_conf:.1f}%** kepercayaan")
    elif best_conf >= 60:
        st.warning(f"⚠️ Model cukup yakin: **{best_conf:.1f}%** kepercayaan")
    else:
        st.error(f"❗ Kepercayaan rendah: **{best_conf:.1f}%** — coba ubah kombinasi spesifikasi")

    st.markdown("""
    <div class="tip-box">
        💡 <b>Tips Analisis:</b> RAM merupakan fitur yang memiliki <i>importance score</i> tertinggi dalam penentuan kelas harga pada model ini. 
        Menaikkan atau menurunkan kapasitas RAM sangat mempengaruhi probabilitas kelas harga.
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────────
# REKOMENDASI HP
# ─────────────────────────────────────────────
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
st.markdown(f'<p class="sec-header">🛍️ Rekomendasi HP Kelas {info["name"]} {info["emoji"]}</p>',
            unsafe_allow_html=True)

df_filtered = df_rec[df_rec["price_range"] == prediction].reset_index(drop=True)

if df_filtered.empty:
    st.warning("Tidak ada rekomendasi HP nyata untuk spesifikasi dan kelas ini.")
else:
    merek_list = ["Semua Merek"] + sorted(df_filtered["merek"].unique().tolist())
    sel_merek  = st.selectbox("Filter berdasarkan merek (Opsional):", merek_list)

    df_show = df_filtered if sel_merek == "Semua Merek" \
              else df_filtered[df_filtered["merek"] == sel_merek]

    if df_show.empty:
        st.info(f"Tidak ada HP dengan merek {sel_merek} di kelas harga {info['name']}.")
    else:
        cols = st.columns(2)
        for i, (_, row) in enumerate(df_show.iterrows()):
            with cols[i % 2]:
                hp_card(row)

# Footer
st.markdown('<hr class="custom-divider">', unsafe_allow_html=True)
st.markdown("""
<p style="text-align:center;color:#475569;font-size:.8rem;font-family:'Space Mono',monospace;">
SmartPick · Proyek Data Mining ST167 · Universitas Amikom Yogyakarta · Random Forest Classifier
</p>
""", unsafe_allow_html=True)