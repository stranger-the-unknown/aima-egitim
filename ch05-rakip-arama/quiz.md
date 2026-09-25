# Bölüm 5 — Quiz (5 soru)

Cevaplar dosyanın sonunda.

---

**S1.** Sıfır toplamlı oyunda MAX ve MIN’in hedefleri nedir?

**S2.** Minimax yaprakta ne döndürür? MAX / MIN düğümünde ne yapar?

**S3.** Alpha-beta budama sonucu değiştirir mi?

**S4.** Değerlendirme fonksiyonu ne zaman devreye girer?

**S5.** İki optimal XOX ajanı oynarsa tipik sonuç nedir? Neden?

---

## Cevaplar

**S1.** MAX utility’yi büyütür; MIN küçültür (MAX açısından).

**S2.** Yaprakta utility. MAX: çocukların max’ı; MIN: çocukların min’i.

**S3.** Hayır — aynı optimal değer; sadece daha az düğüm.

**S4.** Arama derinlik/zaman sınırında kesilince yaprak yerine sezgisel skor için.

**S5.** Beraberlik. Oyun çözülmüştür; kusursuz oyunda kimse zorla kazanamaz.
