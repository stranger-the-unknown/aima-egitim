# Bölüm 5 — Quiz

Cevaplar dosyanın sonunda.

---

**S1.** Sıfır toplamlı bir oyunda MAX ve MIN'in hedefleri nedir?

**S2.** Minimax yaprakta ne döndürür? MAX ve MIN düğümlerinde ne yapar?

**S3.** Kitaptaki iki katlı ağaçta (B: 3 12 8, C: 2 4 6, D: 14 5 2) kökün minimax değeri nedir? Alfa-beta hangi yaprakları budar?

**S4.** Alfa-beta sonucu değiştirir mi? Mükemmel hamle sıralamasında kaç yaprağa bakılır?

**S5.** Transpozisyon tablosu nedir? Alfa-beta ile kullanırken nelere dikkat etmek gerekir?

**S6.** Değerlendirme fonksiyonu ne zaman devreye girer? İyi bir EVAL'ın üç özelliği nedir?

**S7.** Ufuk etkisi nedir? Hangi teknikler hafifletir?

**S8.** MCTS'in dört adımını sırayla yaz.

**S9.** UCB1 formülünü yaz. Hangi terim sömürü, hangisi keşif?

**S10.** MCTS aramayı bitirince hangi hamleyi seçer, neden?

**S11.** Şans düğümünün değeri nasıl hesaplanır? Tavlada neden derin arama yapılamaz?

**S12.** Şanslı oyunlarda EVAL için neden "sırayı korumak" yetmez?

---

## Cevaplar

1. MAX faydayı (kendi açısından) en yükseğe çıkarmak, MIN ise en aza indirmek ister. Birinin kazancı diğerinin kaybıdır.
2. Yaprakta faydayı döndürür. MAX düğümü çocukların en büyüğünü, MIN düğümü en küçüğünü alır.
3. Kök = **3** (B = 3, C = 2, D = 2). C'nin **4 ve 6** yaprakları budanır.
4. Hayır, minimax ile aynı değeri verir. Mükemmel sıralamada b^⌈m/2⌉ + b^⌊m/2⌋ − 1 yaprağa, yani yaklaşık b^(m/2) yaprağa bakılır.
5. Daha önce değerlendirilmiş durumların değerini saklayan önbellek. Aynı duruma farklı hamle sıralarıyla gelindiğinde yeniden arama yapılmaz. Dikkat: Budama olan düğümlerin değeri kesin değil, bir **sınırdır**. Tabloya bayrakla (alt/üst/kesin) yazılmalıdır. Derinliği de anahtara ya da kayda eklemek gerekir.
6. Arama derinlik veya zaman sınırında kesildiğinde, yaprakların yerine. (1) Terminal durumları gerçek faydayla aynı sırada sıralamalı, (2) hızlı hesaplanmalı, (3) kazanma şansıyla güçlü biçimde ilişkili olmalı.
7. Kaçınılmaz bir kaybın, erteleyici hamlelerle arama derinliğinin ötesine itilmesi; program kaybı göremez. Sessizlik araması ve tekil genişletmeler hafifletir.
8. Seçim → genişletme → benzetim → geri yayma.
9. UCB1(n) = U(n)/N(n) + C·√(ln N(ebeveyn)/N(n)). İlk terim sömürü, ikinci terim keşif.
10. **En çok ziyaret edilen** hamleyi. Az ziyaret edilmiş bir hamlenin yüksek ortalaması gürültülü olabilir; çok ziyaret edilen hamlenin değeri daha güvenilirdir.
11. Çocuk değerlerinin olasılıkla ağırlıklı ortalamasıdır. Tavlada 21 farklı zar sonucu ve ~20 hamle vardır. Her kat, ağacı ~420 kat büyütür ve alfa-beta tarzı budama zayıflar.
12. Şans düğümleri ortalama aldığı için değerlerin **büyüklüğü** de sonucu etkiler. Sırayı koruyan ama doğrusal olmayan bir dönüşüm en iyi hamleyi değiştirebilir. EVAL, kazanma olasılığının pozitif doğrusal bir dönüşümü olmalıdır.
