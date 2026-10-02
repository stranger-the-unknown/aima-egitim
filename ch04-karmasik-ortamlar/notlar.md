# Bölüm 4 — Karmaşık ortamlarda arama

> **Kitapta:** AIMA 4. baskı, Bölüm 4 *"Search in Complex Environments"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 4.1 Local Search and Optimization Problems | §1 Tepe tırmanma, tavlama, ışın araması, evrimsel algoritmalar | `tepe_tirmanma_n_queens.py`, `simule_tavlama_demo.py`, `genetik_8vezir.py` |
| 4.2 Local Search in Continuous Spaces | §2 Gradyan, deneysel gradyan, Newton | `havalimani_gradyan.py` |
| 4.3 Search with Nondeterministic Actions | §3 Koşullu planlar, AND-OR araması | `and_or_supurge.py` |
| 4.4 Search in Partially Observable Environments | §4 İnanç durumları, algısız arama, tahmin–güncelleme | `inanc_durumu_supurge.py` |
| 4.5 Online Search Agents and Unknown Environments | §5 Çevrimiçi arama, rekabet oranı, LRTA* | `lrta_yildiz.py` |

## Öğrenme hedefleri

1. Yol değil **durum** arandığında yerel aramanın neden uygun olduğunu açıklamak; tepe tırmanmanın tuzaklarını ve çarelerini sayısal olarak göstermek.
2. Tavlamayı, ışın aramasını ve genetik algoritmayı birbirinden ayırt etmek.
3. Sürekli uzaylarda gradyan ve Newton adımını uygulamak.
4. Deterministik olmayan eylemler için koşullu plan (AND-OR araması) üretmek.
5. İnanç durumlarıyla algısız ve kısmi gözlemli problemleri çözmek.
6. Çevrimiçi aramanın zorluklarını (çıkmazlar, keşif) ve LRTA*'ın öğrenme mantığını anlatmak.

---

## 1. Yerel arama ve eniyileme

Bölüm 3'te **yol** aradık. Birçok problemde ise yolun önemi yoktur, yalnızca iyi bir **son durum** isteriz: 8 veziri çatışmasız yerleştirmek, bir ders programı, bir çip yerleşimi.

**Yerel arama** tek bir mevcut durumu tutar ve komşularına geçer. Yol saklamadığı için bellek kullanımı sabittir ve çok büyük (hatta sürekli) uzaylarda çalışır. Buna karşılık tam değildir ve optimal olduğu garanti edilmez.

### 1.1 Durum uzayı manzarası

Her durumun bir "yüksekliği" (amaç fonksiyonu değeri) varmış gibi düşün. Amaç ya **en yüksek tepe** (global maksimum) ya da **en derin çukur** (global minimum) olabilir.

- **Yerel maksimum:** Çevresindeki her komşudan yüksek ama global maksimum değil.
- **Sırt** (*ridge*): Bir dizi yerel maksimum. Tek adımlık hareketlerle üzerinde ilerlemek zordur.
- **Düzlük** (*plateau*): Komşuların hepsi aynı değerde. Ya çıkışsız **düz yerel maksimum** ya da ilerlenebilen bir **omuz** (*shoulder*) olabilir.

### 1.2 Tepe tırmanma

"Her adımda en iyi komşuya git; daha iyi komşu yoksa dur." Buna *açgözlü yerel arama* da denir.

**8-vezir deneyi** (`tepe_tirmanma_n_queens.py --deney 2000`). Durum: her sütunda bir vezir, 8⁸ ≈ 17 milyon durum. h: tehdit eden çift sayısı.

| Varyant | Başarı | Adım (başarı / takılma) | Kitap |
|---|---|---|---|
| En dik tırmanış | %15 | 4,1 / 3,1 | %14 · 4 / 3 |
| + en fazla 100 art arda **yana hamle** | %95 | 19,5 / 63,6 | %94 · 21 / 64 |

