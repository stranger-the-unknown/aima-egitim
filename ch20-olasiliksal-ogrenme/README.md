# Bölüm 20 — Olasılıksal modelleri öğrenmek

> AIMA 4. baskı, Bölüm 20 · *Learning Probabilistic Models*
> (Klasörün eski adı `ch20-bilgi-ogrenme` idi.)

## Öğrenme hedefleri

1. Bayesçi, MAP ve en büyük olabilirlik öğrenmeyi karşılaştırmak.
2. Ayrık Bayes ağı parametrelerini sayımlarla öğrenmek; sıfır sayım sorununu düzeltmek.
3. Naif Bayes'i öğrenmek; üretici ve ayırt edici modelleri ayırt etmek.
4. Gauss ve doğrusal–Gauss modeller için en büyük olabilirliği türetmek.
5. Beta önselleriyle Bayesçi parametre öğrenmeyi ve Bayesçi doğrusal regresyonu uygulamak.
6. EM algoritmasını izlemek; yerel en büyükleri ve tanımlanabilirliği açıklamak.

## Çalışma sırası

1. Kitapta Bölüm 20'yi oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/istatistiksel_ogrenme.py` | Şeker torbaları: Bayesçi, MAP, ML, MDL; ambalaj ağı; Laplace; Beta önselleri |
| `ornekler/naif_bayes.py` | Naif Bayes (Bölüm 19'un restoran verisiyle), üretici vs ayırt edici |
| `ornekler/surekli_modeller.py` | Gauss ML, doğrusal–Gauss, Bayesçi doğrusal regresyon, k-NN ve çekirdek yoğunluk |
| `ornekler/em_algoritmasi.py` | Karışmış torbalar için EM (kitap değerleri), tanımlanabilirlik, Gauss karışımı, 78 / 708 parametre |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A3, A5–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch20_olasiliksal_ogrenme.py`:

| Değer | Kitap | Kod |
|---|---|---|
| P(sonraki limon) | 0.5 → 0.65 (1 limon) → ≈ 0.8 (3 limon) | ✔ |
| MAP sırası | h3 (1 limon), h4 (2), h5 (≥ 3) | ✔ |
| Beta dizisi | Beta(3,1), Beta(6,2), Beta(30,10), ortalama 0.75 | ✔ |
| EM ilk yineleme | θ = 0.6124, θF1 = 0.6684, θW1 = 0.6483, θH1 = 0.6558, θF2 = 0.3887, θW2 = 0.3817, θH2 = 0.3827 | ✔ |
| 273 şekerin katkısı | 0.22797 | ✔ |
| Log olabilirlik | −2044 → −2021; gerçek model −1982.214; 10. yinelemede geçilir | ✔ |
| Kalp hastalığı ağı | 78 ve 708 parametre | ✔ |
| Bayesçi doğrusal regresyon | θ_N, σ_N² kapalı biçimi | ✔ (sayısal integralle) |
