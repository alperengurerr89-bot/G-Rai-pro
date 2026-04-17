import streamlit as st
import requests
import time
from streamlit_mic_recorder import speech_to_text

# --- YAPILANDIRMA ---
# Ngrok linkin sabit kaldı, tünel açık olduğu sürece dokunma.
OLLAMA_URL = "https://enchilada-dullness-decimal.ngrok-free.dev/api/generate"

st.set_page_config(page_title="GÜRai Pro", page_icon="🛡️", layout="wide")

# --- SES VE TASARIM ---
st.markdown("""
    <script>
    function speak(text) {
        window.speechSynthesis.cancel();
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'tr-TR';
        utterance.rate = 1.1;
        window.speechSynthesis.speak(utterance);
    }
    </script>
    <style>
    .main { background-color: #0e1117; color: white; }
    .stChatMessage { border-radius: 15px; border: 1px solid #333; background-color: #1a1c24; margin-bottom: 10px; }
    .stButton > button { border-radius: 20px; width: 100%; background-color: #ff4b4b; color: white; border: none; }
    .live-status { color: #ff4b4b; font-weight: bold; animation: blinker 1.5s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    </style>
    """, unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- YAN MENÜ (SIDEBAR) ---
with st.sidebar:
    st.title("🛡️ GÜRai Panel")
    
    # İSTEDİĞİN 5 KATEGORİ BURADA
    st.subheader("🧠 Zeka Kategorileri")
    selected_model = st.selectbox(
        "Modeli Değiştir:", 
        ["llama3", "gemma", "mistral", "phi3", "codellama"],
        help="Her modelin uzmanlık alanı farklıdır."
    )
    
    st.divider()
    
    st.subheader("🎙️ Live Modu")
    # Sesli giriş butonu
    text_input = speech_to_text(
        language='tr',
        start_prompt="🎤 Sesli Sor",
        stop_prompt="⏹️ Gönder",
        just_once=True,
        key='speech'
    )
    
    st.divider()
    if st.button("🗑️ Sohbeti Temizle"):
        st.session_state.messages = []
        st.rerun()
    
    st.caption("Geliştirici: Alperen Gürer")

# --- ANA EKRAN ---
st.title("🛡️ GÜRai Pro")
st.caption(f"Aktif Zeka: {selected_model.upper()} | RTX 3050")

# Eski Mesajları Göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Giriş Kontrolü (Sesli veya Yazılı)
prompt = None
if text_input:
    prompt = text_input
elif manual_input := st.chat_input("GÜRai'ye bir mesaj yazın..."):
    prompt = manual_input

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        
        try:
            # --- DOĞRU CEVAP İÇİN KARAKTER VE HAFIZA ---
            system_prompt = (
                "Senin adın GÜRai. Alperen Gürer tarafından geliştirildin. "
                "Kesinlikle TÜRKÇE konuşmalısın. Sorulara mantıklı ve doğru cevaplar ver."
            )
            
            # Son 5 mesajı hafızaya alalım ki konu dağılmasın
            memory = ""
            for msg in st.session_state.messages[-5:]:
                memory += f"{msg['role']}: {msg['content']}\n"

            payload = {
                "model": selected_model, 
                "prompt": f"{system_prompt}\n\nGeçmiş:\n{memory}\nAssistant:", 
                "stream": False,
                "options": {
                    "temperature": 0.4, # Daha az saçmalaması için düşük sıcaklık
                    "num_ctx": 4096      # Hafıza kapasitesi
                }
            }
            
            headers = {
                "Content-Type": "application/json",
                "ngrok-skip-browser-warning": "true"
            }
            
            response = requests.post(OLLAMA_URL, json=payload, headers=headers, timeout=120)
            
            if response.status_code == 200:
                full_response = response.json().get("response", "").strip()
                
                # Yazma Efekti
                temp_text = ""
                for char in full_response:
                    temp_text += char
                    message_placeholder.markdown(temp_text + "▌")
                    time.sleep(0.01)
                
                message_placeholder.markdown(full_response)
                
                # Sesli Okutma
                st.components.v1.html(f"""
                    <script>window.parent.speak("{full_response.replace('"', "'").replace('\\', '')}");</script>
                """, height=0)
                
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            else:
                st.error(f"Hata: {selected_model} hazır değil. Terminale 'ollama pull {selected_model}' yaz!")
        except:
            st.error("Bağlantı koptu! Terminal 1 açık mı?")

st.divider()
st.caption("Balıkesir / 2026")
