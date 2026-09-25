# Bölüm 13 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — CPT okuma

Alarm CPT’sinde `Yangin=F`, `SigaraDumanı=F` iken `P(Alarm=T)` nedir?
Bu satır ne anlama gelir (bir cümle)?

## A2 — Faktörizasyon

`P(Yangin=T, Sigara=F, Alarm=T, MudurArar=T)` ifadesini CPT çarpımı olarak yazın
(sayıları `cpt_goster.py` / koddan doldurun, sonucu hesaplayın).

## A3 — CPT yazdır

```bash
python ornekler/cpt_goster.py
```

MudurArar CPT’sinde Alarm=F iken müdür neden hâlâ küçük bir olasılıkla arar? Sezginizi yazın.

## A4 — Enumeration

```bash
python ornekler/bayes_agi_kucuk.py
```

1. Sadece `MudurArar=T` iken `P(Yangin=T|e)` yaklaşık kaç?
2. `Alarm=T` eklenince bu değer nasıl değişiyor?

## A5 — Explaining away

Alarm çalıyor ve yangın **yok**. Sigara dumanı olasılığı neden artar?
(Koddaki ilgili satıra bakıp sayıyı not edin.)
