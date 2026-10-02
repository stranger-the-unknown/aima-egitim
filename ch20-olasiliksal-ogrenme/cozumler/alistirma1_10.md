# A1–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A1 — İki limon

1. P(d | h) = (limon oranı)²: h1 0, h2 1/16, h3 1/4, h4 9/16, h5 1. Önselle çarp: 0, 0.0125, 0.1, 0.1125, 0.1; toplam 0.325.
   Sonsal: h1 **0**, h2 **0.038**, h3 **0.308**, h4 **0.346**, h5 **0.308**. MAP: **h4**.
2. P(limon) = 0.038 · 0.25 + 0.308 · 0.5 + 0.346 · 0.75 + 0.308 · 1 ≈ **0.731**. MAP öğrenen h4'e göre **0.75** derdi.

## A2 — Ambalaj ağı

1. L = c log θ + ℓ log(1 − θ) + [r_c log θ₁ + g_c log(1 − θ₁)] + [r_ℓ log θ₂ + g_ℓ log(1 − θ₂)].
2. Her terim yalnızca bir parametreyi içerir; türevler ayrı ayrı sıfırlanır: **θ = c/(c + ℓ)**, **θ₁ = r_c/c**, **θ₂ = r_ℓ/ℓ**. Tam veride log olabilirlik parametrelere göre **toplamsal olarak ayrışır**: Her CPT kendi sayımlarından öğrenilir.

## A3 — Önsel ne kadar önemli?

1. Düzgün önselde 1 limondan sonra P(limon) = **0.75** (kitabın önseliyle 0.65). Düzgün önsel uç torbalara (h4, h5) daha çok ağırlık verir.
2. Kitabın önseliyle **11**, düzgün önselle **8** limon. Kitabın önseli h5'e yalnızca 0.1 verir ve h3'ü (0.4) güçlü tutar; kanıtın bu önseli aşması daha uzun sürer. Çok veride iki önsel de aynı yere varır.

## A4 — Beta ile hesap

1. Beta(2 + 3, 2 + 1) = **Beta(5, 3)**. Ortalama 5/8 = **0.625**; mod (5 − 1)/(5 + 3 − 2) = 4/6 ≈ **0.667**.
2. ML: 3/4 = **0.75**. Önsel Beta(2, 2) 0.5 çevresinde toplandığı için tahmini 0.5'e doğru çeker (büzme).
3. Beta(2, 2) = düzgün önsel + 1 kiraz + 1 limon: **2 sanal şeker**.

## A5 — Aynı ipucu, birden çok kez

| k | P(hasta \| belirtiler) |
|---|---|
| 1 | 0.400 |
| 2 | 0.640 |
| 5 | 0.971 |
| 10 | 0.9998 |

Gerçekte tek bir kanıt var ve doğru cevap 0.4. Naif Bayes kopyaları **bağımsız kanıtlar** sayıp olasılığı 1'e iter. Koşullu bağımsızlık yanlışsa (ilişkili nitelikler) naif Bayes aşırı emin olur; sınıflandırma sıralaması çoğu zaman doğru kalsa da olasılıklar güvenilmez.

## A6 — Bayesçi eğim

| N | θ_N | σ_N |
|---|---|---|
| 1 | 1.975 | 0.817 |
| 5 | 1.011 | 0.380 |
| 20 | 0.735 | 0.179 |
| 200 | 0.749 | 0.062 |

σ_N² ≈ σ²/Σxᵢ² olduğundan σ_N kabaca 1/√N gibi azalır. Az veride θ_N gürültülüdür ama σ_N bunu dürüstçe gösterir; tek bir "en iyi doğru" bu belirsizliği gizler.

## A7 — EM'in ilk adımı

P(Bag = 1 | kiraz, kırmızı, delikli) = θ θ_F1 θ_W1 θ_H1 / [θ θ_F1 θ_W1 θ_H1 + (1 − θ) θ_F2 θ_W2 θ_H2]
= 0.6 · 0.6³ / (0.6 · 0.6³ + 0.4 · 0.4³) = 0.1296 / (0.1296 + 0.0256) = 0.8351.
Katkı: 0.273 · 0.8351 ≈ **0.22797** (kitapla aynı). Sekiz şeker türünün katkıları toplanınca θ⁽¹⁾ = **0.6124**.

## A8 — Başlangıç noktası

| Başlangıç | Sonuç | log olabilirlik |
|---|---|---|
| Hepsi 0.5 | θ = 0.5, iki torba aynı (F = 0.56, W = 0.545, H = 0.55) | −2063.16 |
| Kitabın | θ = 0.42, torba 1 "kiraz-kırmızı-delikli" (0.89, 0.80, 0.84), torba 2 (0.32, 0.36, 0.34) | **−1979.36** |
| Ters | Aynı çözüm, torbaların adları yer değiştirmiş | **−1979.36** |

Simetrik başlangıçta iki torbanın sorumlulukları eşit kalır ve EM simetriyi hiç bozamaz: kötü bir durağan nokta. Kitabın ve ters başlangıç aynı çözüme (adlar değişik) varır: Gizli değişkenin etiketleri tanımlanamaz. Bu çözüm, gerçek modelden (−1982.214) bile daha olasıdır: ML, örneklemdeki rastlantısal sapmalara da uyar.

## A9 — Kaç bileşen?

| k | eğitim | test |
|---|---|---|
| 1 | 44.1 | 22.9 |
| 2 | 253.3 | 155.2 |
| 3 | 507.6 | **315.3** |
| 4 | 511.8 | 309.3 |
| 6 | 521.1 | 311.5 |

Eğitim olabilirliği k ile artmaya devam eder (daha esnek model her zaman en az o kadar iyi uyar); test olabilirliği gerçek bileşen sayısında (3) en yüksektir. Model seçimi için ayrı veri (ya da BIC/MDL gibi bir ceza) gerekir.

## A10 — Gizli değişkenin değeri

1. Gizli değişkenle: 3 etken × 2 = 6; Hastalık 3³ × 2 = 54; 3 belirti × (3 × 2) = 18 → **78**. Gizli değişkensiz: etkenler 6; 1. belirti 3³ × 2 = 54; 2. belirti 3⁴ × 2 = 162; 3. belirti 3⁵ × 2 = 486 → **708**.
2. | n | gizliyle | gizlisiz |
   |---|---|---|
   | 3 | 78 | 708 |
   | 5 | 90 | 6 540 |
   | 8 | 108 | 177 126 |

   Gizli değişkenle doğrusal (her belirti 6 parametre ekler), gizlisiz üstel büyür.
