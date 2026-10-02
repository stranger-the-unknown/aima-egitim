# Bölüm 16 — Basit kararlar almak

> AIMA 4. baskı, Bölüm 16 · *Making Simple Decisions*

## Öğrenme hedefleri

1. Beklenen faydayı hesaplamak ve MEU ilkesiyle eylem seçmek.
2. Fayda kuramının altı aksiyomunu ve birinin çiğnenmesinin neden akıl dışı davranışa yol açtığını açıklamak.
3. Paranın faydasını, risk tutumlarını, kesinlik eşdeğerini ve sigorta primini yorumlamak.
4. İyileştiricinin lanetini ve insan kararlarındaki bilinen sapmaları tanımak.
5. Çok nitelikli kararlarda baskınlığı ve toplamsal değer fonksiyonunu kullanmak.
6. Bir karar ağını kurmak ve değerlendirmek.
7. Mükemmel bilginin değerini (VPI) hesaplamak.
8. Tercih belirsizliğinin makineyi neden insana danışmaya yönelttiğini açıklamak.

## Çalışma sırası

1. Kitapta Bölüm 16'yı oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/fayda_kurami.py` | Yarışma kumarı, Bay Beard'ın fayda fonksiyonu, kesinlik eşdeğeri, Allais, Ellsberg, para pompası |
| `ornekler/iyimserlik_laneti.py` | İyileştiricinin laneti: integral ve simülasyon, ilaç denemesi |
| `ornekler/karar_agi.py` | Stokastik baskınlık, havalimanı karar ağı, eylem–fayda tablosu |
| `ornekler/bilgi_degeri.py` | Genel VPI, petrol örneği, VPI özellikleri, miyop bilgi toplayan ajan |
| `ornekler/bilinmeyen_tercihler.py` | Durian dondurması, kapatma düğmesi oyunu |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A4–A7, A9, A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch16_kararlar.py`:

| Değer | Kitap | Kod |
|---|---|---|
| Yarışma: EMV(kumar), EU(kumar), EU(al) | 1 250 000 $; 7; 8 | ✔ |
| İyileştiricinin laneti, beklenen şişkinlik | k = 3: ~0.85σ; k = 30: ~2σ | ✔ |
| Allais ve Ellsberg | tutarlı fayda / dünya yok | ✔ |
| Stokastik baskınlık | S1 ~ U[2.8, 4.8] baskılar S2 ~ U[3.0, 5.2] | ✔ |
| Petrol VPI | C/n | ✔ (tam kesirle) |
| Durian | EU(durian) = +8 > EU(vanilya) = +1 | ✔ |
| Kapatma düğmesi, u ~ U[−40, 60] | hemen yap +10, bekle +18 | ✔ |
| Hazine avı | en iyi sıra P/C'ye göre | ✔ (kaba kuvvetle) |
| Mikromort | 400 mikromort, 60 $ / mikromort | ✔ |

Kitap havalimanı karar ağının olasılıklarını vermez; `karar_agi.py`'deki sayılar varsayımdır.
