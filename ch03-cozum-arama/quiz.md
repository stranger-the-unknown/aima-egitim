# Bölüm 3 — Quiz (5 soru)

Cevaplar dosyanın sonunda.

---

**S1.** Arama problemi formülasyonunun altı temel parçasını sayın.

**S2.** BFS birim maliyetli problemlerde neyi garanti eder?

**S3.** UCS hangi değeri önceliklendirir? Ne bulur?

**S4.** A*’ta f(n) nasıl tanımlanır? Kabul edilebilir sezgisel ne demektir?

**S5.** Graf arama ağaç aramaya göre hangi sorunu azaltır?

---

## Cevaplar

**S1.** Durum uzayı, başlangıç, eylemler, geçiş modeli, hedef testi, yol maliyeti.

**S2.** En az *adımlı* (en sığ) yolu bulur; birim maliyette bu aynı zamanda optimal maliyettir.

**S3.** g(n) — şimdiye kadarki yol maliyeti; negatif olmayan maliyetlerde optimal maliyetli yolu bulur.

**S4.** f(n) = g(n) + h(n). Kabul edilebilir: h(n) gerçek kalan maliyeti asla abartmaz (h ≤ h*).

**S5.** Aynı durumun tekrar tekrar keşfi / döngü riskini azaltır (ziyaret kaydı).
