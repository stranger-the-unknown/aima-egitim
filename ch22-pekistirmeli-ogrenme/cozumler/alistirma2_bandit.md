# A2 çözümü — Bandit ε

Tipik davranış (aynı seed ile tekrarlanabilir):

- **ε = 0.1:** ortalama ödül yükselir; en iyi kol zamanla daha sık seçilir, ara sıra keşif devam eder.
- **ε = 0:** erken yanlış “en iyi”ye kilitlenme riski; keşif yoksa kötü kolda takılı kalınabilir.
- **ε = 0.5:** çok keşif → ortalama ödül daha dalgalı / daha düşük tavan; öğrenme yavaş sömürür.

Özet: orta ε (ör. 0.05–0.2) çoğu bandit demosunda iyi denge verir; ε’yu zamanla düşürmek de yaygındır.
