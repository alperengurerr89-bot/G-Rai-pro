import streamlit as st
import google.generativeai as genai

# 🔑 1. ADIM: API Anahtarını Yapılandır
# Kendi API anahtarını tırnak işaretlerinin arasına yapıştır.
API_KEY = "AIzaSyCGWNPpkXbkyN5DY9NaqoNV07C6iqSYRUc" 
genai.configure(api_key=API_KEY)

# 🧠 2. ADIM: Modeli Hazırla
# 404 hatasını önlemek için en güncel model ismini kullanıyoruz.
model = genai.GenerativeModel('gemini-1.5-flash')

# 🎨 3. ADIM: Sayfa Tasarımı (Streamlit)
st.set_page_config(page_title="GÜRai Yapay Zeka", page_icon="🛡️")

st.title("🛡️ GÜRai - Yapay Zeka")
st.markdown("---")

# 💬 4. ADIM: Kullanıcı Etkileşimi
soru = st.text_input("GÜRai'ye bir şey sor:", placeholder="Merhaba GÜRai...")

if soru:
    with st.spinner('GÜRai düşünüyor...'):
        try:
            # Yapay zekadan cevap al
            response = model.generate_content(soru)
            
            # Cevabı ekrana yazdır
            st.success("GÜRai'nin Yanıtı:")
            st.write(response.text)
            
        except Exception as e:
            # Hata oluşursa kırmızı kutuda göster
            st.error(f"Bir hata oluştu: {e}")
            st.info("İpucu: API anahtarını ve internet bağlantını kontrol et.")

# Alt bilgi
st.markdown("---")
st.caption("GÜRai Project - Powered by Gemini 1.5 Flash")
