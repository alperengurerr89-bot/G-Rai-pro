import subprocess
import time
import os

def gurai_sistemini_uyandir():
    print("🚀 GÜRai Sistemleri Uyandırılıyor...")

    # 1. ADIM: Ollama'yı özel izinle başlat
    print("🦙 Ollama servisi başlatılıyor...")
    # Bu satır Ollama'yı arka planda senin o yıldızlı ayarınla açar
    env = os.environ.copy()
    env["OLLAMA_ORIGINS"] = "*"
    subprocess.Popen(["ollama", "serve"], env=env, creationflags=subprocess.CREATE_NEW_CONSOLE)
    
    time.sleep(3) # Ollama'nın kendine gelmesi için 3 saniye bekle

    # 2. ADIM: Ngrok tünelini aç
    print("🔗 Ngrok tüneli kuruluyor...")
    domain = "enchilada-dullness-decimal.ngrok-free.dev"
    ngrok_command = f"ngrok http 11434 --domain={domain}"
    subprocess.Popen(ngrok_command, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)

    print("\n✅ HER ŞEY HAZIR!")
    print(f"🌍 Site Adresin: https://{domain}")
    print("⚠️  Uyarı: Açılan siyah pencereleri kapatma, onlar GÜRai'nin motorları.")
    print("--------------------------------------------------")

if __name__ == "__main__":
    gurai_sistemini_uyandir()
