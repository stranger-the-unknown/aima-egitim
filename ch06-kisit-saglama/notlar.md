# Bölüm 6 — Kısıt sağlama problemleri (CSP)

> **Kitapta:** AIMA 4. baskı, Bölüm 6 *"Constraint Satisfaction Problems"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 6.1 Defining CSPs | §1 Değişken–alan–kısıt, örnekler, kısıt türleri | `avustralya_csp.py`, `kriptaritmetik.py` |
| 6.2 Constraint Propagation | §2 Düğüm, yay, yol ve k-tutarlılık; AC-3; küresel kısıtlar; Sudoku | `kisit.py` → `ac3`, `sudoku_csp.py` |
| 6.3 Backtracking Search for CSPs | §3 Geri izleme, MRV, derece, LCV, ileri kontrol, MAC, akıllı geri dönüş | `kisit.py` → `geri_izleme`, `n_vezir_csp.py`, `harita_boyama_csp.py` |
| 6.4 Local Search for CSPs | §4 Min-çatışma | `min_catisma_vezir.py` |
| 6.5 The Structure of Problems | §5 Bağımsız alt problemler, ağaçlar, kesme kümesi, ağaç ayrışımı, değer simetrisi | `kisit.py` → `agac_coz`, `kesme_kumesi_coz` |

## Öğrenme hedefleri

1. Bir problemi değişkenler, alanlar ve kısıtlar olarak modellemek; kısıt grafını çizmek.
2. AC-3'ü elle ve kodla uygulamak; yay tutarlılığının neyi yakalayıp neyi kaçırdığını göstermek.
3. Geri izlemeyi MRV, derece, LCV sezgiselleri ve ileri kontrol/MAC çıkarımıyla hızlandırmak; etkilerini ölçmek.
4. Min-çatışma yerel aramasının neden büyük problemlerde bu kadar iyi çalıştığını açıklamak.
5. Kısıt grafının yapısından (ağaç, kesme kümesi) yararlanarak karmaşıklığı düşürmek.

---

## 1. CSP nedir?

Bir CSP üç bileşenden oluşur:

- **X** = {X₁, …, Xₙ}: değişkenler
- **D** = {D₁, …, Dₙ}: her değişkenin **alanı** (olası değerleri)
- **C**: **kısıtlar**. Her kısıt, bir **kapsam** (hangi değişkenler) ve bir **ilişkiden** (hangi değer birleşimlerine izin verildiği) oluşur.

Bir **atama**, bazı değişkenlere değer verir. Hiçbir kısıtı ihlal etmeyen atama **tutarlıdır**; her değişkene değer veren atama **tamdır**. **Çözüm**, tam ve tutarlı bir atamadır.

**Neden CSP?** Temsil **ayrışıktır** (Bölüm 2). Arama algoritması durumun içine bakabilir ve hangi değişkenin hangi kısıtı ihlal ettiğini görür. Avustralya'da SA = mavi seçilince beş komşusunun hiçbiri mavi olamaz. Kısıtları kullanmayan bir arama bu beş değişken için 3⁵ = 243 atamaya bakarken, kısıtlarla yalnızca 2⁵ = 32 atama kalır (%87 azalma).

### 1.1 Örnekler

- **Harita boyama** (`avustralya_csp.py`): WA, NT, Q, NSW, V, SA, T; alan {kırmızı, yeşil, mavi}; komşular farklı renk. **18 çözüm** vardır: anakara için 3! = 6 renk permütasyonu, bağımsız Tazmanya için 3 seçenek.
- **Türkiye'nin 7 bölgesi** (`harita_boyama_csp.py`): İl sınırlarına göre komşuluklar kurulunca harita **3 renkle boyanamaz**, 4 renk gerekir. Geri izleme bunu bütün olasılıkları tüketerek kanıtlar.
- **İş çizelgeleme:** Değişkenler görevlerin başlangıç zamanlarıdır. Kısıtlar önceliktir (T₁ + d₁ ≤ T₂: birinci iş bitmeden ikinci başlamaz) ve **ayrık kısıtlardır** (iki iş aynı aleti kullanıyorsa ya biri önce ya diğeri).
- **Kriptaritmetik** (`kriptaritmetik.py`): TWO + TWO = FOUR. Alldiff(F, T, U, W, R, O) ve sütun toplama kısıtları; C₁, C₂, C₃ elde değişkenleri. **7 çözüm** vardır (734 + 734 = 1468 gibi).

