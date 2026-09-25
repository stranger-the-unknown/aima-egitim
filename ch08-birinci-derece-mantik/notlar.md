# Bölüm 8 — Birinci derece mantık

> **Kitapta:** AIMA 4. baskı, Bölüm 8 *"First-Order Logic"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 8.1 Representation Revisited | §1 Neden önerme mantığı yetmez; ontolojik ve epistemolojik bağlılık | — |
| 8.2 Syntax and Semantics of FOL | §2 Model, sembol, yorum, terim, niceleyici, eşitlik, veritabanı anlamı | `fol_model.py`, `fol_ceviri.py` |
| 8.3 Using First-Order Logic | §3 TELL/ASK/ASKVARS, akrabalık, sayılar, Wumpus | `akrabalik_turkce.py`, `fol_sozluk.py` |
| 8.4 Knowledge Engineering in FOL | §4 Yedi adım, elektronik devre | `tam_toplayici.py` |

## Öğrenme hedefleri

1. Önerme mantığının neden yetersiz kaldığını ve FOL'un neyi eklediğini açıklamak.
2. Bir FOL cümlesinin bir modelde doğru olup olmadığını değerlendirmek.
3. Doğal dil cümlelerini FOL'a doğru çevirmek; ∀/⇒ ve ∃/∧ eşleşmesini, niceleyici sırasını ve eşitliği doğru kullanmak.
4. Bir alan için sözcük dağarcığı ve aksiyomlar yazmak (akrabalık, Wumpus).
5. Bilgi mühendisliğinin yedi adımını bir devre örneğine uygulamak.

---

## 1. Temsili yeniden düşünmek

**Önerme mantığının sınırı:** Nesneler ve ilişkiler yoktur, yalnızca olgular vardır. "Çukurun yanındaki karelerde esinti olur" demek için Wumpus dünyasında her kare için ayrı bir kural yazmak gerekir (16 kare → 16 kural; 100×100 dünyada 10.000 kural).

**Doğal dil** çok güçlüdür ama belirsizdir ("bir"i, "o"yu kimin kastettiği bağlama bağlıdır) ve biçimsel çıkarıma uygun değildir. **FOL**, doğal dildeki üç temel öğeyi biçimsel ve kesin hâle getirir:
- **Nesneler:** insanlar, kareler, sayılar, renkler…
- **İlişkiler:** tekli (özellik: Kırmızı, Kral) ya da n'li (Kardeş, Arasında)
- **Fonksiyonlar:** her nesneye tek bir nesne karşılık getiren ilişkiler (SolBacak, Baba)

| Dil | Ontolojik bağlılık (dünyada ne var?) | Epistemolojik bağlılık (bilgi nasıl?) |
|---|---|---|
| Önerme mantığı | olgular | doğru / yanlış / bilinmiyor |
| Birinci derece mantık | olgular, nesneler, ilişkiler | doğru / yanlış / bilinmiyor |
| Zaman mantığı | + zaman noktaları | doğru / yanlış / bilinmiyor |
| Yüksek dereceli mantık | + ilişkiler ve fonksiyonlar üzerinde ilişkiler | doğru / yanlış / bilinmiyor |
| Olasılık kuramı | olgular | inanç derecesi ∈ [0, 1] |
| Bulanık mantık | doğruluk derecesi ∈ [0, 1] olan olgular | bilinen aralık değeri |

---

## 2. Sözdizimi ve anlam

### 2.1 Modeller ve yorumlar

Bir FOL **modeli**, bir **alan** (boş olmayan nesneler kümesi) ile nesneler arasındaki ilişki ve fonksiyonlardan oluşur. İlişkiler, ilişkideki nesne **demetlerinin** kümesidir. Fonksiyonlar **toplamdır**: Her girdi için bir çıktı olmalıdır.

**Semboller:** sabitler (Richard, John), yüklemler (Kardeş/2, Kral/1), fonksiyonlar (SolBacak/1). Her sembolün bir **çokluğu** (argüman sayısı) vardır. **Yorum**, sembolleri modeldeki nesnelere, ilişkilere ve fonksiyonlara eşler. Aynı model üzerinde birçok yorum mümkündür. Sabit ve nesne sayısı sınırsız olduğu için standart FOL'da model sayısı **sonsuzdur**.

