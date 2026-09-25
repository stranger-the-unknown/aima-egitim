# Bölüm 23 — Doğal dil işleme (giriş): Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe öğretim dilindedir.
> Amaç: dilin sayıya nasıl döküldüğünü, n-gram ve BoW sezgisini, gömülerin yerini görmek.

---

## 1. Dil modeli nedir?

**Dil modeli (LM):** bir sözcük dizisine olasılık atar veya “sıradaki sözcük ne?” sorusuna dağılım verir.

```text
P(w1, w2, …, wn) = P(w1) P(w2|w1) P(w3|w1,w2) …
```

Kullanım: otomatik tamamlama, yazım düzeltme, konuşma tanıma yeniden skorlama, üretim (generate).

---

## 2. n-gram

Tarihsel / eğitici sadeleştirme: yalnızca son **n−1** sözcüğe bak.

- **Unigram:** P(w) — sıra yok
- **Bigram:** P(w_t | w_{t−1})
- **Trigram:** P(w_t | w_{t−2}, w_{t−1})

Sayım + yumuşatma (add-one / Laplace vb.) ile tahmin edilir.  
Artı: basit, hızlı. Eksi: uzun bağlam yok; seyrek sayımlar; morfolojisi zengin dillerde (Türkçe) parçalanma zor.

`n_gram_mini.py` minik Türkçe cümlelerden bigram sayar; skor ve kısa üretim gösterir.

---

## 3. Kelime torbası (bag-of-words)

Metni **sözcük frekans vektörü** yap: sıra çoğu zaman yok sayılır.

```text
"güzel film ama yavaş"  →  {güzel:1, film:1, ama:1, yavaş:1, …}
```

Sınıflandırma (duygu, spam, konu) için klasik ve hâlâ güçlü taban çizgisi.  
Naif Bayes: sınıf verilmişken sözcüklerin koşullu bağımsız olduğunu varsayar; sayımlarla P(sınıf|metin) sıralar.

`bow_siniflandirma.py` elle sayımlı minik duygu / konu örneği verir.

---

## 4. Kelime gömüleri (embeddings) — yüksek seviye

One-hot / BoW seyrek ve “kedi ≈ köpek” benzerliğini bilmez.  
**Gömü:** her sözcük için yoğun vektör (ör. 50–300 boyut); benzer anlamda yakın konum.

Sezgi: “anlam ≈ komşuluk / kullanım bağlamı” (distributional hypothesis).  
Word2Vec, GloVe klasik; modern sistemlerde bağlama duyarlı gömü (transformer) hâkim — Ch24’e köprü.

Bu bölümde kod yazmıyoruz; fikir: **seyrek sayım → yoğun anlam vektörü**.

---

## 5. Görevlere kısa bakış

| Görev | Ne ister? |
|-------|-----------|
| Metin sınıflandırma | etiket (duygu, spam, konu) |
| NER | kişi / yer / kurum span’leri |
| Sözdizim / bağımlılık | cümle yapısı |
| Makine çevirisi | dil A → dil B |
| Özet / QA | uzun metinden kısa cevap |
| Diyalog | çok turlu yanıt |

Pipeline eskiden: tokenize → özellik → model.  
Bugün: büyük dil modelleri birçok görevi tek çatıda; yine de BoW / n-gram **öğrenme ve taban çizgisi** için değerlidir.

---

## 6. Türkçe notu

Ekler (çok şekilli sözcükler) BoW/n-gram sözlüğünü şişirir. Eğitim demolarında küçük derlem + basit tokenize yeter; gerçek sistemde gövdeleme / alt sözcük (BPE) düşünülür.

Özet: **LM = dizi olasılığı; n-gram = kısa bellek; BoW = torba sayım; gömü = yoğun benzerlik.** Kitabı yasal nüshadan oku.