- Yana hamle, düzlüğün bir omuz olabileceği umuduyla eşit değerli bir komşuya geçmektir. Sonsuz döngüyü önlemek için sınır konur.
- **Rastgele yeniden başlatma:** Başarı olasılığı p ise beklenen deneme sayısı **1/p**'dir. 8-vezir için yaklaşık 7 deneme ve toplam ~22 adım gerekir. Bu, "her zaman sonunda çözer" demektir.
- **Stokastik tepe tırmanma:** İyileştiren komşulardan rastgele birini seçer. **İlk seçim** varyantı, komşuları rastgele sırayla üretip ilk iyileştireni alır. Komşu sayısı binlerce olduğunda işe yarar.

> **Manzara her şeydir:** Az sayıda yerel maksimum varsa yeniden başlatmalı tepe tırmanma çok hızlıdır. NP-zor problemlerin manzarası ise genellikle üstel sayıda yerel maksimumla doludur.

### 1.3 Benzetilmiş tavlama

Tepe tırmanma hiç "yokuş aşağı" gitmez. Bu yüzden eksiktir. Tamamen rastgele yürüyüş ise tamdır ama verimsizdir. **Benzetilmiş tavlama** (*simulated annealing*) ikisini birleştirir:

1. Rastgele bir komşu seç.
2. Daha iyiyse kabul et.
3. Daha kötüyse **e^(ΔE/T)** olasılıkla kabul et (ΔE < 0 kötüleşme miktarı, T sıcaklık).
4. T'yi bir **soğuma çizelgesine** göre yavaşça düşür.

Başta (T büyük) kötü adımlar sık kabul edilir ve arama geniş bir alanı dolaşır. Sona doğru (T küçük) arama tepe tırmanmaya dönüşür. T yeterince yavaş düşürülürse global optimum 1'e yaklaşan olasılıkla bulunur. `simule_tavlama_demo.py` 8 şehirli TSP'de kaba kuvvetle bulunan optimumu (17,699) buluyor. 30 şehirde tavlama ortalamada yalnızca iyileşme kabul eden tepe tırmanmayı geçiyor.

### 1.4 Yerel ışın araması

k durum birden tutulur. Her adımda **tüm** k durumun bütün komşuları üretilir ve bunların en iyi k tanesi seçilir. k bağımsız yeniden başlatmadan farkı, **bilgi paylaşımıdır**: İyi bölgeyi bulan durumlar diğerlerini oraya "çağırır". Tehlikesi çeşitlilik kaybıdır; hepsi aynı tepeye toplanabilir. **Stokastik ışın araması**, komşuları değerleriyle orantılı olasılıkla seçerek bu sorunu hafifletir.

### 1.5 Evrimsel algoritmalar ve genetik algoritma

Stokastik ışın aramasının doğal seçilimden esinlenen hâlidir. Bir **popülasyon** (birey = durum) tutulur ve daha uygun bireylerin çocuklar üretmesi sağlanır.

