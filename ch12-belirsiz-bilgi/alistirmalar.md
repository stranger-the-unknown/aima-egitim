# Bölüm 12 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — Bayes elle

Bir fabrika parçasının kusurlu olma önseli `P(K) = 0.02`.  
Sensör uyarısı: `P(U | K) = 0.95`, `P(U | ¬K) = 0.10`.  
Uyarı görüldüğünde `P(K | U)` nedir? Adımları yazın.

## A2 — Marjinalleştirme

İki değişkenli ortak tablo:

| A | B | P |
|---|---|---|
| T | T | 0.12 |
| T | F | 0.18 |
| F | T | 0.28 |
| F | F | 0.42 |

`P(A=T)` ve `P(B=T | A=T)` hesaplayın.

## A3 — Bağımsızlık kontrolü

A2 tablosunda `P(A=T, B=T) == P(A=T)·P(B=T)` mi? Bağımsız mı? Bir cümle.

## A4 — Kod: tıbbi test

```bash
python ornekler/bayes_kurali.py
```

1. Pozitif test sonrası `P(Hasta|+)` yaklaşık yüzde kaç?
2. Önseli `0.01` yapsaydınız (kodda değiştirip) sonsal nasıl değişirdi — tahmininizi yazın, sonra deneyin.

## A5 — Naif Bayes

```bash
python ornekler/naive_bayes_mini.py
```

`"bedava kredi kazan"` neden spam tarafına düşüyor? Hangi kelimeler skorları etkiliyor?
