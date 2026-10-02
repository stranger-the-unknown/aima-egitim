# A1–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A1 — Ödül-kalan

- **2. deneme** (7 geçiş, sonu +1): (1,1) → 6 × (−0.04) + 1 = **0.76**; (2,3) 3. geçişten sonra: 3 × (−0.04) + 1 = **0.88**; (3,2) 5. geçişten sonra: (−0.04) + 1 = **0.96**.
- **3. deneme** (6 geçiş, sonu −1): (1,1) → 5 × (−0.04) − 1 = **−1.20**; (2,3): 2 × (−0.04) − 1 = **−1.08**; (3,2): **−1.00**.

## A2 — Üç denemeden doğrudan kestirim

| Durum | Kestirim | Örnek | Gerçek |
|---|---|---|---|
| (1,1) | 0.107 | 3 | 0.745 |
| (1,2) | 0.330 | 4 | 0.802 |
| (1,3) | 0.370 | 4 | 0.852 |
| (2,3) | 0.253 | 3 | 0.908 |
| (3,2) | −0.020 | 2 | 0.700 |
| (3,3) | 0.470 | 4 | 0.958 |

(1,1): (0.76 + 0.76 − 1.20)/3 = 0.107. Üç denemenin biri −1'e düştü; gerçekte bu yalnızca küçük bir olasılıkla olur. Üç örnek, varyansı çok yüksek bir ortalama verir.

## A3 — Üç denemeden model

| (s, a) | öğrenilen |
|---|---|
| (1,1) Yukarı | (1,2) 1.00 |
| (1,2) Yukarı | (1,3) 1.00 |
| (1,3) Sağ | (2,3) 0.75, (1,2) 0.25 |
| (2,3) Sağ | (3,3) 1.00 |
| (3,2) Yukarı | (3,3) 0.50, (4,2) 0.50 |
| (3,3) Sağ | (4,3) 0.50, (3,2) 0.50 |

(3,2) Yukarı ve (3,3) Sağ için −1'e ya da geri kayma olasılığı 0.1 yerine 0.5 tahmin edildi (2 ve 4 örnekten). Bu model politika değerlendirmesinde hâlâ işe yarar (Bellman denklemleri çözülür), ama faydalar çok kötümser çıkar. Birkaç düzine denemeden sonra sayımlar gerçeğe yaklaşır.

## A4 — TD'yi elle izle

U(1,3) ← 0.84 + 0.1 (−0.04 + 0.96 − 0.84) = 0.84 + 0.008 = **0.848**. Aynı geçiş 10 kez: Fark her adımda 0.9 katına iner: 0.92 − 0.08 · 0.9¹⁰ ≈ **0.892**; sonsuzda 0.92. Gerçek değer 0.8516 çünkü (1,3)'ten Sağ her zaman (2,3)'e gitmez (0.2 olasılıkla (1,2)'ye ya da yerinde kalır). TD tek bir ardıla değil, ardılların **ortalamasına** yakınsar; farklı ardıllar gözlendikçe tahmin 0.85 civarına iner (α azalmalı).

## A5 — Q-öğrenme ve SARSA

1. - Q-öğrenme: 0.5 + 0.5 (−0.04 + max(0.9, 0.2) − 0.5) = 0.5 + 0.5 · 0.36 = **0.68**.
   - SARSA: 0.5 + 0.5 (−0.04 + 0.2 − 0.5) = 0.5 − 0.17 = **0.33**.
2. SARSA, izlenen (keşifli) politikanın değerini öğrenir. Uçurum kenarında keşif bazen düşmeye yol açıyorsa SARSA kenara yakın yolları cezalandırır ve **daha temkinli** bir yol seçer; Q-öğrenme ise en iyi (açgözlü) politikanın değerini öğrenir ve kenardan yürür, keşif sırasında daha sık düşer.

## A6 — Nₑ'nin etkisi

| Nₑ | 20 deneme | 100 deneme |
|---|---|---|
| 1 | 1.739 | 1.739 |
| 5 | 0.024 | 0.013 |
| 20 | 30.885 | 0.013 |

Nₑ = 1: Her eylem bir kez denenir; tek bir örnekle model çok gürültülü ve ajan çabucak kötü bir politikaya takılır. Nₑ = 20: Keşif uzun sürer (20 denemede ajan hâlâ deniyor, politikası kötü), ama sonunda en iyiye varır. Nₑ, keşfin maliyeti ile modelin güvenilirliği arasındaki dengedir.

## A7 — İşlev yaklaşımını elle

Hata 0.4 − 0.8 = −0.4; özellikler (1, 1, 1). θ ← (0.5, 0.2, 0.1) − 0.04 (1, 1, 1) = **(0.46, 0.16, 0.06)**. Û(3,3) = 0.5 + 0.6 + 0.3 = 1.4 iken 0.46 + 0.48 + 0.18 = **1.12**. (1,1)'deki tek gözlem (3,3)'ü de değiştirdi. Genelleme sayesinde az veriyle öğrenme hızlanır; ama gözlem kötü şans eseri düşükse (−1'e düşmek) uzak durumlar da haksız yere etkilenir.

## A8 — Özellik eklemek

| Özellikler | RMS hata |
|---|---|
| (1, x, y) | 0.070 |
| + hedefe uzaklık | 0.070 |
| + uzaklık + "−1'e komşu mu?" | **0.050** |

Bu ızgarada uzaklık |4 − x| + |3 − y| = 7 − x − y'dir: x ve y'nin doğrusal birleşimi, yeni bilgi katmaz. Faydaların asıl doğrusal olmayan kısmı −1 durumunun komşularındaki düşüştür; bunu ayrı bir özellik yakalar.

## A9 — REINFORCE'ta öğrenme hızı

| α | 300 bölüm | 1500 bölüm |
|---|---|---|
| 0.01 | 0.014 | 0.026 |
| 0.05 | 1.187 | 0.014 |
| 0.2 | 0.026 | ~0 |

Sonuçlar tek bir tohumdan ve **gürültülü**dür: Politika gradyanı tahmininin varyansı yüksektir; aynı α farklı tohumlarda farklı sonuç verir. Varyansı azaltmak için: getiriden bir **temel çizgi** çıkarmak (kodda yürüyen ortalama), birçok bölümün ortalamasını almak, **ilişkili örnekleme**, getiriyi değer fonksiyonu tahminiyle değiştirmek (aktör–eleştirmen), daha küçük adımlar.

## A10 — Taklit mi, ters RL mi?

1. (a) Davranış klonlama durumdan eyleme bir eşleme öğrenir. (b) Ters RL uzmanın ödül fonksiyonunu öğrenir, sonra onunla en iyi politikayı planlar.
2. (a) Hiç görülmemiş durumda tahmin keyfidir; küçük hatalar ajanı öğretmenin hiç gitmediği durumlara sürükler ve hatalar birikir. (b) Öğrenilen ödül (ör. "çarpışma çok kötü, yolda kal") yeni durumda da geçerlidir; planlama makul bir eylem bulabilir.
3. (b). Ödülü öğrenince, uzmanın hatalarını tekrarlamak zorunda kalmadan o ödül için en iyiyi arayabilir. (a) en iyi ihtimalle uzmanı kopyalar.
