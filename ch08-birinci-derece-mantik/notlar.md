# Bölüm 8 — Birinci derece mantık: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Kavramları Türkçe, kendi cümlelerimizle öğretir.
> Amaç: FOL’ün “neden gerekli” olduğunu ve sembollerin sezgisini netleştirmek — tam teorem kanıtlayıcı değil.

---

## 1. Önermeler mantığı neden yetmez?

Önermeler mantığında her atomik cümle bölünmez bir doğruluk değeridir: `Yağmur`, `IslakZemin`.  
Ama gerçek dünyada çoğu bilgi **nesneler** ve aralarındaki **ilişkiler** üzerinedir:

- “Ali, Ayşe’nin ebeveynidir.”
- “Her ebeveyn bir atadır.”
- “En az bir öğrenci dersi geçti.”

Bunları önerme sembollerine sıkıştırmak mümkün ama hantal: her kişi çifti için ayrı önerme (`Ebeveyn_Ali_Ayse`) ve her genel kural için sonsuz sayıda cümle gerekir. **Birinci derece mantık (FOL / BDM)** nesne, ilişki ve niceleyici dilini verir.

---

## 2. Ontoloji: nesne, ilişki, fonksiyon

Bir FOL dilinde tipik yapı taşları:

| Tür | Ne işe yarar | Örnek |
|-----|--------------|--------|
| **Sabit** | Belirli bir nesne adı | `Ali`, `Ankara`, `0` |
| **Değişken** | “bir nesne” yer tutucusu | `x`, `y` |
| **Fonksiyon** | nesneden nesneye eşleme | `anne(x)`, `ustu(x,y)` |
| **Yüklem (ilişki)** | nesne(ler) hakkında doğru/yanlış | `Ebeveyn(x,y)`, `Kirmizi(x)` |

**Terim (term):** sabit, değişken veya fonksiyon uygulaması (`anne(Ali)`).  
**Atomik cümle:** yüklem + terimler (`Ebeveyn(Ali, Ayse)`).  
Bileşik cümleler ¬, ∧, ∨, ⇒ ve niceleyicilerle kurulur.

---

## 3. Niceleyiciler: ∀ ve ∃

- **Evrensel (∀):** “her … için” — `∀x Ebeveyn(x,y) ⇒ Ata(x,y)` (y sabitken: y’nin her ebeveyni atasıdır).
- **Varoluşsal (∃):** “en az bir … vardır” — `∃x Gecti(x, Ders8)`.

Niceleyici **etki alanı** (scope) önemlidir: parantez / bağlaç sırası anlamı değiştirir.

| Cümle (sezgi) | Okuma |
|---------------|--------|
| `∀x ∃y Sever(x,y)` | Herkes en az birini sever (kişiden kişiye farklı `y` olabilir) |
| `∃y ∀x Sever(x,y)` | Herkesin sevdiği **tek bir** kişi vardır |

Bu iki cümle **eşit değildir**; niceleyici sırası klasik bir tuzak.

---

## 4. Sözdizim ve anlambilim (sezgi)

- **Sözdizim:** hangi dizilerin geçerli formül olduğu (terim, atom, niceleyici…).
- **Anlambilim:** bir **yorum** (interpretation) sabitleri domain nesnelerine, yüklemleri ilişkilerle, fonksiyonları eşlemelerle bağlar; formül o yorumda doğru veya yanlış olur.

**Domain (evren):** üzerinde konuştuğumuz nesneler kümesi. Aynı semboller farklı domain’de farklı anlam taşır: `Ebeveyn` aile ağacında veya “doğrudan üst klasör” anlamında kullanılabilir — önemli olan tutarlı yorum.

Gerektirme fikri Bölüm 7 ile aynı ruh: KB’nin doğru olduğu **her** yorumda sorgu da doğruysa KB ⊨ sorgu.

---

## 5. Evrensel örnekleme (eğitim seviyesi)

Tam bir çıkarım motoru bu bölümün konusu değil (Bölüm 9). Yine de sık kullanılan bir adım:

**Evrensel örnekleme (UI):** `∀x P(x)` biliniyorsa, domain’deki bir sabit `a` için `P(a)` yazılabilir.

Pratikte küçük KB’lerde:

1. Olgular: `Ebeveyn(Ali, Ayse)`, `Ebeveyn(Ayse, Can)` …
2. Kural şablonu: `Ebeveyn(x,y) ⇒ Ata(x,y)` ve `Ebeveyn(x,z) ∧ Ata(z,y) ⇒ Ata(x,y)`
3. Değişkenleri olgularla **örüntü eşleme** (basit birleştirme) → yeni `Ata(...)` olguları

`fol_sozluk.py` tam teorem kanıtlayıcı değildir; Python sözlük/küme ile bu fikri gösterir.

---

## 6. Sık yapılan hatalar

1. **Niceleyici sırasını karıştırmak** (`∀∃` ≠ `∃∀`).
2. **Özgür değişken bırakmak** — sorgu veya KB cümlesinde `x` niceleyicisiz kalırsa anlam belirsizdir.
3. **İmplikasyonu “ve” sanmak** — `Ebeveyn(x,y) ⇒ Ata(x,y)` her `x,y` için; ebeveyn olmayan çiftlerde öncül yanlış olduğu için formül doğru kalır (önermeler mantığındaki ⇒ ile aynı).
4. **Domain’i unutmak** — “herkes” hangi küme? Boş domain, tek elemanlı domain vb. eğitimde açıkça yazın.
5. **Fonksiyonu yüklem sanmak** — `anne(x)` bir terim üretir; `Anne(x,y)` bir ilişkidir.

---

## 7. Özet

| Kavram | Tek cümle |
|--------|-----------|
| FOL | Nesne + ilişki + fonksiyon + niceleyici dili |
| ∀ / ∃ | Hepsi / en az biri |
| Domain | Konuşulan nesneler kümesi |
| UI + eşleme | Genel kuralı somut olgulara uygulama (eğitim) |
| Tuzak | Niceleyici sırası, özgür değişken, ⇒ okuması |

Örnekler: `fol_sozluk.py`, `fol_ceviri.py`.

Sonraki bölüm (9): FOL’de çıkarım — birleştirme, zincirleme, çözümleme sezgisi.
