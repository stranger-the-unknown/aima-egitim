# Bölüm 14 — Zamansal olasılık: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. HMM, filtreleme, Viterbi, Kalman gibi isimler kamuya açıktır; anlatım özgün Türkçedir.
> Amaç: zaman içinde belirsizliği takip etmek — “şimdi ne biliyorum?”, “yarın ne beklerim?”, “dün aslında neydi?”.

---

## 1. Neden zaman?

Bölüm 13’teki Bayes ağı **statik**ti: bir “anlık dünya”.  
Gerçek ajanlar ise **zaman akışında** yaşar: robot koridorda yürür, hava değişir, sensör gürültülü ölçer.

Zamansal model = her `t` anında durum değişkenleri + gözlemler; komşu zaman dilimleri geçişle bağlanır.

---

## 2. İki yapı taşı

| Parça | Soru | Tipik gösterim |
|-------|------|----------------|
| **Geçiş modeli** | Durum nasıl evrilir? | `P(X_t \| X_{t-1})` (Markov: yalnızca bir önceki) |
| **Duyucu (sensör) modeli** | Bu durumda ne gözlerim? | `P(E_t \| X_t)` |

Ek varsayımlar (eğitim seviyesi):

- **Birinci mertebe Markov:** gelecek, geçmişe yalnızca şimdiki durum üzerinden bağlıdır.
- **Sabit süreç:** geçiş/duyucu tabloları zamana göre değişmez (homojen).

---

## 3. Üç temel soru

Kanıt dizisi `e_{1:t}` verildiğinde:

1. **Filtreleme** — `P(X_t | e_{1:t})`  
   “Şu ana kadar gördüklerime göre **şimdi** durum nedir?” (çevrimiçi)

2. **Kestirim / prediction** — `P(X_{t+k} | e_{1:t})`  
   “Geleceğe `k` adım bak; henüz yeni kanıt yok.”

3. **Yumuşatma / smoothing** — `P(X_k | e_{1:t})` (`k < t`)  
   “Dizi bittikten sonra geçmişteki bir anı daha iyi açıkla.” (ileride + geride bilgi)

Sezgi: filtreleme yalnızca ileri gider; yumuşatma “sonradan gelen ipuçları” ile geçmişi düzeltir.

---

## 4. HMM — gizli Markov modeli (taslak)

**HMM:** durumlar **ayrık** ve gizli; her adımda bir **ayrık gözlem** üretilir.

Klasik oyuncak (özgün Türkçe anlatım):

- Gizli durum: `Yağmur=T/F` (hava)
- Gözlem: `Şemsiye=T/F` (komşunun şemsiye taşıması)

Parametreler:

1. Başlangıç: `P(Yağmur_0)`
2. Geçiş: yağmur → yağmur / güneş → yağmur olasılıkları
3. Duyucu: yağmur varken şemsiye görme olasılığı (ve tersi)

`hmm_filtreleme.py` forward adımıyla sonsalı günceller; `viterbi_kucuk.py` en olası durum yolunu bulur.

---

## 5. Forward filtreleme (sezgi + formül iskeleti)

Her adımda iki alt adım:

1. **Tahmin (predict):** önceki sonsalı geçişle ileri it  
   `P(X_t | e_{1:t-1}) ∝ Σ_{x_{t-1}} P(X_t | x_{t-1}) P(x_{t-1} | e_{1:t-1})`

2. **Güncelle (update):** yeni gözlemi çarp, normalleştir  
   `P(X_t | e_{1:t}) ∝ P(e_t | X_t) P(X_t | e_{1:t-1})`

Bellekte yalnızca son sonsal vektörü tutmak yeter (sabit boyut) — çevrimiçi izleme için ideal.

---

## 6. Viterbi — en olası yol

Filtreleme **marjinal** sonsal verir (`t` anındaki dağılım).  
Bazen istediğimiz: tüm dizi boyunca **tek bir en olası durum yolu**  
`arg max_{x_{1:t}} P(x_{1:t} | e_{1:t})`.

**Viterbi:** dinamik programlama — her zamanda her durum için “buraya en yüksek skorla nasıl geldim?” tutar; sonda geri izler.

Not: en olası yol ≠ her adımdaki marjinal argmax’ların birleşimi (marjinaller tek tek en iyiyi seçebilir ama birlikte tutarsız yol üretebilir).

---

## 7. Kalman — yüksek seviye (sürekli)

Durum sürekli (ör. konum + hız), gürültü yaklaşık **Gaussian**, geçiş/ölçüm **doğrusal** ise:

- Sonsal da Gaussian kalır.
- Ortalama + kovaryans ile özetlenir (Kalman filtresi).

Eğitim notu: ayrıntılı matris türevleri burada yok; fikir = “HMM’nin sürekli kuzeni; predict–update döngüsü aynı.”

Doğrusal değilse genişletilmiş / parçacık filtreleri devreye girer (ileri okuma).

---

## 8. Ajan bakışı

1. Durum ve gözlemi tanımla.
2. Geçiş + duyucu tablolarını (veya Gaussian parametrelerini) yaz.
3. Her yeni gözlemde filtrele → eylem için sonsalı kullan.
4. Geçmişi yeniden yorumlamak gerekirse yumuşat / Viterbi.
5. Sürekli doğrusal dünya → Kalman sezgisine geç.

---

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
