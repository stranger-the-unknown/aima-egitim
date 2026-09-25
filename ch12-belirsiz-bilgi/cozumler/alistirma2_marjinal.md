# A2 ve A3 çözümleri

## A2 — Marjinalleştirme ve koşullama

```text
P(A = T) = 0.12 + 0.18 = 0.30
P(B = T) = 0.12 + 0.28 = 0.40
P(B = T | A = T) = P(A = T, B = T) / P(A = T) = 0.12 / 0.30 = 0.40
```

## A3 — Bağımsızlık

P(B = T | A = T) = 0.40 = P(B = T). Dört hücre de çarpıma eşit:

| A | B | P(A, B) | P(A) · P(B) |
|---|---|---|---|
| T | T | 0.12 | 0.30 · 0.40 = 0.12 |
| T | F | 0.18 | 0.30 · 0.60 = 0.18 |
| F | T | 0.28 | 0.70 · 0.40 = 0.28 |
| F | F | 0.42 | 0.70 · 0.60 = 0.42 |

**A ve B bağımsız.**

İki Boole değişkeninde tek hücre gerçekten yeter: P(a, b) = P(a) P(b) ise
P(a, ¬b) = P(a) − P(a, b) = P(a)(1 − P(b)) = P(a) P(¬b). Diğer iki hücre de aynı şekilde çıkar. Ama değişkenlerin ikiden fazla değeri varsa her hücre ayrı kontrol edilmelidir.
