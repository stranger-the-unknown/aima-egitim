# A1 çözümü — Geçiş mi, algılayıcı mı?

1. **Geçiş modeli:** "Dünya bir adımda nasıl değişir?" → P(X_t | X_{t−1}). **Algılayıcı modeli:** "Bu durumda hangi gözlemi ne olasılıkla görürüm?" → P(E_t | X_t).
2. `T = [[0.7, 0.3], [0.3, 0.7]]` geçiş modeli (satır: dünkü durum, sütun: bugünkü). `sensor(u)` algılayıcı modeli: şemsiye varsa [0.9, 0.2], yoksa [0.1, 0.8].
3. Yağmurun bugün yağıp yağmaması yalnızca dünkü havaya bağlı değil: mevsim, kaç gündür yağdığı, basınç da etkiler. İki yol: (a) daha yüksek dereceli bir Markov süreci (R_{t−2}'yi de ebeveyn yap), (b) durumu zenginleştirmek (Mevsim_t, Basınç_t, Nem_t değişkenleri eklemek). Kitap ikinci yolu önerir: Doğru durum değişkenleri eklenince birinci dereceden varsayım daha doğru olur.