### 1.2 Değişken ve kısıt türleri

| Tür | Örnek |
|---|---|
| Sonlu ayrık alan | Harita boyama, 8-vezir |
| Sonsuz ayrık alan | Tamsayı zamanlar (kısıtlar tek tek sayılamaz, T₁ + d₁ ≤ T₂ gibi bir **kısıt dili** gerekir) |
| Sürekli alan | Doğrusal programlama (Bölüm 4) |
| **Tekli** kısıt | SA ≠ yeşil |
| **İkili** kısıt | SA ≠ NSW |
| **Küresel** kısıt | Alldiff(…) (herhangi sayıda değişken) |
| **Tercih** kısıtı | "Profesör sabah dersi vermeyi tercih etmez" (maliyet taşır → kısıtlı eniyileme, COP) |

Her sonlu kısıt, yardımcı değişkenler eklenerek ikili kısıtlara dönüştürülebilir (**ikili grafik** / *dual graph*). Ama Alldiff gibi küresel kısıtları doğrudan kullanmak hem daha okunaklı hem de özel algoritmalar sayesinde daha verimlidir.

---

## 2. Kısıt yayılımı: arama olmadan çıkarım

### 2.1 Tutarlılık düzeyleri

- **Düğüm tutarlılığı:** Tekli kısıtlar alanlardan elenir.
- **Yay tutarlılığı:** Xᵢ'nin her değeri için, (Xᵢ, Xⱼ) kısıtını sağlayan bir Xⱼ değeri vardır. Kısaca: her değerin bir "destekçisi" vardır.
- **Yol tutarlılığı:** Tutarlı her {Xᵢ = a, Xⱼ = b} ikilisi, üçüncü bir Xₘ'ye tutarlı bir değer verilerek genişletilebilir. Örnek: İki renkle boyanan üçgen, yay tutarlıdır ama yol tutarlı değildir. Yay tutarlılığı bunu fark etmez, yol tutarlılığı fark eder.
- **k-tutarlılık:** Herhangi k − 1 değişkenin tutarlı ataması, k'ıncı değişkene genişletilebilir. **Güçlü n-tutarlı** bir CSP geri izleme olmadan çözülür, ama bu düzeyi sağlamanın maliyeti üsteldir.

### 2.2 AC-3

```text
AC-3(csp):
    kuyruk ← tüm yaylar (Xᵢ, Xⱼ)
    kuyruk boş değilken:
        (Xᵢ, Xⱼ) ← kuyruktan çıkar
        DÜZELT(Xᵢ, Xⱼ) Xᵢ'den değer sildiyse:
            Xᵢ'nin alanı boşsa → tutarsız
            Xⱼ dışındaki her komşu Xₖ için (Xₖ, Xᵢ)'yi kuyruğa ekle
    → tutarlı
DÜZELT(Xᵢ, Xⱼ): Xⱼ'de hiçbir destekçisi olmayan Xᵢ değerlerini sil
```

Karmaşıklık: c ikili kısıt, d alan büyüklüğü için **O(c·d³)**. Her yay en fazla d kez kuyruğa girer, her DÜZELT O(d²) sürer.

### 2.3 Küresel kısıtlar

- **Alldiff:** m değişkenin toplam n farklı olası değeri varsa ve m > n ise tutarsızdır. Tek değerli değişkenleri atayıp değerlerini diğerlerinden silmek, sonra tekrar bakmak basit bir yayılım yöntemidir.
- **Kaynak kısıtları** ("en fazla N"): Alanlardaki en küçük değerlerin toplamı sınırı aşıyorsa tutarsızdır.
- **Sınır yayılımı:** Büyük tamsayı alanları küme yerine [alt, üst] aralığıyla tutulur. İki uçuşta toplam 420 yolcu ve kapasiteler [0,165] ile [0,385] ise, ilk uçuş en az 35, ikincisi en az 255 yolcu taşımak zorundadır.

### 2.4 Sudoku

81 değişken, alan {1..9}, 27 Alldiff (9 satır, 9 sütun, 9 kutu). `sudoku_csp.py`:

