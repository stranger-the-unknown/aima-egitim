# Bölüm 3 — Arama yoluyla problem çözme

> **Kitapta:** AIMA 4. baskı, Bölüm 3 *"Solving Problems by Searching"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 3.1 Problem-Solving Agents | §1 Dört aşama, problemin beş parçası, soyutlama | `arama.py` → `Problem` |
| 3.2 Example Problems | §2 Oyuncak ve gerçek problemler | `romania_arama.py`, `sekiz_bulmaca.py` |
| 3.3 Search Algorithms | §3 Arama ağacı, sınır, ulaşılan tablo, en iyi öncelikli arama, performans ölçütleri | `arama.py` → `en_iyi_oncelikli` |
| 3.4 Uninformed Search Strategies | §4 BFS, UCS, DFS, DLS, IDS, çift yönlü arama | `arama.py`, `romania_arama.py` |
| 3.5 Informed (Heuristic) Search Strategies | §5 Açgözlü arama, A*, ağırlıklı A*, bellek sınırlı arama | `romania_arama.py` (A* izi) |
| 3.6 Heuristic Functions | §6 h1/h2, etkin dallanma, baskınlık, gevşetilmiş problemler, örüntü veritabanları | `sekiz_bulmaca.py` |

## Öğrenme hedefleri

1. Bir problemi beş parçasıyla (durumlar, başlangıç, hedef testi, eylemler + geçiş modeli, eylem maliyeti) biçimsel olarak tanımlamak.
2. Arama ağacı ile durum uzayını, ağaç benzeri arama ile graf aramasını ayırt etmek.
3. Bilgisiz arama algoritmalarını tamlık, optimallik, zaman ve bellek ölçütleriyle karşılaştırmak.
4. A*'ın neden optimal olduğunu kabul edilebilirlik ve tutarlılık kavramlarıyla açıklamak.
5. Bir problem için kabul edilebilir sezgisel türetmek (gevşetme) ve iki sezgiseli etkin dallanma faktörüyle karşılaştırmak.

---

## 1. Problem çözen ajanlar

Hedefe dayalı bir ajan, hedefine ulaşan bir **eylem dizisi** arar. Bunu dört aşamada yapar:

1. **Hedef belirleme:** Ne istiyorum? ("Yarın Bucharest'te olmak.") Hedef, ilgilenilecek eylemleri daraltır.
2. **Problem formülasyonu:** Dünyanın hangi ayrıntıları önemli? Hangi eylemler var?
3. **Arama:** Eylemleri "zihinde" deneyerek hedefe götüren diziyi, yani **çözümü** bul.
4. **Uygulama:** Çözümü adım adım uygula.

Ortam tam gözlemlenebilir, deterministik ve biliniyorsa, çözüm uygulanırken algılara bakmaya gerek yoktur. Buna **açık döngü** denir. Belirsizlik varsa algılar izlenmelidir (**kapalı döngü**, Bölüm 4).

### 1.1 Bir arama probleminin beş parçası

