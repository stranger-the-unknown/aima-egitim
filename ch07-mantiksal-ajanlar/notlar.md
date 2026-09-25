# Bölüm 7 — Mantıksal ajanlar: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Kavramları Türkçe, kendi cümlelerimizle öğretir.
> Klasik “mağara / canavar” anlatısının birebir metni burada yoktur; motivasyon için kısa özgün senaryo kullanılır.

---

## 1. Bilgi tabanlı ajan

Şimdiye kadarki ajanlar çoğunlukla durum → eylem eşlemesi veya arama ağacıyla karar verdi. **Bilgi tabanlı ajan** ise:

1. Dünyadan **algı** alır.
2. Bildiklerini bir **bilgi tabanına (KB)** yazar (`Tell`).
3. Ne yapacağına karar vermek için KB’ye **soru sorar** (`Ask`).
4. Eylemi uygular; yeni algıyla döngü sürer.

KB = ajanın “bildiği cümleler” kümesi. Çıkarım motoru, bu cümlelerden yeni sonuçlar üretir. Ayrıntılı dünya haritası yerine **açıkça ifade edilmiş bilgi** ve mantık kuralları vardır.

---

## 2. Önermeler mantığı — sözdizim

**Önerme sembolleri:** `P`, `Q`, `Esinti_12`, … (doğru veya yanlış olabilir).

Bağlaçlar (eğitimde sık kullanılanlar):

| Sembol | Anlam |
|--------|--------|
| \(\neg\) | değil |
| \(\land\) | ve |
| \(\lor\) | veya |
| \(\Rightarrow\) | ise (implicasyon) |
| \(\Leftrightarrow\) | ancak ve ancak |

Cümleler bu sembollerden kurulur. Örnek: \(\neg P \lor Q\) ile \(P \Rightarrow Q\) aynı modelleri paylaşır (eşdeğerlik).

---

## 3. Modeller ve gerektirme

Bir **model**, her önerme sembolüne doğru/yanlış atayan bir “olası dünya”dır. \(n\) sembol → \(2^n\) model.

- Cümle \(\alpha\) bir modelde **doğru** veya **yanlış** olur.
- KB **gerektirir** \(\alpha\) (yazılır: \(\mathrm{KB} \models \alpha\)) demek: KB’nin doğru olduğu **her** modelde \(\alpha\) da doğrudur.
- Bu, “KB’den \(\alpha\)’yı çıkarsayabiliriz” fikrinin semantik tanımıdır.

**Doyurulabilirlik:** En az bir modelde doğru mu? \(\mathrm{KB} \models \alpha\) ile \(\mathrm{KB} \land \neg\alpha\)’nın **doyurulamaz** olması eşdeğerdir (ispat için sık kullanılır).

Küçük sembol sayısında doğruluk tablosuyla kontrol edilebilir (`onerme_mantigi.py`).

---

## 4. Çıkarım (kısa)

Semantik tanım yeterli ama büyük KB’de \(2^n\) model gezmek pahalıdır. **Çıkarım algoritmaları** sözdizimsel kurallarla yeni cümle üretir:

- **Modus ponens:** \(P\) ve \(P\Rightarrow Q\) varsa \(Q\).
- **Çözümleme (resolution):** CNF cümlelerden çelişki arayarak \(\mathrm{KB} \models \alpha\) kontrolü (tam ve sağlam, önermeler mantığında).

Bu bölümde odak: **gerektirmenin ne olduğu** + küçük örnekte tablo ile `Ask`. Çözümleme ayrıntısı sonraki pratikte derinleştirilir.

---

## 5. Motivasyon: tehlikeli ızgara (özgün mini senaryo)

Ajan küçük bir ızgarada dolaşır. Bazı karelerde **çukur** vardır; çukura komşu karede **esinti** hissedilir. Bazı karelerde tehlikeli bir yaratık olabilir; ona komşu karede **koku** vardır.

Ajan (0,0)’dan başlar; güvenli olduğunu bildiği karelere adım atmak ister. Algı örneği:

- (0,0)’da esinti yok, koku yok → komşularında çukur/yaratık yok **gibi** düşünebilir (kurallara göre).
- (1,0)’da esinti var → (1,0)’ın komşularından **en az birinde** çukur olabilir.

Mantık burada: ham duyuyu doğrudan “şu kare ölümcül” diye yazmak yerine, **kurallar + gözlem** ile hangi karelerin güvenli / şüpheli / tehlikeli olduğunu türetiriz. `wumpus_basit.py` bunu 2×2’de, özgün ve sade kurallarla gösterir.

> Not: Kitaptaki klasik anlatının metnini kopyalamıyoruz; fikir aynı ailede: kısmi gözlem + mantıksal çıkarım.

---

## 6. Tell / Ask döngüsü pratikte

```text
KB ← boş veya arka plan kuralları
döngü:
  algı al
  Tell(KB, PerceptSentence)
  eylem ← Ask(KB, "hangi eylem?")
  Tell(KB, ActionSentence)   # isteğe bağlı: kendi eylemini de kaydet
  eylemi uygula
```

`Ask` başarısız olabilir (bilgi yetmez) → ajan **güvenli keşif** veya “bilmiyorum” politikası seçer. Bu, salt refleks ajanından farkı: karar, KB’nin gerektirdiği sonuçlara dayanır.

---

## 7. Özet

| Kavram | Tek cümle |
|--------|-----------|
| Bilgi tabanlı ajan | Tell ile kaydet, Ask ile sor, ona göre hareket et |
| Model | Sembollere T/F atayan olası dünya |
| Gerektirme | KB’nin doğru olduğu her modelde α doğru |
| Doğruluk tablosu | Küçük n için \(\models\) kontrolü |
| Izgara motivasyonu | Algı + kural → güvenli / riskli kare |

Örnekler: `onerme_mantigi.py`, `wumpus_basit.py`.

Sonraki bölüm (8): birinci mertebe mantık — nesneler, niceleyiciler, ilişkiler.
