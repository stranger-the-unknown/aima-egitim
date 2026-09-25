# Çözümler — A6, A7

## A6 — IDS'nin bedeli

N(BFS) = b + b² + … + b^d, N(IDS) = d·b + (d−1)·b² + … + 1·b^d

1. **b = 10, d = 5:** N(BFS) = 111.110, N(IDS) = 123.450 → IDS yalnızca **%11** fazla.
2. **b = 2, d = 10:** N(BFS) = 2.046, N(IDS) = 4.072 → IDS **~%99** fazla (neredeyse iki katı).
   Neden? En alt düzey, toplamın b küçükken daha küçük bir kısmını oluşturur. b = 10'da düğümlerin ~%90'ı son düzeydedir, bu yüzden üst düzeyleri tekrarlamak ucuzdur. b = 2'de son düzey toplamın ancak yarısıdır, bu yüzden tekrarlar daha pahalıdır. Genel oran yaklaşık b/(b−1)'dir.
3. **b = 10, d = 12, 1 KB/düğüm:**
   - BFS: ~1,1 × 10¹² düğüm → **~1 PB**
   - IDS: ~b·d = 120 düğüm → **~120 KB**

   Bellek farkı on milyar kat. IDS'yi değerli kılan budur.

## A7 — Kabul edilebilir mi, tutarlı mı?

**Gerçek maliyetler:** h*(G) = 0, h*(B) = 1, h*(A) = min(5, 2 + 1) = 3, h*(S) = min(1 + 3, 4 + 1) = 4.

| | S | A | B | G | Kabul edilebilir? | Tutarlı? |
|---|---|---|---|---|---|---|
| h* | 4 | 3 | 1 | 0 | | |
| h₁ | 4 | 1 | 1 | 0 | **Evet** (her yerde ≤ h*) | **Hayır**: S–A kenarında h₁(S) = 4 > c(S,A) + h₁(A) = 1 + 1 = 2 |
| h₂ | 4 | 3 | 1 | 0 | **Evet** | **Evet** (tüm kenarlarda h(n) ≤ c + h(n')) |

**A* ile h₁ (elle):**

| adım | çıkan (f) | yapılan |
|---|---|---|
| 1 | S (4) | A: g=1, f=2 · B: g=4, f=5 |
| 2 | A (2) | B: g=3 < 4 → **güncelle**, f=4 · G: g=6, f=6 |
| 3 | B (4) | G: g=4 < 6 → **güncelle**, f=4 |
| 4 | G (4) | hedef → maliyet **4** (optimal: S–A–B–G) |

Tutarsızlık yüzünden f değeri yol boyunca **düştü** (S'de 4, A'da 2). Yine de optimal yol bulundu, çünkü `en_iyi_oncelikli` içindeki şu koşul daha ucuz bir yol bulunduğunda durumu yeniden açar:

```python
if s not in ulasilan or cocuk.g < ulasilan[s].g:
```

Bu satır olmasaydı, yani bir durum ilk ulaşıldığında kilitlenseydi, B'nin maliyeti 4'te kalırdı. Bu küçük grafta sonuç değişmese de, tutarsız sezgisellerle "ilk ulaşılan yol en iyisidir" varsayımı genel olarak **yanlıştır**. Tutarlılık, bu yeniden açma işlemini gereksiz kılar.

h₂ tutarlı olduğu için f değerleri yol boyunca azalmaz ve her duruma ilk ulaşıldığında en iyi yoldan ulaşılmış olur.
