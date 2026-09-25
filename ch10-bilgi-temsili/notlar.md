# Bölüm 10 — Bilgi temsili: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Kavramlar kamuya açıktır; açıklamalar özgün Türkçedir.
> Amaç: neden “sadece FOL cümleleri yığmak” yetmez; yapılandırılmış temsil ne kazandırır.

---

## 1. KR ne işe yarar?

Birinci derece mantık **dil** verir: nesneler, ilişkiler, niceleyiciler. Ama büyük bir bilgi tabanı yalnızca rastgele cümleler listesi olursa:

- aynı fikri tekrar tekrar yazarsınız,
- ortak “kelime dağarcığı” belirsiz kalır,
- kalıtım / istisna gibi örüntüleri elle yönetirsiniz,
- ajanın sorularına cevap üretmek dağınık hale gelir.

**Bilgi temsili (KR)** burada bir mühendislik katmanıdır: hangi türleri (kategoriler), hangi ilişkileri, hangi olay/durum dilini kullanacağınızı önceden tasarlamak. FOL (veya benzeri) hâlâ formal zemin olabilir; KR onun **organizasyonudur**.

Kısaca: FOL araç; KR mimari + sözlük + yeniden kullanım.

---

## 2. Kategoriler ve nesneler

**Nesne:** tekil bir şey (`minnos`, `ankara_kargo_1`).  
**Kategori (sınıf / tür):** nesnelerin kümesi veya tipi (`Kedi`, `Memeli`, `Hayvan`).

Temel ilişki: **üyelik** — `minnos ∈ Kedi` veya yüklem olarak `Kedi(minnos)`.

Kategoriler arasında **alt-kategori** (`is_a` / `alt_tur`):

```
Hayvan
  └── Memeli
        └── Kedi
```

Sezgi: “Her Kedi bir Memeli’dir; her Memeli bir Hayvan’dır.” Kalıtım: Kedi’ye yazdığınız özellik (ör. `Memeli` üzerinden `sicakkanli`) alt türlere ve örneklere taşınabilir — ta ki **istisna** gelene kadar (bir sonraki bölüm).

`ontoloji_mini.py` bu hiyerarşiyi Python sözlükleriyle gösterir; `is_a(alt, ust)` sorgusu zinciri yürür.

---

## 3. Ontoloji (hafifçe)

**Ontoloji** (eğitim anlamında): bir alan için üzerinde anlaşılmış kategoriler, ilişkiler ve kısıtlar sözlüğü.

Örnek alanlar: lojistik (depo, kargo, uçak), tıp (belirti, hastalık — dikkat: etik/güvenlik!), e-ticaret (ürün, sipariş).

İyi bir ontoloji:

- isimleri netleştirir (`Lokasyon` mi `Yer` mi?),
- hiyerarşiyi paylaşır (kalıtım),
- ajanlar / ekip üyeleri aynı dili konuşur.

Kötü uç: her şeyi tek düz listeye dökmek veya gereksiz derin ağaçlar. Bu pakette “hafif ontoloji” yeter: birkaç kategori + `is_a`.

---

## 4. Olaylar ve durumlar (yüksek seviye)

Dünya zamanla değişir. İki sezgisel dil:

| Fikir | Sezgi | Tipik kullanım |
|-------|--------|----------------|
| **Durum (situation)** | “Dünyanın bir anlık fotoğrafı” | Durumlar arasında eylem geçişi |
| **Olay / akış** | “Bir şey oldu / oluyor” | Süre, örtüşme, neden-sonuç |

Klasik planlamada (Bölüm 11) durumlar liteller kümesi gibi düşünülür: `On(A,B)`, `Clear(A)`.  
Daha zengin KR’de olaylar sürebilir, örtüşebilir; bu notta **isimlendirme** yeter — formal durum hesabı / olay hesabı detayına girmiyoruz.

Unutmayın: temsil seçimi, sonra hangi çıkarımın kolay olacağını belirler.

---

## 5. Varsayılan akıl yürütme (default)

Klasik FOL **monotonic**tır: yeni bilgi eklenince eski sonuçlar bozulmaz. Gerçek hayatta ise:

> “Kuşlar uçar.” — sonra: “Penguen bir kuştur.” — sonra: “Penguenler uçmaz.”

İlk varsayım, istisna gelince **geri alınır**. Buna **nonmonotonic / varsayılan** akıl denir.

Oyuncak kural:

1. `Kus(x)` ve aksi kanıt yoksa ⇒ `Ucar(x)` (varsayılan).
2. `Penguen(x)` ⇒ `¬Ucar(x)` (kesin istisna; penguen de kuş olabilir).

`varsayilan_akil.py` bunu basit öncelikle gösterir: istisna varsa varsayılan uygulanmaz.

---

## 6. Ham FOL yığınına karşı yapılandırılmış KR

| Ham FOL dump | Yapılandırılmış KR |
|--------------|-------------------|
| Cümleler dağınık | Kategoriler, şemalar, olay türleri |
| Kalıtım elle | `is_a` + özellik mirası |
| İstisna zor | Default kurallar / öncelik |
| Yeniden kullanım zayıf | Ortak ontoloji, şablon aksiyonlar |
| Sorgular ad hoc | Standart sorgu kalıpları (`is_a`, `uye_mi`) |

KR, mantığı iptal etmez; onu **okunur, ölçeklenebilir ve ajan dostu** hale getirmeyi hedefler.

---

## 7. Özet

| Kavram | Tek cümle |
|--------|-----------|
| Kategori | Nesnelerin türü / kümesi |
| `is_a` | Alt tür → üst tür zinciri |
| Ontoloji | Alan sözlüğü + ilişkiler |
| Durum / olay | Anlık dünya vs. değişim dili |
| Default | İstisna gelene kadar varsayım |
| KR amacı | Yapı, paylaşım, sorgulanabilir bilgi |

Örnekler: `ontoloji_mini.py`, `varsayilan_akil.py`.

Sonraki bölüm (11): klasik planlama — STRIPS, durum uzayı, planlama grafiği sezgisi.
