# Bölüm 15 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — Program = model

Üretimsel modelde “önce örnekle, sonra gözlem üret” sırası neden doğal?
Bir cümleyle Bayes ağı CPT’sine nasıl benzediğini yazın.

## A2 — Naif koşullandırma

```bash
python ornekler/basit_uretimsel_model.py
```

`P(hileli | zar=6)` yaklaşık değeri ile analitik değer ne kadar yakın?
Önsel `P(hileli)=0.3` iken sonsal neden yükseliyor?

## A3 — Reddetme

```bash
python ornekler/reddetme_ornekleme.py
```

`zar=6` için red oranı kabaca ne? `zar=1` için neden daha yüksek?

## A4 — Açık evren (sezgi)

“Binadaki daire sayısı bilinmiyor; her daireden gürültü gelebilir” senaryosunda
klasik sabit Bayes ağı neden zorlanır? (2–3 cümle, framework adı gerekmez.)

## A5 — Ne zaman BN, ne zaman PP?

Sabit 4 düğümlü ofis alarmı (bölüm 13) için BN yeterli midir?
Rastgele uzunlukta “kaç robot koridorda?” modeli için neden program metaforu daha doğal?
