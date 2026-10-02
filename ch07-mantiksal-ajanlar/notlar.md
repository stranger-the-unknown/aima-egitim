# Bölüm 7 — Mantıksal ajanlar

> **Kitapta:** AIMA 4. baskı, Bölüm 7 *"Logical Agents"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 7.1 Knowledge-Based Agents | §1 TELL/ASK, bildirimsel yaklaşım | `onerme_mantigi.py` |
| 7.2 The Wumpus World | §2 PEAS, kitaptaki dünya | `wumpus_mantik.py` |
| 7.3 Logic | §3 Model, gerektirme, sağlamlık, tamlık | `onerme_mantigi.py` |
| 7.4 Propositional Logic | §4 Sözdizimi, anlam, TT-ENTAILS | `onerme.py` → `tt_gerektirir` |
| 7.5 Propositional Theorem Proving | §5 Eşdeğerlik, çıkarım kuralları, çözümleme, CNF, Horn, ileri/geri zincirleme | `onerme.py`, `ileri_geri_zincirleme.py` |
| 7.6 Effective Propositional Model Checking | §6 DPLL, WalkSAT, faz geçişi | `sat_faz_gecisi.py` |
| 7.7 Agents Based on Propositional Logic | §7 Akışkanlar, ardıl durum aksiyomları, hibrit ajan, SATPLAN | `wumpus_mantik.py` |

## Öğrenme hedefleri

1. Bilgi tabanlı ajanın TELL/ASK döngüsünü açıklamak.
2. Gerektirmeyi modellerle tanımlamak ve doğruluk tablosuyla denetlemek.
3. Cümleleri CNF'ye çevirmek, çözümlemeyle kanıt yapmak; Horn tümcelerinde ileri ve geri zincirlemeyi uygulamak.
4. DPLL'i ve WalkSAT'ı karşılaştırmak; rastgele 3-SAT'taki faz geçişini göstermek.
5. Wumpus dünyasında güvenli kareleri mantıksal çıkarımla bulan bir ajan kurmak; çerçeve probleminin ne olduğunu anlatmak.

---

## 1. Bilgi tabanlı ajanlar

**Bilgi tabanı (KB):** Dünya hakkında bir **bilgi temsil dilinde** yazılmış cümleler kümesi. İki işlem vardır:
- **TELL:** KB'ye yeni bir cümle ekle.
- **ASK:** KB'ye bir soru sor. Yanıt, KB'den **çıkarımla** elde edilir.

```text
fonksiyon BT-AJAN(algı) → eylem
    TELL(KB, ALGI-CÜMLESİ(algı, t))
    eylem ← ASK(KB, EYLEM-SORGUSU(t))
    TELL(KB, EYLEM-CÜMLESİ(eylem, t))
    t ← t + 1
    döndür eylem
```

**Bildirimsel** yaklaşımda ajana ne bilmesi gerektiği cümlelerle anlatılır, nasıl davranacağını çıkarım belirler. **Yordamsal** yaklaşımda ise davranış doğrudan koda yazılır. Başarılı sistemler genellikle ikisini birleştirir. Ajanı **bilgi düzeyinde** ("ne biliyor, amacı ne?") ya da **uygulama düzeyinde** ("veri yapıları ne?") tanımlayabiliriz.

---

## 2. Wumpus dünyası

4×4'lük bir mağara. Bir karede wumpus var, bazı karelerde çukur (her kare için olasılık 0,2), bir karede altın.

| PEAS | İçerik |
|---|---|
| **P** | Altınla çıkış +1000; ölüm (çukur ya da wumpus) −1000; her eylem −1; oku kullanmak −10 |
| **E** | 4×4 ızgara; ajan [1,1]'de doğuya bakarak başlar |
| **A** | İleri, SolaDön, SağaDön, Al, AtEt (tek ok), Tırman |
| **S** | Koku (wumpus komşu karede), Esinti (çukur komşu karede), Parıltı (altın bu karede), Çarpma (duvar), Çığlık (wumpus öldü) |

Ortam ayrık, statik, tek ajanlı ve deterministiktir. Ama **kısmi gözlemlenebilirdir** ve ajan için başta **bilinmeyendir**. Ortamların yaklaşık %21'i "adil değildir": Altın bir çukurdadır ya da çukurlarla çevrilidir.

