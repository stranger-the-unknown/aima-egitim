# Bölüm 22 — Pekiştirmeli öğrenme: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe öğretim dilindedir.
> Amaç: ödül sinyalinden politika öğrenmenin sezgisini kurmak; Q-öğrenme ve keşif–sömürü fikrini bağlamak.

---

## 1. Ajan–ortam döngüsü

Pekiştirmeli öğrenmede (RL) ajan, ortamla **deneme–yanılma** ile etkileşir:

```text
  ajan                    ortam
    |                       |
    |---- eylem a_t ------->|
    |<--- ödül r_t, s_{t+1} |
```

| Sembol | Anlam |
|--------|--------|
| s | durum (gözlem) |
| a | eylem |
| r | anlık ödül (skaler sinyal) |
| π | politika: s → a (veya dağılım) |

Bölüm 17’deki MDP’de geçiş T ve ödül R **bilinirdi**; burada çoğu zaman **bilinmez** — ajan deneyimden öğrenir.

---

## 2. Ödül ve getiri (return)

- **Ödül r_t:** tek adımın anlık geri bildirimi (iyi / kötü sinyal).
- **Getiri G_t:** bundan sonraki indirimli toplam:

```text
G_t = r_t + γ r_{t+1} + γ² r_{t+2} + …
```

γ ∈ [0, 1) geleceğin bugüne göre ne kadar önemli olduğunu ayarlar.  
Amaç: beklenen getiriyi maksimize eden politika bulmak — **R’yi ezberlemek değil**, uzun vadeli başarıyı öğrenmek.

---

## 3. Değer ve Q fonksiyonu (sezgi)

- **V^π(s):** s’den π ile devam edersen beklenen getiri.
- **Q^π(s,a):** s’de a’yı seçip sonra π ile devam edersen beklenen getiri.

Optimal Q* bilinirse politika basit: her s’de `argmax_a Q*(s,a)`.  
RL’nin sık yolu: Q’yu **tabloda veya ağda** tahmin etmek.

---

## 4. Zamansal fark (TD) ve Q-öğrenme

Model (T, R) yoksa Bellman yedeklemesini **örnekle** yaklaşık yaparız.

**Q-öğrenme** (tablo):

```text
Q(s,a) ← Q(s,a) + α [ r + γ max_{a'} Q(s',a') − Q(s,a) ]
```

| Parça | Rol |
|-------|-----|
| α | öğrenme oranı (0–1) |
| r + γ max Q(s′,·) | hedef (TD hedefi) |
| max | sonraki durumda açgözlü devam varsayımı |

Epizotlar: başlangıç → eylemler → terminal (veya max adım).  
`q_ogrenme_grid.py` küçük bir ızgarada bunu çalıştırıp Q tablosu ve açgözlü politikayı basar.

---

## 5. Keşif vs sömürü

- **Sömürü:** şu anki en iyi Q’ya göre hareket et (hızlı kısa vadeli kazanç).
- **Keşif:** bilinmeyen / az denenen eylemleri dene (uzun vadede daha iyi politika).

Klasik denge: **ε-açgözlü**

```text
olasılık 1−ε → argmax Q(s,a)
olasılık ε   → rastgele eylem
```

ε’yu eğitim boyunca düşürmek (annealing) sık kullanılır.  
Bandit örneği (`epsilon_greedy_bandit.py`) tek durumlu basitleştirilmiş dünyada aynı gerilimi gösterir: kolları dene vs en iyi kolu çek.

---

## 6. Kısa yol haritası

| Kavram | Bu bölümde |
|--------|------------|
| MDP / Bellman | Ch17’den hatırla; model *bilinmiyor* |
| Q-öğrenme | model-free, off-policy tablo güncellemesi |
| ε-açgözlü | keşif–sömürü |
| Derin RL | Ch21 + Q/politika ağları (ileride) |

Özet: **ödül → deneyim → Q/politika güncellemesi → daha iyi eylem**. Kitabı yasal nüshadan oku; burası sezgi ve minik kod.
