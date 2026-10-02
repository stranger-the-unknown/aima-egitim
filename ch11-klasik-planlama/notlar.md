# Bölüm 11 — Otomatik planlama

> **Kitapta:** AIMA 4. baskı, Bölüm 11 *"Automated Planning"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 11.1 Definition of Classical Planning | §1 PDDL: durumlar, eylem şemaları, üç örnek alan | `planlama.py`, `kitap_problemleri.py`, `aksiyon_semasi.py` |
| 11.2 Algorithms for Classical Planning | §2 İleri ve geri arama, SAT, planlama grafiği, kısmi sıralı planlama | `kitap_problemleri.py`, `strips_bloklar.py` |
| 11.3 Heuristics for Planning | §3 Önkoşulları / silme listelerini yok sayma, soyutlama, ayrıştırma, alana bağımsız budama | `planlama.py` → `h_max`, `h_add`, `h_seviye_toplami` |
| 11.4 Hierarchical Planning | §4 Üst düzey eylemler, inceltmeler, meleksi anlam | `hiyerarsik_plan.py` |
| 11.5 Planning and Acting in Nondeterministic Domains | §5 Algısız, koşullu ve çevrimiçi planlama, izleme | — |
| 11.6 Time, Schedules, and Resources | §6 İş atölyesi çizelgeleme, kritik yol, kaynaklar | `kritik_yol.py` |
| 11.7 Analysis of Planning Approaches | §7 Karmaşıklık ve yaklaşımların karşılaştırması | — |

## Öğrenme hedefleri

1. Bir planlama problemini PDDL ile tanımlamak: başlangıç, hedef, eylem şemaları.
2. İleri ve geri aramayı, planlama grafiğini ve SAT tabanlı planlamayı karşılaştırmak.
3. Gevşetilmiş problemlerden alana bağımsız sezgiseller türetmek (h_max, h_add, seviye toplamı).
4. Hiyerarşik planlamanın neden büyük problemlerde işe yaradığını açıklamak.
5. Kritik yol yöntemiyle çizelge hesaplamak ve kaynak kısıtlarının etkisini göstermek.

---

## 1. Klasik planlama ve PDDL

**Klasik planlama:** Ayrık, deterministik, statik, tam gözlemlenebilir bir ortamda hedefe ulaşan bir eylem dizisi bulmak. Bölüm 3'teki aramadan farkı **ayrışık temsildir**: Durum, doğru olan temel atomların (akışkanların) kümesidir. Olmayan atomlar yanlıştır (veritabanı anlamı).

**Eylem şeması** (PDDL):

```text
Action(Fly(p, from, to),
   PRECOND: At(p, from) ∧ Plane(p) ∧ Airport(from) ∧ Airport(to)
   EFFECT:  ¬At(p, from) ∧ At(p, to))
```

- a eylemi s'de **uygulanabilir**, ancak ve ancak önkoşulları s'de doğruysa.
- **SONUÇ(s, a) = (s − SİL(a)) ∪ EKLE(a).** Etkinin olumsuz literalleri **silme listesini**, olumluları **ekleme listesini** oluşturur.
- Etkide adı geçmeyen atomlar olduğu gibi kalır. Bu, çerçeve problemini (Bölüm 7) kendiliğinden çözer.

### 1.1 Kitaptaki üç alan (`kitap_problemleri.py`)

| Alan | Başlangıç / hedef | Kitaptaki plan |
|---|---|---|
| **Hava kargo** | C1 SFO'da, C2 JFK'de → C1 JFK'ye, C2 SFO'ya | Load(C1,P1,SFO), Fly(P1,SFO,JFK), Unload(C1,P1,JFK), Load(C2,P2,JFK), Fly(P2,JFK,SFO), Unload(C2,P2,SFO): **6 adım** |
| **Yedek lastik** | Patlak lastik aksta, yedek bagajda → yedek aksta | Remove(Flat,Axle), Remove(Spare,Trunk), PutOn(Spare,Axle): **3 adım** |
| **Bloklar dünyası** | C, A'nın üstünde → A B'nin, B C'nin üstünde | MoveToTable(C,A), Move(B,Table,C), Move(A,Table,B): **3 adım** |

Kodumuz üç planı da bulur. Hava kargoda BFS aynı 6 eylemi eşdeğer bir sırayla bulur, çünkü iki uçağın işleri birbirinden bağımsızdır. Bazı sezgisellerle A* başka bir 6 adımlık plan da bulabilir: P1, C1'i JFK'ye götürür ve C2'yi alıp geri döner. İkisi de optimaldir.

