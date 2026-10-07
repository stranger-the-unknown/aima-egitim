# Bölüm 25 — Bilgisayarlı görü

> AIMA 4. baskı, Bölüm 25 · *Computer Vision*

## Öğrenme hedefleri

1. Perspektif izdüşümü, kaybolma noktasını ve ölçekli ortografik yaklaşımı hesaplamak.
2. Lambert yasasıyla parlaklığı hesaplamak; parlaklık ve renk belirsizliklerini açıklamak.
3. Gauss düzeltmesi + türevle kenar bulmak; yön histogramıyla doku betimlemek.
4. SSD ile optik akış ölçmek; derinliği eşitsizlikten ve akıştan hesaplamak.
5. CNN'lerin neden iyi sınıflandırdığını açıklamak.
6. Nesne tespitinin adımlarını (öneri, NMS, değerlendirme) uygulamak.

## Çalışma sırası

1. Kitapta Bölüm 25'i oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır (yalnızca numpy gerekir).
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/goruntu_olusumu.py` | Perspektif izdüşüm, kaybolma noktası, ortografik yaklaşım, Lambert yasası, stereo derinlik, optik akış geometrisi |
| `ornekler/ozellikler.py` | Gauss türeviyle kenar (1B/2B), yön histogramı (doku), SSD optik akış, normalleştirilmiş kesme |
| `ornekler/tespit.py` | Konvolüsyon + ReLU desen dedektörleri, alıcı alan, pencere ve çapa sayıları, IoU, NMS, kesinlik/duyarlılık |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A2, A5–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch25_bilgisayarli_goru.py`:

| Değer | Kitap | Kod |
|---|---|---|
| Perspektif izdüşüm | x = −fX/Z, y = −fY/Z | ✔ |
| Kaybolma noktası | P∞ = (fU/W, fV/W) | ✔ uzak noktalar oraya yakınsar |
| Lambert yasası | I = ρ I₀ cos θ | ✔ |
| Stereo çözünürlük | b = 6 cm, δθ = 5″: Z = 100 cm → 0.4 mm, Z = 30 cm → 0.036 mm | ✔ |
| Optik akış | vx = (−Tx + xTz)/Z; genişleme odağında 0; ölçek belirsizliği | ✔ |
| Düzeltme + türev | (f ∗ g)′ = f ∗ g′; düzeltme sahte tepeleri bastırır | ✔ |
| Gradyan yönü | Işık değişince değişmez | ✔ |
| Doku | Dikey çizgilerde iki tepe | ✔ |
| SSD | Beyaz duvarda kör tahmin | ✔ |
| Faster RCNN | Adım 16, 9 çapa kutusu | ✔ (640 × 480 → 10 800) |
| Pencere sayısı | O(n⁴) | ✔ (n(n+1)/2)² |

Bizim seçimlerimiz: NMS ve değerlendirmede IoU ≥ 0.5 (kitap belirli bir ölçü vermez); normalleştirilmiş kesmenin özvektörle yaklaşık çözümü ve benzerlik parametreleri; elle ayarlanmış 2. ve 3. katman ağırlıkları (gerçek CNN'de öğrenilir).
