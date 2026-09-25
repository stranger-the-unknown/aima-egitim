# Bölüm 8 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — FOL vs önerme

“Her çalışan bir ofiste oturur” bilgisini:

1. Yalnız önerme sembolleriyle (en az 3 çalışan varsayarak) nasıl temsil edersiniz? Zorluk ne?
2. Tek bir FOL cümlesiyle nasıl yazarsınız?

## A2 — Niceleyici sırası

Aşağıdaki iki cümleyi Türkçe yorumlayın; neden farklı olduklarını bir örnek domain ile gösterin:

1. `∀x ∃y Bagli(x, y)`
2. `∃y ∀x Bagli(x, y)`

## A3 — Sözlük KB demosu

```bash
python ornekler/fol_sozluk.py
```

1. `Ata(Leyla, Ece)` neden türetilir? Hangi kural adımları?
2. `Ask Ata(Ece, Leyla)` neden HAYIR?

## A4 — Çeviri demosu

```bash
python ornekler/fol_ceviri.py
```

“Her kedi bir hayvanı sever” ile “Bir hayvan vardır ki her kedi onu sever” arasındaki FOL farkını kendi cümlelerinizle yazın.

## A5 — Tuzak teşhisi

Şu “kural” yanlış mı? Neden?

`∀x ∀y (Ebeveyn(x, y) ∧ Ata(x, y))`  — “Her ebeveyn aynı zamanda atadır” demek istenmişti.