**Kitaptaki dünya** (`wumpus_mantik.py`): Wumpus [1,3]'te, çukurlar [3,1], [3,3] ve [4,4]'te, altın [2,3]'te. Ajanın akıl yürütmesi:
1. [1,1]: Algı yok → [1,2] ve [2,1] güvenli.
2. [2,1]: Esinti → [2,2] ya da [3,1]'de çukur var.
3. [1,2]: Koku var ama esinti yok → [2,2]'de çukur yok. [2,1]'de koku olmadığı için [2,2]'de wumpus da yok, yani **[2,2] güvenli**. Wumpus [1,3]'te, çukur [3,1]'de.

Bizim ajanımız bu çıkarımların hepsini kurallardan ve algılardan DPLL ile **kanıtlayarak** yapar ve güvenli olduğu kanıtlanmamış hiçbir kareye girmez.

---

## 3. Mantık: temel kavramlar

- **Sözdizimi:** Hangi cümlelerin iyi biçimli olduğu.
- **Anlam (semantik):** Bir cümlenin her **modelde** (olası dünyada) doğru mu yanlış mı olduğu. M(α), α'nın doğru olduğu modellerin kümesidir.
- **Gerektirme:** KB ⊨ α ancak ve ancak M(KB) ⊆ M(α). KB'nin doğru olduğu her dünyada α da doğrudur.
- **Model denetimi:** Tüm modelleri sayıp M(KB) ⊆ M(α) koşulunu doğrulamak.
- **Çıkarım algoritması:** KB ⊢ α türetmesi.
  - **Sağlam** (*sound*): Yalnızca gerektirilen cümleleri türetir.
  - **Tam** (*complete*): Gerektirilen her cümleyi türetebilir.
- **Temellendirme** (*grounding*): KB'nin gerçek dünyayla ilişkisi. Algılayıcılar dünyayı doğru yansıtıyorsa ve kurallar doğruysa, sağlam çıkarımla elde edilen sonuçlar gerçek dünyada da doğrudur.

---

## 4. Önerme mantığı

**Sözdizimi:** Atomik cümleler (P, W13, …), ¬ (değil), ∧ (ve), ∨ (veya), ⇒ (ise), ⇔ (ancak ve ancak). Öncelik: ¬ > ∧ > ∨ > ⇒ > ⇔.

**İma ile ilgili sezgi:** P ⇒ Q yalnızca P doğru ve Q yanlışken yanlıştır. "5 çiftse, Ali akıllıdır" cümlesi doğrudur, çünkü öncül yanlıştır. ⇒ bir nedensellik değil, "P doğruysa Q da doğrudur" iddiasıdır.

**Wumpus için küçük KB (kitaptaki):**

| Kural | Anlamı |
|---|---|
| R1: ¬P11 | Başlangıç karesinde çukur yok |
| R2: B11 ⇔ (P12 ∨ P21) | [1,1]'de esinti ⟺ komşularından birinde çukur |
| R3: B21 ⇔ (P11 ∨ P22 ∨ P31) | [2,1] için aynısı |
| R4: ¬B11 | [1,1]'de esinti algılanmadı |
| R5: B21 | [2,1]'de esinti algılandı |

**TT-ENTAILS** (doğruluk tablosu) 7 sembolün 2⁷ = **128** modelini dener. KB yalnızca **3** modelde doğrudur. Üçünde de P12 yanlış olduğu için **KB ⊨ ¬P12**. P22 bazılarında doğru, bazılarında yanlıştır; yani ne P22 ne de ¬P22 gerektirilir (`wumpus_mantik.py`, Bölüm 1).

TT-ENTAILS sağlam ve tamdır, ama zamanı **O(2ⁿ)**'dir. Önerme mantığında gerektirme co-NP-tamdır.

---

## 5. Önerme mantığında teorem ispatı

### 5.1 Eşdeğerlik, geçerlilik, karşılanabilirlik

- **Eşdeğerlik:** α ≡ β, ancak ve ancak her modelde aynı doğruluk değerine sahiplerse. Örnekler: karşıt ters (P ⇒ Q ≡ ¬Q ⇒ ¬P), De Morgan, ⇒ ve ⇔ eliminasyonu, dağılma.
- **Geçerli** (totoloji): Her modelde doğru. **Tümdengelim teoremi:** KB ⊨ α ⟺ (KB ⇒ α) geçerlidir.
- **Karşılanabilir:** En az bir modelde doğru. **Çelişki ile kanıt:** KB ⊨ α ⟺ (KB ∧ ¬α) karşılanamaz.