- **Kolay** bulmacada 49 boş kare var. AC-3 tek başına hepsini çözer, **arama gerekmez**.
- **Zor** bulmacada AC-3 aday sayısını 561'den 275'e indirir ama hiçbir kareyi kesinleştiremez. MRV + MAC ile arama 3273 atamada çözer.

İnsanların kullandığı "gizli üçlüler" gibi teknikler, daha güçlü tutarlılık biçimleridir.

---

## 3. CSP'ler için geri izleme araması

CSP'ler **değişmelidir** (*commutative*): Atamaların sırası sonucu değiştirmez. Bu yüzden her düğümde yalnızca **tek bir değişkenin** değerleri denenir. Böylece ağacın yaprak sayısı n!·dⁿ yerine dⁿ olur.

```text
GERİ-İZLE(atama):
    atama tamsa → döndür
    X ← DEĞİŞKEN-SEÇ(…)                       ← MRV / derece
    her x için DEĞERLERİ-SIRALA(X, …):         ← LCV
        x tutarlıysa:
            atama'ya X = x ekle
            çıkarımlar ← ÇIKARIM(X = x)        ← ileri kontrol / MAC
            çıkarım başarısız değilse: sonuç ← GERİ-İZLE(…); başarılıysa döndür
            X = x'i ve çıkarımları geri al
    → başarısız
```

### 3.1 Hangi değişken? Hangi değer?

- **MRV** (en az kalan değer, "önce başarısız ol"): Yasal değeri en az olan değişkeni seç. Çıkmaz dalları erkenden yakalar.
- **Derece sezgiseli:** Atanmamış değişkenlerle en çok kısıtı olanı seç. Başlangıçta ve MRV'de eşitlik bozmak için kullanılır. Avustralya'da SA'nın derecesi 5'tir, ilk o seçilir.
- **LCV** (en az kısıtlayan değer, "başarıyı en sona bırakma"): Komşuların alanlarından en az değer silen değeri önce dene. WA = kırmızı, NT = yeşil iken Q = mavi, SA'nın son değerini (mavi) de silerdi; LCV **kırmızıyı** önce dener.

> Neden değişkende "önce başarısız", değerde "en son başarısız"? Her değişken eninde sonunda atanacağı için zorunu erken çözmek geri dönüşleri azaltır. Değer içinse tek bir çözüm yeter; en umut verici değeri önce denemek mantıklıdır.

### 3.2 Arama ile çıkarımı iç içe yürütmek

- **İleri kontrol:** X = x atanınca, X'in atanmamış komşularının alanlarından x ile uyumsuz değerler silinir. Kitaptaki iz (`avustralya_csp.py` bunu birebir üretir):

| | WA | NT | Q | NSW | V | SA | T |
|---|---|---|---|---|---|---|---|
| Başlangıç | KYM | KYM | KYM | KYM | KYM | KYM | KYM |
| WA = kırmızı | K | YM | KYM | KYM | KYM | YM | KYM |
| Q = yeşil | K | M | Y | KM | KYM | M | KYM |
| V = mavi | K | M | Y | K | M | **∅** | KYM |

  V = mavi atanınca SA'nın alanı boşalır ve hemen geri dönülür.

- **İleri kontrolün kaçırdığı:** Q = yeşil satırında NT ve SA'nın ikisinin de tek değeri mavi kalmıştır, ama birbirlerine komşudurlar. İleri kontrol bu çelişkiyi görmez, çünkü yalnızca atanan değişkenin komşularına bakar.
- **MAC** (yay tutarlılığını koru): Atamadan sonra AC-3'ü, atanmamış komşuların yaylarıyla başlatır ve değişiklikleri zincirleme yayar. Yukarıdaki çelişkiyi **Q = yeşil anında** yakalar.

**Ölçüm** (`n_vezir_csp.py`, ilk çözüme kadar yapılan atama sayısı):

| n | Sıralı | + ileri kontrol | MRV + ileri kontrol | MRV + LCV + MAC |
|---|---|---|---|---|
| 8 | 113 | 88 | 75 | 14 |
| 16 | 10.052 | 7.560 | 44 | 128 |
| 20 | 199.635 | 145.151 | 145 | 20 |

### 3.3 Akıllı geri dönüş