**İnce noktalar:**
- Hava kargoda, uçağa yüklenen kargo artık hiçbir yerde "At" değildir, yalnızca "In" dir. PDDL'de "uçaktaki her şey uçakla gider" gibi bir niceleyici olmadığı için bu yol seçilir.
- Yedek lastikte PutOn'un önkoşulunda **negatif** literaller var (¬At(Flat, Axle)). LeaveOvernight eyleminin önkoşulu yoktur ama bütün lastikleri siler.
- Bloklar dünyasında masayı ayrı ele almak gerekir: Masa her zaman "Clear"dır. Bu yüzden MoveToTable ayrı bir şemadır.

---

## 2. Klasik planlama algoritmaları

### 2.1 İleri (progression) arama

Başlangıçtan uygulanabilir eylemlerle ileri git. Sorun: **dallanma**. Kitaptaki hesaba göre 10 havalimanı, her birinde 5 uçak ve 20 kargo olan bir hava kargo probleminde durum başına yaklaşık 2000 eylem vardır. 41 adımlık çözümün derinliğine kadar ağaçta ~2000⁴¹ düğüm olur. İyi bir **alana bağımsız sezgisel** olmadan umutsuzdur.

### 2.2 Geri (regression) arama

Hedeften geri git. Yalnızca **ilgili** eylemler dikkate alınır: hedefin bir atomunu ekleyen ve hiçbir hedef atomunu silmeyen eylemler. Gerileme:

g' = (g − EKLE(a)) ∪ ÖN(a)

Yedek lastikte hedef At(Spare, Axle) için tek ilgili eylem PutOn(Spare, Axle)'dır. Gerilemiş hedef ise Tire(Spare) ∧ At(Spare, Ground) ∧ ¬At(Flat, Axle) ∧ ¬At(Spare, Axle) olur (`kitap_problemleri.py`). Geri arama, **kısmen belirlenmiş durum kümeleri** üzerinde çalışır ve değişkenli (yükseltilmiş) eylemler kullanabilir. Dallanması genelde küçüktür, ama iyi sezgisel bulmak zordur. Bu yüzden pratikte ileri arama daha yaygındır.

### 2.3 Diğer yaklaşımlar

- **SAT olarak planlama (SATPlan):** Bölüm 7'deki fikir. PDDL problemi önermesel mantığa çevrilir: Eylemler her zaman adımı için temellendirilir (Fly_P1_SFO_JFK¹ gibi), **eylem dışlama** aksiyomları (aynı anda iki eylem yok), **önkoşul** aksiyomları (eylem yapıldıysa önkoşulları doğruydu), başlangıç durumu (bahsedilmeyen atomlar yanlış), **ardıl durum** aksiyomları ve T anındaki hedef eklenir. T = 1, 2, … için SAT çözücü çağrılır. Çeviri PDDL'den çok daha büyüktür, ama modern SAT çözücülerin hızı bunu çoğu zaman telafi eder.
- **Planlama grafiği (Graphplan):** Kitap bu yöntemi yalnızca kısaca anar. Seviye seviye büyüyen bir yapıdır: S₀ (başlangıç atomları), A₀ (uygulanabilir eylemler), S₁ (onların olası etkileri)… Hangi eylem ve atomların birbirini **dışladığını** (mutex) da kaydeder. Bu repodaki `planlama_grafigi_seviyeleri`, dışlamaları atlayan basit bir hâlidir: Yalnızca her atomun ilk göründüğü seviyeyi hesaplar ve sezgisel olarak kullanılır (§3).
- **Durum hesabı (situation calculus):** Planlamayı birinci dereceden mantıkla ifade eder. Kuramsal olarak önemlidir ama pratikte önermesel yöntemler kadar etkili olmamıştır.
- **Kısmi sıralı planlama:** Planı bir dizi değil, bir **grafik** olarak tutar: Yalnızca gerekli sıralama kısıtları ve hangi eylemin hangi önkoşulu sağladığı kaydedilir. Hava kargodaki iki uçağın işleri birbirine göre sıralanmak zorunda kalmaz. 1980'ler ve 90'larda en iyi yöntem sayılırdı. Bugün ileri arama ve SAT daha hızlıdır, ama insanların planı okuyup denetlemesi gereken alanlarda (uzay görevleri, operasyon çizelgeleme) hâlâ kullanılır.

