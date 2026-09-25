# Bölüm 26 — Robotik: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe öğretim dilindedir.
> Amaç: mobil/manipülatör robotların temel problem dilini kurmak; toy kodla sezgi.

---

## 1. Algı–eylem döngüsü

Bir robot sürekli şunu yapar:

```text
algıla (sensör) → durumunu tahmin et → eylem seç → motorlara uygula → tekrarla
```

- **Algı:** kamera, lidar, enkoder, IMU…
- **Durum:** konum, yönelim, eklem açıları, hız…
- **Eylem:** tekerlek hızı, eklem torku, tutucu kapat…

Belirsizlik her yerdedir: sensör gürültüsü, kayma, dinamik engeller. Bu yüzden olasılıksal filtreler (Ch.14 ile bağ) robotikte doğal bir araçtır.

---

## 2. Konfigürasyon uzayı (C-space) sezgisi

Robotun "nerede olduğu" yalnızca (x,y) değildir. Bir kol için eklem açıları (θ₁, θ₂, …) tüm **konfigürasyonu** tanımlar.

- **Serbest C-space:** çarpışmasız konfigürasyonlar
- **Engel C-space:** bir engelin robot gövdesinde çarpışmaya yol açtığı konfigürasyonlar

Sezgi: çalışma uzayında "küçük engel", C-space'te robotun geometrisine göre şişmiş bir yasak bölge olabilir. Planlama genelde C-space'te yapılır.

```text
çalışma uzayı: masa üzerindeki nesneler
C-space:       kolun açı kombinasyonları → hangileri masaya çarpar?
```

---

## 3. Lokalizasyon ve haritalama (taslak)

- **Lokalizasyon:** harita biliniyor; "ben neredeyim?"
- **Haritalama:** konum kabaca biliniyor; "çevre nasıl?"
- **SLAM:** ikisini birlikte (eşzamanlı lokalizasyon ve haritalama)

Ayrık Bayes filtresi (ızgara): her hücre için "burada olma" olasılığı; hareket tahmin eder, landmark gözlemi günceller.

`grid_lokalizasyon.py` küçük bir koridorda landmark'larla bu döngüyü gösterir.

---

## 4. Yol planlama vs kontrol

| Katman | Soru | Örnek |
|--------|------|--------|
| **Planlama** | Hangi yoldan / hangi ara hedefler? | A*, RRT, potansiyel alan |
| **Kontrol** | Bu an motorlara ne komut? | PID, model öngörülü kontrol |

Plan "gidilecek hücre dizisi" verebilir; kontrol o hücrelere yaklaşırken tekerlek hızlarını ayarlar. Gerçekte kayma ve gecikme yüzünden plan sık sık yeniden yapılır (**yeniden planlama**).

`potansiyel_alan_path.py` ızgara üzerinde çekim (hedefe) + itme (engelden) ile basit bir gradyan inişi yolu üretir. Yerel minimum riski toy örneğin sınırıdır — tartışma konusu.

---

## 5. İnsan–robot etkileşimi (üst düzey)

Robot yalnız değildir: fabrika, ev, hastane, sokak.

Üst düzey başlıklar (vaaz değil, kontrol listesi):

- **Güvenlik:** acil durdurma, sınırlı kuvvet, öngörülebilir hareket
- **İletişim:** niyetin anlaşılması (ışık, ses, ekran, jest)
- **Güven / şeffaflık:** operatör ne beklemeli?
- **Paylaşılan alan:** hız, mesafe, öncelik kuralları

Etik ve güvenlik tartışmasının devamı Ch.27'de.

---

## 6. Bu bölümün kodu neyi gösterir?

| Dosya | Sezgi |
|-------|--------|
| `grid_lokalizasyon.py` | predict–update lokalizasyon |
| `potansiyel_alan_path.py` | çekim/itme ile yol |

İkisi de eğitici oyuncak; gerçek robot stack'i (ROS 2, hareket planlama kütüphaneleri) ayrı bir öğrenme yoludur — bkz. Ch.28 yetenek haritası.
