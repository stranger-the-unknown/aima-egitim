# Bölüm 9 — Quiz (5 soru)

Cevaplar dosyanın sonunda.

---

**S1.** Sonlu domain’de `∀x P(x)` önermeselleştirmede neye dönüşür?

**S2.** Birleştirmenin (unify) amacı nedir?

**S3.** Occurs-check neden vardır?

**S4.** İleri zincirleme veri güdümlü mü, sorgu güdümlü mü?

**S5.** Horn maddelerinde geriye zincirleme tipik olarak ne yapar?

---

## Cevaplar

**S1.** Domain’deki her sabit için `P(aᵢ)`’lerin ∧ ile birleşimi.

**S2.** İki terim/atomu ortak bir örneğe getiren (tercihen en genel) değişken atamasını bulmak.

**S3.** `?x` ile `f(?x)` gibi sonsuz / döngüsel bağları reddetmek için.

**S4.** Veri güdümlü (olgudan yeni olguya).

**S5.** Hedeften başlayıp kural öncüllerini alt-hedef yaparak olgulara inmek (birleştirme ile).
