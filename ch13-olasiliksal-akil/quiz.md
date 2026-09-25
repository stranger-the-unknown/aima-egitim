# Bölüm 13 — Quiz (5 soru)

Cevaplar dosyanın sonunda.

---

**S1.** Bayes ağında oklar neyi kodlar (eğitim cevabı)?

**S2.** CPT neyin kısaltmasıdır ve bir düğüm için ne tutar?

**S3.** Joint nasıl CPT’lerden yazılır?

**S4.** Enumeration çıkarımında “gizli değişkenler”e ne yapılır?

**S5.** Rejection sampling’te kanıta uymayan örnekler ne olur?

---

## Cevaplar

**S1.** Değişkenler arası doğrudan bağımlılıkları / koşullu bağımlılık yapısını (DAG).

**S2.** Conditional Probability Table; `P(X | Parents(X))` yerel dağılımı.

**S3.** `P(x₁,…,xₙ) = ∏ P(xᵢ | parents(Xᵢ))`.

**S4.** Tüm olası değerleri üzerinde toplanır (marjinalleştirilir).

**S5.** Atılır (reddedilir); yalnızca kanıta uyan örnekler sayılır.
