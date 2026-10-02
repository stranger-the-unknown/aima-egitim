# A1–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A1 — Kazancı elle hesapla

**Hungry:** Yes → x1, x2, x4, x6, x8, x10, x12: 5 olumlu, 2 olumsuz. No → x3, x5, x7, x9, x11: 1 olumlu, 4 olumsuz.
Kalan = 7/12 · B(5/7) + 5/12 · B(1/5) = 7/12 · 0.863 + 5/12 · 0.722 ≈ 0.503 + 0.301 = 0.804.
Kazanç = 1 − 0.804 ≈ **0.196**.

**Price:** $ → x2, x3, x4, x7, x9, x11, x12: 3 olumlu, 4 olumsuz. $$ → x6, x8: 2 olumlu. $$$ → x1, x5, x10: 1 olumlu, 2 olumsuz.
Kalan = 7/12 · B(3/7) + 2/12 · 0 + 3/12 · B(1/3) ≈ 0.575 + 0 + 0.230 = 0.804.
Kazanç ≈ **0.196**.

İkisi de Patrons'un (0.541) çok altında. Patrons iki dalı (None, Some) tamamen saf bırakıyor; Hungry ve Price hiçbir dalı ya da yalnızca küçük bir dalı saflaştırıyor.

## A2 — Kaç fonksiyon?

1. 2^(2³) = **256**. 20 nitelik: 2^(2²⁰) = 2^1 048 576 ≈ **10^315 653**.
2. **8 yaprak** (tam ağaç). Eşlik fonksiyonunda tek bir niteliğin değişmesi her zaman sonucu değiştirir; hiçbir yolda bir test atlanamaz, bu yüzden her yol üç niteliği de test etmelidir.
3. Ağaç testleri eksenlere paralel bölmelerdir. Çapraz bir sınırı ancak çok sayıda küçük "basamakla" yaklaşık olarak çizebilir; daha iyi yaklaşım için daha çok düğüm gerekir.

## A3 — Patrons olmasaydı

