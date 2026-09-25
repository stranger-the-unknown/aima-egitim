# Bölüm 9 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — Önermeselleştirme

Domain D = {a, b}. `∀x ∃y R(x, y)` cümlesini önerme mantığına (∧ / ∨ açılımı) çevirin. Kaç atomik önerme sembolü kullanırsınız?

## A2 — Birleştirme elle

`unify` sonuçlarını yazın (veya BAŞARISIZ):

1. `f(?x)` ve `f(Ankara)`
2. `f(?x)` ve `g(Ankara)`
3. `?x` ve `f(?x)`

Sonra `python ornekler/birlesim_unification.py` ile kontrol edin.

## A3 — İleri vs geri

Bir KB’de yüzlerce olgu ve onlarca kural var; tek bir soru soruyorsunuz (“USB son nerede görüldü?”). İleri mi geriye mi zincir tercih edersiniz? Neden?

## A4 — Geriye zincir demosu

```bash
python ornekler/geriye_zincir.py
```

1. `SonGorulen(USB, ?yer)` hangi yer bağını üretir?
2. `IzSur(USB, ?kim)` kimleri döndürür? Hangi olgular zincire girer?

## A5 — Çözümleme eskizi

KB ⊨ α kontrolünde neden `KB ∧ ¬α` üzerinde çelişki (boş cümle) aranır? Bir cümleyle açıklayın.
