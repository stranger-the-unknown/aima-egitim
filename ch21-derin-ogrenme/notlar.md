# Bölüm 21 — Derin öğrenme: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe öğretim dilindedir.
> Amaç: çok katmanlı ağ dilini kurmak; geriye yayılım ve genelleme sezgisi vermek. Ağır framework şart değil.

---

## 1. Çok katmanlı ağ nedir?

Her katman: doğrusal dönüşüm + doğrusal olmayan aktivasyon.

```text
z¹ = W¹ x + b¹
a¹ = σ(z¹)
z² = W² a¹ + b²
a² = σ(z²)
…
```

Tek doğrusal katman yalnızca doğrusal sınır çizer. Ara katman + aktivasyon → XOR gibi doğrusal ayrılmaz problemler çözülebilir.

---

## 2. Aktivasyonlar (sezgi)

| σ | Aralık | Not |
|---|--------|-----|
| sigmoid | (0,1) | yumuşak eşik; doyunca gradyan küçülür |
| tanh | (−1,1) | sıfır merkezli sigmoid kuzeni |
| ReLU | max(0,z) | basit, seyrek; negatifte gradyan 0 |

`aktivasyon_goster.py` aynı z değerlerinde üçünü yan yana basar (matplotlib varsa grafik de dener).

---

## 3. Kayıp ve öğrenme

Hedef y ile tahmin ŷ arasındaki hata ölçüsü: kare hata, çapraz entropi, …

```text
L(W) = ortalama kayıp(y, f_W(x))
W ← W − η ∇_W L
```

η: öğrenme oranı. Çok büyük → salınım; çok küçük → yavaş.

---

## 4. Geriye yayılım (yüksek seviye)

İleri geçişte ara değerleri sakla.  
Kayıptan geriye doğru zincir kuralı ile her W, b için gradyanı hesapla.

Sezgi: “hata sinyalini katman katman geri dağıt”.  
Modern kütüphaneler bunu otomatik türevle yapar; burada `mlp_numpy_mini.py` 2 katman için elle yazar.

---

## 5. Aşırı öğrenme ve düzenlileştirme

Ağ çok kapasiteli + az veri → eğitimi ezberler, testte zayıf kalır.

Yüksek seviye çareler:

- Daha fazla / çeşitli veri
- Erken durdurma (doğrulama kaybı artınca kes)
- Ağırlık cezası (L2 / weight decay): büyük W’ye ceza
- Dropout (eğitimde rastgele birimleri kapatma) — bu pakette kodlanmadı
- Daha sade mimari

---

## 6. Ajan bakışı

1. Girdi/çıktı kodlamasını netleştir.
2. Minik mimari ile başla; kaybın düştüğünü izle.
3. Train/val ayır; ezber belirtisinde düzenlileştir.
4. Gerekirse derinleştir / genişlet — körü körüne değil.

---

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
