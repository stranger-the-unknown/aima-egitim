# Bölüm 20 — Olasılıksal modellerle öğrenme: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe öğretim dilindedir.
> Amaç: parametre öğrenme dilini kurmak; MLE / MAP / Bayes / EM sezgisini vermek.

---

## 1. Ne öğreniyoruz?

Elimizde bir **olasılıksal model** var: parametreler θ (ör. yazı gelme olasılığı θ, CPT satırları, Gaussian μ,σ).

```text
veri D  →  model P(· | θ)  →  θ̂ (tahmin) veya P(θ | D) (sonradan)
```

- **Tam veri:** her örnekte ilgili değişkenler gözüküyor.
- **Eksik / gizli:** bazı değişkenler hiç gözükmüyor → EM tarzı yöntemler.

---

## 2. MLE — en büyük olabilirlik

**Fikir:** Veriyi en olası kılan parametreyi seç.

```text
θ_MLE = argmax_θ  P(D | θ)   (= argmax_θ  log P(D | θ))
```

Bernoulli örneği: N atışta k yazı → `θ_MLE = k / N`.

Kategorik (zar): her yüz için `θ_i = n_i / N` (sayımlar / toplam).

Sezgi: “göreli frekanslar”. Küçük N’de aşırı güvenebilir (0 veya 1’e yapışır).

---

## 3. MAP — en büyük sonradan

Önsel P(θ) eklenir; sonradan ∝ olabilirlik × önsel:

```text
θ_MAP = argmax_θ  P(D | θ) P(θ)
```

Beta(α, β) önseli + Bernoulli: sanki α−1 “sanal yazı”, β−1 “sanal tura” eklenmiş gibi.

```text
θ_MAP ≈ (k + α − 1) / (N + α + β − 2)
```

Az veride önsel “düzenlileştirir”; çok veride MLE’ye yaklaşır.

---

## 4. Bayesyen öğrenme (taslak)

Tek bir θ̂ seçmek yerine **tüm sonradan dağılımı** tutarsın:

```text
P(θ | D) ∝ P(D | θ) P(θ)
yeni x için:  P(x | D) = ∫ P(x | θ) P(θ | D) dθ
```

Pratikte integral zor → yaklaşık yöntemler veya eşlenik önseller (Beta–Bernoulli gibi kapalı form).

---

## 5. EM — eksik veri / gizli değişken

Klasik hikâye: iki bozuk madeni para; hangi atışın hangi paradan geldiği **gizli**.

**E adımı (Expectation):** Mevcut θ ile her örneğin “hangi bileşenden geldiği” sorumluluğunu (yumuşak etiket) hesapla.

**M adımı (Maximization):** Bu sorumlulukları ağırlık gibi kullanıp parametreleri MLE tarzı güncelle.

Tekrarla → (yerel) olabilirlik artar. Global en iyi garanti yok; başlangıca duyarlı olabilir.

`em_karisim_mini.py` iki-para demosunu adım adım yazdırır.

---

## 6. Ajan bakışı

1. Model ailesini seç (Bernoulli? karışım? Bayes ağı?).
2. Veri tam mı, gizli değişken var mı?
3. Tam → MLE / MAP; gizli → EM veya örnekleme.
4. Küçük N’de önsel / düzenlileştirme düşün.
5. Öğrenilen parametreleri bir tahmin veya karar görevine bağla.

---

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
