# A2 çözümü — Alpha-beta

Alpha-beta **aynı sonucu** (aynı optimal utility / hamle) üretir; yaklaşık değildir. Sadece minimax’ın zaten seçmeyeceği alt ağaçları gezmez (**budama**).

- **α:** MAX’ın o ana kadar elindeki en iyi (en yüksek) garanti değeri.
- **β:** MIN’ın o ana kadar elindeki en iyi (en düşük) garanti değeri.

α ≥ β olduğunda o dalın geri kalanı sonucu değiştiremez → kesilir.
