# Bölüm 14 — Zaman içinde olasılıksal akıl yürütme

> AIMA 4. baskı, Bölüm 14 · *Probabilistic Reasoning over Time*

## Öğrenme hedefleri

1. Zamanla değişen bir dünyayı durum ve gözlem değişkenleriyle, geçiş ve algılayıcı modelleriyle kurmak.
2. Filtreleme, tahmin, yumuşatma ve en olası dizi görevlerini ayırt edip hesaplamak.
3. HMM'lerin matris algoritmalarını uygulamak (ileri–geri, Viterbi).
4. Kalman filtresinin güncellemesini yorumlamak; ne zaman yetersiz kaldığını bilmek.
5. DBN'lerin HMM'lerden neden daha tıkız olduğunu açıklamak ve parçacık filtresi uygulamak.

## Çalışma sırası

1. Kitapta Bölüm 14'ü oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/zamansal.py` | Kütüphane: HMM; filtreleme, tahmin, olabilirlik, ileri–geri yumuşatma, Viterbi, durağan dağılım |
| `ornekler/semsiye.py` | Kitabın şemsiye dünyası: bütün sayılarıyla |
| `ornekler/lokalizasyon.py` | Labirentte HMM ile robot konumlandırma; algılayıcı hatasının etkisi |
| `ornekler/kalman.py` | Tek boyutlu Kalman (kitaptaki şekil), varyansın yakınsaması, konum–hız izleme |
| `ornekler/pil_sensoru.py` | DBN'de algılayıcı arızaları: Gauss, geçici ve kalıcı arıza modelleri |
| `ornekler/parcacik_filtresi.py` | Parçacık filtresi ve yeniden örneklemesiz SIS karşılaştırması |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A2, A4–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch14_zamansal.py`:

| Değer | Kitap | Kod |
|---|---|---|
| P(R_1 \| u_1), P(R_2 \| u_1), P(R_2 \| u_1, u_2) | ⟨0.818, 0.182⟩, ⟨0.627, 0.373⟩, ⟨0.883, 0.117⟩ | ✔ |
| Geri mesaj b_{2:2}, P(R_1 \| u_1, u_2) | ⟨0.69, 0.41⟩, ⟨0.883, 0.117⟩ | ✔ |
| Viterbi mesajları ve yolu, [u, u, ¬u, u, u] | .8182/.1818 … .0210/.0024; yağmur, yağmur, kuru, yağmur, yağmur | ✔ |
| Durağan dağılım | ⟨0.5, 0.5⟩ | ✔ |
| Kalman (μ₀ = 0, σ₀ = 1.5, σx = 2, σz = 1, z₁ = 2.5) | tahmin N(0, 6.25) → N(2.155, 0.862) | ✔ |
