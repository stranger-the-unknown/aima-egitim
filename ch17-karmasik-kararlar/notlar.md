# Bölüm 17 — Karmaşık kararlar alma: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe öğretim dilindedir.
> Amaç: sıralı belirsiz kararları MDP ile modellemek; değer / politika yineleme sezgisini kurmak.

---

## 1. Neden “karmaşık”?

Bölüm 16 tek hamle: eylem → sonuç → fayda.  
Burada **zaman uzar**: bugünkü eylem yarının durumunu etkiler; ödüller birikir.

```text
s0 --a0→ s1 --a1→ s2 --…→  (indirimli toplam ödül)
```

Amaç: uzun vadeli beklenen getiriyi maksimize eden **politika** π(s) = eylem.

---

## 2. MDP beşlisi

| Bileşen | Anlam |
|---------|--------|
| S | durum kümesi |
| A | eylem kümesi |
| T(s′ \| s, a) | geçiş (Markov: yalnızca bugünkü s) |
| R(s, a, s′) veya R(s) | anlık ödül |
| γ ∈ [0,1) | indirim (gelecek daha az ağır) |

Epizodik terminaller (ödül / ceza hücresi) eğitim gridworld’lerinde sık görülür.

---

## 3. Bellman denklemi (sezgi)

Optimal değer `V*(s)`: s’den başlayıp optimal oynarsanız beklenen indirimli getiri.

```text
V*(s) = max_a  Σ_{s′} T(s′|s,a) [ R(s,a,s′) + γ V*(s′) ]
```

Okuma: “her eylem için beklenen (ödül + indirimli devam); en iyisini seç.”  
Politika: her s’de bu max’ı veren a.

---

## 4. Değer yineleme

`V` bilinmiyor → **yardımcı tahmin** ile güncelle:

1. V₀ ← 0 (veya rastgele)
2. Her s için Bellman yedeklemesiyle Vₖ₊₁(s) hesapla
3. Δ küçük olunca dur
4. Açgözlü politika: π(s) = argmax_a Q(s,a; V)

`deger_yineleme.py` 3×2’lik minik gridworld’te bunu basar.

---

## 5. Politika yineleme (özet)

1. **Değerlendir:** sabit π için V^π’yi çöz (doğrusal sistem veya yineleme)
2. **İyileştir:** her s’de V^π’ye göre açgözlü eylem seç → yeni π
3. π değişmeyince optimal

`politika_degerlendirme.py` sabit bir politikayı değerlendirir ve tek bir iyileştirme adımı gösterir.

---

## 6. Ajan bakışı

1. Durum / eylem / ödül / geçişi yaz (model varsa).
2. γ seç (ufuk ne kadar önemli?).
3. Değer veya politika yineleme ile π bul.
4. Model yoksa → pekiştirmeli öğrenme (ileriki bölüm).

---

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
