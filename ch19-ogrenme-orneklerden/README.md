# Bölüm 19 — Örneklerden öğrenme

> AIMA 4. baskı, Bölüm 19 · *Learning from Examples*

## Öğrenme hedefleri

1. Denetimli, denetimsiz ve pekiştirmeli öğrenmeyi; sınıflandırma ile regresyonu ayırt etmek.
2. Bilgi kazancıyla karar ağacı öğrenmek; aşırı uydurmayı budamayla azaltmak.
3. Eğitim, doğrulama ve test kümelerini doğru kullanmak; çapraz doğrulamayla model seçmek.
4. Kayıp, düzenlileştirme ve hiperparametre ayarını açıklamak.
5. PAC sınırıyla gereken örnek sayısını tahmin etmek.
6. Doğrusal regresyon, algılayıcı ve lojistik regresyonu uygulamak.
7. k-NN, SVM ve çekirdek hilesini açıklamak; boyutların lanetini göstermek.
8. Topluluk yöntemlerinin neden işe yaradığını açıklamak.

## Çalışma sırası

1. Kitapta Bölüm 19'u oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/karar_agaci.py` | Restoran verisi, entropi, bilgi kazancı, LEARN-DECISION-TREE, χ², karar listesi, öğrenme eğrisi |
| `ornekler/model_secimi.py` | Çapraz doğrulamayla model seçimi, kayıp fonksiyonları, PAC sınırı, boyutların laneti |
| `ornekler/dogrusal_modeller.py` | Regresyon (kapalı biçim, gradyan inişi), normal denklemler, L1/L2, algılayıcı, lojistik regresyon |
| `ornekler/parametrik_olmayan.py` | k-NN, normalleştirme, k-d ağacı, yerel ağırlıklı regresyon, SVM, çekirdek hilesi |
| `ornekler/topluluk.py` | Çoğunluk oyu, AdaBoost (karar kütükleri), torbalama, rastgele ağırlıklı çoğunluk |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A3–A6, A8–A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch19_ogrenme.py`:

| Değer | Kitap | Kod |
|---|---|---|
| Olası girdi sayısı | 9216 | ✔ |
| Entropiler | 1, 2, ≈ 0.08 bit | ✔ |
| Kazanç(Patrons), Kazanç(Type) | 0.541, 0 | ✔ |
| 12 örnekten öğrenilen ağaç | Şekil 19.6 | ✔ (birebir) |
| χ² eşikleri (3 sd) | 7.82, 11.35 | ✔ |
| Boyutların laneti | ℓ = 0.003, 0.02, ~0.5, 0.94; dış kabuk %2 → %98 | ✔ |
| Çoğunluk oyu | %89 (5 sınıflandırıcı), %99 (17) | ✔ |
| Rastgele ağırlıklı çoğunluk | 1.39 M* + 4.6; 1.15 M* + 9.2 | ✔ |
| Deprem/patlama sınırı | ⟨−4.9, 1.7, −1⟩ | ✔ (sentetik veride) |

Kitabın ev fiyatı ve sismik veri kümeleri depoda yok; aynı yapıda sentetik veri kullanıldı. Kitabın Şekil 19.10'daki karar listesi bir gösterim örneğidir; 12 örnekle tam tutarlı değildir (notlar §5).
