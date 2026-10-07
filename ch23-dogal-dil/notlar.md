# Bölüm 23 — Doğal dil işleme

> **Kitapta:** AIMA 4. baskı, Bölüm 23 *"Natural Language Processing"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 23.1 Language Models | §1 Sözcük torbası, n-gram, düzeltme, sözcük temsilleri, sözcük türü etiketleme, karşılaştırma | `dil_modelleri.py` |
| 23.2 Grammar | §2 PCFG ve E₀ dilbilgisi, sözlük | `ayristirma.py` |
| 23.3 Parsing | §3 CYK, A* ve ışın araması, bağımlılık ayrıştırma, ağaç bankasından öğrenme | `ayristirma.py` |
| 23.4 Augmented Grammars | §4 Bileşimsel anlambilim, λ-hesabı | `anlambilim.py` |
| 23.5 Complications of Real Natural Language | §5 Niceleme, edimbilim, belirsizlik, mecaz | — |
| 23.6 Natural Language Tasks | §6 Konuşma tanıma, çeviri, bilgi çıkarma, soru yanıtlama | — |

## Öğrenme hedefleri

1. Sözcük torbası ve n-gram dil modellerini kurmak; görülmemiş olaylar için düzeltme yapmak.
2. Şaşkınlıkla dil modellerini karşılaştırmak; HMM ile sözcük türü etiketlemek.
3. Olasılıksal bağlamdan bağımsız dilbilgisiyle (PCFG) bir cümlenin olasılığını hesaplamak.
4. CYK algoritmasıyla en olası ayrıştırma ağacını bulmak; belirsizliği tanımak.
5. Ağaç bankasından PCFG öğrenmek.
6. Bileşimsel anlambilimle bir öbeğin anlamını alt öbeklerinden kurmak.
7. Gerçek dilin zorluklarını (belirsizlik, edimbilim, mecaz) ve temel NLP görevlerini tanımak.

---

## 1. Dil modelleri (`dil_modelleri.py`)

Doğal diller biçimsel diller gibi kesin tanımlı değildir: dilbilgisine "uygun" ile "uygun olmayan" arasında keskin sınır yoktur, bir cümlenin tek bir doğru ağacı olmayabilir, anlam belirsizdir. Bu yüzden **olasılıksal** bir dil modeli kurarız: dizelere olasılık dağılımı.

### 1.1 Sözcük torbası

Sözcük sırası yok sayılır; naif Bayes (Bölüm 12) ile metin sınıflandırma:

```text
P(Sınıf | w₁:N) = α P(Sınıf) Πⱼ P(wⱼ | Sınıf)
```

Sayımla öğrenme (kitaptaki sayılar): 3000 metnin 300'ü ekonomi → P(ekonomi) ≈ 0.1; ekonomi metinlerindeki 100 000 sözcükte "stocks" 700 kez → P(stocks | ekonomi) ≈ 0.007. Özellik vektörü çok büyük ve seyrektir. Derlemler: Vikipedi ~2.5 milyar sözcük, iWeb 14 milyar sözcük.

### 1.2 n-gram modelleri

Zincir kuralıyla P(w₁:N) = Πⱼ P(wⱼ | w₁:j−1); tam koşullu olasılıklar için çok fazla parametre gerekir (100 000 sözcük ve 40 sözcüklük cümle: 10²⁰⁰). **Markov varsayımı:** Her sözcük yalnızca önceki n − 1 sözcüğe bağlı (unigram, bigram, trigram). **Karakter düzeyinde** n-gramlar bilinmeyen sözcüklerde ve sözcükleri bitiştiren dillerde (Türkçe gibi eklemeli diller) yararlıdır. **Atlamalı n-gramlar** ara sözcükleri atlar.

### 1.3 Düzeltme (smoothing)

- **Bilinmeyen sözcük:** Seyrek sözcükleri eğitimde `<UNK>` ile değiştir; test sırasındaki bilinmeyen sözcük `<UNK>` olasılığını alır.
- **Görülmemiş n-gramlar** sıfır olasılık almamalı.
- **Laplace (+1) düzeltmesi:** Sayımları 1'den başlat. Laplace'ın ardıllık kuralı: N kez görülen olayın bir sonraki seferde olmama olasılığı 1/(N + 2) (güneşin 2 milyon gündür doğması örneği). Seyrek veride kaba kalır.
- **Geri çekilme (backoff):** n-gram sayısı yoksa (n−1)-grama düş.
- **Doğrusal ara değerleme:** P̂(cᵢ | cᵢ₋₂ cᵢ₋₁) = λ₃ P(cᵢ | cᵢ₋₂ cᵢ₋₁) + λ₂ P(cᵢ | cᵢ₋₁) + λ₁ P(cᵢ), λ'lar toplamı 1.