| Parça | Anlamı | Romanya örneği |
|---|---|---|
| **Durum uzayı** | Olası durumların kümesi | 20 şehir |
| **Başlangıç durumu** | Nereden başlıyoruz? | `Arad` |
| **Hedef durumları** / `HEDEF-Mİ(s)` | Hangi durumlar hedef? (bir ya da birden çok) | `s == Bucharest` |
| **Eylemler** `EYLEMLER(s)` ve **geçiş modeli** `SONUÇ(s, a)` | s'de ne yapılabilir, yapılınca ne olur? | `EYLEMLER(Arad) = {Sibiu'ya git, Timisoara'ya git, Zerind'e git}`; `SONUÇ(Arad, Sibiu'ya git) = Sibiu` |
| **Eylem maliyeti** `MALİYET(s, a, s')` | Eylemin bedeli | Yolun km'si |

Eylem dizisine **yol** denir. Başlangıçtan hedefe giden yol bir **çözümdür**. Yol maliyeti en düşük olan çözüm **optimal çözümdür**. `arama.py`'deki `Problem` sınıfı bu beş parçanın doğrudan kod karşılığıdır.

### 1.2 Soyutlama

Gerçek bir yolculukta radyo kanalı, hava durumu ve yol kenarındaki manzara da vardır. Formülasyon bunları **atar**. İyi bir soyutlama:

- **geçerlidir:** Soyut çözümdeki her adım gerçek dünyada da uygulanabilir ("Arad'dan Sibiu'ya git" gerçekten yapılabilir),
- **kullanışlıdır:** Soyut adımlar, gerçekleştirilmesi için yeniden arama gerektirmeyecek kadar kolaydır.

---

## 2. Örnek problemler

**Standart (oyuncak) problemler:** Algoritmaları karşılaştırmak için kesin tanımlıdır.

- **Süpürge dünyası:** 2 kare → 2 × 2² = 8 durum.
- **Kaydırmalı taş bulmacaları:** 8-bulmacanın 9!/2 = **181.440** erişilebilir durumu vardır (kitabın 3.6. bölümünde bu sayı dizgi hatasıyla "181, 400" diye geçer; doğrusu 181.440). 15-bulmacanın ~10¹³, 24-bulmacanın ~10²⁵ durumu vardır. `sekiz_bulmaca.py` 8-bulmacanın durum uzayını BFS ile neredeyse tamamen dolaşıyor. 15-bulmacada bu imkânsızdır.
- **Sokoban**, ızgara dünyaları, sayı dönüştürme bulmacaları.

**Gerçek dünya problemleri:** Rota bulma (navigasyon, havayolu seyahati), gezi problemleri, **gezgin satıcı** (TSP), VLSI yerleşimi, robot navigasyonu, otomatik montaj sıralaması.

---

## 3. Arama algoritmalarının ortak iskeleti

### 3.1 Arama ağacı ve durum uzayı

- **Durum uzayı** bir graftır: düğümler durumlar, kenarlar eylemlerdir. Sonludur (Romanya'da 20 durum).
- **Arama ağacı** bu graf üzerindeki *yolları* temsil eder. Aynı duruma farklı yollardan gelinebildiği için ağaç sonsuz olabilir (Arad → Sibiu → Arad → …).
- Ağaçtaki her **düğüm** şunları tutar: durum, ebeveyn, ona getiren eylem ve yol maliyeti g(n). Düğüm ≠ durum.

### 3.2 Genişletme, sınır, ulaşılan tablo

- **Genişletmek:** Bir düğümün tüm eylemlerini deneyip çocuk düğümleri üretmek.
- **Sınır** (*frontier*): Üretilmiş ama henüz genişletilmemiş düğümler. Arama, "hangi sınır düğümünü önce genişletirim?" sorusuna verilen cevaptır.
- **Ulaşılan** (*reached*) tablo: Daha önce görülen durumlar ve onlara giden en iyi düğüm.

**Gereksiz yollar:** Aynı duruma ikinci kez, daha pahalı bir yolla gelmek boşa iştir. Üç strateji vardır:
1. **Graf araması:** Ulaşılan tabloyu tut; tekrar eden durumları ele (`en_iyi_oncelikli`, `genislik_oncelikli`).
2. **Ağaç benzeri arama:** Tablo tutma. Bellek azdır, ama aynı durum tekrar tekrar genişletilebilir. Yalnızca mevcut yoldaki **döngüleri** kontrol etmek ucuz bir ara yoldur (`derinlik_sinirli`).
3. Gereksiz yolların imkânsız olduğu problemlerde hiçbir şey yapma.

### 3.3 En iyi öncelikli arama: tek iskelet, çok algoritma

```text
fonksiyon EN-İYİ-ÖNCELİKLİ(problem, f):
    düğüm ← DÜĞÜM(problem.başlangıç)
    sınır ← f'ye göre öncelik kuyruğu, içinde düğüm
    ulaşılan ← {başlangıç: düğüm}
    sınır boş değilken:
        düğüm ← sınırdan f'si en küçüğü çıkar
        eğer HEDEF-Mİ(düğüm.durum): döndür düğüm        ← hedef testi ÇIKARKEN
        her çocuk için GENİŞLET(problem, düğüm):
            s ← çocuk.durum
            eğer s ulaşılanda değil ya da çocuk.g < ulaşılan[s].g:
                ulaşılan[s] ← çocuk;  sınıra ekle
    döndür başarısızlık
```

`f` seçimi algoritmayı belirler: **f = g** ise UCS, **f = h** ise açgözlü arama, **f = g + h** ise A*, **f = g + W·h** ise ağırlıklı A*. `arama.py` tam olarak böyle kurulmuştur.

### 3.4 Performans nasıl ölçülür?

- **Tamlık:** Çözüm varsa bulur mu? Yoksa bunu bildirir mi?
- **Maliyet optimalliği:** En düşük maliyetli çözümü bulur mu?
- **Zaman karmaşıklığı:** Kaç düğüm üretir veya genişletir?
- **Bellek karmaşıklığı:** Aynı anda en fazla kaç düğüm saklar?

Kitap "genişletilen" yerine çoğu zaman **üretilen** düğüm sayısını raporlar. `arama.py` ikisini de sayar (`genisletilen`, `uretilen`).

Sonsuz ya da çok büyük uzaylarda karmaşıklık üç parametreyle ifade edilir: **b** dallanma faktörü (bir düğümün en fazla çocuk sayısı), **d** en sığ çözümün derinliği, **m** herhangi bir yolun en büyük uzunluğu (sonsuz olabilir).

---

## 4. Bilgisiz (kör) arama

Bu algoritmalar hedefin "ne kadar uzakta" olduğu hakkında hiçbir şey bilmez.

### 4.1 Genişlik öncelikli arama (BFS)

- FIFO kuyruğu: Önce tüm 1. derinlik düğümleri, sonra 2. derinlik düğümleri…
- **Erken hedef testi** yapılabilir: Çocuk üretilirken hedef olup olmadığına bakılır, çünkü BFS en sığ hedefi zaten ilk bulur.
- Tamdır. **Yalnızca tüm eylemlerin maliyeti eşitse** optimaldir. Romanya'da en az kenarlı yolu bulur (Fagaras üzerinden 450 km), en kısa km'yi değil.
- Zaman ve bellek O(b^d). **Asıl sorun bellektir:**

| d | Düğüm (b = 10) | Süre (10⁶ düğüm/sn) | Bellek (1 KB/düğüm) |
|---|---|---|---|
| 6 | ~10⁶ | ~1 sn | ~1 GB |
| 8 | ~10⁸ | ~2 dk | ~100 GB |
| 10 | ~10¹⁰ | ~3 saat | ~10 TB |
| 12 | ~10¹² | ~13 gün | ~1 PB |
| 14 | ~10¹⁴ | ~3,5 yıl | ~100 PB |

Üstel karmaşıklıklı arama problemleri, en küçük örnekler dışında bilgisiz yöntemlerle çözülemez.

### 4.2 Tekdüze maliyet araması (UCS, Dijkstra)

- f = g: Yol maliyeti en küçük düğüm önce genişletilir.
- Hedef testi düğüm **çıkarılırken** yapılır. Üretilirken yapılsaydı, Romanya'da Fagaras üzerinden gelen 450'lik yol kabul edilirdi (§5.2'deki ize bak).
- Tüm eylem maliyetleri bir ε > 0 değerinden büyükse tamdır ve optimaldir.
- Karmaşıklık O(b^(1+⌊C*/ε⌋)). Burada C* optimal maliyettir. Ucuz adımlar çoksa BFS'ten çok daha fazla iş yapabilir.

### 4.3 Derinlik öncelikli arama (DFS)

- LIFO: En derindeki düğüm önce genişletilir.
- **Optimal değildir.** Sonlu ve döngüsüz uzaylarda tamdır, sonsuz uzaylarda sonsuz bir dala dalabilir.
- Ağaç benzeri sürümünün avantajı **bellektir**: O(b·m). BFS'in üstel belleğine karşı doğrusal.
- **Geri izleme** (*backtracking*) sürümü, çocukları teker teker üretir ve durumu yerinde değiştirir. Bellek O(m)'ye iner (Bölüm 6'daki CSP'lerin temelidir).

### 4.4 Derinlik sınırlı arama ve yinelemeli derinleşme (IDS)

- **DLS:** DFS'e bir ℓ derinlik sınırı koyar. ℓ < d ise çözümü kaçırır.
- **IDS:** ℓ = 0, 1, 2, … için DLS'yi tekrarlar. Böylece **BFS'in tamlığını ve birim maliyetteki optimalliğini, DFS'in doğrusal belleğiyle** birleştirir.
- Üst düzeyler tekrar tekrar genişletildiği için israf gibi görünür, ama öyle değildir. Çoğu düğüm en alt düzeydedir. b = 10, d = 5 için:
  - N(BFS) = 10 + 100 + 1.000 + 10.000 + 100.000 = **111.110**
  - N(IDS) = 5·10 + 4·100 + 3·1.000 + 2·10.000 + 1·100.000 = **123.450** (yalnızca %11 fazla)
- Durum uzayı büyük ve çözüm derinliği bilinmiyorsa **tercih edilen bilgisiz yöntemdir**.

### 4.5 Çift yönlü arama

Biri başlangıçtan, biri hedeften iki arama aynı anda yürütülür ve ortada buluşmaları beklenir. Mantığı şudur: b^(d/2) + b^(d/2), b^d'den çok çok küçüktür. Ama hedeften geriye doğru arayabilmek için eylemlerin **tersini** bilmek gerekir. Doğru bir durma koşulu da önemlidir: İlk buluşma her zaman en iyi yol değildir (`romania_arama.py` → `iki_yonlu_ucs`).

### 4.6 Karşılaştırma

| Ölçüt | BFS | UCS | DFS | DLS | IDS | Çift yönlü |
|---|---|---|---|---|---|---|
| Tam mı? | Evet¹ | Evet¹˒² | Hayır | Hayır | Evet¹ | Evet¹˒⁴ |
| Maliyette optimal mi? | Evet³ | Evet | Hayır | Hayır | Evet³ | Evet³˒⁴ |
| Zaman | O(b^d) | O(b^(1+⌊C*/ε⌋)) | O(b^m) | O(b^ℓ) | O(b^d) | O(b^(d/2)) |
| Bellek | O(b^d) | O(b^(1+⌊C*/ε⌋)) | O(bm) | O(bℓ) | O(bd) | O(b^(d/2)) |

¹ b sonluysa ve (sonsuz uzayda) bir çözüm varsa · ² tüm maliyetler ≥ ε > 0 ise · ³ tüm maliyetler eşitse · ⁴ iki yön de BFS veya UCS ise

---

## 5. Bilgili (sezgisel) arama

**Sezgisel fonksiyon** h(n): n düğümünün durumundan en yakın hedefe *tahmini* en ucuz yol maliyeti. Hedefte h = 0'dır. Romanya'da h_SLD(n), n'den Bucharest'e kuş uçuşu mesafedir.

### 5.1 Açgözlü en iyi öncelikli arama (f = h)

"Hedefe en yakın görünen düğümü genişlet." Romanya'da Arad → Sibiu → Fagaras → Bucharest yolunu yalnızca 3 genişletmeyle bulur. Ama yol **450 km'dir**, optimal değildir: Fagaras hedefe yakın görünür, ama oradan Bucharest'e giden yol uzundur. Graf araması sürümü sonlu uzaylarda tamdır, ağaç benzeri sürümü döngüye girebilir.

### 5.2 A* araması (f = g + h)

f(n) = g(n) + h(n), yani n'den geçen en ucuz çözümün tahmini maliyeti. `romania_arama.py`'nin ürettiği iz, kitaptaki şekille aynıdır:

| Sıra | Şehir | g | h | f |
|---|---|---|---|---|
| 1 | Arad | 0 | 366 | 366 |
| 2 | Sibiu | 140 | 253 | 393 |
| 3 | Rimnicu Vilcea | 220 | 193 | 413 |
| 4 | Fagaras | 239 | 176 | 415 |
| 5 | Pitesti | 317 | 100 | 417 |
| 6 | **Bucharest** | 418 | 0 | **418** |

4. adımda Fagaras genişletilince Bucharest sınıra **f = 450** ile girer. A* onu hemen almaz, çünkü f = 417 olan Pitesti daha umut vericidir. Pitesti'den Bucharest'e 418 ile ulaşılır ve kayıt güncellenir. Hedef testinin çıkarken yapılmasının nedeni budur.

**Kabul edilebilirlik:** h(n), n'den hedefe gerçek en ucuz maliyeti **asla aşmıyorsa** h kabul edilebilirdir. Kuş uçuşu, iki nokta arasındaki en kısa yol olduğu için hiçbir zaman gerçek yol mesafesini aşmaz.

> **Teorem:** h kabul edilebilirse, A* maliyette optimaldir.
> **Sezgi:** Optimal olmayan bir hedef düğümü G₂ (maliyeti C₂ > C*) kuyruktan çıkmadan önce, optimal yol üzerindeki bir n düğümü hâlâ sınırdadır ve f(n) = g(n) + h(n) ≤ C* < C₂ = f(G₂) olur. Bu yüzden n, G₂'den önce çıkar. Bu tekrarlana tekrarlana optimal hedefe ulaşılır.

**Tutarlılık (monotonluk):** Her n, her a eylemi ve onun sonucu n' için **h(n) ≤ c(n, a, n') + h(n')**. Bu bir üçgen eşitsizliğidir. Tutarlılık kabul edilebilirliği gerektirir (tersi her zaman doğru değildir). Tutarlı h ile:
- f değerleri yol boyunca **azalmaz**,
- bir duruma **ilk ulaşıldığında** en iyi yoldan ulaşılmış olur, yani graf aramasında bir durumu yeniden açmak gerekmez.

**Konturlar:** A*, f < C* olan tüm düğümleri genişletir, f = C* olanların bazılarını genişletir, f > C* olanların hiçbirini genişletmez. h ne kadar isabetliyse konturlar hedefe doğru o kadar dar uzanır. Yani **budama**: f > C* olan alt ağaçlara hiç bakılmaz.

**Sınırı:** A* genellikle bellek yüzünden tıkanır. Sınır ve ulaşılan tablo üstel büyüyebilir.

### 5.3 Yeterince iyi arama: ağırlıklı A*

f = g + W·h (W > 1). Sezgisele daha çok güvenir, daha az düğüm genişletir. Bulunan çözümün maliyeti en fazla W·C* olur. Romanya'da W = 2 açgözlü arama gibi davranır ve 450'lik yolu bulur. Pratikte "optimal olmasa da yeterince iyi, hızlı bir çözüm" gerektiğinde kullanılır.

### 5.4 Bellek sınırlı arama

- **Işın araması** (*beam search*): Sınırda yalnızca en iyi k düğümü tutar. Hızlıdır ama tam değildir.
- **IDA\***: IDS'nin A* sürümü. Sınır, derinlik yerine f değeridir; her turda aşılan en küçük f bir sonraki eşik olur. Bellek yalnızca yol kadardır (`arama.py` → `ida_yildiz`; 8-bulmacada A* kadar hızlı).
- **RBFS** ve **SMA\***: Sınırlı belleği daha akıllı kullanan, unutulan alt ağaçların en iyi f değerini hatırlayan yöntemler.

---

## 6. Sezgisel fonksiyonlar

### 6.1 8-bulmaca için iki sezgisel

- **h1** = yanlış yerdeki taş sayısı. Her yanlış taş en az bir kez hareket etmelidir.
- **h2** = taşların hedef konumlarına **Manhattan** uzaklıklarının toplamı. Her taş en az bu kadar adım atmalıdır.

Kitaptaki başlangıç durumu (7 2 4 / 5 _ 6 / 8 3 1) için h1 = **8**, h2 = **18**, optimal çözüm **26** hamledir. `sekiz_bulmaca.py` üçünü de hesaplar ve testlerle doğrular.

### 6.2 Etkin dallanma faktörü b*

A* derinliği d olan bir çözümü N düğüm genişleterek bulduysa, b*, d derinliğinde N + 1 düğümlü düzgün bir ağacın dallanma faktörüdür:

N + 1 = 1 + b* + (b*)² + … + (b*)^d

Burada N, kitaptaki gibi **üretilen** düğüm sayısıdır. Örnek: d = 5 ve N = 52 ise b* ≈ 1,92 (`arama.py` → `etkin_dallanma`). İyi bir sezgisel b*'ı 1'e yaklaştırır. `sekiz_bulmaca.py` kitap örneği için şunları buldu:

| Algoritma | Üretilen düğüm | b* |
|---|---|---|
| BFS | 425.624 | 1,58 |
| A*(h1) | 121.196 | 1,50 |
| A*(h2) | 10.548 | 1,36 |

Rastgele bulmacalarda da b* değerleri kitaptaki deneyle uyumludur: h1 için ~1,5, h2 için ~1,3.

### 6.3 Baskınlık

Her n için h2(n) ≥ h1(n) ise **h2, h1'i baskılar**. İkisi de tutarlıysa A*(h2)'nin genişlettiği her düğümü A*(h1) de genişletir. Bu yüzden **kabul edilebilir kaldığı sürece daha büyük sezgisel daha iyidir**. Birkaç kabul edilebilir sezgisel varsa, **h(n) = max(h1(n), …, hk(n))** de kabul edilebilirdir ve hepsini baskılar.

### 6.4 Sezgisel nereden bulunur? Gevşetilmiş problemler

Bir problemin kurallarını gevşeterek (bazı kısıtları atarak) elde edilen probleme **gevşetilmiş problem** denir. **Gevşetilmiş problemin optimal çözüm maliyeti, özgün problem için kabul edilebilir ve tutarlı bir sezgiseldir**, çünkü gevşetilmiş problem özgün problemin tüm çözümlerini (ve fazlasını) içerir.

8-bulmacanın kuralı: *"Bir taş A'dan B'ye geçebilir, eğer A ile B komşuysa **ve** B boşsa."*
- "ve B boşsa" koşulunu at → taşlar komşu karelere serbestçe kayar → **h2** (Manhattan).
- İki koşulu da at → taş istediği yere tek adımda ışınlanır → **h1**.
- "A ile B komşuysa" koşulunu at → başka bir sezgisel elde edilir (bkz. Alıştırma A9).

### 6.5 Başka kaynaklar

- **Örüntü veritabanları:** Alt problemin (ör. yalnızca 1–4 numaralı taşlar) tüm durumları için kesin çözüm maliyetini önceden hesaplayıp sakla. Ayrık alt problemlerin maliyetleri toplanabilir.
- **Yer imleri** (*landmarks*): Rota bulmada birkaç önemli noktaya olan uzaklıkları önceden hesaplayıp üçgen eşitsizliğiyle sezgisel üret (navigasyon sistemlerinde kullanılır).
- **Deneyimden öğrenmek:** Çözülmüş örneklerin özniteliklerinden (yanlış yerdeki taş sayısı, komşu çiftler…) h'yi regresyonla tahmin et. Genellikle kabul edilebilirlik garantisi kaybolur.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "UCS/A*'da hedef testini düğüm üretilirken yaparım." | Optimal olmayan yolu kabul edersin. Test, kuyruktan **çıkarken** yapılmalı (BFS istisnadır). |
| "BFS en kısa yolu bulur." | En az **kenarlı** yolu bulur. Maliyetler farklıysa optimal değildir (Romanya: 450 ≠ 418). |
| "Kabul edilebilir = h(n) ≤ bir adımın maliyeti." | Kabul edilebilir = h(n) ≤ n'den hedefe **toplam** gerçek maliyet. |
| "Her kabul edilebilir sezgisel tutarlıdır." | Genelde öyledir ama zorunlu değildir. Tutarlılık daha güçlü bir koşuldur. |
| "Büyük h her zaman iyidir." | Yalnızca kabul edilebilir kaldığı sürece. Abartan h optimalliği bozar (ağırlıklı A*). |
| "IDS aynı düğümleri tekrar genişlettiği için çok yavaştır." | b = 10'da BFS'ten yalnızca ~%11 fazla iş yapar ve belleği doğrusal kalır. |
| "Düğüm ile durum aynı şeydir." | Aynı duruma birçok düğüm karşılık gelebilir (farklı yollar). |

## Kendini yokla

1. Romanya'da Bucharest'in hedef testi üretilirken yapılsaydı, A* hangi yolu döndürürdü?
2. Tüm eylem maliyetleri 1 ise UCS ile BFS nasıl ilişkilidir?
3. h(n) = 0 ile A* hangi algoritmaya dönüşür? h(n) = h*(n) (kusursuz sezgisel) ise ne olur?
4. 8-bulmacada h3 = h1 + h2 kabul edilebilir mi? Neden?

## Kod rehberi

```bash
python ornekler/arama.py            # kütüphanenin küçük kendini sınaması
python ornekler/romania_arama.py    # 8 algoritma + A* izi (kitaptaki değerler)
python ornekler/romania_arama.py --baslangic Oradea --hedef Neamt
python ornekler/sekiz_bulmaca.py    # h1 = 8, h2 = 18, optimal = 26; b* karşılaştırması
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| durum uzayı | state space | Tüm durumlar ve aralarındaki eylemler (graf) |
| geçiş modeli | transition model | SONUÇ(s, a): eylemin sonucu |
| eylem maliyeti | action cost | Bir eylemin bedeli |
| yol maliyeti g(n) | path cost | Başlangıçtan n'ye kadarki toplam maliyet |
| arama ağacı | search tree | Durum uzayındaki yolların ağacı |
| genişletme | expansion | Bir düğümün çocuklarını üretmek |
| sınır | frontier | Üretilmiş ama genişletilmemiş düğümler |
| ulaşılan tablo | reached table | Görülen durumlar ve en iyi düğümleri |
| gereksiz yol | redundant path | Aynı duruma daha pahalı bir yoldan gelmek |
| graf araması / ağaç benzeri arama | graph search / tree-like search | Tekrar eden durumları eleyen / elemeyen arama |
| dallanma faktörü | branching factor (b) | Bir düğümün en fazla çocuk sayısı |
| tekdüze maliyet araması | uniform-cost search | f = g |
| yinelemeli derinleşme | iterative deepening | Artan derinlik sınırlarıyla DLS |
| çift yönlü arama | bidirectional search | İki uçtan aynı anda arama |
| sezgisel | heuristic h(n) | Hedefe tahmini kalan maliyet |
| kabul edilebilir | admissible | Gerçek maliyeti asla aşmayan |
| tutarlı | consistent | h(n) ≤ c(n,a,n') + h(n') |
| açgözlü arama | greedy best-first search | f = h |
| ağırlıklı A* | weighted A* | f = g + W·h |
| etkin dallanma faktörü | effective branching factor (b*) | Sezgiselin kalitesinin ölçüsü |
| baskınlık | dominance | h2 ≥ h1 her yerde |
| gevşetilmiş problem | relaxed problem | Kısıtları azaltılmış problem |
| örüntü veritabanı | pattern database | Alt problemlerin kesin maliyet tablosu |
