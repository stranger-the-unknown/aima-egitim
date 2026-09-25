# Bölüm 17 — Alıştırmalar

Özgün sorular. Kitap metnini kopyalamayın.

---

## A1 — MDP beşlisi

Kendi cümlelerinizle S, A, T, R, γ’yi bir robot koridor örneğinde doldurun
(3–5 cümle veya madde).

## A2 — Değer yineleme

```bash
python ornekler/deger_yineleme.py
```

(0,0) için V yaklaşık kaç? Açgözlü politikada (0,0) hangi yönü seçiyor?
γ’yi 0.5 yapsaydınız sezgisel olarak V’ler nasıl değişirdi?

## A3 — Politika değerlendirme

```bash
python ornekler/politika_degerlendirme.py
```

π₀ “hep doğu” iken V(0,0) neden π₁’den düşük kalır?
Bir iyileştirme adımında hangi hücrelerin eylemi değişti?

## A4 — Bellman okuma

`V*(s) = max_a Σ_{s′} T(s′|s,a)[R + γ V*(s′)]` satırını Türkçe “hikâye” gibi anlatın.

## A5 — Model yoksa

Geçiş T bilinmiyorsa değer yineleme doğrudan uygulanabilir mi?
Hangi aile yöntemlere (isim düzeyinde) geçilir? (pekiştirmeli öğrenmeye köprü)
