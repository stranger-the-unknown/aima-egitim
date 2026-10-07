# Bölüm 24 — Doğal dil işleme için derin öğrenme

> AIMA 4. baskı, Bölüm 24 · *Deep Learning for Natural Language Processing*

## Öğrenme hedefleri

1. One-hot gösterimin sorununu ve sözcük gömmelerinin nasıl öğrenildiğini açıklamak.
2. Gömmelerle benzerlik ve benzetme hesaplamak.
3. RNN tabanlı dizi-dizi modellerinin sınırlarını ve dikkatin bunları nasıl giderdiğini açıklamak.
4. Öz-dikkati, çok başlı dikkati, konum gömmesini ve maskeyi hesaplamak.
5. Açgözlü kod çözme ile ışın aramasını karşılaştırmak.
6. Önceden eğitme, bağlamsal temsiller ve maskeli dil modellerini açıklamak.

## Çalışma sırası

1. Kitapta Bölüm 24'ü oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır (yalnızca numpy gerekir).
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/gomme.py` | One-hot ve gömme, birlikte geçme + PPMI + SVD, kosinüs benzerliği, benzetmeler |
| `ornekler/dikkat.py` | Dizi-dizi dikkati, öz-dikkat, maske, çok başlı dikkat, sin/cos konum kodlaması, √d ölçekleme |
| `ornekler/kod_cozme.py` | Açgözlü kod çözme ve ışın araması (Şekil 24.8'deki çeviri örneği) |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A3, A5, A6, A8, A9 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch24_derin_dil.py`:

| Değer | Kitap | Kod |
|---|---|---|
| One-hot benzerlik | Benzerlik taşımaz | ✔ kosinüs 0 |
| Benzetme | "Athens is to Greece as Oslo is to …" → Norway | ✔ (yapay gömmeler) |
| Dikkat | rᵢⱼ = hᵢ₋₁ · sⱼ, softmax, cᵢ = Σ aᵢⱼ sⱼ | ✔ A5 elle hesapla aynı |
| Öz-dikkat | rᵢⱼ = (qᵢ · kⱼ)/√d; olasılıkların toplamı 1 | ✔ |
| Sıraya duyarsızlık | Öz-dikkat sözcük sırasını bilmez | ✔ permütasyon testi; konum eklenince bozulur |
| Kod çözücü maskesi | Her sözcük yalnızca öncekilere bakar | ✔ üst üçgen 0 |
| Işın araması | Şekil 24.8: "La entrada" ışından düşer, "La puerta de entrada es roja" | ✔ (olasılıklar bizim varsayımımız) |
| Işın genişliği | Günümüz modelleri 4–8, eski istatistiksel modeller 100+ | notlarda |
| Maskeli dil modeli | Çift yönlü bağlam | ✔ A9 |

Bizim seçimlerimiz: Kitaptaki transformer konum gömmelerini öğrenir; kodumuz öğrenme yapmadığı için sabit sin/cos kodlaması kullanır. Gömme örnekleri küçük bir Türkçe derlemle ve elle kurulmuş yapay vektörlerle çalışır; gerçek GloVe/word2vec sonuçlarını taklit etmez.
