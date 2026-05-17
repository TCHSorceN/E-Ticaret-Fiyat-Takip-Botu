import requests
from bs4 import BeautifulSoup
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import time
import json 
import csv # Excel uyumlu veri kaydetmek için ekledik
import os  # Dosya kontrolü yapmak için ekledik
from datetime import datetime # Tarih ve saat bilgisi için ekledik

# --- GİZLİ AYARLARI DOSYADAN OKUMA ---
try:
    with open("config.json", "r", encoding="utf-8") as dosya:
        ayarlar = json.load(dosya)
        
    GONDEREN_MAIL = ayarlar["gonderen_mail"]
    ALICI_MAIL = ayarlar["alici_mail"]
    GOOGLE_UYGULAMA_SIFRESI = ayarlar["google_sifre"]
except Exception as e:
    print("❌ config.json dosyası okunurken hata oluştu! Hata:", e)
    exit() 


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

urun_listesi = [
    {
        "urun_adi": "SteelSeries Arctis Nova 7P",
        "url": "https://www.itopya.com/steelseries-arctis-nova-7p-gen2-kablosuz-siyah-gaming-kulaklik_u30976",
        "hedef_fiyat": 9500
    },
    {
        "urun_adi": "Asus TUF Gaming Monitör",
        "url": "https://www.itopya.com/asus-tuf-gaming-vg279qm5a-27-240hz-03ms-hdmi-dp-g-sync-freesync-premium-fhd-fast-ips-gaming-monito_u30385",
        "hedef_fiyat": 8499
    }
]

def fiyat_kontrol_et(urun):
    print(f"\n[BİLGİ] {urun['urun_adi']} için fiyat kontrolü başlatılıyor...")
    try:
        sayfa = requests.get(urun["url"], headers=headers)
        soup = BeautifulSoup(sayfa.content, "html.parser")

        fiyatlar = []
        for etiket in soup.find_all(["div", "span", "strong"]):
            metin = etiket.text.strip()
            if "TL" in metin and len(metin) < 20:
                temiz_metin = metin.replace("TL", "").replace(".", "").split(",")[0].strip()
                if temiz_metin.isdigit(): 
                    fiyatlar.append(int(temiz_metin))

        if not fiyatlar:
            print(f"❌ {urun['urun_adi']} için fiyat bulunamadı.")
            return

        guncel_fiyat = min(fiyatlar)
        print(f"[BAŞARILI] Güncel Fiyat: {guncel_fiyat} TL")

        # --- 📊 2. YÖNTEM: EXCEL / CSV DOSYASINA KAYDETME KISMI ---
        su_an = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # Şu anki tarih ve saati aldık
        dosya_var_mi = os.path.exists("fiyat_gecmisi.csv")   # Dosya daha önce oluşturulmuş mu?
        
        # Dosyayı "append" (ekleme) modunda açıyoruz. encoding="utf-8-sig" Excel'de Türkçe karakterlerin düzgün görünmesini sağlar.
        with open("fiyat_gecmisi.csv", "a", newline="", encoding="utf-8-sig") as f:
            yazar = csv.writer(f, delimiter=";") # Hücreleri noktalı virgül ile ayırıyoruz (Excel standardı)
            
            # Eğer dosya bilgisayarda ilk kez açılıyorsa en üste başlık sütunlarını yazıyoruz
            if not dosya_var_mi:
                yazar.writerow(["Tarih", "Urun Adi", "Fiyat (TL)"])
                
            # Veriyi satır olarak ekliyoruz
            yazar.writerow([su_an, urun["urun_adi"], guncel_fiyat])
            print(f"💾 {urun['urun_adi']} fiyatı Excel dosyasına kaydedildi.")


        # --- E-POSTA KONTROL KISMI ---
        if guncel_fiyat <= urun["hedef_fiyat"]:
            print("🔥 Fiyat düştü! E-posta gönderiliyor...")
            mesaj = MIMEMultipart()
            mesaj["From"] = GONDEREN_MAIL
            mesaj["To"] = ALICI_MAIL
            mesaj["Subject"] = f"Fiyat Dustu! {urun['urun_adi']}"
            
            icerik = f"Sef Mujde! {urun['urun_adi']} fiyati {guncel_fiyat} TL oldu. Satin al:\n{urun['url']}"
            mesaj.attach(MIMEText(icerik, "plain"))
            
            sunucu = smtplib.SMTP("smtp.gmail.com", 587)
            sunucu.starttls()
            sunucu.login(GONDEREN_MAIL, GOOGLE_UYGULAMA_SIFRESI)
            sunucu.sendmail(GONDEREN_MAIL, ALICI_MAIL, mesaj.as_string())
            sunucu.quit()
            print(f"✅ {urun['urun_adi']} bildirimi başarıyla gönderildi!")
        else:
            print(f"❌ {urun['urun_adi']} fiyatı hala yüksek, e-posta atılmadı.")

    except Exception as hata:
        print(f"❌ {urun['urun_adi']} kontrol edilirken hata oluştu:", hata)

print("🤖 Çoklu Ürün ve Fiyat Arşivi Botu Başlatıldı!")

while True:
    for her_bir_urun in urun_listesi:
        fiyat_kontrol_et(her_bir_urun)
        time.sleep(2) 
    
    print("\n💤 Tüm liste kontrol edildi. 30 saniye boyunca uyunuyor...")
    time.sleep(30)