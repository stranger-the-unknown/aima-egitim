# A2 çözümü — Filtreleme elle

**Tahmin** (geçiş modeliyle ileri taşı):

```text
P(R_3 | u_1, u_2) = ⟨0.7, 0.3⟩ × 0.883 + ⟨0.3, 0.7⟩ × 0.117
                  = ⟨0.618 + 0.035, 0.265 + 0.082⟩ ≈ ⟨0.653, 0.347⟩
```

**Güncelleme** (şemsiye yok: P(¬u | r) = 0.1, P(¬u | ¬r) = 0.8):

```text
P(R_3 | u_1, u_2, ¬u_3) = α ⟨0.1 × 0.653, 0.8 × 0.347⟩ = α ⟨0.0653, 0.2776⟩ ≈ ⟨0.191, 0.809⟩
```

Neden bu kadar düştü: Yağmurlu bir günde şemsiyesiz gelme olasılığı (0.1), kuru bir günde şemsiyesiz gelme olasılığının (0.8) sekizde biri. Olabilirlik oranı 1/8, önceki oran (0.653 / 0.347 ≈ 1.9) ile çarpılınca ≈ 0.235 olur: Yağmur olasılığı ≈ 0.19.
