# Bölüm 21 — Derin öğrenme

> AIMA 4. baskı, Bölüm 21 · *Deep Learning*

## Öğrenme hedefleri

1. Bir ileri beslemeli ağı hesap grafiği olarak yazmak; geri yayılımı türetmek.
2. Aktivasyonları, softmax'ı ve çapraz entropi kaybını açıklamak.
3. Evrişim, adım, dolgu, alıcı alan ve havuzlamayı hesaplamak.
4. Kaybolan gradyanı ve çarelerini (ReLU, artık bağlantı, toplu normalleştirme, LSTM) açıklamak.
5. Ağırlık bozunumu ve dropout'u açıklamak.
6. Doğrusal otokodlayıcı ile PCA ilişkisini göstermek; üretici modelleri tanımak.

## Çalışma sırası

1. Kitapta Bölüm 21'i oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır (yalnızca numpy gerekir).
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/hesap_grafigi.py` | Aktivasyonlar, Şekil 21.3 ağı, geri yayılım (sayısal gradyanla doğrulanır), softmax, çapraz entropi, kaybolan gradyan |
| `ornekler/cnn.py` | 1B evrişim (Şekil 21.4), matris biçimi, alıcı alan, havuzlama, 2B kenar bulucu, parametre paylaşımı, artık katman |
| `ornekler/mlp_egitim.py` | numpy MLP: XOR, SGD/momentum, ağırlık bozunumu, dropout, toplu normalleştirme, artık bağlantı |
| `ornekler/rnn.py` | Temel RNN, BPTT'de kaybolan gradyan, hatırlama görevi, LSTM bellek çarpanı |
| `ornekler/otokodlayici.py` | PPCA verisi, PCA, doğrusal otokodlayıcı = PCA alt uzayı |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A2–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch21_derin_ogrenme.py`:

| Değer | Kitap | Kod |
|---|---|---|
| Softmax ⟨5, 2, 0, −2⟩ | ⟨0.946, 0.047, 0.006, 0.001⟩ | ✔ |
| Şekil 21.4 evrişimi | ⟨5, 9, 4⟩; matris biçimi (21.9) | ✔ |
| tanh = 2σ(2x) − 1; softplus' = σ | özdeşlikler | ✔ |
| Geri yayılım (21.4–21.5) | sonlu farklarla aynı | ✔ |
| Doğrusal otokodlayıcı | PCA alt uzayı | ✔ (temel açılar ≈ 0°) |
| XOR | gizli katmansız öğrenilemez, gizli katmanla öğrenilir | ✔ |