### 2.2 Terimler ve cümleler

- **Terim:** nesneye gönderme yapan ifade: sabit (John), değişken (x), fonksiyon uygulaması (SolBacak(John)).
- **Atomik cümle:** Yüklem(terimler). Kardeş(Richard, John).
- **Bileşik cümle:** ¬, ∧, ∨, ⇒, ⇔ ile.

`fol_model.py`, kitaptakine benzer bir modelde (Richard, John, iki bacak, bir taç) bu cümleleri değerlendirir.

### 2.3 Niceleyiciler

- **∀x P(x)**: Alandaki **her** nesne için P doğru. Doğal eşi **⇒**'dir: ∀x Kral(x) ⇒ Kişi(x).
- **∃x P(x)**: En az **bir** nesne için P doğru. Doğal eşi **∧**'dir: ∃x Taç(x) ∧ Başında(x, John).

**İki klasik hata** (`fol_model.py` ikisini de gösterir):
- ∀x Kral(x) **∧** Kişi(x): "Herkes kraldır ve kişidir" der. Modelde yanlıştır, çünkü taç bir kral değildir.
- ∃x Taç(x) **⇒** Başında(x, John): Taç olmayan herhangi bir nesne için ⇒ doğru olur. Bu yüzden cümle neredeyse her modelde doğrudur ve hiçbir şey söylemez.

**Niceleyici sırası önemlidir:**
- ∀x ∃y Sever(x, y): Herkes birini sever (belki herkes farklı birini).
- ∃y ∀x Sever(x, y): Herkesin sevdiği biri vardır.

İkinci cümle birincisini gerektirir, tersi doğru değildir. `fol_model.py`, "herkes başka birini seviyor" modelinde birincinin doğru, ikincinin yanlış olduğunu gösterir.

**Niceleyicilerin ilişkisi (De Morgan):** ∀x ¬P ≡ ¬∃x P; ¬∀x P ≡ ∃x ¬P; ∀x P ≡ ¬∃x ¬P; ∃x P ≡ ¬∀x ¬P.

### 2.4 Eşitlik

t₁ = t₂, iki terimin **aynı nesneye** gönderme yaptığını söyler. "Richard'ın en az iki kardeşi var" için şunu yazmak yetmez:

Kardeş(John, Richard) ∧ Kardeş(Geoffrey, Richard)

Çünkü standart anlamda John ile Geoffrey **aynı nesne** olabilir (`fol_model.py`, standart anlam bölümü). Doğrusu: ∃x, y Kardeş(x, Richard) ∧ Kardeş(y, Richard) ∧ ¬(x = y).

### 2.5 Veritabanı anlamı

Standart anlamın getirdiği bu zorlukları azaltan üç varsayım:
1. **Benzersiz isimler:** Farklı sabitler farklı nesnelerdir.
2. **Kapalı dünya:** Doğru olduğu bilinmeyen atomik cümleler yanlıştır.
3. **Alan kapanışı:** Modelde, sabitlerin gösterdiklerinden başka nesne yoktur.

Bu anlamda 2 sabit ve 1 ikili ilişkiyle yalnızca 2⁴ = **16** model vardır; standart anlamda ise sonsuz. Veritabanları ve mantık programlama (Prolog) bu anlamı kullanır. "Doğru" tek bir anlam yoktur; uygun olanı kullanım amacı belirler.

---

## 3. FOL'u kullanmak

### 3.1 TELL, ASK, ASKVARS

- TELL(KB, Kral(John)), TELL(KB, ∀x Kral(x) ⇒ Kişi(x))
- ASK(KB, Kişi(John)) → evet
- ASK(KB, ∃x Kişi(x)) → evet, ama *kim* olduğunu söylemez. **ASKVARS(KB, Kişi(x))** ise bir **yerine koyma** (bağlama listesi) döndürür: {x/John}, {x/Richard}.

### 3.2 Akrabalık alanı

**Temel** ilişkilerden (Ebeveyn, Erkek, Kadın) diğerleri **tanımlanır**:

