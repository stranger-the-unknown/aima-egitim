# Bölüm 9 — Birinci derece mantıkta çıkarım

> **Kitapta:** AIMA 4. baskı, Bölüm 9 *"Inference in First-Order Logic"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 9.1 Propositional vs. First-Order Inference | §1 Örnekleme, önermeselleştirme, yarı karar verilebilirlik | — |
| 9.2 Unification and First-Order Inference | §2 Genelleştirilmiş Modus Ponens, UNIFY, MGU, occurs check, değişken ayırma | `birlesim_unification.py`, `fol_cikarim.py` |
| 9.3 Forward Chaining | §3 Kesin tümceler, Datalog, suç örneği, verimlilik | `suclu_bati.py` |
| 9.4 Backward Chaining | §4 Geri zincirleme, Prolog, sonsuz döngü, tablolama | `suclu_bati.py`, `prolog_yol.py`, `geriye_zincir.py` |
| 9.5 Resolution | §5 FOL için CNF, Skolemleştirme, çözümleme, tamlık, eşitlik, stratejiler | `kedi_cozumleme.py` |

## Öğrenme hedefleri

1. Önermeselleştirmenin nasıl çalıştığını ve neden verimsiz olduğunu açıklamak.
2. İki terimi elle birleştirmek; MGU'yu, occurs check'i ve değişken ayırmayı açıklamak.
3. Kesin tümcelerle ileri ve geri zincirleme yapmak; Prolog'un güçlü ve zayıf yanlarını bilmek.
4. Bir FOL cümlesini CNF'ye çevirmek (Skolemleştirme dahil) ve çözümlemeyle kanıt yapmak.
5. Çözümlemenin tamlığını ve pratik stratejilerini açıklamak.

---

## 1. Önerme mantığına indirgemek

- **Evrensel örnekleme (UI):** ∀v α'dan, herhangi bir temel terim g için SUBST({v/g}, α) çıkarılabilir. ∀x Kral(x) ∧ Açgözlü(x) ⇒ Kötü(x) → Kral(John) ∧ Açgözlü(John) ⇒ Kötü(John).
- **Varoluşsal örnekleme (EI):** ∃v α'yı, KB'de hiç geçmeyen **yeni** bir sabitle (Skolem sabiti) bir kez örnekle. ∃x Taç(x) ∧ Başında(x, John) → Taç(C1) ∧ Başında(C1, John).
- **Önermeselleştirme:** Tüm evrensel cümleleri tüm temel terimlerle örnekle, sonra önerme mantığı çıkarımı yap. Sorun: Fonksiyon sembolleri varsa temel terimler sonsuzdur (Baba(Baba(Baba(John)))…).
- **Herbrand teoremi:** Bir cümle FOL KB'si tarafından gerektiriliyorsa, önermeselleştirilmiş KB'nin **sonlu bir alt kümesiyle** kanıtlanabilir. Önce derinlik-0 terimleri, sonra derinlik-1 terimleri… denenir.
- **Yarı karar verilebilirlik** (Turing, Church): Gerektirilen her cümleyi kanıtlayan bir algoritma vardır, ama gerektirilmeyen bir cümle için bunu her durumda söyleyen bir algoritma yoktur. Program sonsuza kadar çalışabilir.

---

## 2. Birleştirme

### 2.1 Genelleştirilmiş Modus Ponens (GMP)

p₁', …, pₙ' atomik cümleleri ve (p₁ ∧ … ∧ pₙ ⇒ q) kuralı için, her i'de SUBST(θ, pᵢ') = SUBST(θ, pᵢ) sağlayan bir θ varsa, SUBST(θ, q) çıkarılır. GMP, Modus Ponens'in **yükseltilmiş** (*lifted*) hâlidir: Önermeselleştirme gibi tüm örnekleri üretmez, yalnızca gereken yerine koymayı yapar.

### 2.2 UNIFY

