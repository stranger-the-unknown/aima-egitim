# Çözüm — A3: Mimari seçimi

| # | Durum | Mimari | Gerekçe |
|---|---|---|---|
| 1 | Asansör kapısı engel algılayınca kapanmayı durdurur | **Basit refleks** | Karar yalnızca *şu anki* algıya bağlı ("engel var mı?"). Bellek, hedef veya ödünleşim gerekmiyor; hız ve güvenilirlik önemli. |
| 2 | Depo robotu görünmeyen rafların doluluğunu hatırlar | **Modele dayalı** (+ hedefe dayalı) | Kısmi gözlem var: şu an göremediği rafların durumunu *iç durumda* tutmak zorunda. Rota seçimi hedefe dayalı aramaya dayanır. |
| 3 | Tatil planlayıcı bütçe, süre ve ilgi arasında ödünleşim yapar | **Faydaya dayalı** | Birden fazla *çatışan* ölçüt var. "Hedefe ulaştım mı?" değil, "ne kadar iyi bir plan?" sorusu önemli. |
| 4 | Oyun ajanı değişen rakip stratejisine göre politikasını günceller | **Öğrenen ajan** | Ortam (rakip) zamanla değişiyor ve önceden modellenemiyor. Eleştirmen maç sonuçlarından geri bildirim üretir, öğrenme öğesi politikayı günceller. |

**Not:** Mimariler iç içedir. Öğrenen bir ajanın performans öğesi faydaya dayalı olabilir, faydaya dayalı bir ajan da bir iç model tutar. "En uygun" demek, **en az karmaşık ama yeterli** olan mimariyi seçmek demektir.