- ∀p, c Anne(p, c) ⇔ Ebeveyn(p, c) ∧ Kadın(p)
- ∀x, y Kardeş(x, y) ⇔ x ≠ y ∧ ∃p Ebeveyn(p, x) ∧ Ebeveyn(p, y)
- ∀x, y Amca(x, y) ⇔ Erkek(x) ∧ ∃b Baba(b, y) ∧ Kardeş(x, b)
- ∀x, y Dayı(x, y) ⇔ Erkek(x) ∧ ∃a Anne(a, y) ∧ Kardeş(x, a)

**Aksiyomlar** alan hakkında temel gerçeklerdir. **Tanımlar**, ⇔ ile yazılmış aksiyomlardır. **Teoremler** aksiyomlardan çıkar ("kardeşlik simetriktir"). Teoremler mantıksal olarak gereksizdir ama çıkarımı hızlandırır.

**Ontoloji dile bağlıdır:** İngilizcede "uncle" tek kavramdır. Türkçe onu **amca** (babanın erkek kardeşi) ve **dayı** (annenin erkek kardeşi) olarak ayırır; "aunt" da **hala** ve **teyze** olur. `akrabalik_turkce.py` aynı aile için iki sözcük dağarcığını karşılaştırır. Hangi kavramların temel, hangilerinin türetilmiş olacağı bir tasarım kararıdır.

### 3.3 Sayılar, kümeler, listeler

**Peano aksiyomları:** NatNum(0); ∀n NatNum(n) ⇒ NatNum(S(n)). 0 hiçbir sayının ardılı değildir; ardıl fonksiyonu birebirdir. Toplama ardıl üzerinden tanımlanır: ∀m NatNum(m) ⇒ +(0, m) = m; ∀m, n +(S(m), n) = S(+(m, n)). Kümeler ve listeler de aynı biçimde birkaç sabit ve fonksiyonla aksiyomlaştırılır.

### 3.4 Wumpus dünyası FOL'da

- Algı zamanla birlikte yazılır: Algı([Koku, Esinti, Parıltı, Yok, Yok], 5).
- Kare komşuluğu tek bir aksiyomdur: ∀x, y, a, b Komşu([x, y], [a, b]) ⇔ (x = a ∧ (y = b − 1 ∨ y = b + 1)) ∨ (y = b ∧ (x = a − 1 ∨ x = a + 1)).
- Esinti kuralı, **her** kare için tek bir cümledir: ∀s Esintili(s) ⇔ ∃r Komşu(r, s) ∧ Çukur(r).

**Teşhis kuralı** (gözlemden nedene: esinti ⇒ komşuda çukur) ile **nedensel kural** (nedenden gözleme: çukur ⇒ komşularda esinti) farklıdır. Nedensel kurallarla kurulan sistemlere **model tabanlı akıl yürütme** denir. Bölüm 13'te Bayes ağlarında da bu ayrım önemlidir.

---

## 4. Bilgi mühendisliği

Belirli bir alan için bilgi tabanı kurma sürecidir. Kitaptaki yedi adım, bir bitlik tam toplayıcı (C1) örneğiyle (`tam_toplayici.py`):

| Adım | C1 için |
|---|---|
| 1. Görevi belirle | Devre doğru topluyor mu? Hangi girişler hangi çıkışı verir? |
| 2. İlgili bilgiyi topla | Kapılar, uçlar, bağlantılar, sinyaller. Gecikme, güç gibi ayrıntılar **dışarıda**. |
| 3. Sözcük dağarcığına karar ver | Kapı(x), Tip(x) = XOR, Bağlı(u₁, u₂), Sinyal(u), Giriş(n, x), Çıkış(n, x) |
| 4. Genel alan bilgisini kodla | Bağlı uçların sinyali eşittir; AND'in çıkışı 1 ⟺ tüm girişleri 1… |
| 5. Problem örneğini tanımla | C1'in iki XOR, iki AND ve bir OR kapısı, 12 bağlantı |
| 6. Sorguları sor | ∃ i₁, i₂, i₃: Sinyal(Çıkış(1, C1)) = 0 ∧ Sinyal(Çıkış(2, C1)) = 1? |
| 7. Hata ayıkla | Bilgi tabanını boz, davranışı izle |

**Kitaptaki sorgunun yanıtı:** Toplam = 0 ve elde = 1 veren girişler **{1, 1, 0}, {1, 0, 1}, {0, 1, 1}**. `tam_toplayici.py` bunu ve tam giriş–çıkış tablosunu üretir ve devrenin gerçekten topladığını doğrular. Bir bağlantıyı bozunca yalnızca (0, 1, 1) girişinin yanlış sonuç verdiğini gösterir.

