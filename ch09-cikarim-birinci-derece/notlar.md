# Bölüm 9 — FOL’de çıkarım: Özgün Notlar

> Bu notlar kitabın metninin kopyası değildir. Algoritma isimleri kamuya açıktır; açıklamalar özgün Türkçedir.
> Amaç sezgi + küçük çalışan örnek; endüstriyel teorem kanıtlayıcı değil.

---

## 1. Çıkarım sorunu (hatırlatma)

KB ⊨ α mı? Bölüm 7’de önermeler için doğruluk tablosu / çözümleme gördük. FOL’de domain sonsuz olabileceğinden aynı tablo doğrudan uygulanmaz. Üç büyük yol:

1. **Önermeselleştirme** — domain sonluysa FOL’ü önerme mantığına çevir.
2. **Lifted çıkarım** — birleştirme ile doğrudan FOL üzerinde zincirleme / çözümleme.
3. **Özel parçalar** — Horn maddeleri → ileri/geri zincir (verimli pratik).

---

## 2. Önermeselleştirme sezgisi

Sonlu domain D = {a₁, …, aₙ} olsun.

- `∀x P(x)` ≈ `P(a₁) ∧ … ∧ P(aₙ)`
- `∃x P(x)` ≈ `P(a₁) ∨ … ∨ P(aₙ)`

Her FOL cümlesi böyle (ve Skolem vb. tekniklerle) önerme cümlelerine indirgenebilir; sonra Bölüm 7 motoru çalışır.

**Bedel:** domain büyüdükçe ve iç içe niceleyicilerde üretilen önerme sayısı patlar. Eğitimde fikir yeter: “FOL → çok önerme → eski araçlar”; pratikte çoğu zaman lifted yöntem tercih edilir.

---

## 3. Birleştirme (unification)

İki atomik cümleyi **aynı anda doğru kılacak** en genel değişken atamasını ararız.

Örnekler (sezgi):

| x | y | Sonuç |
|---|---|--------|
| `P(A)` | `P(A)` | {} (boş birleştirici) |
| `P(x)` | `P(A)` | {x/A} |
| `P(x)` | `P(y)` | {x/y} (veya {y/x}) |
| `P(x)` | `Q(A)` | başarısız (yüklem farklı) |
| `P(x)` | `P(f(x))` | başarısız (occurs-check: x, f(x) içinde) |

**MGU (most general unifier):** gereksiz yere somutlaştırmayan birleştirici. Algoritmalar MGU üretir; eğitim kodumuz basit terimler için `unify` gösterir (`birlesim_unification.py`).

Birleştirme, modus ponens’i FOL’e “kaldırmanın” anahtarıdır: kuraldaki değişkenler sorgu/olgularla eşleşir.

---

## 4. İleri zincirleme

**Horn maddesi** (kabaca): `P₁ ∧ … ∧ Pₖ ⇒ Q` (en fazla bir pozitif sonuç).

**İleri zincir:** bilinen olgulardan kuralların öncüllerini birleştirerek yeni olgular üret; sabitleşene kadar tekrarla. Veri güdümlüdür (“ne biliyorum → ne türetirim”).

Ne zaman iyi? Birçok olgu var, tüm sonuçları önceden üretmek istiyorsanız (veya doygun KB). Bölüm 8’deki `fol_sozluk.py` doyurma adımı ileri zincire yakındır.

---

## 5. Geriye zincirleme

**Geriye zincir:** hedeften başla. Hedef bir olguyla birleşiyorsa tamam; değilse sonucu hedefe uyan bir kural seç, öncülleri alt-hedef yap (derinlik öncelikli arama + birleştirme).

Soru güdümlüdür (“bunu kanıtlamak için neye ihtiyacım var?”).

Klasik oyuncak: aile ilişkileri veya “kim ne yaptı?” tarzı kural kümeleri. `geriye_zincir.py` **özgün** olgular kullanır; kitaptaki örnek metinleri kopyalamaz.

---

## 6. Çözümleme eskizi

CNF’e çevir → iki cümleden zıt literalleri birleştirerek çözümle → boş cümle = çelişki → KB ∧ ¬α doyurulamaz ⇒ KB ⊨ α.

FOL’de literal birleştirme yine **unify** ister. Tam ve sağlamdır (uygun koşullarda) ama arama uzayı büyük olabilir; strateji gerekir. Bu pakette tam çözümleyici yok — sezgi için yeterli.

---

## 7. Ne zaman hangisi?

| Durum | Eğilim |
|-------|--------|
| Çok küçük sonlu domain, hazır önerme motoru | Önermeselleştirme |
| “Tüm sonuçları üret”, olgu yağmuru | İleri zincir |
| Tek / az sorgu, büyük kural seti | Geriye zincir |
| Genel (Horn dışı) ispat, çelişki arama | Çözümleme |
| Öğrenme / ilk okuma | Önce birleştirme + geriye zincir demoları |

---

## 8. Özet

| Kavram | Tek cümle |
|--------|-----------|
| Önermeselleştirme | ∀/∃ → ∧/∨ açılımı (sonlu domain) |
| Birleştirme | İki terimi ortak örneğe getiren atama |
| İleri zincir | Olgudan kurala, yeni olgu |
| Geriye zincir | Hedeften kurala, alt-hedefler |
| Çözümleme | CNF + çelişki ile ⊨ kontrolü |

Örnekler: `birlesim_unification.py`, `geriye_zincir.py`.

Sonraki bölüm (10): bilgi temsili — kategoriler, durumlar, olaylar.
