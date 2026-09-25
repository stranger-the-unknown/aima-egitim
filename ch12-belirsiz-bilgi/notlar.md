# Bölüm 12 — Belirsiz bilgi: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Olasılık, Bayes kuralı, naif Bayes gibi isimler kamuya açıktır; anlatım özgün Türkçedir.
> Amaç: ajanın kısmi / gürültülü gözlem altında inançlarını sayılarla güncellemesi.

---

## 1. Neden olasılık?

Mantık (Bölüm 7–9) “doğru / yanlış” ile çalışır. Gerçek ortamda:

- sensör gürültülüdür,
- birçok olası açıklama vardır,
- ajan tam bilgiye sahip değildir.

**Olasılık**, inancı `[0, 1]` aralığında tutar. Ajan yeni kanıt görünce bu sayıları **günceller** (Bayes).

İnanç derecesi ≠ “nesnel frekans” tartışması burada açılmaz; eğitimde “ajanın inanç ölçüsü” yeterlidir.

---

## 2. Rastgele değişken ve olay

**Rastgele değişken (RV):** olası değerler alan sembol.

| Tür | Örnek değerler |
|-----|----------------|
| Boolean | `Yagmur ∈ {doğru, yanlış}` |
| Ayrık | `Hava ∈ {güneş, bulut, yağmur}` |
| Sürekli | `Sıcaklık ∈ ℝ` (bu bölümde az kullanırız) |

**Olay:** değişkenlerin belirli değer aldığı durumlar kümesi.  
Örn. `Yagmur = doğru`.

**Önsel (prior)** `P(H)`: kanıt yokken hipoteze inanç.  
**Sonsal (posterior)** `P(H | E)`: kanıt `E` görüldükten sonraki inanç.

---

## 3. Ortak dağılım (joint)

Birkaç değişkenin birlikte dağılımı: **tam ortak (full joint)** tablo.

İki boolean değişken `A`, `B` için 4 satır:

| A | B | P(A, B) |
|---|---|---------|
| T | T | … |
| T | F | … |
| F | T | … |
| F | F | … |

Kurallar (eğitim özeti):

- tüm girdiler ≥ 0,
- toplam = 1.

**Marjinalleştirme:** ilgilenmediğin değişkeni topla / “çıkar”.

```
P(A = T) = P(A=T, B=T) + P(A=T, B=F)
```

**Koşullu:**

```
P(A | B) = P(A, B) / P(B)     (P(B) > 0)
```

Tam ortak her soruyu cevaplar ama değişken sayısı artınca tablo **üstel** büyür → Bölüm 13’te Bayes ağları bunu sıkıştırır.

---

## 4. Bağımsızlık

`A` ve `B` **bağımsız** ise:

```
P(A, B) = P(A) · P(B)
```

eşdeğeri: `P(A | B) = P(A)` (B’yi bilmek A hakkındaki inancı değiştirmez).

**Koşullu bağımsızlık:** `C` verildiğinde `A` ⊥ `B | C`:

```
P(A, B | C) = P(A | C) · P(B | C)
```

Naif Bayes ve Bayes ağları bu fikre dayanır.

---

## 5. Bayes kuralı — sezgi

```
P(H | E) = P(E | H) · P(H) / P(E)
```

| Parça | İsim (eğitim) | Anlam |
|-------|---------------|--------|
| `P(H)` | önsel | kanıttan önce |
| `P(E \| H)` | olabilirlik (likelihood) | hipotez doğruysa kanıtın olasılığı |
| `P(E)` | kanıtın marjinali | normalleştirme |
| `P(H \| E)` | sonsal | güncellenmiş inanç |

İki hipotez (`H` ve `¬H`) için payda:

```
P(E) = P(E | H)P(H) + P(E | ¬H)P(¬H)
```

`bayes_kurali.py` tıbbi test ve yağmur–şemsiye sayılarını Türkçe yazdırır.

---

## 6. Naif Bayes — iskelet

Sınıf `C`, özellikler `X₁ … Xₙ`. **Naif** varsayım: özellikler sınıfa göre koşullu bağımsız:

```
P(C | X) ∝ P(C) · ∏ᵢ P(Xᵢ | C)
```

Metin örneği: “spam / ham”, kelime var/yok özellikleri.  
`naive_bayes_mini.py` el sayımlarıyla (sklearn yok) küçük bir demo yapar.

Dikkat: varsayım gerçekte çoğu zaman yanlışır; yine de pratikte şaşırtıcı derecede işe yarar.

---

## 7. Ajan bakışı (kısa)

1. Dünyayı RV’lerle modelle.
2. Önselleri ve olabilirlikleri bil / öğren.
3. Gözlem gelince Bayes ile sonsal güncelle.
4. Karar için sonsalı kullan (karar teorisi sonraki bölümlerde).

---

## 8. Bu klasördeki kod

| Script | Ne gösterir |
|--------|-------------|
| `bayes_kurali.py` | Sayısal Bayes güncellemesi + adım adım Türkçe çıktı |
| `naive_bayes_mini.py` | Kelime sayımları → spam/ham skor |

---

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