UNIFY(p, q), p ile q'yu özdeş yapan bir θ döndürür. Kitaptaki örnekler (`birlesim_unification.py` hepsini üretir):

| p | q | θ |
|---|---|---|
| Knows(John, x) | Knows(John, Jane) | {x/Jane} |
| Knows(John, x) | Knows(y, Bill) | {x/Bill, y/John} |
| Knows(John, x) | Knows(y, Mother(y)) | {y/John, x/Mother(John)} |
| Knows(John, x) | Knows(x, Elizabeth) | **başarısız** |

- **Değişkenleri ayırmak:** Son örnek, iki cümledeki "x"lerin aynı ad olmasından dolayı başarısızdır. Oysa bu değişkenler farklı ∀-cümlelerinden gelir. İkincisini x17 olarak yeniden adlandırınca: {x/Elizabeth, x17/John}.
- **En genel birleştirici (MGU):** Knows(John, x) ile Knows(y, z) için {y/John, x/z} de {y/John, x/John, z/John} de işe yarar. İlki **daha geneldir**: Diğerini ondan türetebiliriz. Her birleştirilebilir çift için yeniden adlandırmaya kadar tek bir MGU vardır.
- **Occurs check:** x ile f(x) birleşemez, çünkü x = f(f(f(…))) sonsuz bir terim olurdu. Bu kontrol, karmaşıklığı ifadenin boyutunda karesel yapabilir. Bu yüzden bazı Prolog sistemleri bu kontrolü atlar (ve sağlamlıktan ödün verir).

### 2.3 Depolama ve getirme

STORE(s) ve FETCH(q), bilgi tabanındaki cümleleri sorgulara hızlı eşlemek için kullanılır. **Yüklem indeksleme** (her yüklem için ayrı bir liste), ikinci argümana göre indeksleme ve **kapsama kafesi** (bir sorguyu genelleştiren tüm sorgular) buna örnektir.

---

## 3. İleri zincirleme

**Birinci derece kesin tümce:** Ya atomik bir cümle ya da atomik cümlelerin ∧'sinin tek bir pozitif atoma ima ettiği bir kural. Fonksiyon sembolü içermeyen kesin tümcelerden oluşan KB'lere **Datalog** denir.

