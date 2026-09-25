# A1 çözümü — CSP modeli

1. **Değişkenler:** `MAT`, `FIZ`, `YAZ` (her ders bir zaman alır).
   **Domain:** her biri için `{09:00, 11:00, 14:00}`.
   **Kısıtlar:** `MAT ≠ FIZ`, `MAT ≠ YAZ`, `FIZ ≠ YAZ` (hepsi ikili “farklı saat”; hoca kısıtı zaten `MAT ≠ FIZ` içinde).

2. Amaç belirli bir “başlangıç → hedef yolu” değil; **tüm atamaların aynı anda kısıtlara uyması**. Durum uzayı kısmi atamalarla büyür; budama kısıtlardan gelir. Bu yüzden CSP çerçevesi doğal.