### 5.2 Çıkarım kuralları ve kanıt

**Modus Ponens:** α ⇒ β ve α'dan β. **Ve-eliminasyonu:** α ∧ β'dan α. Tüm eşdeğerlikler de çıkarım kuralı olarak kullanılabilir. Kanıt bulmak bir **arama problemidir** (durum: cümle kümesi, eylem: kural uygulamak). Önerme mantığı **monotondur**: Yeni bilgi eski sonuçları geçersiz kılmaz.

### 5.3 Çözümleme (resolution)

**Birim çözümleme:** (ℓ₁ ∨ … ∨ ℓₖ) ve ¬ℓᵢ → ℓᵢ'yi at. **Tam çözümleme:** İki tümcede birbirinin değili olan literal çifti varsa, ikisini birleştir ve bu çifti çıkar. Tekrar eden literalleri tek bırakmaya **çarpanlama** (*factoring*) denir.

**CNF'ye dönüştürme adımları:**
1. ⇔ eliminasyonu: α ⇔ β → (α ⇒ β) ∧ (β ⇒ α)
2. ⇒ eliminasyonu: α ⇒ β → ¬α ∨ β
3. ¬'yi içe itme (De Morgan, çift değilleme)
4. ∨'yi ∧ üzerine dağıtma

Örnek: B11 ⇔ (P12 ∨ P21) → (¬B11 ∨ P12 ∨ P21) ∧ (¬P12 ∨ B11) ∧ (¬P21 ∨ B11).

**Çözümleme algoritması:** KB ∧ ¬α'nın tümcelerini al; yeni tümce kalmayana kadar tüm çiftleri çözümle. **Boş tümce** (□) türetilirse KB ⊨ α. `wumpus_mantik.py` (Bölüm 2), ¬P12'yi iki adımda kanıtlar:
(B11 ∨ ¬P12) + (P12) → B11; (¬B11) + (B11) → □.

**Temel çözümleme teoremi:** Çözümleme **çürütme açısından tamdır**: Bir tümce kümesi karşılanamazsa, çözümleme kapanışı boş tümceyi içerir.

### 5.4 Horn tümceleri; ileri ve geri zincirleme

- **Kesin tümce:** Tam olarak bir pozitif literal. Örnek: (¬L ∨ ¬M ∨ P), yani L ∧ M ⇒ P.
- **Horn tümcesi:** En fazla bir pozitif literal. Pozitif literal hiç yoksa bir **hedef tümcesidir**.
- Horn KB'lerde gerektirme **doğrusal zamanda** kararlaştırılabilir.

**İleri zincirleme** (veri güdümlü): Bilinen gerçeklerle başla. Öncüllerinin hepsi bilinen her kuralı ateşle, sonucunu gündeme ekle. Kitaptaki örnekte (`ileri_geri_zincirleme.py`) A, B → L → M → P → Q sırasıyla ilerler. Sağlamdır ve kesin tümceler için tamdır.

**Geri zincirleme** (hedef güdümlü): Q'dan başla. Q'yu sonuç olarak veren bir kural bul, öncüllerini alt hedef yap. Çoğu zaman yalnızca ilgili gerçeklere dokunduğu için ileri zincirlemeden çok daha az iş yapar. Döngüleri kesmek gerekir: A ∧ P ⇒ L kuralı P'yi tekrar sorar.

---

## 6. Etkili model denetimi: DPLL ve WalkSAT