### 2.4 Sussman anomalisi: alt hedefler bağımsız değil

Bloklar problemi iki alt hedeften oluşur: On(A, B) ve On(B, C). `kitap_problemleri.py`, bunları **sırayla ve birbirinden habersiz** çözmeyi dener:
- Önce On(A, B): C'yi masaya indir, A'yı B'ye koy. Ama şimdi B'yi C'nin üstüne koymak için A'yı indirmek gerekir. İkinci alt hedef birinciyi bozar.
- Önce On(B, C): B'yi C'nin üstüne koy. Ama A hâlâ C'nin altındadır! A'yı almak için B'yi ve C'yi indirmek gerekir.

İki sırada da sonuçta iki hedef birden sağlanmaz. Doğru plan, ikisini **birlikte** düşünen tam aramadan çıkar.

Kitaptaki çözüm yolu: Hedef bir kuleyse, alt hedefler **aşağıdan yukarı** sıralanabilir (§3.1). Hedefe On(C, Table)'ı da ekleyip önce On(C, Table), sonra On(B, C), sonra On(A, B) çözülürse hiçbir alt hedef bozulmaz. `kitap_problemleri.py` bu sırayı da dener ve doğrudan 3 adımlık planı bulur.

---

## 3. Planlama sezgiselleri

Sezgisel, bir **gevşetilmiş problemin** kesin çözüm maliyetidir (Bölüm 3'teki fikir). Bölüm 3'teki atomik durumlarda sezgiseli bir insan bulmak zorundaydı. PDDL'in ayrışık yapısı ise gevşetmeleri **alana bağımsız** ve otomatik yapmayı sağlar. İki yol var: grafiğe kenar eklemek (problemi kolaylaştırmak) ya da durumları gruplamak (soyutlama).

| Sezgisel | Gevşetme | Kitaptaki değerlendirme |
|---|---|---|
| **Önkoşulları yok say** | Her eylem her zaman uygulanabilir | Hedefi sağlayan en az eylem sayısı bir **küme örtme** problemidir (NP-zor). Açgözlü algoritma en iyinin log n katı içinde kalır ama kabul edilebilirliği kaybeder. Kaba hâli: sağlanmamış hedef sayısı (`h_hedef_sayisi`). |
| Bazı önkoşulları yok say | 8'li bulmacada Blank ve Adjacent atılınca "yanlış yerdeki taş sayısı", yalnızca Blank atılınca "Manhattan uzaklığı" çıkar | Bölüm 3'teki sezgiseller eylem şemasından otomatik türetilir. |
| **Silme listelerini yok say** | Eylemler hiçbir şeyi silmez; ilerleme hiç geri alınmaz | Bu gevşetilmiş problemin en iyi çözümü (h⁺) bile NP-zordur. Yaklaşık çözüm polinom zamanda bulunur. Birçok problemde sezgisel yüzeyinde yerel minimum yoktur; tepe tırmanma bile iyi çalışır. |
| **Durum soyutlama** | Bazı akışkanları at | Kitaptaki büyük hava kargo örneği: ~10⁴⁰⁵ durum, soyutlamayla ~10¹¹'e iner. Soyut çözüm daha kısadır, bu yüzden kabul edilebilir. |
| **Ayrıştırma** | Hedefi alt hedeflere böl | Alt maliyetlerin **en büyüğü** kabul edilebilir. **Toplamı** ancak alt hedefler bağımsızsa kabul edilebilir. Alt planlar ortak eylem içeriyorsa toplam fazla tahmin eder (kabul edilemez); alt planlar birbirini bozuyorsa az tahmin eder. |

**Bu repodaki ek sezgiseller (kitabın ötesinde; silme listesi gevşetmesinin hesaplanabilir yaklaşımları):**
- `h_max`: Her atomun gevşetilmiş maliyeti = onu üreten en ucuz eylemin 1 + en pahalı önkoşulu. Hedef atomlarının en büyüğü alınır. **Kabul edilebilir** (h_max ≤ h⁺ ≤ h\*).
- `h_add`: Aynısı, ama önkoşulların ve hedeflerin maliyetleri **toplanır**. Kabul edilemez ama çok bilgilendiricidir.
- `h_seviye_toplami`: Mutex'siz planlama grafiğinde her hedefin ilk göründüğü seviyelerin toplamı. Kabul edilemez.

Kitap, bu fikri kullanan güçlü bir sistem olarak **FF**'i (FastForward) anlatır: İleri arama yapar; sezgiseli silme listelerini yok sayarak, bir planlama grafiği yardımıyla hesaplar. Aramada tepe tırmanma kullanır. Takılınca daha iyi bir duruma varana kadar genişlik öncelikli arar; o da başarısız olursa açgözlü en iyi öncelikli aramaya geçer.

`kitap_problemleri.py` karşılaştırması (A*, genişletilen düğüm):

| Problem | BFS | Hedef sayısı | h_max | h_add | Seviye toplamı |
|---|---|---|---|---|---|
| Hava kargo | 56 | 51 | 45 | 21 | 30 |
| Bloklar dünyası | 12 | 6 | 4 | 3 | 3 |

Kabul edilemez sezgiseller (h_add, seviye toplamı) burada da optimal planı buldu, ama bu bir garanti değildir.

### 3.1 Alana bağımsız budama

- **Simetri azaltma:** Birbirinin kopyası olan dallardan yalnızca birini dene. Masada bir düzine blok varken "herhangi bir bloğu başka birinin üstüne koy" adımının 110 seçeneği aslında birbirine denktir.
- **Tercih edilen eylemler:** Gevşetilmiş planın bir adımı olan ya da onun bir önkoşulunu sağlayan eylemlere öncelik ver. Optimal çözümü budama riski vardır.
- **Sıralanabilir alt hedefler:** Alt hedefler, önceden sağlananları hiç bozmadan belirli bir sırayla sağlanabiliyorsa arama büyük ölçüde azalır. Bloklar dünyasında kule **aşağıdan yukarı** kurulursa her problem geri dönmeden çözülür (her zaman en kısa plan olmasa da). Kitaptaki örnek: NASA'nın Deep Space One aracını yöneten Remote Agent planlayıcısı, alt hedeflerin sıralanabilir olmasından yararlanarak gerçek zamanlı çalışabildi.

---

## 4. Hiyerarşik planlama

Büyük problemlerde (bir tatil, bir bina) ilkel eylemlerle planlamak umutsuzdur. **Üst düzey eylemler** (HLA) birkaç **inceltmeye** sahiptir:

```text
Git(Ev, Havalimanı) → [Sür(Ev, Otopark), Servis(Otopark, Havalimanı)]
                    | [Taksi(Ev, Havalimanı)]
```

**Hiyerarşik arama** (`hiyerarsik_plan.py`): Plan içindeki ilk HLA'yı seç ve onun her inceltmesiyle yeni planlar üret. Yalnızca ilkel eylemler kalınca planı başlangıçtan uygula ve hedefe ulaşıp ulaşmadığına bak. Arabası olan ajan otoparka sürer; arabası olmayıp parası olan taksiye biner; ikisi de olmayanın planı yoktur. İnceltmeler **özyineli** de olabilir: Yürü(a, b) → [bir adım, Yürü(…)].

**Meleksi anlam:** HLA'ların etkisini, ulaşılabilir durum kümeleriyle tanımlamak.
- **İyimser betimleme:** Ulaşılabilir kümenin üst yaklaşımıdır. Hedefle kesişmiyorsa plan kesinlikle işe yaramaz; budanır.
- **Kötümser betimleme:** Alt yaklaşımdır. Hedefle kesişiyorsa plan kesinlikle işe yarar; inceltmeye devam etmeden kabul edilir.

Böylece plan, ilkel düzeye inmeden değerlendirilebilir. Hiyerarşi, çözüm uzunluğu d için karmaşıklığı büyük ölçüde azaltabilir.

---

## 5. Deterministik olmayan alanlarda planlama

Kitabın örneği: Bir masa ve bir sandalye aynı renge boyanacak. İki kutu boya var ama renkleri bilinmiyor.
- **Algısız (uyumlu) planlama:** Bir kutuyu aç, ikisini de aynı kutudan boya. Hangi renk olduğu önemsiz; hedef yine sağlanır. Bölüm 4'teki inanç durumlarıyla aynı fikirdir.
- **Koşullu planlama:** Algılar kullanılır: "Masanın rengi sandalyeninkiyle aynıysa bitir, değilse…"
- **Çevrimiçi planlama ve yeniden planlama:** Eylemler beklenmedik sonuç verirse (boya tutmadı) plan düzeltilir.
  - **Eylem izleme:** Bir sonraki eylemin önkoşulları hâlâ sağlanıyor mu?
  - **Plan izleme:** Kalan plan hâlâ işe yarar mı?
  - **Hedef izleme:** Daha iyi bir hedef ortaya çıktı mı?

---

## 6. Zaman, çizelgeler ve kaynaklar

**İş atölyesi çizelgeleme:** İşler, her biri süreli eylemlerden oluşur. Sıralama kısıtları ve paylaşılan kaynaklar vardır. Kitabın yaklaşımı "önce planla, sonra çizelgele"dir.

**Kitaptaki iki arabalık montaj** (`kritik_yol.py`):

| Eylem | Süre | [ES, LS] | Bolluk |
|---|---|---|---|
| MotorTak1 | 30 | [0, 15] | 15 |
| TekerTak1 | 30 | [30, 45] | 15 |
| Denetle1 | 10 | [60, 75] | 15 |
| MotorTak2 | 60 | [0, 0] | 0 (kritik) |
| TekerTak2 | 15 | [60, 60] | 0 (kritik) |
| Denetle2 | 10 | [75, 75] | 0 (kritik) |

**Kritik yol yöntemi (CPM):**
- ES(Başla) = 0; ES(B) = max_{A≺B} [ES(A) + Süre(A)]
- LS(Bitir) = ES(Bitir); LS(A) = min_{B≻A} LS(B) − Süre(A)

En uzun yol **kritik yoldur** (85 dk). Kritik yoldaki eylemlerin bolluğu 0'dır: Birini geciktirmek bütün planı geciktirir. Hesap O(Nb) zamanda yapılır (N eylem sayısı, b bir eyleme giren ya da çıkan en fazla bağlantı sayısı).

**Kaynak kısıtları:** İki motor tek vinci paylaşır, bu yüzden üst üste binemez. Kaynaksız çizelge, başlama ve bitiş zamanları üzerindeki doğrusal eşitsizliklerin bir birleşimidir. Kaynak kısıtı ise "A, B'den önce **ya da** B, A'dan önce" biçiminde bir ayrılma getirir ve problemi NP-zor yapar. Kitaptaki en iyi çizelge **115 dk**'dır: Kaynaksız hâlden 30 dk uzun. Kodumuz dört sıralama seçeneğini deneyerek aynı sonucu bulur (kısa iş olan MotorTak1 önce). **En az bolluk** sezgiseli, açgözlü çizelgelemede bolluğu en az olan eylemi önce yerleştirir.

---

## 7. Planlama yaklaşımlarının analizi

- Planlama, kitabın iki büyük alanını birleştirir: **arama** ve **mantık**. Planlayıcı, çözüm arayan bir program ya da bir çözümün var olduğunu yapıcı biçimde kanıtlayan bir program olarak görülebilir.
- Planlama, her şeyden önce **kombinatoryal patlamayı** kontrol etme işidir: n önermeli bir alanda 2ⁿ durum vardır. En güçlü silah, **bağımsız alt problemleri** bulmaktır. Eylemler arasındaki olumsuz etkileşimler bu ayrışabilirliği bozar.
- **Karmaşıklık:** PlanSAT (bir plan var mı?) ve Sınırlı PlanSAT (en fazla k adımlık plan var mı?) klasik planlamada karar verilebilir problemlerdir. Önermeselleştirilmiş problemler için ikisi de **PSPACE** sınıfındadır (NP'den geniş, dolayısıyla daha zor olabilecek bir sınıf). Dile fonksiyon sembolleri eklenirse durum sayısı sonsuz olur ve PlanSAT yalnızca yarı karar verilebilir kalır. Kuramsal sonuçlar kötümser, ama pratikteki problemler genellikle o kadar kötü değildir.
- Hangi tekniğin hangi problemde en iyi olduğu henüz tam anlaşılmış değildir. **Portföy** planlayıcıları birkaç algoritmayı birlikte kullanır: probleme göre seçerek, paralel çalıştırarak ya da sırayla dönüşümlü çalıştırarak.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Eylemin etkisinde adı geçmeyen atomlar belirsiz olur." | Olduğu gibi kalır (PDDL'in çerçeve varsayımı). |
| "Geri arama için hedefin herhangi bir atomunu ekleyen her eylem ilgilidir." | Hiçbir hedef atomunu **silmemesi** de gerekir (tutarlılık). |
| "Alt hedef maliyetlerinin toplamı her zaman kabul edilebilir." | Yalnızca alt hedefler bağımsızsa. En büyüğü ise her zaman kabul edilebilir. |
| "Silme listelerini yok saymak problemi kolaylaştırır, o hâlde h⁺ kolay hesaplanır." | h⁺'yı kesin hesaplamak da NP-zordur. h_max ve h_add yaklaşımlardır. |
| "Kaynak kısıtları çizelgelemeyi biraz zorlaştırır." | Ayrılmalar getirdikleri için NP-zor yapar. Kaynaksız CPM ise polinomdur. |
| "Alt hedefleri sırayla çözmek yeterlidir." | Sussman anomalisi: Bağımsız olmayan alt hedeflerde işe yaramaz. |

## Kendini yokla

1. SONUÇ(s, a) formülünü yaz. Neden (s ∪ EKLE) − SİL yazılmaz?
2. Yedek lastikte LeaveOvernight bir plana hiç yararlı olabilir mi?
3. Bloklar dünyasında h_add neden kabul edilemez olabilir? Küçük bir örnek düşün.
4. Kaynak kısıtlarıyla 115 dakikalık çizelgede ikinci denetçiye ne zaman ihtiyaç var?
5. Meleksi anlamda iyimser betimleme hedefle kesişiyorsa ne söyleyebiliriz?

## Kod rehberi

```bash
python ornekler/planlama.py            # kütüphane: süpürge dünyası PDDL ile
python ornekler/kitap_problemleri.py   # hava kargo, yedek lastik, bloklar; sezgiseller; Sussman
python ornekler/kritik_yol.py          # CPM: 85 dk; kaynaklarla 115 dk
python ornekler/hiyerarsik_plan.py     # HLA inceltmeleri
python ornekler/strips_bloklar.py      # elli-elsiz bloklar dünyası (Kaldır/Koy)
python ornekler/aksiyon_semasi.py      # eylem şeması yazdırma
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| klasik planlama | classical planning | Deterministik, tam gözlemli ortamda eylem dizisi bulma |
| PDDL | Planning Domain Definition Language | Planlama problemleri için standart dil |
| eylem şeması | action schema | Değişkenli eylem tanımı (önkoşul, etki) |
| ekleme / silme listesi | add / delete list | Etkinin olumlu / olumsuz literalleri |
| ileri / geri arama | progression / regression search | Başlangıçtan / hedeften arama |
| ilgili eylem | relevant action | Hedef atomu ekleyen, hiçbirini silmeyen eylem |
| planlama grafiği | planning graph | Seviyeli durum–eylem grafiği |
| karşılıklı dışlama | mutex | Aynı seviyede birlikte olamayan eylem/atom çifti |
| kısmi sıralı plan | partial-order plan | Yalnızca gerekli sıralamaları içeren plan |
| SAT olarak planlama | planning as satisfiability (SATPlan) | Problemi CNF'ye çevirip SAT çözücüyle çözme |
| durum soyutlama | state abstraction | Durumları gruplayarak küçültme |
| simetri azaltma / tercih edilen eylem | symmetry reduction / preferred action | Alana bağımsız budama yöntemleri |
| portföy planlama | portfolio planning | Birden çok algoritmayı birlikte kullanma |
| önkoşulları / silme listelerini yok sayma | ignore preconditions / ignore delete lists | Gevşetmeler |
| alt hedef bağımsızlığı / sıralanabilir alt hedefler | subgoal independence / serializable subgoals | Alt hedeflerin etkileşimi |
| üst düzey eylem / inceltme | high-level action / refinement | Hiyerarşik planlamanın yapı taşları |
| meleksi anlam | angelic semantics | HLA'ları ulaşılabilir kümelerle değerlendirme |
| uyumlu (algısız) / koşullu planlama | conformant / contingent planning | Algısız / algılara bağlı dallanan planlar |
| yürütme izleme / yeniden planlama | execution monitoring / replanning | Planı uygularken denetleme ve düzeltme |
| iş atölyesi çizelgeleme | job-shop scheduling | Süreli işler ve paylaşılan kaynaklar |
| kritik yol / bolluk | critical path / slack | En uzun yol / LS − ES |
| en az bolluk | minimum slack | Açgözlü çizelgeleme sezgiseli |
