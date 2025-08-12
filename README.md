# Mackolik API (Firebase Functions - Python)

Bu proje, Mackolik arşivinden maç ve oran verilerini scrape ederek Firebase Realtime Database’e yazan bir Cloud Functions (Python) uygulamasıdır.

## Özellikler
- **HTTP ile tetiklenen fonksiyonlar**:
  - `mackolik`: Basit sağlık kontrolü ("Hello world!")
  - `digersekme`: Mackolik arşivinden aktif maç kodlarını toplar, her maç için oranları çeker ve `maclar` düğümüne yazar
- **Scraping**: `requests` + `beautifulsoup4` (BS4)
- **Firebase Realtime Database** entegrasyonu
- **Uzun scraping işlemi**: `digersekme` fonksiyonunda `timeout_sec=540`

## Mimari
- `functions/main.py`: Tüm fonksiyonlar ve scraping mantığı
  - `get_match_code()` → `https://arsiv.mackolik.com/Iddaa-Programi` içinden maç kodlarını toplar
  - `maclar(matches)` → Her maç için `https://arsiv.mackolik.com/Match/Default.aspx?id={match_code}` sayfasından oranları parse eder
  - `digersekme` → Yukarıdaki iki fonksiyonu birleştirip sonuçları Realtime DB `maclar` düğümüne `update` eder
- `firebase.json`: Çalışma zamanı (`python313`) ve RTDB kural dosyası (`dbrules.json`) ayarı
- `dbrules.json`: Realtime Database kuralları (geliştirme için herkese açık; prod için kısıtlayın)
- `functions/requirements.txt`: Bağımlılıklar

## Gereksinimler
- Python 3.13 (önerilen, `firebase.json` ile uyumlu)
- Firebase CLI (giriş ve dağıtım için)
- Bir Firebase projesi (Realtime Database etkin)

## Kurulum (Yerel)
Windows PowerShell için örnek:
```powershell
# Proje kökünden çalıştırın
python -m venv functions\venv
functions\venv\Scripts\python -m pip install --upgrade pip

# Önemli: yalnızca 'beautifulsoup4' kullanın
functions\venv\Scripts\python -m pip install -r functions\requirements.txt
```


## Dağıtım
```powershell
firebase login
firebase use <PROJE_ID>
firebase deploy --only functions
```
- Varsayılan bölge genellikle `us-central1`.

## Kullanım
Dağıtımdan sonra fonksiyon URL’leri (örnek):
- `mackolik`: `https://us-central1-<PROJE_ID>.cloudfunctions.net/mackolik`
- `digersekme`: `https://us-central1-<PROJE_ID>.cloudfunctions.net/digersekme`

Örnek istek:
```powershell
# Sağlık kontrolü
Invoke-WebRequest "https://us-central1-<PROJE_ID>.cloudfunctions.net/mackolik"

# Scrape + DB yazma
Invoke-WebRequest "https://us-central1-<PROJE_ID>.cloudfunctions.net/digersekme"
```

## Veri Şeması (Realtime Database: `maclar`)
`digersekme` çağrısı sonrasında Realtime DB’de `maclar` düğümünde şu biçimde kayıtlar oluşur:
```json
{
  "1234567": {
    "Taraflar": "TakımA - TakımB",
    "Maç Kodu": 1234567,
    "MS 1": "1.65",
    "MS X": "3.20",
    "MS 2": "2.45"
  },
  "2345678": { "...": "..." }
}
```
Notlar:
- Alan adları `/` içermeyecek şekilde normalize edilir (örn. `/` → `-`).
- `.` karakterleri anahtar adlarında `'nci` ile değiştirilir (Firebase RTDB anahtar kısıtları).
- Oran `-` ise `"1"` olarak normalize edilir.

## Güvenlik
`dbrules.json` şu an herkese açık (geliştirme amaçlı):
```json
{
  "rules": { 
    ".read": true,
    ".write": true
  }
}
```
Üretimde mutlaka kimlik doğrulama ve yetkilendirme kısıtları tanımlayın.

## Performans ve Limitler
- `max_instances=10`: Ani trafik artışına karşı maliyet/performans dengesini sağlar.
- `timeout_sec=540`: Scraping uzun sürebilir. Ücretsiz kota ve hedef sitenin kullanım şartlarını dikkate alın.
- Periyodik çalıştırma gerekiyorsa Cloud Scheduler + IAM ile güvenli tetikleme düşünün.

## Geliştirme İpuçları
- Yerel testlerde etik scraping yapın, istekleri aralıklı gönderin.
- Çok sık tetikleme gerekiyorsa oranı düşürün ve hedef siteyi aşırı yüklemeyin.

## Lisans ve Yasal Uyarı
Bu proje, eğitim/deney amaçlı scraping içerir. Hedef sitenin kullanım şartlarına, robots.txt politikasına ve yerel yasalara uyduğunuzdan emin olun. Üçüncü taraf içerik ve markalar ilgili sahiplerine aittir.


