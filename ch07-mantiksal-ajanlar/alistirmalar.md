# Bölüm 7 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — Tell / Ask

Bilgi tabanlı ajanın bir turunu dört adımda yazın: algı → ? → ? → eylem. `Tell` ve `Ask` nereye girer?

## A2 — Gerektirme

Semboller: `P`, `Q`. KB = { `P`, `P ⇒ Q` }.

1. KB ⊨ `Q` midir? Neden? (modellerle düşünün)
2. KB ⊨ `P ∧ Q` midir?
3. KB ⊨ `¬P` midir?

## A3 — Doğruluk tablosu demosu

```bash
python ornekler/onerme_mantigi.py
```

1. `Ask: IslakZemin` neden EVET?
2. `Ask: Bulut` neden HAYIR? (KB’de `Bulut ∨ Yağmur` ve `Yağmur` varken.)

## A4 — Izgara çıkarımı

```bash
python ornekler/wumpus_basit.py
```

1. (0,0)’da esinti yokken hangi kareler hemen güvenli ilan edilir?
2. “Tek aday elimasyonu” ne zaman kesin çukur üretir?

## A5 — Model sayısı

5 önerme sembolü varsa kaç olası model vardır? Doğruluk tablosuyla gerektirme kontrolü neden büyük KB’de pratik olmaz?
