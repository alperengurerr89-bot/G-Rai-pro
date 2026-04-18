import streamlit as st
import requests

# Linkinin doğru olduğundan emin ol
BASE_URL = "https://enchilada-dullness-decimal.ngrok-free.dev"

st.title("🛡️ GÜRai Teknik Servis Modu")

if st.button("Bağlantıyı Kontrol Et"):
    try:
        # Ngrok'un o sinir bozucu mavi ekranını geçmek için özel başlık ekledik
        headers = {"ngrok-skip-browser-warning": "true"}
        res = requests.get(f"{BASE_URL}/api/tags", headers=headers, timeout=10)
        
        if res.status_code == 200:
            st.success("✅ BAŞARILI! Bilgisayarına ulaştım.")
            st.write("Yüklü Modellerin:", res.json())
        else:
            st.error(f"❌ Kapı kilitli! Hata Kodu: {res.status_code}")
            st.info("Ollama'yı kapatıp '$env:OLLAMA_ORIGINS=\"*\"; ollama serve' komutuyla açtığından emin ol.")
    except Exception as e:
        st.error(f"❌ Bağlantı tamamen kopuk: {e}")

prompt = st.chat_input("Llama'ya bir şey yaz...")
if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    
    with st.chat_message("assistant"):
        try:
            headers = {"ngrok-skip-browser-warning": "true"}
            response = requests.post(
                f"{BASE_URL}/api/generate",
                json={"model": "llama3", "prompt": prompt, "stream": False},
                headers=headers
            )
            st.write(response.json().get("response"))
        except:
            st.error("Mesaj gönderilemedi. Ngrok terminalini kontrol et.")