> **Kitaptaki önemli hata ayıklama dersi:** Sinyal değerleri 1 ve 0 için "1 ≠ 0" aksiyomu unutulursa, genel bir FOL çıkarım sistemi çoğu çıkışı kanıtlayamaz. Standart anlamda iki farklı sabitin farklı nesneleri gösterdiği varsayılmaz (bkz. §2.5).

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| ∀x Kral(x) ∧ Kişi(x) | ∀x Kral(x) **⇒** Kişi(x) |
| ∃x Taç(x) ⇒ Başında(x, John) | ∃x Taç(x) **∧** Başında(x, John) |
| "∀x∃y ile ∃y∀x aynıdır." | Farklıdır. İkincisi birincisini gerektirir, tersi doğru değildir. |
| "Farklı isimler farklı nesnelerdir." | Standart anlamda değil; bunun için x ≠ y ya da veritabanı anlamı gerekir. |
| "Fonksiyon her girdi için tanımsız bırakılabilir." | FOL'da fonksiyonlar toplamdır. Anlamsız girdiler için bile bir çıktı nesnesi olmalıdır. |
| "Kardeş(x, y) ⇔ ∃p Ebeveyn(p, x) ∧ Ebeveyn(p, y)" | x ≠ y unutulursa herkes kendinin kardeşi olur. |

## Kendini yokla

1. "Her öğrenci bir dersi sever" cümlesinin iki farklı okunuşunu FOL'da yaz.
2. Taç olmayan hiçbir nesne olmayan bir modelde ∃x Taç(x) ⇒ Başında(x, John) ne zaman yanlış olur?
3. Veritabanı anlamında 3 sabit ve 1 ikili ilişkiyle kaç model vardır?
4. Kuzen ilişkisini Ebeveyn ve Kardeş cinsinden tanımla.
5. Tam toplayıcıda Bağlı ilişkisinin simetrik olduğunu neden ayrıca belirtmek gerekir?

## Kod rehberi

```bash
python ornekler/fol_model.py          # modelde değerlendirme, iki klasik hata, niceleyici sırası, veritabanı anlamı
python ornekler/fol_ceviri.py         # Türkçe ↔ FOL çeviri örnekleri
python ornekler/fol_sozluk.py         # Ebeveyn/Ata olgularından ileri zincirleme
python ornekler/akrabalik_turkce.py   # amca/dayı/hala/teyze tanımları
python ornekler/tam_toplayici.py      # bilgi mühendisliği: kitaptaki C1 devresi
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| birinci derece mantık | first-order logic (FOL) | Nesneler, ilişkiler, niceleyiciler |
| ontolojik bağlılık | ontological commitment | Dilin dünyada neyin var olduğunu varsayması |
| epistemolojik bağlılık | epistemological commitment | Dilin olası bilgi durumları |
| alan | domain | Modeldeki nesneler kümesi |
| demet | tuple | İlişkideki sıralı nesne listesi |
| yorum | interpretation | Sembollerin modeldeki karşılıkları |
| çokluk | arity | Argüman sayısı |
| terim | term | Nesneye gönderme yapan ifade |
| atomik cümle | atomic sentence | Yüklem(terimler) |
| evrensel / varoluşsal niceleyici | universal / existential quantifier | ∀ / ∃ |
| eşitlik | equality | İki terimin aynı nesneyi göstermesi |
| benzersiz isimler varsayımı | unique-names assumption | Farklı sabit → farklı nesne |
| kapalı dünya varsayımı | closed-world assumption | Bilinmeyen = yanlış |
| alan kapanışı | domain closure | Sabitlerin gösterdiklerinden başka nesne yok |
| yerine koyma / bağlama listesi | substitution / binding list | {x/John} |
| aksiyom / tanım / teorem | axiom / definition / theorem | Temel gerçek / ⇔ ile aksiyom / türetilen |
| teşhis / nedensel kural | diagnostic / causal rule | Gözlemden nedene / nedenden gözleme |
| bilgi mühendisliği | knowledge engineering | Bir alan için KB kurma süreci |
| ontoloji | ontology | Alanın kavramları ve ilişkileri |