**DPLL**, TT-ENTAILS'e üç iyileştirme ekler:
1. **Erken sonlandırma:** Bir tümce kısmi atamayla zaten doğruysa (ya da yanlışsa) geri kalan sembollere bakmaya gerek yoktur.
2. **Saf sembol:** Açık tümcelerde hep aynı işaretle görünen sembolü o işarete ata.
3. **Birim tümce:** Tek atanmamış literali kalan tümcede o literali doğru yap. Bu zincirleme olarak **birim yayılım** oluşturur (CSP'deki ileri kontrolün karşılığı).

Modern SAT çözücüler bunlara bileşen analizi, değişken/değer sıralaması, **tümce öğrenmeli** akıllı geri dönüş, rastgele yeniden başlatma ve akıllı indeksleme ekler. Milyonlarca değişkenli problemleri çözebilirler.

**WalkSAT:** Rastgele bir modelle başla. Yanlış bir tümce seç. p olasılıkla onun içinden rastgele bir sembolü, 1 − p olasılıkla yanlış tümce sayısını en çok azaltan sembolü çevir. Hızlıdır ama **tam değildir**: Cümle karşılanamazsa bunu kanıtlayamaz, yalnızca zamanı dolar.

**Faz geçişi** (`sat_faz_gecisi.py`): Rastgele 3-CNF'de m/n (tümce/sembol) oranı büyüdükçe karşılanabilirlik olasılığı 1'den 0'a keskin biçimde düşer. Geçiş m/n ≈ **4,3** civarındadır ve **en zor** problemler de oradadır: Az kısıtlı problemler kolayca karşılanır, çok kısıtlı problemler hızla çelişkiye düşer. Bizim deneyimizde (n = 30) DPLL'in medyan işi 4,3–4,6 civarında tepe yapar.

---

## 7. Önerme mantığına dayalı ajanlar

### 7.1 Dünyanın o anki durumu

Konum, yön ve algılar zamanla değişir. Bu yüzden her sembolün bir zaman indeksi olmalıdır: L^t_{1,1} (t anında [1,1]'deyim), FacingEast^t. Zamanla değişen bu sembollere **akışkan** (*fluent*), değişmeyenlere (P13 gibi) **zamandan bağımsız değişken** denir.

### 7.2 Çerçeve problemi

**Etki aksiyomları** bir eylemin neyi değiştirdiğini söyler: L^t_{1,1} ∧ FacingEast^t ∧ Forward^t ⇒ L^{t+1}_{2,1} ∧ ¬L^{t+1}_{1,1}. Ama neyin **değişmediğini** söylemezler. İleri gitmek oku harcamaz, ama bunu da yazmak gerekir. Her eylem × her akışkan için bir "değişmezlik" aksiyomu yazmak O(m·n) aksiyom demektir. Bu **çerçeve problemidir**.

**Çözüm: ardıl durum aksiyomları.** Her akışkan için tek bir aksiyom:

F^{t+1} ⇔ (F'yi doğru yapan bir eylem^t) ∨ (F^t ∧ ¬(F'yi yanlış yapan bir eylem^t))

Örnek: HaveArrow^{t+1} ⇔ (HaveArrow^t ∧ ¬Shoot^t).

**Nitelendirme problemi** (*qualification problem*): Bir eylemin başarılı olması için gereken tüm koşulları (kaygan zemin, ok sıkışması…) saymak imkânsızdır. Olasılık bu sorunu hafifletir (Bölüm 12).

### 7.3 Hibrit ajan

Kitaptaki hibrit ajan, mantıksal çıkarımı (hangi kareler güvenli?) arama ile (güvenli kareler üzerinden A* ile rota) birleştirir. Öncelik sırası: altını gördüysen al ve çık; güvenli ve ziyaret edilmemiş bir kareye git; wumpus'un yeri biliniyorsa ok at; en son çare olarak riskli bir kareye git. `wumpus_mantik.py` bunun sadeleştirilmiş bir hâlidir: Yalnızca güvenli olduğu kanıtlanmış karelere girer.

**Durum tahmini:** Her adımda tüm geçmişle çıkarım yapmak pahalılaşır. Çözüm, bir **inanç durumunu** (Bölüm 4) mantıksal bir formül olarak tutmaktır. Kesin temsil üstel büyüyebilir. Bu yüzden **1-CNF** (literallerin birleşimi) gibi muhafazakâr yaklaşımlar kullanılır: Kesin bilinen akışkanları tutar, gerisini bilinmiyor sayar.

### 7.4 SATPLAN

Planlamayı bir SAT problemine çevirir. Başlangıç durumu, T adımlık ardıl durum aksiyomları, eylem **önkoşul** aksiyomları, **eylem dışlama** aksiyomları (aynı anda tek eylem) ve hedef (T anında) tek bir CNF'de birleştirilir. T = 0, 1, 2, … için SAT çözücü çağrılır. Bulunan modeldeki doğru eylem sembolleri plandır. Konu Bölüm 11'de tekrar ele alınır.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "P ⇒ Q, P'nin Q'ya neden olduğu anlamına gelir." | Yalnızca "P doğruysa Q da doğru" demektir. Öncül yanlışsa ima doğrudur. |
| "KB ⊭ α ise KB ⊨ ¬α'dır." | Hayır. Üçüncü durum "bilinmiyor"dur (P22 örneği). |
| "Çözümleme her doğru cümleyi doğrudan türetir." | Çürütme açısından tamdır: α'yı değil, KB ∧ ¬α'dan □'yu türetir. |
| "WalkSAT 'çözüm yok' diyebilir." | Diyemez; tam değildir. Zaman sınırı dolması karşılanamazlık kanıtı değildir. |
| "Horn tümcesi = kesin tümce." | Kesin tümcede tam bir pozitif literal vardır; Horn'da en fazla bir. |
| "Etki aksiyomları yeter." | Neyin değişmediğini söylemezler; ardıl durum aksiyomları gerekir (çerçeve problemi). |

## Kendini yokla

1. R1–R5 KB'sinde KB ⊨ P22 ∨ P31 midir? Doğruluk tablosuna bakmadan düşün.
2. (A ∨ B) ∧ (¬A ∨ C) tümcelerinin çözümleyicisi nedir?
3. İleri zincirleme hangi durumlarda geri zincirlemeden çok daha fazla iş yapar?
4. DPLL'in birim yayılımı, CSP'lerdeki hangi tekniğe karşılık gelir?
5. HaveArrow için ardıl durum aksiyomunu yaz.

## Kod rehberi

```bash
python ornekler/onerme.py                  # kütüphane testi: ayrıştırma, CNF, TT, DPLL, çözümleme
python ornekler/onerme_mantigi.py          # TELL/ASK, geçerlilik, eşdeğerlik
python ornekler/wumpus_mantik.py           # 128 model / 3 model, çözümleme kanıtı, mantıksal ajan
python ornekler/ileri_geri_zincirleme.py   # kitaptaki Horn KB
python ornekler/sat_faz_gecisi.py          # rastgele 3-SAT: m/n ≈ 4,3
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| bilgi tabanı | knowledge base (KB) | Dünya hakkındaki cümleler |
| bildirimsel / yordamsal | declarative / procedural | "Ne" anlatılır / "nasıl" kodlanır |
| model | model | Olası bir dünya (sembollere doğruluk değeri ataması) |
| gerektirme | entailment (⊨) | KB'nin her modelinde α doğru |
| sağlam / tam | sound / complete | Yalnızca doğruyu türetir / her doğruyu türetebilir |
| temellendirme | grounding | KB ile gerçek dünya arasındaki bağ |
| geçerli (totoloji) | valid (tautology) | Her modelde doğru |
| karşılanabilir | satisfiable | En az bir modelde doğru |
| tümdengelim teoremi | deduction theorem | KB ⊨ α ⟺ KB ⇒ α geçerli |
| çelişki ile kanıt | reductio ad absurdum | KB ∧ ¬α karşılanamaz |
| çözümleme | resolution | Tümcelerdeki zıt literalleri birleştirme |
| tümce / literal | clause / literal | Literallerin ∨'si / sembol ya da değili |
| birleşik normal biçim | conjunctive normal form (CNF) | Tümcelerin ∧'si |
| kesin tümce / Horn tümcesi | definite clause / Horn clause | Tam bir / en fazla bir pozitif literal |
| ileri / geri zincirleme | forward / backward chaining | Veri güdümlü / hedef güdümlü çıkarım |
| birim yayılım | unit propagation | Birim tümcelerin zincirleme uygulanması |
| saf sembol | pure symbol | Hep aynı işaretle görünen sembol |
| akışkan | fluent | Zamanla değişen sembol |
| çerçeve problemi | frame problem | Neyin değişmediğini ifade etme sorunu |
| ardıl durum aksiyomu | successor-state axiom | Bir akışkanın sonraki değerini tanımlayan aksiyom |
| nitelendirme problemi | qualification problem | Tüm önkoşulları sayamama sorunu |