Kronolojik geri izleme en son atanan değişkene döner, ama sorunun kaynağı çok daha önceki bir atama olabilir. **Çatışma kümesi**, bir değişkenin değerlerini dışlayan önceki atamaları tutar. **Geri atlama** (*backjumping*), çatışma kümesindeki en son değişkene doğrudan atlar. **Çatışma yönlendirmeli geri atlama**, çatışma kümelerini yukarı doğru birleştirir. **Kısıt öğrenme**, çelişkiye yol açan en küçük atama kümesini "iyi değil" (*no-good*) olarak kaydeder, böylece aynı çıkmaza bir daha girilmez. Modern SAT çözücülerin temelidir (Bölüm 7).

---

## 4. CSP'ler için yerel arama: min-çatışma

Tam bir atamayla başla. Her adımda çatışan bir değişken seç ve ona **en az çatışma** yaratan değeri ver.

- 8-vezir, kitaptaki örnekte iki adımda çözülür.
- **Büyüklükten bağımsızlık:** Açgözlü bir başlangıçla adım sayısı n'den neredeyse bağımsızdır. Kitap, bir milyon vezirin ortalama **~50 adımda** çözüldüğünü söyler. `min_catisma_vezir.py` n = 8'den 5000'e kadar ortalama 60–90 adım bulur. Rastgele başlangıçta ise adım sayısı n ile büyür. Çözümler uzayda yoğun dağıldığı için yerel arama bu kadar etkilidir.
- **Takılma:** Küçük tahtalarda algoritma, her çatışan değişkenin en iyi değerinin zaten mevcut değeri olduğu bir yerel minimumda sonsuza kadar dönebilir. Çareler: düzlük araması (eşit değerli hamlelere izin), **tabu araması** (son ziyaret edilen durumları yasakla), **kısıt ağırlıklandırma** (sık ihlal edilen kısıtların ağırlığını artır), ya da biraz rastgelelik. Kodumuz %5 olasılıkla rastgele bir satır seçer.
- **Gerçek kullanım:** Hubble Uzay Teleskobu'nun bir haftalık gözlem çizelgesinin hazırlanması üç haftadan yaklaşık 10 dakikaya indi.
- **Çevrimiçi onarım:** Çizelge bozulduğunda (ör. hava muhalefeti), sıfırdan aramak yerine mevcut çözümü onarmak idealdir.

---

## 5. Problemin yapısı

- **Bağımsız alt problemler:** Kısıt grafında bağlantısız parçalar (Tazmanya) ayrı ayrı çözülür. n değişkenli bir problem c'lik parçalara bölünürse iş dⁿ yerine (n/c)·d^c olur, yani üstelden doğrusala iner.
- **Ağaç yapılı CSP'ler:** Kısıt grafı bir ağaçsa **O(n·d²)** zamanda çözülür (`agac_coz`):
  1. Bir kök seç, düğümleri topolojik sıraya koy.
  2. Sondan başa doğru her (ebeveyn, çocuk) yayını tutarlı yap (**yönlü yay tutarlılığı**).
  3. Baştan sona her değişkene ebeveyniyle uyumlu bir değer ver; geri dönüş hiç gerekmez.
- **Döngü kesme kümesi:** Bazı değişkenler (S) atanınca kalan graf ağaç olur. Avustralya'da S = {SA}. S'nin her tutarlı ataması için kalan ağaç çözülür. Süre **O(d^c · (n − c)·d²)**; c küçükse çok hızlıdır. En küçük kesme kümesini bulmak NP-zordur, ama iyi yaklaşık yöntemler vardır.
- **Ağaç ayrışımı:** Graf, örtüşen alt problemlerden oluşan bir ağaca bölünür. Her alt problem tek bir "süper değişken" olur. En büyük alt problemin boyutu − 1'e **ağaç genişliği** (w) denir; süre O(n·d^(w+1))'dir.
- **Değer simetrisi:** d renkle her çözüm aslında d! çözümdür (renk isimlerini değiştir). **Simetri kırıcı kısıt** (ör. NT < SA < WA alfabetik sırası) arama uzayını d! kat küçültür.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Yay tutarlı ise çözüm vardır." | Hayır. İki renkli üçgen yay tutarlıdır ama çözümü yoktur. Yay tutarlılığı yereldir. |
| "İleri kontrol = MAC." | İleri kontrol yalnızca atanan değişkenin komşularına bakar. MAC değişiklikleri zincirleme yayar. |
| "MRV ve LCV aynı fikirdir." | Değişken seçiminde "önce başarısız ol", değer seçiminde "en son başarısız ol" ilkesi geçerlidir. |
| "Sezgiseller her örnekte işi azaltır." | Ortalamada azaltır. n = 16 vezirde MAC, MRV + ileri kontrolden daha çok atama yaptı. |
| "Min-çatışma her zaman çözer." | Yerel minimumlarda takılabilir; gürültü, tabu ya da yeniden başlatma gerekir. Çözüm olmadığını da kanıtlayamaz. |
| "Harita boyamada 3 renk hep yeter." | Türkiye'nin 7 bölgesi 3 renkle boyanamaz. Dört renk teoremi yalnızca 4 rengin **yeteceğini** söyler. |

