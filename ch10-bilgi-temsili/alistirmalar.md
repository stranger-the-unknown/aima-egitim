# Bölüm 10 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — Kategori zinciri

Aşağıdaki hiyerarşiyi çizin veya listeleyin: `Canli → Hayvan → Kus → Penguen`.  
`is_a(Penguen, Canli)` doğru mu? Neden?

## A2 — Üyelik vs alt-tür

`Kedi(minnos)` ile `is_a(Kedi, Memeli)` farkını birer cümleyle ayırt edin. Hangisi nesne–kategori, hangisi kategori–kategori?

## A3 — Ontoloji mini demosu

```bash
python ornekler/ontoloji_mini.py
```

1. `is_a("Kedi", "Hayvan")` ne döner?
2. Yeni kategori `Tekir` ekleyip `Kedi` altına bağlayın; `is_a("Tekir", "Memeli")` beklenen sonuç nedir?

## A4 — Varsayılan akıl

```bash
python ornekler/varsayilan_akil.py
```

1. `serce` için uçma sonucu nedir?
2. `penguen_pingu` için neden farklıdır?
3. Yeni bir `deve_kusu` ekleyip “kuş ama uçmaz” istisnası nasıl modellersiniz? (kodda veya sözle)

## A5 — KR vs FOL dump

“Tüm bilgimi yüzlerce bağımsız FOL cümlesi olarak yazdım; ortak kategori yok.” Bu yaklaşımın iki sakıncasını yazın.
