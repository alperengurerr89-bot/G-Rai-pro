import streamlit as st

# --- ÖZEL TASARIM (CSS) ---
st.markdown("""
    <style>
    /* Ana Arka Plan */
    .stApp {
        background-color: #0e1117;
        color: #ffffff;
    }
    
    /* Yan Menü (Sidebar) */
    [data-testid="stSidebar"] {
        background-color: #161b22;
        border-right: 2px solid #30363d;
    }

    /* Başlık Stilize Etme */
    h1 {
        color: #58a6ff;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        text-shadow: 2px 2px 10px rgba(88, 166, 255, 0.3);
        border-bottom: 2px solid #58a6ff;
        padding-bottom: 10px;
    }

    /* Butonları Adobe Stiline Çevir */
    div.stButton > button:first-child {
        background-color: #238636;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 10px 24px;
        font-weight: bold;
        transition: 0.3s;
        width: 100%;
    }
    
    div.stButton > button:first-child:hover {
        background-color: #2ea043;
        box-shadow: 0px 0px 15px rgba(46, 160, 67, 0.5);
        transform: scale(1.02);
    }

    /* Input Alanları */
    .stTextInput > div > div > input {
        background-color: #0d1117;
        color: #58a6ff;
        border: 1px solid #30363d;
    }
    </style>
    """, unsafe_allow_html=True)

# --- SİTE İÇERİĞİ ---
st.title("🛡️ GÜRai Adobe Pro v1.0")
st.sidebar.title("Kontrol Paneli")

# Örnek Butonlar
col1, col2 = st.columns(2)
with col1:
    st.button("🎨 Resmi AI ile Düzenle")
with col2:
    st.button("🎬 Videoyu Kurgula")

st.text_input("Yapay Zeka'ya emir ver:", placeholder="Örn: Arka planı sil ve gökyüzünü gece yap...")
