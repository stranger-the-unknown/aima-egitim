# Bölüm 24 — Quiz (5 soru)

Cevaplar dosyanın sonunda.

---

**S1.** Kelime gömüsü one-hot’a göre ne kazandırır?

**S2.** LSTM’in RNN’e göre yüksek seviye katkısı nedir?

**S3.** Dikkatte α = softmax(QKᵀ) neyi temsil eder?

**S4.** Transformer katmanında self-attention’tan sonra tipik olarak ne gelir? (yüksek seviye)

**S5.** Aktarım öğrenmesinde “fine-tune” kısaca ne demektir?

---

## Cevaplar

**S1.** Yoğun vektör; benzer anlamlı / benzer bağlamlı sözcükleri yakın gösterir; genelleme.

**S2.** Kapılarla seçici bellek; uzun bağımlılıklarda daha dayanıklı (gradyan kaybını yumuşatma sezgisi).

**S3.** Sorgunun her anahtara verdiği ağırlıklar (satır toplamı 1); “nereye ne kadar bakayım?”.

**S4.** (Artık bağlantı / norm ile birlikte) konum-bağımsız feed-forward (MLP) bloğu.

**S5.** Önceden eğitilmiş modeli hedef görevin etiketleriyle biraz daha eğiterek uyarlamak.
