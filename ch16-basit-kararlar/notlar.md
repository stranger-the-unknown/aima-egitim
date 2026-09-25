# Bölüm 16 — Basit kararlar alma: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Anlatım özgün Türkçe öğretim dilindedir.
> Amaç: belirsizlik altında “hangi eylemi seçmeliyim?” sorusuna fayda teorisiyle cevap vermek.

---

## 1. Tercihlerden faydaya

Ajan sonuçlar arasında **tercih** sıralar: A ≻ B ≻ C gibi.  
Rasyonel tercihler (tamlık, geçişlilik vb. varsayımlarla) bir **fayda fonksiyonu** `U` ile temsil edilebilir:

```text
A ≻ B  ⇔  U(A) > U(B)
```

Fayda yalnızca “para” değildir: sağlık, riskten kaçınma, zaman… hepsi aynı ölçeğe indirgenebilir (eğitim sezgisi).

---

## 2. Belirsizlik ve beklenen fayda

Sonuç kesin değilse eylem `a` bir **sonuç dağılımı** üretir.  
**Beklenen fayda:**

```text
EU(a) = Σ_s  P(sonuç=s | a) · U(s)
```

**MEU ilkesi:** seç `a*` = argmax_a EU(a).  
Bu, tek adımlı karar problemlerinin çekirdeğidir.

`beklenen_fayda.py` piyango ve tıbbi tedavi senaryolarında MEU’yu sayısal gösterir.

---

## 3. Risk tutumu (kısa)

Aynı beklenen para için farklı faydalar:

| Tutum | Sezgi |
|-------|--------|
| Risk nötr | U(para) ≈ doğrusal |
| Risk kaçınan | kesin küçük kazanç ≻ riskli büyük umut |
| Risk seven | tersi |

Eğitim notu: U’yu “mutluluk skoru” gibi düşünün; para ile karıştırmayın.

---

## 4. Bilgi değeri (VOI) — yüksek seviye

Bir testi / gözlemi **şimdi** yapmak, sonra daha iyi eylem seçmenizi sağlar.  
**Bilgi değeri:** test sonrası beklenen MEU − testsiz MEU − (test maliyeti, varsa).

- VOI > maliyet → testi al.
- Her zaman pozitif olmak zorunda değil (maliyetli veya eylemi değiştirmeyen bilgi).

`voi_mini.py` iki hastalık hipotezi + test senaryosuyla minik sayısal demo verir.

---

## 5. Karar ağları (iskelet)

Bayes ağına **karar** ve **fayda** düğümleri eklenir:

```text
[Şans düğümleri]  →  olasılık (CPT)
[Karar düğümü]    →  ajanın seçtiği eylem
[Fayda düğümü]    →  U(ebeveynler)
```

Çözüm fikri: karar düğümünü sabitle → şansları çıkarımla çöz → beklenen faydayı hesapla → en iyi kararı seç.  
Bu bölümde tam çıkarım motoru yazmıyoruz; iskeleti ve MEU bağını kavramanız yeterli.

---

## 6. Ajan bakışı

1. Sonuçları listele, `U` ata (veya tercihlerden türet).
2. Her eylem için `P(sonuç | eylem)` modelini kur.
3. EU hesapla → MEU eylemini seç.
4. Gözlem alabilirsen VOI’ye bak.
5. Yapı büyürse karar ağı / sonraki bölümde MDP’ye geç.

---

## Kaynaklar

- [aima.cs.berkeley.edu](https://aima.cs.berkeley.edu/)
- [github.com/aimacode](https://github.com/aimacode)
