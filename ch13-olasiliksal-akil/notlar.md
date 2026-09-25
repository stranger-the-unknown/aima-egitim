# Bölüm 13 — Bayes ağları: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Bayes ağı, CPT, enumeration gibi isimler kamuya açıktır; anlatım özgün Türkçedir.
> Amaç: tam ortak tabloyu patlatmadan belirsizliği yapılandırmak ve küçük ağda çıkarım yapmak.

---

## 1. Sorun: tam ortak patlar

`n` boolean değişken → ortak tabloda `2ⁿ` satır.  
Çoğu dünya **seyrek bağımlılık** taşır: her şey her şeye bağlı değildir.

**Bayes ağı**, bağımlılıkları bir DAG ile kodlar; her düğüm yalnızca **ebeveynlerine** koşullu bir küçük tablo (CPT) tutar.

---

## 2. Yapı (DAG)

- Düğüm = rastgele değişken
- Ok `X → Y` = “X, Y’nin doğrudan etkilerinden biri” (nedensel okuma sık kullanılır ama grafik aslında koşullu bağımsızlık kodlar)
- Döngü yok (yönlü asiklik)

Örnek senaryo (özgün Türkçe ofis):

```
Yangin          SigaraDumanı
   \              /
    \            /
     v          v
        Alarm
          |
          v
     MudurArar
```

- Yangın veya sigara dumanı alarmı tetikleyebilir.
- Müdür, alarm çalınca (bazen yanlışlıkla) arayabilir.

---

## 3. CPT — koşullu olasılık tablosu

Her düğüm `X` için `P(X | Parents(X))` tablosu.

Kök düğümde ebeveyn yok → önsel `P(X)`.

Örnek (Alarm, ebeveynler Yangin, Sigara):

| Yangin | Sigara | P(Alarm=T \| …) |
|--------|--------|-----------------|
| T | T | 0.95 |
| T | F | 0.88 |
| F | T | 0.70 |
| F | F | 0.001 |

`cpt_goster.py` bu tabloları düzgün yazdırır.

---

## 4. Ortak dağılımın çarpanlara ayrılması

Ağın tanımladığı joint:

```
P(x₁,…,xₙ) = ∏ᵢ P(xᵢ | parents(Xᵢ))
```

Böylece büyük tablo yerine yerel CPT’lerin çarpımı yeterlidir.

---

## 5. Koşullu bağımsızlık (sezgi)

Eğitim seviyesi kurallar (tam d-ayrıştırma teorisi derinleştirilmeden):

- Bir düğüm, **ebeveynleri verildiğinde**, ebeveyn olmayan atalarından koşullu bağımsızdır (Markov koşulu — kabaca).
- Ortak çocuk üzerinden “açıklama” (explaining away): alarm çaldıysa yangın ve sigara birbirini “açar” — biri doğrulanınca diğeri daha az olası görünür.

Detaylı grafik kriterleri (d-separation) ileri okumada; burada sezgi yeter.

---

## 6. Exact çıkarım — enumeration

Sorgu: `P(Q | e)` — kanıt `e` sabitken sorgu değişkeninin dağılımı.

**Enumeration** fikri:

1. Gizli (ne sorgu ne kanıt) değişkenler üzerinde topla.
2. Her tam atamada joint’i CPT çarpımıyla hesapla.
3. Kanıta uymayanları at / sıfırla.
4. Sorgu değerlerine göre topla, normalleştir.

Küçük ağlarda (`bayes_agi_kucuk.py`) işe yarar; büyük ağlarda maliyet üstel → yaklaşık yöntemler.

---

## 7. Örnekleme — yüksek seviye

| Yöntem | Fikir (tek cümle) |
|--------|-------------------|
| Prior sampling | Köktan yaprağa CPT’lere göre örnek üret |
| Rejection | Kanıta uymayan örnekleri at |
| Likelihood weighting | Kanıt düğümlerini sabitle, ağırlıkla düzelt |
| Gibbs / MCMC | Tek değişkeni koşullu güncelleyerek gez |

Bu bölümde kod örnekleme yapmaz; sezgi yeter. Exact enumeration kodda vardır.

---

## 8. Ajan bakışı

1. Nedensel / bağımlılık yapısını çiz.
2. CPT’leri uzman veya veriden doldur.
3. Gözlemleri kanıt olarak bağla.
4. Enumeration veya yaklaşık çıkarımla sonsal al.
5. Karar için sonsalı kullan (sonraki bölümler).

---

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
