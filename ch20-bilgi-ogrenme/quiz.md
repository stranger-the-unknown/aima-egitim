# Bölüm 20 — Quiz (5 soru)

Cevaplar dosyanın sonunda.

---

**S1.** MLE neyi en büyütür?

**S2.** MAP, MLE’den temel olarak nasıl farklıdır?

**S3.** Bernoulli’de N atışta k yazı için θ_MLE nedir?

**S4.** EM’de E adımı kabaca ne yapar?

**S5.** Bayesyen öğrenmede yeni gözlem için tahmin nasıl yapılır? (tek cümle)

---

## Cevaplar

**S1.** Verinin olabilirliğini: P(D | θ) (veya log’unu).

**S2.** Önsel P(θ) ekler; θ_MAP = argmax P(D|θ)P(θ).

**S3.** k / N.

**S4.** Mevcut parametrelerle gizli değişkenlerin (yumuşak) sorumluluklarını / beklenen yeter istatistiklerini hesaplar.

**S5.** Sonradan P(θ|D) üzerinden P(x|θ)’yı entegre eder (marjinal tahmin); nokta θ̂ seçmek zorunda değildir.
