# Bölüm 14 — Quiz (5 soru)

Cevaplar dosyanın sonunda.

---

**S1.** Zamansal modelde geçiş modeli neyi verir?

**S2.** Filtreleme ile yumuşatma arasındaki temel fark nedir?

**S3.** HMM’de “gizli” olan nedir, “gözlenen” nedir?

**S4.** Forward filtrelemede predict ve update sırası nasıldır?

**S5.** Viterbi neyi optimize eder (tek cümle)?

---

## Cevaplar

**S1.** `P(X_t | X_{t-1})` — durumun zamanla nasıl evrildiği.

**S2.** Filtreleme yalnızca şimdiye kadar olan kanıtla `P(X_t|e_{1:t})`; yumuşatma geçmiş bir `k<t` için tüm `e_{1:t}` kullanır.

**S3.** Gizli: durum dizisi (ör. yağmur); gözlenen: duyucu çıktıları (ör. şemsiye).

**S4.** Önce geçişle predict, sonra yeni gözlemle update + normalleştir.

**S5.** Gözlem dizisi verildiğinde en yüksek olasılıklı durum yolunu (`arg max P(x_{1:t}|e_{1:t})`).
