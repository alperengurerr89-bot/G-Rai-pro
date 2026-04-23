import streamlit as st
import os
import platform
import subprocess
from PIL import Image, ImageEnhance, ImageFilter
from moviepy import VideoFileClip

# --- SAYFA AYARLARI ---
st.set_page_config(page_title="GÜRai OMNI Pro", page_icon="🛡️", layout="wide")

# --- ÖZEL CYBER TASARIM (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0d1117; color: #ffffff; }
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 2px solid #58a6ff; }
    h1 { color: #58a6ff; text-shadow: 0px 0px 15px #58a6ff; border-bottom: 2px solid #58a6ff; }
    .stButton>button { 
        background: linear-gradient(45deg, #238636, #2ea043); 
        color: white; border-radius: 10px; border: none; 
        transition: 0.3s; width: 100%; font-weight: bold;
    }
    .stButton>button:hover { transform: scale(1.05); box-shadow: 0px 0px 20px #2ea043; }
    .stTextInput>div>div>input { background-color: #010409; color: #58a6ff; border: 1px solid #30363d; }
    </style>
    """, unsafe_allow_html=True)

# --- ARKA PLAN SİSTEMLERİ ---
def ollama_kontrol():
    try:
        env = os.environ.copy()
        env["OLLAMA_ORIGINS"] = "*"
        flags = subprocess.CREATE_NEW_CONSOLE if platform.system() == "Windows" else 0
        subprocess.Popen(["ollama", "serve"], env=env, creationflags=flags)
    except:
        pass

# --- ANA ARAYÜZ ---
st.title("🛡️ GÜRai OMNI: AI Creative Suite")

# --- YAN MENÜ (MODLAR) ---
with st.sidebar:
    st.image("https://img.icons8.com/neon/96/artificial-intelligence.png")
    st.title("GÜRai Modları")
    mod = st.radio("Bir Araç Seç:", [
        "🎨 AI Resim Üret (Firefly)", 
        "📸 Fotoğraf Düzenle (Photoshop)", 
        "🎬 Video Kurgu (Premiere)",
        "🧠 GÜRai Chat (Llama 3)"
    ])
    st.info(f"Sistem: RTX 3050 | 32GB RAM")
    if st.button("Sistemleri Uyandır"):
        ollama_kontrol()
        st.success("Ollama ve AI motorları hazır!")

# --- MOD 1: AI RESİM ÜRETME ---
if mod == "🎨 AI Resim Üret (Firefly)":
    st.header("Yazıdan Resme (Generative AI)")
    prompt = st.text_input("Ne hayal ediyorsun?", placeholder="Örn: Cyberpunk bir İstanbul manzarası, yağmurlu...")
    if st.button("Resmi Oluştur"):
        with st.spinner("AI hayal ediyor..."):
            # Buraya Stable Diffusion veya DALL-E API bağlanabilir
            st.warning("Bu mod için 'diffusers' kütüphanesi ve model yüklemesi gerekir.")
            st.image("https://via.placeholder.com/800x400/0d1117/58a6ff?text=GURai+AI+Cizim+Modu+Aktif")

# --- MOD 2: FOTOĞRAF DÜZENLEME ---
elif mod == "📸 Fotoğraf Düzenle (Photoshop)":
    st.header("Akıllı Fotoğraf Düzenleyici")
    yuklenen_dosya = st.file_uploader("Bir resim seç...", type=["jpg", "png", "jpeg"])
    if yuklenen_dosya:
        img = Image.open(yuklenen_dosya)
        col1, col2 = st.columns(2)
        with col1:
            st.image(img, caption="Orijinal")
            keskinlik = st.slider("Keskinlik", 1.0, 5.0, 1.0)
        with col2:
            if st.button("Efektleri Uygula"):
                enhancer = ImageEnhance.Sharpness(img)
                img = enhancer.enhance(keskinlik)
                img = img.filter(ImageFilter.DETAIL)
                st.image(img, caption="GÜRai Edit")
                st.success("Düzenleme Tamamlandı!")

# --- MOD 3: VİDEO KURGU ---
elif mod == "🎬 Video Kurgu (Premiere)":
    st.header("Hızlı Video Kesici")
    video_dosya = st.file_uploader("Video yükle...", type=["mp4", "mov"])
    if video_dosya:
        t1 = st.number_input("Başlangıç Saniyesi", value=0)
        t2 = st.number_input("Bitiş Saniyesi", value=5)
        if st.button("Videoyu İşle"):
            with st.spinner("RTX 3050 Render alıyor..."):
                # Video işleme kodu buraya gelecek (moviepy)
                st.success(f"{t1} - {t2} arası kesme işlemi sıraya alındı.")

# --- MOD 4: CHAT ---
elif mod == "🧠 GÜRai Chat (Llama 3)":
    st.header("GÜRai Akıllı Asistan")
    soru = st.chat_input("Bana bir şey sor...")
    if soru:
        st.chat_message("user").write(soru)
        with st.chat_message("assistant"):
            st.write("Ollama/Llama 3 üzerinden cevap bekleniyor...")
            # Buraya ollama request kodu eklenecek
