# Bölüm 3 — Quiz

Cevaplar dosyanın sonunda.

---

**S1.** Bir arama probleminin beş parçasını say.

**S2.** Düğüm ile durum arasındaki fark nedir?

**S3.** BFS'te hedef testi çocuk *üretilirken* yapılabilir, UCS'de neden yapılamaz?

**S4.** b = 10, d = 5 için N(IDS) / N(BFS) oranı yaklaşık kaçtır? Bu neden IDS için iyi bir haberdir?

**S5.** Tüm eylemlerin maliyeti 1 ise, aşağıdakilerden hangisi optimal **değildir**?
A) BFS  B) UCS  C) IDS  D) DFS

**S6.** A*'ta f(n) neyi temsil eder? h kabul edilebilirse A* hangi özelliği kazanır?

**S7.** Tutarlılık koşulunu yaz. Tutarlılık ile kabul edilebilirlik arasındaki ilişki nedir?

**S8.** Romanya'da açgözlü arama hangi yolu bulur, maliyeti kaçtır, neden optimal değildir?

**S9.** 8-bulmacada h2 neden h1'den daha iyi bir sezgiseldir? "Daha iyi"yi ölçmek için hangi sayı kullanılır?

**S10.** Gevşetilmiş bir problemin optimal çözüm maliyeti neden özgün problem için kabul edilebilir bir sezgiseldir?

**S11.** Ağırlıklı A* (f = g + W·h, W > 1) optimal midir? Değilse ne garanti eder?

**S12.** IDA*, A*'a göre hangi kaynaktan tasarruf eder, bedeli nedir?

---

## Cevaplar

1. Durum uzayı, başlangıç durumu, hedef durumları (hedef testi), eylemler ve geçiş modeli, eylem maliyeti.
2. Durum dünyanın bir yapılandırmasıdır. Düğüm ise arama ağacında o duruma giden *belirli bir yolu* (ebeveyn, eylem, g) temsil eder. Aynı duruma birçok düğüm karşılık gelebilir.
3. UCS'de daha sonra daha ucuz bir yol bulunabilir. Hedefi ilk üretildiğinde kabul etmek, optimal olmayan bir yolu döndürebilir (Romanya'da Fagaras üzerinden 450). BFS'te ise ilk bulunan hedef en sığ olandır ve birim maliyette bu optimaldir.
4. 123.450 / 111.110 ≈ **1,11**. Tekrarlanan üst düzeyler toplam işin küçük bir kısmıdır. IDS neredeyse BFS kadar hızlıdır ama belleği doğrusaldır.
5. **D (DFS).**
6. n üzerinden geçen en ucuz çözümün tahmini maliyeti (g + h). h kabul edilebilirse A* **maliyette optimaldir**.
7. h(n) ≤ c(n, a, n') + h(n'). Her tutarlı sezgisel kabul edilebilirdir. Tersi her zaman doğru değildir.
8. Arad → Sibiu → Fagaras → Bucharest, **450 km**. Yalnızca "hedefe yakın görünene" (h'ye) bakar ve o ana kadarki maliyeti (g) umursamaz. Fagaras'tan Bucharest'e giden yol uzundur.
9. h2 ≥ h1 (her yerde; baskınlık) ve ikisi de kabul edilebilir, bu yüzden h2 gerçeğe daha yakın bir tahmindir. Ölçü **etkin dallanma faktörü b\***'dır: h2 ile ~1,3, h1 ile ~1,5.
10. Gevşetilmiş problem, özgün problemin tüm çözümlerini (ve fazlasını) içerir. Bu yüzden onun en iyi çözümü, özgün problemin en iyi çözümünden pahalı olamaz.
11. Optimal değildir. Bulunan çözümün maliyeti en fazla **W · C\*** olur.
12. **Bellekten** tasarruf eder: yalnızca mevcut yolu saklar. Bedeli, her yeni f eşiğinde düğümleri **yeniden** genişletmesidir. Farklı f değeri çoksa (gerçel maliyetler) çok yavaşlayabilir.
