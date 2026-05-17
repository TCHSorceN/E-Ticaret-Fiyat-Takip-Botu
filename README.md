# 🤖 Çoklu Ürün Fiyat Takip ve Veri Arşivi Botu

Bu proje, belirli e-ticaret sitelerindeki (İtopya) seçili ürünlerin fiyatlarını arka planda dinamik olarak takip eden, fiyat hedeflenen seviyeye düştüğünde kullanıcıya **otomatik e-posta bildirimi** gönderen ve tüm fiyat değişimlerini **Excel/CSV formatında arşivleyen** gelişmiş bir Python otomasyon botudur.

## 🚀 Öne Çıkan Özellikler

* **Çoklu Ürün Takibi:** Tek bir ürünle sınırlı kalmadan, bir liste içerisindeki sonsuz sayıda ürünü sırayla kontrol eder.
* **Dirençli Mimari (Error Handling):** Ağ kopmaları veya anlık site hatalarında programın çökmesini engelleyen `try-except` hata yönetim yapısına sahiptir. Bot hata alsa bile çalışmaya devam eder.
* **Siber Güvenlik Standartları (`config.json`):** E-posta ve uygulama şifreleri gibi hassas veriler ana kodun içinde ham metin olarak tutulmaz; harici bir JSON dosyasından güvenli bir şekilde okunur ve `.gitignore` ile korunur.
* **Veri Günlüğü & Arşivleme (Data Logging):** Botun yaptığı her tarama, gelecekte fiyat analizi ve grafik çıkarma işlemlerinde kullanılmak üzere `fiyat_gecmisi.csv` dosyasına tarih-saat damgasıyla kaydedilir.
* **Arka Plan Servisi:** Belirlenen periyotlarda (örn: 24 saatte bir) kendi kendine uyanarak insan müdahalesine ihtiyaç duymadan 7/24 çalışır.

## 🛠️ Kullanılan Teknolojiler

* **Python 3.x**
* **BeautifulSoup4 & Requests:** Web Scraping (Veri Kazıma) işlemleri için.
* **SMTPlib & Email:** Güvenli Google SMTP sunucusu üzerinden mail otomasyonu için.
* **JSON & CSV:** Güvenli veri okuma ve Excel uyumlu veri loglama için.

## 📦 Kurulum ve Çalıştırma

1. Projeyi bilgisayarınıza indirin.
2. Klasörün içinde `config.json` adında bir dosya oluşturup aşağıdaki şablonu kendi bilgilerinizle doldurun:
```json
{
    "gonderen_mail": "example@gmail.com",
    "alici_mail": "example@gmail.com",
    "google_sifre": "your_app_password"
}