Kök **WaitEstimate** (kazanç 0.208) olur ve ağaç **15 düğüme** çıkar (Patrons'la 12). Bar ve Raining gibi gerçek ağaçta önemsiz niteliklerin dalları belirir: Az örnekle ağaç tesadüfi örüntüleri yakalar. İyi bir nitelik eksik olunca hipotez hem büyür hem de genelleme olasılığı düşer.

## A4 — χ² ile anlamlılık

| Nitelik | Δ | sd | p |
|---|---|---|---|
| Patrons | 6.67 | 2 | **0.036** |
| Hungry | 3.09 | 1 | 0.079 |
| Price | 2.48 | 2 | 0.29 |
| WaitEstimate | 2.67 | 3 | 0.45 |
| Fri, Rain, Res | 0.34 | 1 | 0.56 |
| Alt, Bar, Type | 0 | 1 / 1 / 3 | 1 |

Yalnızca **Patrons** %5 düzeyinde anlamlıdır. 12 örnekle güçlü sonuç çıkarmak zordur; Hungry'nin gerçekten ilgili olduğunu bildiğimiz hâlde (gerçek ağaçta var) bu veride anlamlı çıkmaz. Az veride budama, gerçek ama zayıf etkileri de silebilir.

## A5 — Kimlik niteliği

1. Kazanç = **1 bit**, en büyük olası değer. Her dal tek örnek içerir, dolayısıyla saftır; Kalan = 0. Ama bu niteliğin yeni örnekler için hiçbir değeri yoktur (yeni bir kimlik hiç görülmemiştir).
2. | Nitelik | Kazanç | Bölünme bilgisi | Oran |
   |---|---|---|---|
   | Kimlik | 1.000 | 3.585 (log₂ 12) | 0.279 |
   | Patrons | 0.541 | 1.459 | **0.371** |
   | Hungry | 0.196 | 0.980 | 0.200 |
   | Type | 0 | 1.918 | 0 |

   Kazanç oranı Patrons'u yine öne çıkarır: Çok sayıda küçük dala bölen nitelikler bölünme bilgisiyle cezalandırılır.

## A6 — Gürültüde budama

| | Eğitim | Test | Düğüm |
|---|---|---|---|
| Budamasız | 0.997 | 0.747 | 143 |
| Budanmış (χ², %5) | 0.868 | **0.837** | 53 |

Budamasız ağaç gürültüyü ezberler (eğitimde neredeyse mükemmel, testte kötü). Budama eğitim doğruluğunu düşürür ama testte belirgin biçimde iyileştirir ve ağacı üçte birine indirir.

## A7 — Gradyan inişini elle izle

1. Hatalar y − h(x): 3 − 0 = 3 ve 5 − 0 = 5.
   - w₀ ← 0 + 0.1 (3 + 5) = **0.8**
   - w₁ ← 0 + 0.1 (3 · 1 + 5 · 2) = **1.3**
   - Tahminler 2.1 ve 3.4; kare kayıp 3² + 5² = 34'ten (0.9² + 1.6²) = 3.37'ye iner.
2. İki noktadan geçen doğru: **w₁ = 2, w₀ = 1** (kayıp 0).
3. α = 1: w₀ = 8, w₁ = 13 → tahminler 21 ve 34, kayıp ~1063: Adım çok büyük, en küçük noktanın üstünden atlar ve **ıraksar**.

## A8 — L1 ve L2

| λ | L1: sıfır ağırlık | L1: ilgili ağırlıklar | L2: sıfır | L2: ilgili ağırlıklar |
|---|---|---|---|---|
| 0 | 0 | 2.92, −1.94 | 0 | 2.92, −1.94 |
| 0.05 | 0 | 2.89, −1.93 | 0 | 2.73, −1.86 |
| 0.3 | 5 | 2.74, −1.84 | 0 | 2.07, −1.56 |
| 1 | 6 | 2.31, −1.58 | 0 | 1.26, −1.09 |
| 3 | 6 | 1.07, −0.83 | 0 | 0.60, −0.59 |

L1 ilgisiz ağırlıkları tam sıfıra indirirken ilgili ağırlıkları görece az küçültür (sabit miktarda kırpar). L2 hiçbir ağırlığı sıfırlamaz; büyük ağırlıkları orantılı olarak daha çok küçültür.

## A9 — Kaymış çember

1. **Hayır.** F'nin özellikleri x₁², x₂², x₁x₂ ikinci dereceden terimlerdir; ama (x₁ − 1)² + (x₂ − 0.5)² < 1.44 açılınca −2x₁ ve −x₂ gibi **doğrusal terimler** de çıkar. F bunları içermez.
2. (x₁, x₂, x₁² + x₂²) ve sabit terim: x₁² + x₂² − 2x₁ − x₂ + (1 + 0.25 − 1.44) < 0, bu özelliklerde **doğrusaldır**. Kod bunu algılayıcıyla doğrular. (Kitap herhangi bir çember için dört boyutun yettiğini söyler; sabit terimi bir boyut sayarsak aynı sonuç.)

## A10 — Uzmanlara ne kadar güvenmeli?

1. M* = 250, K = 10 için sınır (250 ln(1/β) + ln 10)/(1 − β), **β ≈ 0.88**'de en küçük: ~**285.5**. β = 0.5 ile 351.2. En iyi uzmanın hata sayısı büyükken β'yı 1'e yakın seçmek ödüllendirilir.
2. β → 1: Ağırlıklar çok yavaş değişir; ln K/(1 − β) terimi patlar, başlangıçta kötü uzmanlara uzun süre güvenilir. β → 0: Tek bir hata uzmanı neredeyse siler; M* ln(1/β) terimi patlar, ajan şanssız bir hatayla iyi uzmanı kaybedebilir. Uzmanların başarısı zamanla değişiyorsa **β → 1 tehlikelidir**: Eski iyi uzmanın biriken ağırlığı yeni iyi uzmana geçişi geciktirir.
