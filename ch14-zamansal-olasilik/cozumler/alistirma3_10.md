# A3–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A3 — Dört görev

| Görev | Soru | Örnek |
|---|---|---|
| Filtreleme | Şu an dünya ne durumda (şimdiye kadarki kanıtla)? | GPS'in şu anki konumu göstermesi |
| Tahmin | Gelecekte ne olacak? | Yarınki hava tahmini |
| Yumuşatma | Geçmişte ne olmuştu (sonraki kanıtla birlikte)? | Kara kutudan uçuşun yeniden kurulması |
| En olası açıklama | Hangi durum dizisi gözlemleri en iyi açıklar? | Konuşma tanıma: ses dizisine en uygun kelime dizisi |

## A4 — Yumuşatma elle

1. b_{3:3}(R_2) = Σ_{r_3} P(¬u_3 | r_3) P(r_3 | R_2):
   - R_2 = yağmur: 0.1 × 0.7 + 0.8 × 0.3 = **0.31**
   - R_2 = kuru: 0.1 × 0.3 + 0.8 × 0.7 = **0.59**
2. P(R_2 | u_1, u_2, ¬u_3) = α ⟨0.883 × 0.31, 0.117 × 0.59⟩ = α ⟨0.274, 0.069⟩ ≈ **⟨0.799, 0.201⟩**.
   Filtrelenmiş değer 0.883'tü. Ertesi günün şemsiyesiz olması, 2. günde de yağmur yağmadığı ihtimalini biraz artırdı (hava ardışık günlerde benzer olma eğiliminde).

## A5 — Viterbi ile adım adım en olası durum

En kısa dizi: **[¬u, u, ¬u]**.
- Yumuşatılmış P(yağmur): 0.148, **0.554**, 0.148 → adım adım en olası: kuru, **yağmur**, kuru.
- Viterbi: **kuru, kuru, kuru**.

Neden: Tek başına 2. gün için, yağmur ve kuru hipotezleri, bütün olası dizilerin toplamında yağmur lehine hafifçe ağır basar. Ama tek bir dizi olarak "kuru, yağmur, kuru" iki kez hava değişimi (0.3 × 0.3) gerektirir. "kuru, kuru, kuru" ise hiç değişim gerektirmez. Şemsiye kanıtı (0.9 / 0.2 = 4.5 kat) iki değişimin cezasını (0.09 / 0.49 ≈ 0.18) karşılamaya yetmez. Ders: **Her adımda en olası durumu seçmek en olası diziyi vermez.**

## A6 — Karışma süresi

| Model | Durağan P(yağmur) | 0.01 yakınına adım |
|---|---|---|
| 0.7 / 0.3 | 0.5 | 5 |
| 0.9 / 0.1 | 0.5 | 18 |
| 0.7 / 0.2 | **0.4** | 6 |

Fark her adımda (P(yağmur | yağmur) − P(yağmur | kuru)) katına iner: 0.4 ya da 0.8. İnatçı havada geçmişin etkisi daha uzun sürer. Üçüncü modelde durağan dağılım π = 0.7π + 0.2(1 − π) ⇒ π = 0.2 / 0.5 = **0.4**.

## A7 — Kalman ikinci adım

1. Tahmin varyansı: 0.862 + 4 = 4.862.
   μ_2 = (4.862 × 1.0 + 1 × 2.155) / (4.862 + 1) ≈ **1.197**, σ_2² = 4.862 × 1 / 5.862 ≈ **0.829**.
2. - σz → ∞ (algılayıcı işe yaramaz): μ_{t+1} → μ_t. Gözlem yok sayılır.
   - σz → 0 (algılayıcı mükemmel): μ_{t+1} → z_{t+1}. Önceki kestirim yok sayılır.
   Kalman filtresi, iki bilgi kaynağını güvenilirliklerine göre ağırlıklandırır.

## A8 — Uzun koridor

1. **Hayır.** Ortadaki beş kare aynı algılayıcı değerini verir (yalnızca kuzey ve güney kapalı). Robot yalnızca uçlara geldiğinde yerini öğrenir. Sonra, hangi yöne gittiği gözlenmediği için belirsizlik yeniden büyür. 20 koşunun ortalamasında beklenen hata ≈ 0.87 kare.
2. İnanç yalnızca **tek** ya da yalnızca **çift** sütunlarda sıfırdan farklıdır. Robot her adımda mutlaka bir kare hareket ettiği için sütun numarasının tek/çift olması her adım değişir. Bir uçta görüldüğü anda bu parite kesinleşir ve sonsuza kadar bilinir.

## A9 — Parçacık filtresiyle konumlandırma

Bir çalıştırmanın beklenen konum hataları (ε = 0.1, 25 adım, 10 koşu):

| | Kesin | N = 20 | N = 100 | N = 1000 |
|---|---|---|---|---|
| Hata | 1.05 | 3.85 | 1.88 | 0.93 |

20 parçacık 45 kareyi temsil etmeye yetmez: Doğru kare hiç parçacık içermeyebilir ve filtre kaybolur. 1000 parçacıkla sonuç kesin filtreyle aynı düzeyde. (Kesin değerden küçük çıkması rastgele dalgalanmadır.)

## A10 — Hangi model?

| Model (P(yağmur \| dün yağmur)) | 60 gün | 500 gün |
|---|---|---|
| 0.5 | −39.7 | −344.3 |
| 0.7 | **−38.4** | −315.1 |
| 0.9 (gerçek) | −41.1 | **−309.3** |
| 0.95 | −43.2 | −320.7 |

1. 60 günde **yanlış model (0.7)** kazanıyor.
2. 500 günde **doğru model (0.9)** kazanıyor.
3. Olabilirlik, modelleri karşılaştırmanın ve öğrenmenin temel aracıdır (Bölüm 20'deki EM algoritması bunu yapar). Ama az veriyle rastlantısal dalgalanmalar yanıltabilir. Veri arttıkça doğru model belirginleşir.