Kodumuzda düzeltmesiz trigram görülmemiş bir üçlü için −∞ verir; Laplace ve ara değerleme sonlu olasılık verir.

### 1.4 Sözcük temsilleri

n-gramlar "kedi" ile "köpek"in benzer olduğunu bilmez. **Sözcük gömmeleri** (Bölüm 24), sözcükleri benzer anlamlıların yakın düştüğü düşük boyutlu vektörlere yerleştirir. Elle kurulan sözlük ağları (WordNet gibi) de kullanılır.

### 1.5 Sözcük türü (POS) etiketleme

Her sözcüğe ad, fiil, sıfat… etiketi (Penn Treebank'te 45 etiket). Saklı Markov modeli (Bölüm 14): gizli durum = etiket, gözlem = sözcük; **Viterbi** ile en olası etiket dizisi. Kodumuz küçük bir Türkçe etiketli derlemle HMM eğitip Viterbi uygular. Lojistik regresyon gibi ayırt edici modeller de kullanılır (zengin özellikler: sözcüğün eki, büyük harf, önceki etiket…). Işın araması ile hızlandırma.

### 1.6 Dil modellerini karşılaştırmak

Kitap, aynı metinden 1-, 2-, 3- ve 4-gram modelleriyle rastgele metin üretir: n büyüdükçe metin kitaba benzer hâle gelir, ama 4-gram çoğu zaman eğitim metnini aynen kopyalar. Nicel ölçü **şaşkınlık**: Perplexity(c₁:N) = P(c₁:N)^(−1/N); düşük olan daha iyi. Kodumuzda ara değerlenmiş model en düşük şaşkınlığı verir.

---

## 2. Dilbilgisi (`ayristirma.py`)

**Dilbilgisi:** İzin verilen öbeklerin ağaç yapısını tanımlayan kurallar. **Sözdizimsel kategoriler** (ad öbeği NP, fiil öbeği VP…) ve **öbek yapısı** anlam için bir iskelet sağlar.

**Olasılıksal bağlamdan bağımsız dilbilgisi (PCFG):** Her kuralın bir olasılığı var; aynı sol taraflı kuralların olasılıkları toplamı 1. "Bağlamdan bağımsız": Bir kural her bağlamda aynı olasılıkla kullanılır. Bir ağacın olasılığı, kullanılan kuralların olasılıklarının çarpımıdır.

**E₀:** Wumpus dünyası için küçük bir İngilizce parçası (Şekil 23.2): S → NP VP [0.90] | S Conj S [0.10]; NP → Pronoun [0.25] | Name [0.10] | Noun [0.10] | Article Noun [0.25] | Article Adjs Noun [0.05] | Digit Digit [0.05] | NP PP [0.10] | NP RelClause [0.05] | NP Conj NP [0.05]; VP → Verb [0.40] | VP NP [0.35] | VP Adjective [0.05] | VP PP [0.10] | VP Adverb [0.10]; …

E₀ **fazla üretir** ("Me go I" kabul edilir) ve **eksik üretir** ("I think the wumpus is smelly" reddedilir).

**Sözlük:** Açık sınıflar (ad, fiil, sıfat, belirteç, özel ad: sürekli yeni sözcük eklenir) ve kapalı sınıflar (zamir, ilgi zamiri, tanımlık, edat, bağlaç: yüzyıllarca az değişir).

---

## 3. Ayrıştırma

**Ayrıştırma:** Sözcük dizisinin öbek yapısını bulmak; yaprakları sözcükler olan geçerli bir ağaç araması. Yukarıdan aşağıya ya da aşağıdan yukarıya arama boşa iş yapabilir ("Have the students in section 2 of Computer Science 101 take/taken the exam": İlk 10 sözcük aynı, ayrıştırma tamamen farklı). Çözüm dinamik programlama: Bulunan her alt öbeği bir **çizelgeye** kaydet (**çizelge ayrıştırıcı**).

### 3.1 CYK algoritması

Dilbilgisinin **Chomsky normal biçiminde** olmasını ister: X → sözcük [p] ve X → Y Z [p]. Her bağlamdan bağımsız dilbilgisi bu biçime çevrilebilir (üçlü kurallar ara simgelerle ikiliye, tekli kurallar kapanışla). Aşağıdan yukarıya: Önce uzunluğu 1 olan aralıklar, sonra 2, … Her aralık (i, j) ve her bölme noktası k için X → Y Z kuralını dene; her kategori için en olası değeri ve geri işaretçiyi tut.

Uzay O(n² m), zaman O(n³ m) (n sözcük, m kategori). Bütün CFG'ler için daha iyisi yok; ama doğal diller gerçek zamanda anlaşılmak üzere evrilmiştir. **A\*** (maliyet = olasılığın tersi, öğrenilmiş sezgisel) ilk bulduğu ayrıştırmanın en olası olduğunu garanti eder ve genelde daha hızlıdır; **ışın araması** yalnızca en olası b ayrıştırmayı tutar.

Kitaptaki örnek (Şekil 23.4), kodumuzun bulduğuyla aynı:

```text
the wumpus is dead → [S [NP [Article the] [Noun wumpus]] [VP [VP [Verb is]] [Adjective dead]]]
P = 0.90 × (0.25 × 0.40 × 0.15) × (0.05 × 0.40 × 0.10 × 0.05) = 1.35 × 10⁻⁶
```

**Belirsizlik:** "I feel the wumpus near 1 3"te edat öbeği fiile ya da ada bağlanabilir: 2 ağaç. E₀'da VP → VP PP ile NP → NP PP aynı olasılıklı (0.10) olduğu için iki ağacın olasılığı **eşittir** (A7): Bağlamdan bağımsız dilbilgisi hangi bağlanmanın doğru olduğunu ayırt edemez; sözcüklere duyarlı (sözcükselleştirilmiş) olasılıklar gerekir.

### 3.2 Bağımlılık ayrıştırma

Öbekler yerine sözcükler arasında ikili ilişkiler (özne, nesne, belirleyici…). Öbek yapısıyla notasyon farkı gibidir; ama sözcük sırası serbest dillerde (Latince gibi) daha doğaldır. **Evrensel Bağımlılıklar** projesi 70'ten fazla dilde milyonlarca ayrıştırılmış cümle sunar.

### 3.3 Ayrıştırıcıyı örneklerden öğrenmek

Dilbilgisini elle yazmak yerine **ağaç bankasından** öğren. **Penn Treebank:** 100 binden fazla cümle. Her düğüm türünü say: X → α'nın olasılığı = sayı(X → α) / sayı(X) (kitaptaki örnek: S → NP VP [0.6]). Penn Treebank'te 10 000'den fazla farklı düğüm türü var. Kodumuz 5 ağaçlık oyuncak bir bankadan PCFG çıkarır. Ağaç bankası yoksa EM benzeri **iç–dış** algoritmasıyla etiketsiz metinden de öğrenilebilir (daha zayıf).

---

## 4. Artırılmış dilbilgileri (`anlambilim.py`)

Kategorilere bağımsız değişkenler eklemek: tekillik/çoğulluk, durum (özne/nesne zamiri: "I" ve "me"), anlam. **Sözcükselleştirilmiş PCFG'ler** kuralların olasılığını başsözcüğe bağlar (ör. "ate a banana" ile "ate a bandanna").

### 4.1 Anlamsal yorum

**Bileşimsel anlambilim:** Bir öbeğin anlamı alt öbeklerinin anlamlarının bir fonksiyonudur. Aritmetik dilbilgisi:

```text
Exp(op(x₁, x₂)) → Exp(x₁) Operator(op) Exp(x₂)
Exp(x) → ( Exp(x) )            Exp(x) → Number(x)
Number(x) → Digit(x)           Number(10x + y) → Number(x) Digit(y)
```

"3 + (4 ÷ 2)" ağacının kökü **Exp(5)**.

İngilizcede anlam birinci derece mantık: "Ali loves Bo" → Loves(Ali, Bo). "loves Bo" → **λx Loves(x, Bo)** (λ-gösterimi, Bölüm 8); S(pred(obj)) → NP(obj) VP(pred) kuralı (λx Loves(x, Bo))(Ali) = Loves(Ali, Bo) verir.

### 4.2 Anlamsal dilbilgilerini öğrenmek

Penn Treebank anlamsal gösterim içermez; başka örnek kaynakları gerekir. Kitaptaki örnek: Zettlemoyer ve Collins (2005), "What states border Texas?" gibi cümleleri mantıksal biçimleriyle (λx.state(x) ∧ λx.borders(x, Texas)) eşleyen çiftlerden soru yanıtlama dilbilgisi öğrenir ve görülmemiş cümlelerde %79 doğruluğa ulaşır; daha sonraki bir kaydır-indirge ayrıştırıcı %85'e çıkar.

---

## 5. Gerçek dilin zorlukları

- **Niceleme:** "Every agent feels a breeze": Her ajan için ayrı bir esinti mi, herkesin hissettiği tek bir esinti mi? Tek ayrıştırma, iki anlam.
- **Edimbilim (pragmatics):** Bağlama bağlı anlam. **Gösterge sözcükler** ("I", "today") duruma göre çözülür; **söz edimleri** (soru, istek, bilgi verme) konuşanın niyetini yorumlamayı gerektirir.
- **Uzak bağımlılıklar** ve zaman/kip.
- **Belirsizlik:** Neredeyse her cümle belirsizdir. **Sözcüksel** (bir sözcüğün birden çok anlamı), **sözdizimsel** (ağaç belirsizliği), **anlamsal** belirsizlik.
- **Mecaz:** **Düz değişmece** (metonymy: "Chrysler announced…" ile şirketin sözcüsü kastedilir; "Masa 4'teki jambonlu sandviç bira istiyor") ve **eğretileme** (metaphor: benzerliğe dayanan değişmece).
- **Belirsizlik giderme:** En olası anlamı bulmak; dünya modeli, zihin modeli, dil modeli ve akustik model birlikte gerekir.

---

## 6. Doğal dil görevleri

Konuşma tanıma, metinden konuşmaya, makine çevirisi, bilgi çıkarma (metinden yapılandırılmış bilgi: şablonlar, kurallı ifadeler, olasılıksal modeller), bilgi erişimi (arama motorları, sorgu–belge benzerliği), soru yanıtlama. Bunların çoğu bugün derin öğrenmeyle yapılır (Bölüm 24).

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Görülmemiş bir n-gramın olasılığı sıfırdır." | Düzeltme olmadan öyle hesaplanır, ama yanlıştır; Laplace, geri çekilme, ara değerleme gerekir. |
| "Daha uzun n-gram her zaman daha iyidir." | Veri seyrekleşir; 4-gram eğitim metnini kopyalamaya başlar. |
| "Şaşkınlık ne kadar büyükse model o kadar iyi." | Tersine: Düşük şaşkınlık daha iyi model demektir. |
| "Dilbilgisi ya kabul eder ya reddeder." | PCFG her dizeye bir olasılık verir; E₀ hem fazla hem eksik üretir. |
| "CYK her dilbilgisiyle doğrudan çalışır." | Chomsky normal biçimi ister; üçlü ve tekli kurallar dönüştürülmelidir. |
| "PCFG edat öbeğinin doğru bağlanmasını bilir." | Bağlamdan bağımsız olasılıklar sözcüklere bakmaz; sözcükselleştirme gerekir. |
| "Bir cümlenin tek bir anlamı vardır." | Niceleme, gösterge sözcükler, mecaz ve belirsizlik birden çok anlam doğurur. |

## Kendini yokla

1. Sözcük torbası modeli neyi yok sayar? Hangi görevde yine de iyi çalışır?
2. Bigram modelinde P(okula | ayşe) nasıl hesaplanır? Görülmemiş bir bigrama ne olur?
3. Doğrusal ara değerleme ile geri çekilme arasındaki fark nedir?
4. Şaşkınlık nedir? Neden düşük olması iyidir?
5. "the wumpus is dead" cümlesinin E₀'daki olasılığını hesapla.
6. CYK'nin zaman ve uzay karmaşıklığı nedir? Neden Chomsky normal biçimi ister?
7. "I feel the wumpus near 1 3" neden belirsizdir? E₀ iki ağacı ayırt edebilir mi?
8. Ağaç bankasından bir PCFG nasıl öğrenilir?
9. "3 + (4 ÷ 2)"nin anlamı bileşimsel olarak nasıl hesaplanır?
10. Düz değişmece (metonymy) ile eğretileme (metaphor) arasındaki fark nedir?

## Kod rehberi

```bash
python ornekler/dil_modelleri.py   # naif Bayes, n-gram, Laplace, ara değerleme, şaşkınlık, HMM etiketleme
python ornekler/ayristirma.py      # E₀ PCFG, CYK, kitaptaki örnek, belirsizlik, ağaç bankasından PCFG
python ornekler/anlambilim.py      # aritmetik dilbilgisi (3 + (4 ÷ 2) = 5), λ-hesabıyla cümle anlamı
python cozumler/alistirma_kod.py   # A3, A5, A7, A8, A9
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| doğal dil işleme | natural language processing (NLP) | Dili anlama ve üretme |
| dil modeli | language model | Dizeler üzerinde olasılık dağılımı |
| sözcük torbası | bag of words | Sırasız sözcük sayımları |
| derlem | corpus | Metin topluluğu |
| n-gram | n-gram | n öğelik dizi |
| unigram / bigram / trigram | unigram / bigram / trigram | 1, 2, 3 öğelik |
| atlamalı n-gram | skip-gram | Ara öğeleri atlayan n-gram |
| bilinmeyen sözcük | out-of-vocabulary (OOV) word | Eğitimde görülmemiş sözcük |
| düzeltme | smoothing | Görülmemiş olaylara olasılık verme |
| geri çekilme | backoff | Daha kısa n-grama düşme |
| doğrusal ara değerleme | linear interpolation smoothing | n-gramların ağırlıklı ortalaması |
| şaşkınlık | perplexity | P^(−1/N) |
| sözcük türü etiketleme | part-of-speech (POS) tagging | Sözcüklere sözcük türü atama |
| dilbilgisi | grammar | Öbek yapısı kuralları |
| sözdizimsel kategori | syntactic category | NP, VP gibi |
| öbek yapısı | phrase structure | Hiyerarşik yapı |
| olasılıksal bağlamdan bağımsız dilbilgisi | probabilistic context-free grammar (PCFG) | Olasılıklı kurallar |
| fazla / eksik üretme | overgeneration / undergeneration | Yanlışı kabul / doğruyu reddetme |
| sözlük | lexicon | İzin verilen sözcükler |
| açık / kapalı sınıf | open / closed class | Büyüyen / sabit sözcük kümeleri |
| ayrıştırma | parsing | Öbek yapısını bulma |
| ayrıştırma ağacı | parse tree | Öbek yapısı ağacı |
| çizelge ayrıştırıcı | chart parser | Alt sonuçları saklayan ayrıştırıcı |
| CYK algoritması | CYK algorithm | O(n³m) dinamik programlama |
| Chomsky normal biçimi | Chomsky normal form | X → Y Z ve X → sözcük |
| bağımlılık dilbilgisi | dependency grammar | Sözcükler arası ilişkiler |
| ağaç bankası | treebank | Ayrıştırılmış cümle topluluğu |
| iç–dış algoritması | inside–outside algorithm | PCFG için EM |
| artırılmış dilbilgisi | augmented grammar | Bağımsız değişkenli kategoriler |
| sözcükselleştirilmiş PCFG | lexicalized PCFG | Başsözcüğe bağlı olasılıklar |
| bileşimsel anlambilim | compositional semantics | Anlam alt anlamlardan kurulur |
| niceleme | quantification | "her", "bir" gibi niceleyiciler |
| edimbilim | pragmatics | Bağlama bağlı anlam |
| gösterge sözcük | indexical | Duruma göre çözülen sözcük |
| söz edimi | speech act | Konuşmanın eylem türü |
| sözcüksel / sözdizimsel / anlamsal belirsizlik | lexical / syntactic / semantic ambiguity | Belirsizlik türleri |
| düz değişmece | metonymy | Bir şeyi ilişkili başka şeyle anmak |
| eğretileme | metaphor | Benzerliğe dayalı mecaz |
| belirsizlik giderme | disambiguation | En olası anlamı seçme |
| bilgi çıkarma / bilgi erişimi | information extraction / retrieval | Bilgi edinme / belge bulma |
| soru yanıtlama | question answering | Soruya doğrudan yanıt |
