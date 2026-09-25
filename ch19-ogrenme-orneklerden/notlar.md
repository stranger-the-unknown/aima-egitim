# Bölüm 19 — Örneklerden öğrenme: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe öğretim dilindedir.
> Amaç: denetimli öğrenmenin dilini kurmak; ağaç ve doğrusal sınıflandırıcıya sezgi kazandırmak.

---

## 1. Denetimli öğrenme nedir?

Elinde **etiketli örnekler** var: her biri `(x, y)` — özellikler + doğru çıktı.

```text
eğitim kümesi D = {(x¹, y¹), …, (xⁿ, yⁿ)}
amaç: yeni x için y’yi tahmin eden h hipotezi
```

- Sınıflandırma: y kategorik (spam / değil, hasta / değil).
- Bağlanım (regresyon): y sayısal (bu bölümde odak sınıflandırma).

---

## 2. Hipotez uzayı

Öğrenici, olası fonksiyonlar kümesi **H** içinden bir `h` seçer.

- H çok dar → gerçeği kaçırma riski (yetersiz uyum).
- H çok geniş → eğitimde ezber, genelleme zayıf (aşırı öğrenme).

“İyi öğrenme” ≈ eğitim hatasını düşürmek **ve** görülmemiş veride de iyi olmak.

---

## 3. Karar ağacı (sezgi)

İç düğüm: bir özelliğe göre soru (“Outlook = Güneşli?”).  
Yaprak: sınıf etiketi.

Öğrenme fikri (ID3 tarzı):

1. Hep aynı etiket → yaprak.
2. Değilse: etiketleri en çok “saflaştıran” özelliği seç (bilgi kazancı / entropi azalması sezgisi).
3. Alt kümelere bölün, özyinele.

`karar_agaci_mini.py` Türkçe etiketli minik bir hava → oyun veri setinde ağaç kurar.

---

## 4. Aşırı öğrenme ve train / test

Ağaç çok derinleşirse her eğitim örneğini ezberleyebilir; gürültüyü de “öğrenir”.

Pratik:

| Küme | Rol |
|------|-----|
| Eğitim | modeli uydur |
| Doğrulama (opsiyonel) | hiperparametre (derinlik, …) |
| Test | **bir kez** genelleme ölç |

Erken durdurma, budama, düzenlileştirme → aşırı öğrenmeyi yumuşatır.

---

## 5. Doğrusal sınıflandırma taslağı

2 boyutta bir doğru (genelde hiperdüzlem) ile ayırma:

```text
skor = w · x + b
tahmin = 1 eğer skor > 0, değilse 0 (veya ±1)
```

**Perceptron:** yanlış sınıflandırılan örnekte `w` ve `b`’yi örnek yönünde güncelle.  
Doğrusal ayrılabilir veride sonlu adımda ayracı bulur; değilse salınabilir.

Lojistik regresyon benzer skoru olasılığa (sigmoid) çevirir; kayıp gradyanı ile öğrenir — `lineer_siniflandirma.py` perceptron gösterir.

---

## 6. Ajan bakışı

1. Görevi ve etiketi netleştir (ne tahmin?).
2. Özellikleri seç / dönüştür.
3. H’yi seç (ağaç? doğrusal? daha karmaşık?).
4. Train/test ayır; metriği (doğruluk, …) izle.
5. Aşırı öğrenme belirtilerinde modeli sadeleştir.

---

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
