# Bölüm 15 — Olasılıksal programlama

> AIMA 4. baskı, Bölüm 15 · *Probabilistic Programming*

## Öğrenme hedefleri

1. Bayes ağlarının neden "önermesel" kaldığını ve birinci dereceden olasılık modellerinin neden gerektiğini açıklamak.
2. İlişkisel bir olasılık modeli (RPM) yazmak ve onu Bayes ağına temellendirmek.
3. Açık evren modellerinde nesne sayısı ve kimlik belirsizliğini modellemek.
4. Veri ilişkilendirme probleminin neden zor olduğunu göstermek.
5. Bir programı olasılık modeli olarak görmek ve gözlemlerden onun rastgele seçimlerini çıkarmak.

## Çalışma sırası

1. Kitapta Bölüm 15'i oku.
2. [`notlar.md`](notlar.md)
3. Örnekleri çalıştır.
4. [`alistirmalar.md`](alistirmalar.md) → [`cozumler/`](cozumler/)
5. [`quiz.md`](quiz.md)

## Dosyalar

| Dosya | İçerik |
|---|---|
| `ornekler/rpm_oneriler.py` | Kitabın kitap önerisi RPM'i: tip imzaları, temellendirme, bağlama özgü bağımsızlık, kesin çıkarım |
| `ornekler/beceri_derecelendirme.py` | Beceri–performans–galibiyet modeli (TrueSkill benzeri), olabilirlik ağırlıklandırma |
| `ornekler/acik_evren.py` | Sayı ifadeleri (#Customer, #LoginID), sybil çıkarımı, Poisson |
| `ornekler/metin_okuma.py` | Bozulmuş metni okumak: bağımsız harf modeli ve ikili harf Markov modeli |
| `ornekler/basit_uretimsel_model.py` | Özgün hileli zar modeli: program olarak olasılık modeli |
| `ornekler/reddetme_ornekleme.py` | Aynı modelde reddetme örneklemesi |
| `alistirmalar.md` | 10 alıştırma |
| `cozumler/` | Tüm çözümler (A5–A7, A9, A10 kod) |
| `quiz.md` | 12 soru + cevaplar |

## Kitapla doğrulama

`tests/test_ch15_olasiliksal_programlama.py`:

| Değer | Kitap | Kod |
|---|---|---|
| Honest, Kindness, Quality önselleri; dürüst olmayanların öneri dağılımı | ⟨0.99, 0.01⟩; ⟨0.1, 0.1, 0.2, 0.3, 0.3⟩; ⟨0.05, 0.2, 0.4, 0.2, 0.15⟩; ⟨0.4, 0.1, 0.0, 0.1, 0.4⟩ | ✔ |
| Temellendirilmiş düğüm sayısı | 2C + B + BC | ✔ |
| Sayı ifadeleri | #Customer ~ U(1, 3), #Book ~ U(2, 4), #LoginID ~ 1 ya da U(2, 5) | ✔ |
| Poisson standart sapması | √λ | ✔ |

Kitap HonestRecCPT'yi ve beceri modelinin sayılarını vermez; bunlar kodda açıkça varsayım olarak belirtildi.