**Suç örneği** (`suclu_bati.py`). Kitaptaki tümceler:
- American(x) ∧ Weapon(y) ∧ Sells(x, y, z) ∧ Hostile(z) ⇒ Criminal(x)
- Owns(Nono, M1), Missile(M1) (∃x Owns(Nono, x) ∧ Missile(x)'in EI ile örneklenmesi)
- Missile(x) ∧ Owns(Nono, x) ⇒ Sells(West, x, Nono)
- Missile(x) ⇒ Weapon(x); Enemy(x, America) ⇒ Hostile(x)
- American(West), Enemy(Nono, America)

İleri zincirleme **iki turda** biter:
1. Sells(West, M1, Nono), Weapon(M1), Hostile(Nono)
2. Criminal(West)

Bir olgu, bilinen bir olgunun yalnızca **yeniden adlandırılmışı** ise (Likes(x, Dondurma) ile Likes(y, Dondurma)) yeni sayılmaz.

**Verimlilik:**
- **Eşleme:** Bir kuralın öncüllerini olgularla eşlemek, bir CSP çözmek kadar zor olabilir (NP-zor). Öncülleri iyi bir sırayla denemek (en az eşleşeni önce) yardımcı olur. Bölüm 6'daki MRV gibi.
- **Artımlı ileri zincirleme:** Her turda yalnızca bir önceki turda eklenen olguları içeren eşleşmelere bak. **Rete** algoritması kısmi eşleşmeleri bir ağda saklar.
- **İlgisiz olgular:** İleri zincirleme sorguyla ilgisiz birçok sonuç türetebilir. **Sihirli kümeler** (*magic sets*) yöntemi, ileri zincirlemeyi sorguya odaklar.

---

## 4. Geri zincirleme

Hedeften başla. Sonucu hedefle birleşen her kural için öncüllerini alt hedef yap. Doğal olarak bir **üreteçtir**: Her yanıtı (yerine koymayı) sırayla verir. Suç örneğinde kanıt ağacı: Criminal(West) ← American(West), Weapon(M1) ← Missile(M1), Sells(West, M1, Nono) ← Missile(M1) ∧ Owns(Nono, M1), Hostile(Nono) ← Enemy(Nono, America).

### 4.1 Mantık programlama: Prolog

- "Algoritma = Mantık + Denetim." Program kesin tümcelerden oluşur. Çalıştırma, derinlik öncelikli geri zincirlemedir: Kurallar yukarıdan aşağıya, öncüller soldan sağa denenir.
- **Sapmalar:** Occurs check yoktur; **başarısızlık olarak değilleme** (\\+ P, P kanıtlanamazsa doğrudur); **kapalı dünya** ve **benzersiz isimler** varsayımları (veritabanı anlamı, Bölüm 8); aritmetik yerleşik yüklemlerle yapılır.
- Verimli derleme: Warren Soyut Makinesi (WAM), seçim noktaları, iz yığını.

### 4.2 Gereksiz çıkarım ve sonsuz döngüler

`prolog_yol.py` (kitaptaki şekildeki iki sıra):

```text
(a) yol(X,Z) :- bag(X,Z).                  (b) yol(X,Z) :- yol(X,Y), bag(Y,Z).
    yol(X,Z) :- yol(X,Y), bag(Y,Z).            yol(X,Z) :- bag(X,Z).
```

İki program mantıksal olarak **aynıdır**. Ama (b)'de Prolog yol(X, Y) alt hedefini hemen tekrar açar ve **sonsuz döngüye** girer. Derinlik sınırıyla denersek, ilk yanıttan önce açılan alt hedef sayısı sınırla doğrusal büyür (25, 61, 97). Sınırsız Prolog'da ilk yanıt hiç gelmez. İleri zincirleme ise iki durumda da 3 turda aynı 7 yolu türetir.

**Tablolama** (*memoization*): Sorulmuş alt hedefleri ve yanıtlarını sakla. Aynı alt hedef tekrar sorulunca yeniden aramak yerine tablodan al. Datalog programlarında sonsuz döngüleri önler.

**Kısıt mantık programlama (CLP):** Değişkenlerin sayısal kısıtlarla (X > 3 gibi) sınırlanmasına izin verir; Prolog'u Bölüm 6'nın CSP çözücüleriyle birleştirir.

---

## 5. Çözümleme

### 5.1 FOL için CNF

Adımlar (önerme mantığındakilere ek olarak):
1. ⇔ ve ⇒ eliminasyonu.
2. ¬'yi içe it; ¬∀x p ≡ ∃x ¬p ve ¬∃x p ≡ ∀x ¬p.
3. **Değişkenleri standartlaştır:** Her niceleyici farklı bir değişken adı kullansın.
4. **Skolemleştir:** Varoluşsal değişkeni, onu kapsayan evrensel değişkenlerin bir **Skolem fonksiyonuyla** değiştir. ∀x [∃y Hayvan(y) ∧ ¬Sever(x, y)] → ∀x Hayvan(F(x)) ∧ ¬Sever(x, F(x)). (F(x): "x'in sevmediği hayvan"; her x için farklı olabilir.)
5. ∀ niceleyicilerini düşür (kalan değişkenler örtük olarak evrenseldir).
6. ∨'yi ∧ üzerine dağıt.

### 5.2 Çözümleme kuralı

**İkili çözümleme:** İki tümcede, UNIFY(ℓᵢ, ¬mⱼ) = θ olan birer literal varsa, ikisini çıkarıp kalanları birleştir ve θ'yı uygula. **Çarpanlama:** Bir tümcede birleşebilen iki literali teke indir. İkisi birlikte, çürütme açısından tam bir sistem verir.

### 5.3 Kitaptaki kanıt: Kediyi Curiosity mi öldürdü?

`kedi_cozumleme.py`, kitaptaki A1, A2, B, C, D, E, F tümcelerinden ve ¬Kills(Curiosity, Tuna)'dan başlar. Destek kümesi stratejisiyle **8 adımda** boş tümceye ulaşır. Özet: Curiosity öldürmediyse Jack öldürmüştür. Tuna bir kedi, dolayısıyla bir hayvan. Hayvan öldüren kimse sevilmez, demek ki kimse Jack'i sevmez. Ama Jack tüm hayvanları sever, bu yüzden biri onu sever. Çelişki.

**Yanıt çıkarma:** "Kediyi kim öldürdü?" (∃w Kills(w, Tuna)) için hedefin değiline Yanıt(w) literali eklenir. İlk bulunan tümce **Yanıt(Curiosity) ∨ Yanıt(Jack)** olabilir: Bir katil olduğu kanıtlanmıştır ama kim olduğu belli değildir. Buna **yapıcı olmayan kanıt** denir. Arama sürdürülünce tek başına **Yanıt(Curiosity)** bulunur.

### 5.4 Tamlık

**Gödel'in tamlık teoremi** (1930): FOL'da gerektirilen her cümlenin sonlu bir kanıtı vardır. **Çözümleme çürütme açısından tamdır**: KB ∧ ¬α karşılanamazsa, çözümleme boş tümceyi türetir. Kanıt fikri: Herbrand teoremi, temel (önerme) çözümleme teoremi ve **yükseltme önsavı** (temel kanıtın her adımını birleştirmeyle yükseltilmiş bir adıma çevirme).

Gödel'in **eksiklik** teoremi ise farklı bir şey söyler: Aritmetiği ifade edebilen tutarlı her sistemde, doğru ama kanıtlanamayan cümleler vardır.

### 5.5 Eşitlik

= özel bir ilişkidir. Ya eşitlik aksiyomları eklenir (yansıma, simetri, geçişlilik, yerine koyma) ya da özel kurallar kullanılır: **demodülasyon** (x = y birim tümcesiyle terimleri yeniden yaz), **paramodülasyon** (koşullu eşitlikler için genelleştirilmiş hâli), eşitliği dikkate alan birleştirme.

### 5.6 Stratejiler

- **Birim tercihi:** Tek literalli tümcelerle çözümlemeyi önce dene (çözümleyici kısalır).
- **Destek kümesi:** Her çözümlemede en az bir ebeveyn, hedeften türemiş tümcelerden olsun. KB kendi içinde tutarlıysa tamlık korunur. `fol_cikarim.cozumleme` bu stratejiyi kullanır.
- **Girdi çözümlemesi:** Her adımda bir ebeveyn özgün girdilerden olsun (Horn KB'lerde tamdır).
- **Kapsama** (*subsumption*): Daha genel bir tümce varken ondan daha özel tümceleri at.

Pratik teorem ispatlayıcılar (Vampire, E, Otter/Prover9) donanım ve yazılım doğrulamasında, sentezinde ve matematikte kullanılır.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "EI'da istediğim sabiti seçebilirim." | Sabit **yeni** olmalı, KB'de hiç geçmemeli. Aksi hâlde yanlış bilgi eklenir. |
| "Skolemleştirmede her zaman sabit kullanılır." | ∃, bir ∀'nin içindeyse Skolem **fonksiyonu** gerekir (F(x)). |
| "Knows(John, x) ile Knows(x, Elizabeth) birleşemez, demek ki birbirleriyle ilgisizler." | Değişkenleri ayırınca birleşirler. x'ler farklı cümlelerdendir. |
| "Mantıksal olarak eşdeğer iki Prolog programı aynı davranır." | Kural sırası denetimi değiştirir. Biri biter, diğeri sonsuz döngüye girebilir. |
| "Çözümleme her doğru α'yı doğrudan türetir." | Çürütme açısından tamdır: KB ∧ ¬α'dan □ türetir. |
| "Çözümleme 'kim?' sorusuna hep tek bir yanıt verir." | Yapıcı olmayan (ayrık) yanıtlar verebilir. |

## Kendini yokla

1. ∀x ∃y Anne(y, x) cümlesini Skolemleştir.
2. UNIFY(P(x, f(x)), P(f(y), y)) sonucu nedir?
3. Suç örneğinde üçüncü bir tur olur mu? Neden?
4. Destek kümesi stratejisi neden KB'nin kendi içinde tutarlı olmasını gerektirir?
5. Tablolama, (b) sırasındaki yol programını nasıl kurtarır?

## Kod rehberi

```bash
python ornekler/fol_cikarim.py            # kütüphane: kitaptaki birleştirme örnekleri
python ornekler/birlesim_unification.py   # UNIFY, MGU, occurs check, değişken ayırma
python ornekler/suclu_bati.py             # Criminal(West): ileri (2 tur) ve geri zincirleme
python ornekler/kedi_cozumleme.py         # çözümleme, yanıt çıkarma, yapıcı olmayan kanıt
python ornekler/prolog_yol.py             # kural sırası ve sonsuz döngü
python ornekler/geriye_zincir.py          # kayıp USB: özgün bir geri zincirleme örneği
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| evrensel / varoluşsal örnekleme | universal / existential instantiation | ∀'yi temel terimle, ∃'yi yeni sabitle değiştirme |
| Skolem sabiti / fonksiyonu | Skolem constant / function | ∃ değişkeninin yerine konan yeni sembol |
| önermeselleştirme | propositionalization | FOL KB'sini önerme KB'sine indirgeme |
| yarı karar verilebilir | semidecidable | Evet yanıtları bulunur, hayır garantisi yok |
| genelleştirilmiş Modus Ponens | generalized Modus Ponens | Yükseltilmiş çıkarım kuralı |
| yükseltme | lifting | Temel çıkarımı değişkenli hâle getirme |
| birleştirme / birleştirici | unification / unifier | İki ifadeyi özdeş yapan yerine koyma |
| en genel birleştirici | most general unifier (MGU) | En az kısıtlayıcı birleştirici |
| occurs check | occurs check | Değişkenin kendini içeren terime bağlanmasını engelleme |
| değişkenleri ayırma | standardizing apart | Değişkenleri yeniden adlandırma |
| kesin tümce | definite clause | Tam bir pozitif literal |
| yeniden adlandırma | renaming | Yalnızca değişken adları farklı olan cümle |
| artımlı ileri zincirleme | incremental forward chaining | Yalnızca yeni olgularla eşleştirme |
| sihirli kümeler | magic sets | İleri zincirlemeyi sorguya odaklama |
| başarısızlık olarak değilleme | negation as failure | Kanıtlanamayan = yanlış |
| tablolama | tabling (memoization) | Alt hedef yanıtlarını saklama |
| kısıt mantık programlama | constraint logic programming | Prolog + kısıt çözücü |
| çarpanlama | factoring | Birleşen iki literali teke indirme |
| çürütme açısından tam | refutation-complete | Karşılanamazlığı her zaman bulur |
| yükseltme önsavı | lifting lemma | Temel kanıttan FOL kanıtına geçiş |
| demodülasyon / paramodülasyon | demodulation / paramodulation | Eşitlikle yeniden yazma kuralları |
| birim tercihi / destek kümesi / girdi çözümlemesi | unit preference / set of support / input resolution | Çözümleme stratejileri |
| kapsama | subsumption | Genel tümce varken özel olanı atma |
