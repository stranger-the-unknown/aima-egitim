# A1 çözümü — MDP beşlisi (örnek)

- **S:** koridor hücreleri + “şarj istasyonu / engel” durumları
- **A:** ileri, sol, sağ (veya bekle)
- **T:** teker kayması yüzünden istenen komşuya %80, yanlara sapma
- **R:** her adım küçük eksi; hedefe +; engele çarpınca büyük eksi
- **γ:** 0.9 → yakın ödüller biraz daha önemli, ama uzun vadeyi de umursar
