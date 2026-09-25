# A1 çözümü — FOL vs önerme

1. **Önerme yolu (örnek):** `Calisan_Ali`, `Calisan_Ayse`, `Calisan_Can` ve her biri için `Oturur_Ali_O1` ∨ `Oturur_Ali_O2` ∨ … gibi cümleler. Çalışan veya ofis eklenince yeni semboller ve cümleler gerekir; “her” genellemesi otomatik taşınmaz.

2. **FOL:** `∀x (Calisan(x) ⇒ ∃y (Ofis(y) ∧ Oturur(x, y)))`. Tek cümle; domain büyüyünce aynı kural geçerli kalır.