## Kendini yokla

1. WA = kırmızı, Q = yeşil atamasından sonra AC-3 hangi alanları boşaltır?
2. Avustralya'da T'yi ilk atamak geri izlemeyi neden hiç zorlaştırmaz?
3. Kesme kümesi {SA} ile kalan Avustralya grafı neden ağaçtır? {NSW} de iş görür müydü?
4. Sudoku'da AC-3'ün hiçbir kareyi kesinleştiremediği bir bulmacada bile işe yaraması ne demektir?
5. Türkiye haritası için 3 rengin yetmediğini elle, zincirleme bir akıl yürütmeyle göster.

## Kod rehberi

```bash
python ornekler/kisit.py                    # kütüphane testi
python ornekler/avustralya_csp.py           # ileri kontrol izi, MAC, LCV, 18 çözüm, kesme kümesi
python ornekler/harita_boyama_csp.py        # Türkiye: 3 renk yetmez, 4 renk yeter
python ornekler/harita_boyama_csp.py --karsilastir
python ornekler/n_vezir_csp.py              # sezgisellerin etkisi (n = 4…20)
python ornekler/min_catisma_vezir.py        # min-çatışma: adım sayısı n'den bağımsız
python ornekler/sudoku_csp.py               # AC-3 kolay bulmacayı tek başına çözer
python ornekler/kriptaritmetik.py           # TWO + TWO = FOUR: 7 çözüm
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| kısıt sağlama problemi | constraint satisfaction problem (CSP) | Değişken, alan, kısıt |
| alan | domain | Değişkenin alabileceği değerler |
| kapsam / ilişki | scope / relation | Kısıtın değişkenleri / izin verilen birleşimler |
| tutarlı / tam atama | consistent / complete assignment | Kısıt ihlali yok / her değişken atanmış |
| kısıt grafı | constraint graph | Düğümler değişken, kenarlar kısıt |
| küresel kısıt | global constraint | Çok değişkenli kısıt (Alldiff) |
| tercih kısıtı | preference constraint | İhlali maliyetli ama yasak olmayan kısıt |
| yay tutarlılığı | arc consistency | Her değerin destekçisi var |
| yol tutarlılığı | path consistency | Her ikili üçüncü değişkene genişleyebilir |
| sınır yayılımı | bounds propagation | Aralık uçlarını daraltma |
| en az kalan değer | minimum-remaining-values (MRV) | En kısıtlı değişken önce |
| derece sezgiseli | degree heuristic | En çok kısıtı olan değişken önce |
| en az kısıtlayan değer | least-constraining-value (LCV) | Komşulara en çok seçenek bırakan değer önce |
| ileri kontrol | forward checking | Atanan değişkenin komşularını buda |
| yay tutarlılığını koruma | maintaining arc consistency (MAC) | Her atamadan sonra AC-3 |
| çatışma kümesi | conflict set | Bir değişkenin değerlerini dışlayan atamalar |
| geri atlama | backjumping | Çatışmanın kaynağına doğrudan dönme |
| kısıt öğrenme | constraint learning (no-good) | Çelişkili atama kümelerini kaydetme |
| min-çatışma | min-conflicts | Çatışmayı en aza indiren yerel arama |
| tabu araması | tabu search | Yakın geçmişteki durumları yasaklama |
| döngü kesme kümesi | cycle cutset | Çıkarılınca grafı ağaç yapan değişkenler |
| ağaç ayrışımı / ağaç genişliği | tree decomposition / tree width | Grafı alt problemlerden oluşan ağaca bölme |
| değer simetrisi | value symmetry | Değer isimlerinin permütasyonu |
