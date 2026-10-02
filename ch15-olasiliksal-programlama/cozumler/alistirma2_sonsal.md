# A2 çözümü — Hileli zar

1. Bayes kuralı:

   ```text
   P(hileli | 6) = 0.3 × 0.7 / (0.3 × 0.7 + 0.7 × 1/6)
                 = 0.21 / (0.21 + 0.1167) ≈ 0.643
   ```

   Örneklemeyle bulunan ≈ 0.641; fark Monte Carlo hatası (örnek sayısı arttıkça azalır). 6, hileli zarda (0.7) adil zardan (≈ 0.167) dört kat daha olası; bu yüzden sonsal önselden (0.3) çok yüksek.

2. P(1) = 0.3 × 0.05 + 0.7 × 1/6 ≈ 0.132. Üretilen dünyaların yalnızca ~%13'ünde zar 1 gelir; geri kalanı kanıtla uyuşmadığı için reddedilir. Kanıt ne kadar nadirse reddetme örneklemesi o kadar verimsizdir (Bölüm 13). P(hileli | 1) = 0.015 / 0.132 ≈ 0.11.
