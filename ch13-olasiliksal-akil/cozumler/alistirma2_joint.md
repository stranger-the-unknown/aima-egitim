# A2 çözümü — Ortak olasılık

Ağın anlamı: Her değişkenin, ebeveynleri verildiğindeki olasılığını çarp.

```text
P(Y=T, S=F, A=T, M=T)
  = P(Y=T) · P(S=F) · P(A=T | Y=T, S=F) · P(M=T | A=T)
  = 0.01   · 0.95   · 0.88              · 0.80
  = 0.006688
```

Dört değişkenli tam tablo 2⁴ − 1 = 15 sayı isterdi. Ağ 1 + 1 + 4 + 2 = 8 sayıyla aynı dağılımı tanımlar.
