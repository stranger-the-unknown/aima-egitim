# Bölüm 12 — Belirsizliği nicelendirme

> AIMA 4. baskı, Bölüm 12 · *Quantifying Uncertainty*

## Öğrenme hedefleri

1. Mantığın belirsiz alanlarda neden yetersiz kaldığını ve karar kuramının ne eklediğini açıklamak.
2. Olası dünyalar, önsel ve koşullu olasılık, çarpım kuralı ve aksiyomlarla çalışmak.
3. Tam ortak dağılımdan marjinalleştirme ve normalizasyonla her sorguyu yanıtlamak.
4. Mutlak ve koşullu bağımsızlığın temsili nasıl küçülttüğünü göstermek.
5. Bayes kuralını ve naif Bayes modelini uygulamak; Wumpus dünyasında olasılıkla karar vermek.

## Çalışma sırası

1. Kitapta Bölüm 12'yi oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/olasilik.py` | Kütüphane: tam ortak dağılım, P(olay \| kanıt), normalizasyon, marjinal, bağımsızlık testi; iki zar |
| `ornekler/dis_hekimi.py` | Kitaptaki Toothache–Catch–Cavity tablosu; bağımsızlık ve koşullu bağımsızlık; hava durumu |
| `ornekler/bayes_kurali.py` | Menenjit (0.0014), salgın, kanıtları birleştirme, nadir hastalık testi, odds biçimi |
| `ornekler/hollanda_kitabi.py` | de Finetti: tutarsız inançlara karşı garanti kaybettiren bahisler |
| `ornekler/naive_bayes_mini.py` | Kelime sayılarıyla naif Bayes metin sınıflandırma, Laplace yumuşatma |
| `ornekler/wumpus_olasilik.py` | Çukur olasılıkları: tam toplam (4096 terim) ve sınır yöntemi (4 terim) |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A4–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch12_olasilik.py`:

| Değer | Kitap | Kod |
|---|---|---|
| P(Toplam = 11), iki adil zar | 1/18 | ✔ |
| P(cavity), P(cavity ∨ toothache) | 0.2, 0.28 | ✔ |
| P(Cavity \| toothache) | ⟨0.6, 0.4⟩ | ✔ |
| P(Cavity \| toothache, catch) | ≈ ⟨0.871, 0.129⟩ | ✔ |
| Toothache ⊥ Catch \| Cavity | koşullu bağımsız, mutlak bağımsız değil | ✔ |
| Menenjit P(m \| s) | 0.0014 | ✔ |
| Hollanda kitabı (P(a)=0.4, P(b)=0.3, P(a∧b)=0, P(a∨b)=0.8) | −11, −1, −1, −1 | ✔ |
| Wumpus P(P₁,₃), P(P₂,₂) | ≈ 0.31, ≈ 0.86 | ✔ |