Tasarım kararları: popülasyon büyüklüğü, **temsil** (GA'da sonlu alfabeli dizgi, evrim stratejilerinde gerçel sayılar, genetik programlamada program), **karışım sayısı** ρ (bir çocuğun kaç ebeveyni var), **seçim** (uygunlukla orantılı, turnuva…), **çaprazlama**, **mutasyon oranı** ve yeni kuşağın oluşumu (**elitizm**: en iyiler aynen aktarılır; **ayıklama**: eşiğin altındakiler atılır).

`genetik_8vezir.py` kitaptaki örneği birebir doğrular:

| Birey | Uygunluk (saldırmayan çift) | Seçilme olasılığı |
|---|---|---|
| 24748552 | 24 | %31 |
| 32752411 | 23 | %29 |
| 24415124 | 20 | %26 |
| 32543213 | 11 | %14 |

Çaprazlama: `327|52411` × `247|48552` → `32748552`.

**Çaprazlama ne zaman işe yarar?** Dizgide birbirinden bağımsız olarak iyi olabilen **yapı taşları** (*schema*) varsa. Örneğin 8-vezirde ilk üç vezirin çatışmasız bir yerleşimi, ikinci bir ebeveynin son beş veziriyle birleşebilir. Rastgele sıralanmış bir temsilde çaprazlama bu faydayı sağlamaz. Pratikte 8-vezir için yeniden başlatmalı tepe tırmanma GA'dan çok daha hızlıdır; GA'nın gücü daha karmaşık, modüler problemlerde ortaya çıkar.

---

## 2. Sürekli uzaylarda yerel arama

Kitaptaki örneğin Türkiye uyarlaması (`havalimani_gradyan.py`): 3 havalimanını, 20 il merkezinin **en yakın** havalimanına uzaklığının karesi toplamı en küçük olacak şekilde yerleştir. Durum 6 boyutludur: (x₁, y₁, x₂, y₂, x₃, y₃).

f(x) = Σᵢ Σ_{c ∈ Cᵢ} (xᵢ − x_c)² + (yᵢ − y_c)², burada Cᵢ, i. havalimanına en yakın illerdir.

- **Ayrıklaştırma:** Koordinatları ±δ adımlarla değiştir. 6 değişken × 2 yön = 12 komşu, ardından bildiğimiz tepe tırmanma. Bu, **deneysel gradyan** yöntemidir; türev bilmeyi gerektirmez.
- **Gradyan inişi:** ∂f/∂xᵢ = 2 Σ_{c∈Cᵢ} (xᵢ − x_c). Güncelleme x ← x − α∇f. α **adım büyüklüğüdür**: çok küçükse yavaş ilerler, çok büyükse minimumu aşar. **Doğru arama** (*line search*) α'yı her adımda ayarlar.
- **Newton–Raphson:** x ← x − H⁻¹∇f (H = Hessian, ikinci türevler matrisi). Bu problemde H = 2|Cᵢ|·I olduğundan Newton adımı her havalimanını doğrudan kümesinin **ağırlık merkezine** taşır. Bu tam olarak **k-ortalamalar** algoritmasıdır (Bölüm 19–20). Demo'da 2 adımda yakınsıyor.
- **Uyarı:** Gradyan yalnızca **yerel olarak** doğrudur, çünkü havalimanı hareket edince Cᵢ kümeleri değişir. Farklı başlangıçlar farklı yerel minimumlara gider (demoda 934 ile 1.080 bin km² arası).

**Kısıtlı eniyileme:** Çözümün bazı koşulları sağlaması gerekir (ör. havalimanı denizde olamaz). En önemli özel durum **doğrusal programlamadır**: kısıtlar doğrusal eşitsizlikler, amaç doğrusal. Polinom zamanda çözülür. Daha geneli **dışbükey eniyilemedir**: Dışbükey problemlerde yerel minimum aynı zamanda globaldir.

---

## 3. Deterministik olmayan eylemler

Eylemin sonucu tek bir durum değil, **olası durumlar kümesidir**: SONUÇLAR(s, a). Çözüm artık bir eylem dizisi değil, **koşullu plandır**: "eğer … ise …".

**Kararsız süpürge dünyası:** Kirli karede süpürmek bazen yandaki kareyi de temizler, temiz karede süpürmek bazen kir döker. Kitaptaki numaralandırmayla (7 ve 8 hedef):

- SONUÇLAR(1, Süpür) = {5, 7}
- Plan: **[Süpür, eğer durum = 5 ise [Sağ, Süpür] değilse []]**

### AND-OR arama ağacı

- **VEYA düğümleri:** Ajan seçer. Eylemlerden **birinin** işe yaraması yeter.
- **VE düğümleri:** Ortam seçer. Olası **her** sonuç için bir alt plan gerekir.

```text
VEYA-ARA(s, yol):
    s hedefse → boş plan
    s yolda varsa → başarısız (döngü)
    her eylem a için:
        plan ← VE-ARA(SONUÇLAR(s, a), [s] + yol)
        plan başarısız değilse → [a] + plan
    → başarısız
VE-ARA(durumlar, yol):
    her sᵢ için planᵢ ← VEYA-ARA(sᵢ, yol);  biri başarısızsa → başarısız
    → [eğer s₁ ise plan₁ değilse eğer s₂ ise plan₂ …]
```

`and_or_supurge.py` bu algoritmayı uygular ve kitaptaki planı bulur. Plan, ortam hangi sonucu seçerse seçsin hedefe ulaşır.

**Döngüsel çözümler:** Eylem *bazen* başarısız oluyorsa (kaygan zemin: "Sağ" bazen yerinde bırakır), hiçbir döngüsüz plan garanti vermez. Çözüm "başarana kadar tekrar dene" türünden bir döngüdür. Böyle bir planın kabul edilebilmesi için her yaprağın bir hedef olması ve her noktadan bir hedefe ulaşılabilmesi gerekir. Bu da eylemin eninde sonunda başarılı olacağı varsayımına dayanır.

---

## 4. Kısmi gözlemlenebilir ortamlar

Ajan hangi durumda olduğunu tam bilmiyorsa, **inanç durumu** (*belief state*) ile düşünür: "şu an olabileceğim fiziksel durumların kümesi".

### 4.1 Algısız (sensorless, conformant) problemler

Hiçbir algı yok. Yine de çözülebilir. `inanc_durumu_supurge.py` kitaptaki sonucu üretir:

| Eylem | İnanç |
|---|---|
| (başlangıç) | {1, 2, 3, 4, 5, 6, 7, 8} |
| Sağ | {2, 4, 6, 8} |
| Süpür | {4, 8} |
| Sol | {3, 7} |
| Süpür | **{7}** |

Ajan hiçbir şey görmeden dünyayı durum 7'ye **zorlar**. Arama, inanç durumları uzayında yapılır: N fiziksel durum için 2^N inanç durumu olabilir, ama erişilebilir olanlar çok daha azdır.

**Budama:** Bir inanç durumu için çalışan plan, onun **her alt kümesi** için de çalışır (daha az olasılık = daha kolay problem). Bu yüzden:
- Aramada, daha önce ulaşılmış bir inancın **üst kümesine** varılırsa o düğüm atılabilir. Örneğin {5, 7}'ye zaten ulaşıldıysa {1, 3, 5, 7}'yi çözmeye çalışmak gereksizdir.
- Tersine, bir üst küme çözüldüyse alt kümeleri de çözülmüş olur.

### 4.2 Kısmi algılar: tahmin ve güncelleme

Algı fonksiyonu ALGI(s) varsa, bir eylemden sonra inanç iki adımda güncellenir:

1. **TAHMİN:** b̂ = ∪_{s ∈ b} SONUÇ(s, a)
2. **GÜNCELLE:** b' = {s ∈ b̂ : ALGI(s) = gözlenen algı}

Yerel algılı süpürge: İlk algı [Sol, Kirli] → {1, 3}. Sağ → {2, 4}. Algı [Sağ, Kirli] → {2}, algı [Sağ, Temiz] → {4}.

Çözüm, inanç durumları üzerinde **AND-OR araması**dır: VE düğümleri artık "hangi algıyı alacağım?" belirsizliğini temsil eder. Aynı TAHMİN–GÜNCELLE döngüsü, olasılıklarla yapıldığında **filtreleme** (Bölüm 14) ve robotlarda **konum belirleme** (Bölüm 26) adını alır.

---

## 5. Çevrimiçi arama ve bilinmeyen ortamlar

**Çevrimdışı** ajan önce tam planı hesaplar, sonra uygular. **Çevrimiçi** ajan ise hesaplama ile eylemi iç içe yürütür. Bu iki durumda gereklidir:
- Ortam **bilinmiyordur**: SONUÇ(s, a)'yı öğrenmenin tek yolu a'yı s'de denemektir (keşif problemi).
- Ortam **dinamik** veya yarı dinamiktir ve uzun düşünmek pahalıdır.

**Rekabet oranı:** Ajanın gerçek yol maliyeti / ortamı baştan bilseydi ödeyeceği maliyet. Kötü haber: **Geri dönüşsüz eylemler** (çıkmazlar) varsa hiçbir algoritma bu oranı sınırlayamaz. Bir "düşman" ortam her zaman ajanın seçtiği yolu çıkmaza çevirebilir. Bu yüzden genellikle **güvenle keşfedilebilir** ortamlar varsayılır: Her erişilebilir durumdan bir hedefe ulaşılabilir.

- **Çevrimiçi DFS:** Geri izleme için ajanın fiziksel olarak **geri dönmesi** gerekir. Eylemler geri alınabilir olmalıdır.
- **Rastgele yürüyüş:** Sonlu ve güvenle keşfedilebilir uzaylarda eninde sonunda hedefi bulur, ama üstel sürebilir.

### LRTA* (öğrenen gerçek zamanlı A*)

Tepe tırmanmaya rastgelelik yerine **bellek** eklenir. Her ziyaret edilen durum için bir tahmin H(s) tutulur (başta h(s)):

- Görünüşte en iyi eylemi seç: argmin_a [c(s, a, s') + H(s')].
- Ayrıldığın durumun tahminini güncelle: H(s) ← min_a [c(s, a, s') + H(s')].
- **Belirsizlik karşısında iyimserlik:** Denenmemiş bir eylemin doğrudan hedefe h(s) maliyetle götürdüğü varsayılır. Bu, keşfi teşvik eder.

`lrta_yildiz.py` kitaptaki tek boyutlu örneği adım adım üretir: H = 8 9 **2** 2 4 3 iken ajan düz bir yerel minimumdadır. İleri geri giderek tahminleri 3 → 5 ve 4 → 5'e yükseltir, minimumu "doldurur" ve sağa kaçar. İkinci bölümde haritası bilinmeyen bir labirentte ilk deneme 154 adım sürer. 11. denemeden itibaren optimal olan 25 adımlık yol izlenir.

Sonlu ve güvenle keşfedilebilir her ortamda LRTA* hedefi bulur. En kötü durumda n durumlu bir uzayı O(n²) adımda keşfeder. Bu "tahmin güncelle" kuralları, Bölüm 22'deki pekiştirmeli öğrenmenin öncülüdür.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Tepe tırmanma optimal çözümü bulur." | Yerel maksimuma, sırta veya düzlüğe takılır. 8-vezirde yalnızca %14 başarılı. |
| "Tavlama rastgele arama gibidir." | Başta öyledir, ama soğudukça tepe tırmanmaya dönüşür. Anahtar, soğuma çizelgesidir. |
| "k ışınlı arama = k bağımsız yeniden başlatma." | Işınlar bilgi paylaşır: bir sonraki k durum *tüm* ışınların komşuları arasından seçilir. |
| "Genetik algoritma her problemde iyidir." | Çaprazlama, temsilde anlamlı yapı taşları varsa işe yarar. |
| "Gradyan bir kez hesaplanır." | Havalimanı örneğinde Cᵢ kümeleri değiştikçe gradyanın formülü de değişir. Gradyan yerel olarak doğrudur. |
| "Deterministik olmayan problemin çözümü bir eylem dizisidir." | Çözüm koşullu bir plandır (bir ağaç, hatta döngülü bir graf). |
| "Algı yoksa problem çözülemez." | Algısız süpürge dört adımda hedefe zorlanır. |
| "Çevrimiçi arama her ortamda başarılı olur." | Geri dönüşsüz eylemler varsa hiçbir algoritmanın rekabet oranı sınırlı değildir. |

## Kendini yokla

1. 8-vezirde yana hamle izni başarıyı neden bu kadar artırıyor? Bedeli nedir?
2. Tavlamada T → 0 ve T → ∞ limitlerinde algoritma neye dönüşür?
3. Newton adımı havalimanı probleminde neden kümenin ağırlık merkezidir?
4. AND-OR aramasında bir döngü neden başarısızlık sayılır? Bu, döngüsel çözümleri nasıl dışlar?
5. {1, 3} inancındaki bir ajan Süpür yaparsa yeni inancı ne olur (deterministik dünyada)?
6. LRTA*'ta H neden hiçbir zaman gerçek maliyetin üstüne çıkmaz (h kabul edilebilirse)?

## Kod rehberi

```bash
python ornekler/tepe_tirmanma_n_queens.py --deney 2000   # %14 / %94 deneyi
python ornekler/simule_tavlama_demo.py                   # TSP: tavlama ve tepe tırmanma
python ornekler/genetik_8vezir.py                        # kitaptaki uygunluk değerleri + GA
python ornekler/havalimani_gradyan.py                    # sürekli uzay: gradyan ve Newton
python ornekler/and_or_supurge.py                        # koşullu plan
python ornekler/inanc_durumu_supurge.py                  # algısız ve yerel algılı süpürge
python ornekler/lrta_yildiz.py                           # LRTA*: kitaptaki şekil + labirent
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| yerel arama | local search | Tek bir mevcut durumu iyileştirerek arama |
| amaç fonksiyonu | objective function | En iyilenmek istenen değer |
| durum uzayı manzarası | state-space landscape | Durumların "yükseklik" haritası |
| yerel maksimum / sırt / düzlük / omuz | local maximum / ridge / plateau / shoulder | Tepe tırmanmanın tuzakları |
| en dik tırmanış | steepest ascent | En iyi komşuya geçen tepe tırmanma |
| yana hamle | sideways move | Eşit değerli komşuya geçmek |
| rastgele yeniden başlatma | random restart | Takılınca rastgele yeni başlangıç |
| benzetilmiş tavlama | simulated annealing | Kötü adımları azalan olasılıkla kabul etme |
| soğuma çizelgesi | schedule | Sıcaklığın zamanla nasıl düştüğü |
| yerel ışın araması | local beam search | k durumu birlikte ilerletme |
| genetik algoritma | genetic algorithm | Popülasyon, seçim, çaprazlama, mutasyon |
| uygunluk fonksiyonu | fitness function | Bireyin ne kadar iyi olduğu |
| elitizm / ayıklama | elitism / culling | En iyileri aktarma / kötüleri atma |
| deneysel gradyan | empirical gradient | Türevsiz, ölçerek eğim bulma |
| adım büyüklüğü | step size (α) | Gradyan güncellemesinin katsayısı |
| doğrusal programlama | linear programming | Doğrusal amaç ve kısıtlarla eniyileme |
| dışbükey eniyileme | convex optimization | Yerel minimumu global olan problemler |
| koşullu plan | conditional plan | "Eğer … ise …" dallı plan |
| AND-OR arama ağacı | AND-OR search tree | Ajan seçimi (VEYA) + ortam seçimi (VE) |
| inanç durumu | belief state | Olası fiziksel durumlar kümesi |
| algısız problem | sensorless (conformant) problem | Hiç algı olmadan çözülen problem |
| tahmin / güncelleme | prediction / update | İnanç güncellemenin iki adımı |
| çevrimiçi arama | online search | Hesaplama ile eylemi iç içe yürütme |
| rekabet oranı | competitive ratio | Çevrimiçi maliyet / en iyi çevrimdışı maliyet |
| güvenle keşfedilebilir | safely explorable | Her durumdan hedefe ulaşılabilen ortam |
| belirsizlik karşısında iyimserlik | optimism under uncertainty | Bilinmeyeni iyi varsayarak keşfi teşvik |
