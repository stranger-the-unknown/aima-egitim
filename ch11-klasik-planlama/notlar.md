# Bölüm 11 — Klasik planlama: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. STRIPS, durum-uzayı arama gibi isimler kamuya açıktır; anlatım özgün Türkçedir.
> Amaç: küçük, belirleyici, tam gözlemlenebilir dünyada plan üretme sezgisi.

---

## 1. Klasik planlama nedir?

**Klasik** varsayımlar (eğitim özeti):

- durum **tam** bilinir,
- eylemler **belirleyici**dir (sonuç kesin),
- zaman **ayrık** adımlardır,
- amaç bir **hedef liteller** kümesidir.

Plan = başlangıç durumundan hedefi sağlayan **aksiyon dizisi**.

Arama (Bölüm 3) ile bağ: her düğüm bir durum, her yay bir uygulanabilir aksiyon.

---

## 2. Durum = liteller kümesi

Örnek (bloklar):

```
{On(A, Masa), On(B, Masa), On(C, A), Clear(B), Clear(C), ElBos}
```

Literal doğruysa kümede; yoksa yanlış sayılır (kapalı dünya varsayımı — eğitim basitleştirmesi).

---

## 3. STRIPS-benzeri aksiyon şeması

Bir aksiyon (şema veya somut örnek) üç parçayla anlatılır:

| Parça | Anlam |
|-------|--------|
| **Önkoşul (precond)** | Uygulanmadan önce durumda olması gereken liteller |
| **Add (ekle)** | Uygulanınca duruma eklenen liteller |
| **Delete (sil)** | Uygulanınca durumdan çıkan liteller |

Örnek sezgi — `Kaldır(B, Masa)`:

- önkoşul: `On(B, Masa)`, `Clear(B)`, `ElBos`
- sil: `On(B, Masa)`, `ElBos`, …
- ekle: `Tutuyor(B)`, …

`aksiyon_semasi.py` şemaları Türkçe başlıklarla yazdırır.  
`strips_bloklar.py` somut aksiyonlarla BFS plan üretir.

---

## 4. Durum geçişi

Aksiyon `a` durum `s` üzerinde uygulanabilirse:

```
s' = (s − delete(a)) ∪ add(a)
```

Önkoşullar `s` içinde değilse aksiyon **uygulanamaz**.

---

## 5. İleri ve geri arama (sezgi)

**İleri (progression):** başlangıçtan hedefe. Her adımda uygulanabilir aksiyonları dene. BFS → en kısa plan (birim maliyet varsayımıyla). `strips_bloklar.py` bunu yapar.

**Geri (regression):** hedeften geriye. “Bu hedef literalini hangi aksiyon üretir? O aksiyonun önkoşulları yeni alt-hedef olur.” Sezgi güçlüdür; kod boyutu büyüyebilir (ilgisiz liteller, değişkenler).

| | İleri | Geri |
|---|--------|------|
| Başlangıç | s₀ | hedef |
| Yön | uygulanabilir aksiyonlar | hedefe katkı sunan aksiyonlar |
| Risk | dallanma büyük dünyada | alt-hedef şişmesi |

---

## 6. Planlama grafiği ve sezgiseller (yüksek seviye)

Durum uzayı kocaman olabilir. **Planlama grafiği** fikri (özet):

- katman katman “belki ulaşılabilir liteller / aksiyonlar” büyütülür,
- karşılıklı dışlama (mutex) gibi kısıtlar işaretlenir,
- hedefe ilk kez kaçıncı katmanda değinildiği **alt sınır / sezgisel** maliyet verir.

Bu paket GraphPlan’ı kodlamaz; unutmayın: sezgisel = “en az bu kadar adım gerekir” tahmini → A* / bilgilendirilmiş planlama için yakıt.

Diğer sezgiseller (isim düzeyinde): silinmeyen hedefler sayısı, gevşetilmiş plan (delete’leri yok say) uzunluğu.

---

## 7. Ne zaman klasik planlama?

| Uygun | Zor / başka paradigma |
|-------|------------------------|
| Küçük–orta ayrık durum | Sürekli robotik, belirsizlik |
| Belirleyici eylem | Stokastik / kısmi gözlem |
| Tek ajan, paylaşılan hedef | Çok ajanlı rekabet |

Bölüm 10’daki ontoloji / aksiyon şemaları, planlama domain’ini yazmayı kolaylaştırır: ortak `On`, `Clear`, `At` sözlüğü.

---

## 8. Özet

| Kavram | Tek cümle |
|--------|-----------|
| Durum | Doğru liteller kümesi |
| STRIPS aksiyon | precond + add + delete |
| Plan | Hedefe götüren aksiyon dizisi |
| İleri arama | s₀ → hedef (ör. BFS) |
| Geri arama | hedef → s₀ alt-hedeflerle |
| Planlama grafiği | Katmanlı ulaşılabilirlik + sezgisel |

Örnekler: `aksiyon_semasi.py`, `strips_bloklar.py`.

Sonraki temalar: belirsizlik altında nicel bilgi (olasılık).
