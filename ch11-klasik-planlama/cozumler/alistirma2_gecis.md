# A2 çözümü — Durum geçişi

Kaldır(A, Masa) sonrası tipik durum:

- **Silinenler:** `On(A, Masa)`, `ElBos`, (ve modelinize göre `Clear(A)` tutulabilir veya `Tutuyor` ile değişir)
- **Eklenen:** `Tutuyor(A)`
- **Kalan:** `On(B, Masa)`, `Clear(B)`, …

Somut küme `strips_bloklar.py` içindeki `Kaldir` tanımıyla birebir kontrol edilebilir.
