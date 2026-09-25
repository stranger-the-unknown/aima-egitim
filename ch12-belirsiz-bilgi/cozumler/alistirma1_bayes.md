# A1 çözümü — Bayes elle

```text
P(U) = P(U | K) P(K) + P(U | ¬K) P(¬K)
     = 0.95 · 0.02 + 0.10 · 0.98
     = 0.019 + 0.098
     = 0.117

P(K | U) = 0.019 / 0.117 ≈ 0.162   (yaklaşık %16)
```

Sezgi: 1000 parçadan 20'si kusurlu, bunların ~19'u uyarı verir. 980 sağlam parçadan ~98'i de yanlış uyarı verir. Uyarı veren 117 parçadan yalnızca 19'u kusurlu.

Sonsal (%16), önselden (%2) sekiz kat yüksek ama hâlâ düşük. Kusur nadir, yanlış uyarı oranı ise görece yüksek. Menenjit örneğiyle aynı ders: **Önsel olasılığı yok sayma.**
