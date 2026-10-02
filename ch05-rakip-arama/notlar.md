# Bölüm 5 — Rakip arama ve oyunlar

> **Kitapta:** AIMA 4. baskı, Bölüm 5 *"Adversarial Search and Games"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 5.1 Game Theory | §1 İki oyunculu sıfır toplamlı oyunlar, oyun ağacı | `minimax_tictactoe.py --mod istatistik` |
| 5.2 Optimal Decisions in Games | §2 Minimax, çok oyunculu oyunlar, alfa-beta, hamle sıralaması | `oyun_agaci.py`, `minimax_tictactoe.py` |
| 5.3 Heuristic Alpha-Beta Tree Search | §3 Değerlendirme fonksiyonu, kesme, sessizlik, ufuk etkisi, ileri budama | `dortlu_ab.py` |
| 5.4 Monte Carlo Tree Search | §4 Seçim–genişletme–benzetim–geri yayma, UCB1 | `mcts_xox.py` |
| 5.5 Stochastic Games | §5 Şans düğümleri, beklenti-minimaks | `beklenti_minimax.py` |
| 5.6 Partially Observable Games | §6 Kriegspiel, kart oyunları | — |
| 5.7 Limitations of Game Search Algorithms | §7 Sınırlar | — |

## Öğrenme hedefleri

1. Bir oyunu (başlangıç, sıra, eylemler, sonuç, terminal testi, fayda) biçimsel olarak tanımlamak.
2. Minimax değerini elle ve kodla hesaplamak; alfa-betanın neyi, neden budadığını izleyebilmek.
3. Hamle sıralamasının alfa-beta verimliliğine etkisini sayısal olarak göstermek.
4. Sezgisel alfa-betanın bileşenlerini (değerlendirme, kesme, sessizlik araması, TT) açıklamak.
5. MCTS'in dört adımını ve UCB1 formülünü uygulamak.
6. Şans düğümlü oyunlarda beklenti-minimaksı ve değerlendirme fonksiyonunun ölçeğinin neden önemli olduğunu açıklamak.

---

## 1. Oyunlar ve oyun teorisi

Bu bölümün odağı **iki oyunculu, sıra tabanlı, tam bilgili, sıfır toplamlı** oyunlardır (satranç, Go, XOX). "Sıfır toplamlı": Birinin kazancı diğerinin kaybıdır; ortak çıkar yoktur.

Bir oyunun biçimsel tanımı:

| Öğe | Anlamı |
|---|---|
| S₀ | Başlangıç durumu |
| SIRA(s) | s'de hamle sırası kimde |
| EYLEMLER(s) | Yasal hamleler |
| SONUÇ(s, a) | Geçiş modeli |
| TERMİNAL-Mİ(s) | Oyun bitti mi? |
| FAYDA(s, p) | Terminal s'de p oyuncusunun kazancı (satrançta 1, 0, ½) |

Oyuncular **MAX** (faydayı büyütmek ister) ve **MIN** (küçültmek ister) olarak adlandırılır. **Kat** (*ply*), tek bir oyuncunun tek hamlesidir.

**XOX'un boyutu** (`minimax_tictactoe.py --mod istatistik`): Oyun ağacında 549.946 düğüm ve 255.168 yaprak vardır (9! = 362.880'den az), ama yalnızca **5.478 farklı durum**. Satrançta ise düğüm sayısı 10⁴⁰'ı aşar. Ağaç, fiziksel olarak kurulamayan kuramsal bir nesnedir.

---

## 2. Oyunlarda optimal karar

### 2.1 Minimax

Rakibin de kusursuz oynadığını varsayarak her durumun değerini hesapla:

MINIMAX(s) = FAYDA(s) terminalse; sıra MAX'ta ise çocukların **en büyüğü**; sıra MIN'de ise çocukların **en küçüğü**.

**Kitaptaki iki katlı örnek** (`oyun_agaci.py`):

| MIN düğümü | Yapraklar | Değer |
|---|---|---|
| B | 3, 12, 8 | **3** |
| C | 2, 4, 6 | **2** |
| D | 14, 5, 2 | **2** |

Kök A = max(3, 2, 2) = **3**. MAX a1'i oynar, MIN b1 ile cevap verir.

Minimax tam bir derinlik öncelikli aramadır: zaman O(b^m), bellek O(bm). Satrançta b ≈ 35 ve m ≈ 80 olduğu için pratikte imkânsızdır, ama sonraki bütün yöntemlerin temelidir.

**Rakip kusursuz değilse?** Minimax en kötü duruma karşı güvencedir. Rakibin hata yapacağı biliniyorsa daha "riskli" bir hamle daha yüksek beklenen sonuç verebilir. Ama minimax hamlesi hiçbir zaman minimax değerinden kötü sonuç vermez.

### 2.2 Çok oyunculu oyunlar

Tek bir sayı yerine her düğüme bir **fayda vektörü** (u_A, u_B, u_C) atanır. Sırası gelen oyuncu, kendi bileşenini en büyüten çocuğu seçer. Çok oyunculu oyunlarda **ittifaklar** doğal olarak ortaya çıkabilir ve bozulabilir: Önde olan oyuncuya karşı diğerleri ortak hareket etmeyi "rasyonel" bulabilir.

### 2.3 Alfa-beta budama

Minimax değerini değiştirmeden, sonucu etkileyemeyecek dalları atlar.

- **α:** MAX için yol boyunca o ana kadar bulunan **en iyi** (en yüksek) değer. "MAX en az bunu garantiler."
- **β:** MIN için yol boyunca o ana kadar bulunan en iyi (en düşük) değer. "MIN en fazla buna izin verir."

Bir MIN düğümünde değer α'nın altına düşerse, üstteki MAX bu dala zaten gelmeyecektir; kalan çocuklar budanır. MAX düğümünde değer β'yı aşarsa simetrik durum oluşur.

Kitaptaki ağaçta B'den sonra α = 3 olur. C'nin ilk yaprağı 2 görülünce C ≤ 2 < 3 anlaşılır ve **C'nin 4 ile 6 yaprakları hiç değerlendirilmez**. D için budama olmaz, çünkü en küçük yaprak (2) en sonda gelir. D'nin yaprakları 2, 5, 14 sırasında olsaydı yalnızca 5 yaprağa bakılırdı.

### 2.4 Hamle sıralaması

Alfa-betanın verimliliği **hangi çocuğun önce denendiğine** bağlıdır (`oyun_agaci.py`, Bölüm 2):

| Sıralama | Değerlendirilen yaprak |
|---|---|
| En kötü | ≈ b^m (minimax kadar) |
| Rastgele | minimax'tan çok daha az (kitaba göre orta b için kabaca b^(3m/4)) |
| **En iyi** | **b^⌈m/2⌉ + b^⌊m/2⌋ − 1** (Knuth–Moore); yani ≈ b^(m/2) |

Mükemmel sıralama, etkin dallanma faktörünü b'den √b'ye indirir: Aynı sürede **iki kat derinliğe** inilebilir. Pratikte iyi sıralamaya yaklaşmanın yolları:
- **Öldürücü hamleler** (*killer moves*): Başka dallarda budama yaptırmış hamleleri önce dene.
- **Yinelemeli derinleşme:** Bir önceki sığ aramanın en iyi hamlesini önce dene.
- **Transpozisyon tablosu:** Aynı duruma farklı hamle sırasıyla gelinirse (satrançta çok sık olur) değeri yeniden hesaplama. Dikkat: Alfa-beta çoğu zaman kesin değer değil, **sınır** üretir; tabloya "alt sınır / üst sınır / kesin" bayrağıyla yazılmalıdır (`dortlu_ab.py`).

**Tip A ve Tip B stratejiler** (Shannon): Tip A, belirli bir derinliğe kadar tüm hamleleri inceler. Tip B ise "umut verici" hamleleri derinlemesine inceler (ileri budama). Satranç programları tarihsel olarak A'yı, Go programları B'yi tercih etti.

---

## 3. Sezgisel alfa-beta ağaç araması

Ağacın sonuna inilemiyorsa, aramayı belirli bir derinlikte **kesip** yaprakların yerine bir **değerlendirme fonksiyonu** EVAL(s) koyarız:

- TERMİNAL-Mİ yerine **KESME-Mİ(s, d)** (ör. d > derinlik sınırı)
- FAYDA yerine **EVAL(s, p)**

### 3.1 İyi bir değerlendirme fonksiyonu

1. Terminal durumları gerçek faydayla **aynı sırada** sıralamalıdır.
2. **Hızlı** hesaplanmalıdır; amaç zaten hızlı olmaktır.
3. Terminal olmayan durumlarda, **kazanma şansıyla** güçlü biçimde ilişkili olmalıdır.

En yaygın biçim **ağırlıklı doğrusal fonksiyondur**: EVAL(s) = w₁f₁(s) + … + wₙfₙ(s). Satrançta klasik malzeme değerleri (piyon 1, at/fil 3, kale 5, vezir 9) böyle bir fonksiyonun ağırlıklarıdır. `dortlu_ab.py` her 4'lü pencereye 1, 10 ve 100 puan veren doğrusal bir fonksiyon kullanır. Doğrusallık, öznitelikler **bağımsız** katkı yapıyorsa uygundur. "Oyun sonunda filler daha değerlidir" gibi etkileşimler için doğrusal olmayan fonksiyonlar (ör. sinir ağları) gerekir.

### 3.2 Kesme testi ve sorunları

- **Sessizlik araması** (*quiescence search*): Değerlendirme yalnızca "sakin" konumlarda güvenilirdir. Bir sonraki hamlede büyük bir taş alışverişi olacaksa aramayı biraz daha uzatmak gerekir.
- **Ufuk etkisi:** Kaçınılmaz bir kaybı "geciktiren" hamleler (ör. anlamsız şahlar), kaybı arama derinliğinin **ötesine** iter; program kaybı görmez ve kötü hamleler seçer. **Tekil genişletmeler** (*singular extensions*) tek başına açıkça en iyi olan hamleleri kesme sınırının ötesinde de izleyerek bunu hafifletir.

### 3.3 İleri budama ve arama–tablo dengesi

- **İleri budama:** Bazı hamleleri hiç incelemeden atmak. **Işın araması**, PROBCUT (istatistiğe dayanarak "büyük olasılıkla penceredeki değer dışında" olan hamleleri budamak) ve **geç hamle azaltma** (*late move reduction*: sıralamada geride kalan hamleleri daha sığ aramak) buna örnektir. Hız kazandırır ama hata riski taşır.
- **Arama mı tablo mu?** Açılışlarda hazır **açılış kitapları**, oyun sonunda **geriye dönük analizle** (*retrograde analysis*) çıkarılmış kesin oyun sonu tabloları kullanılır. Ortada ise arama yapılır.

`dortlu_ab.py` boş tahtada ilk hamle için üretilen düğüm sayılarını gösterir. Derinlik 8'de düz alfa-beta 275.251 düğüm üretir; merkezden başlayan sıralamayla bu sayı 12.923'e, üstüne transpozisyon tablosu eklenince 7.368'e iner.

---

## 4. Monte Carlo ağaç araması (MCTS)

Go'da b ≈ 361 ve iyi bir değerlendirme fonksiyonu yazmak çok zordur. MCTS değerlendirme fonksiyonu kullanmaz. Bir durumun değerini, o durumdan başlayan birçok **benzetim** (*playout*) oyununun ortalama sonucuyla tahmin eder.

Her yinelemede dört adım:

1. **Seçim:** Kökten başla, bir **seçim politikasıyla** yaprağa kadar in.
2. **Genişletme:** Yaprağa yeni bir çocuk ekle.
3. **Benzetim:** O çocuktan oyunu bir **benzetim politikasıyla** (en basiti rastgele) sonuna kadar oyna. Bu hamleler ağaca eklenmez.
4. **Geri yayma:** Sonucu yol üzerindeki tüm düğümlerin sayaçlarına işle.

**UCT (UCB1 ile seçim):**

UCB1(n) = U(n) / N(n) + C · √( ln N(ebeveyn(n)) / N(n) )

İlk terim **sömürü** (bilinen ortalama), ikinci terim **keşiftir** (az denenmiş düğümler için büyük). C bu dengeyi ayarlar: kuramsal değer √2'dir, pratikte deneyerek seçilir.

**Kitaptaki sayısal örnek** (`mcts_xox.py`): Ebeveyn 100 benzetim, çocuklar 60/79, 1/10 ve 2/11. C = 1,4 için UCB1 değerleri 1,098 / 1,050 / 1,088 olur ve **60/79** seçilir. C = 1,5 için 1,122 / 1,118 / 1,152 olur ve **2/11** seçilir.

> **Kitaptaki dizgi hatası:** Geri yayma anlatımında "27/35 becomes 28/26" geçer. Doğrusu **28/36**'dır; bir benzetim eklendiği için payda 35'ten 36'ya çıkar.

Arama bitince **en çok ziyaret edilen** hamle seçilir. En yüksek ortalamalı hamle seçilmez, çünkü 2/3'lük bir düğümün belirsizliği 65/100'lük bir düğümden çok daha fazladır.

MCTS'in güçlü yanları: değerlendirme fonksiyonu gerektirmemesi, büyük dallanmada iyi çalışması, her an durdurulabilmesi. Zayıf yanı: Tek bir hamlenin oyunu kaybettirdiği "keskin" konumlarda rastgele benzetimler bu hamleyi kaçırabilir. AlphaGo ve AlphaZero, benzetimlerin yerine sinir ağıyla öğrenilmiş değer ve politika tahminleri koyarak bu sorunu aştı.

`mcts_xox.py`, XOX'ta hiçbir oyun bilgisi kullanmadan kazanan ve savunan hamleleri buluyor ve kusursuz minimax'a karşı 10'da 10 berabere kalıyor.

---

## 5. Şanslı (stokastik) oyunlar

Tavlada her hamleden önce zar atılır. Oyun ağacına **şans düğümleri** eklenir ve **beklenti-minimaks** kullanılır:

EM(s) = FAYDA (terminal) · max (MAX) · min (MIN) · Σ_r P(r)·EM(SONUÇ(s, r)) (şans)

- Tavlada iki zarın n = **21** farklı sonucu vardır (6 çift, her biri 1/36; 15 farklı çift olmayan sonuç, her biri 1/18). Dallanma faktörü genellikle b ≈ 20'dir. Karmaşıklık O(b^m n^m) olur; arama birkaç katı geçemez.
- **Değerlendirme fonksiyonunun ölçeği önemlidir.** Kitaptaki örnekte yaprak değerleri [1, 2, 3, 4] iken en iyi hamle a1, sırayı koruyan [1, 20, 30, 400] dönüşümünde ise a2'dir (`beklenti_minimax.py`: a1 = 2,1 → 21; a2 = 1,3 → 40,9). Bu yüzden EVAL, kazanma olasılığının (ya da beklenen faydanın) **pozitif doğrusal** bir dönüşümü olmalıdır. Aynı fikir Bölüm 16'da fayda kuramında tekrar karşımıza çıkar.
- Şans düğümleri için de budama mümkündür, ama bunun için fayda değerlerinin sınırlı olduğunun bilinmesi gerekir.

---

## 6. Kısmi gözlemlenebilir oyunlar

- **Kriegspiel:** Oyuncu rakibin taşlarını görmez; hakem yalnızca "yasadışı", "şah" gibi bilgiler verir. Oyuncu olası tahta durumlarından oluşan bir **inanç durumu** tutar (Bölüm 4'teki fikrin oyun hâli). Bazı oyun sonlarında belirsizlik altında bile **garantili** mat vardır.
- **Kart oyunları:** Rakibin elleri bilinmez, ama olasılık dağılımı bilinir. Basit fikir: olası dağılımlar üzerinden **ortalama al** ("her dağıtım için açık kartlarla çöz, ortalamasını al"). Bu yaklaşım, **bilgi toplamanın** ve **bilgiyi saklamanın** (blöf) değerini göremez. Çünkü her dağıtımda, sanki ajan her şeyi biliyormuş gibi davranır.

---

## 7. Oyun arama algoritmalarının sınırları

- Değerlendirme fonksiyonları ve benzetimler **kusurludur**. İki katlı bir ağaçta küçük tahmin hataları bile yanlış hamle seçtirebilir.
- Alfa-beta her hamleyi "eşit dikkatle" düşünür. İnsanlar ise yalnızca birkaç anlamlı hamleye odaklanır. Hangi hesaplamanın yapmaya **değer** olduğunu seçmek (**metamuhakeme**) önemli bir araştırma konusudur.
- Oyuncular tek tek hamleler üzerinden değil, **soyut hedefler** ve planlar üzerinden düşünür ("fili hapset").
- Günümüzün güçlü sistemleri (AlphaZero) arama ile **öğrenilmiş** değerlendirmeyi birleştirir (Bölüm 22).

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Alfa-beta yaklaşık bir sonuç verir." | Minimax ile **aynı** değeri verir; yalnızca gereksiz dalları atlar. |
| "Alfa-beta her zaman b^(m/2)'dir." | Bu yalnızca **mükemmel sıralamada** geçerlidir. En kötü sıralamada minimax kadar iş yapar. |
| "Transpozisyon tablosuna her değeri kesin olarak yazarım." | Budanmış düğümlerin değeri bir sınırdır. Kesin sanmak yanlış sonuç verir. |
| "Değerlendirme fonksiyonunda yalnızca sıralama önemlidir." | Deterministik minimaksta öyledir. Şans düğümleri varsa ölçek de önemlidir. |
| "MCTS'te en yüksek kazanma oranlı hamleyi seçerim." | En çok ziyaret edilen hamle daha güvenilirdir. Az denenmiş yüksek oranlar gürültülüdür. |
| "Derinliği artırmak her zaman daha iyi oynatır." | Genellikle öyledir, ama ufuk etkisi ve kusurlu EVAL yüzünden garantisi yoktur. |

## Kendini yokla

1. Kitaptaki ağaçta C'nin yaprakları 6, 4, 2 sırasında olsaydı hangi yapraklar budanırdı?
2. Minimax ile alfa-beta aynı hamleyi mi seçer? Eşitlik durumunda da mı?
3. UCB1'de C = 0 olsaydı MCTS nasıl davranırdı? C çok büyük olsaydı?
4. Beklenti-minimaksta değerlendirme fonksiyonunu 2 ile çarpmak en iyi hamleyi değiştirir mi? Değerleri karesine çevirmek değiştirebilir mi?
5. XOX'ta 5.478 farklı durum varken ağaçta neden 549.946 düğüm var?

## Kod rehberi

```bash
python ornekler/minimax_tictactoe.py --mod istatistik   # 549.946 / 255.168 / 5.478
python ornekler/minimax_tictactoe.py --alpha-beta       # iki optimal ajan: berabere
python ornekler/oyun_agaci.py                           # kitaptaki ağaç + hamle sıralaması
python ornekler/dortlu_ab.py                            # sezgisel alfa-beta, sıralama, TT
python ornekler/dortlu_ab.py --oyna                     # bilgisayara karşı oyna
python ornekler/mcts_xox.py                             # UCB1 örneği + MCTS
python ornekler/beklenti_minimax.py                     # şans düğümleri
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| sıfır toplamlı oyun | zero-sum game | Birinin kazancı diğerinin kaybı |
| tam bilgili | perfect information | Durumun tamamı görünür |
| kat | ply | Tek oyuncunun tek hamlesi |
| oyun ağacı | game tree | Hamle dizilerinin ağacı |
| minimax değeri | minimax value | Kusursuz oyunda durumun değeri |
| alfa-beta budama | alpha–beta pruning | Sonucu etkilemeyen dalları atlama |
| hamle sıralaması | move ordering | Önce iyi hamleleri deneme |
| öldürücü hamle | killer move | Başka dalda budama yaptırmış hamle |
| transpozisyon tablosu | transposition table | Daha önce değerlendirilen durumların önbelleği |
| değerlendirme fonksiyonu | evaluation function | Terminal olmayan durumun tahmini değeri |
| kesme testi | cutoff test | Aramanın nerede durdurulacağı |
| sessizlik araması | quiescence search | Hareketli konumlarda aramayı uzatma |
| ufuk etkisi | horizon effect | Kaçınılmaz kaybı derinlik sınırının ötesine itme |
| tekil genişletme | singular extension | Açıkça en iyi hamleyi daha derin izleme |
| ileri budama | forward pruning | Bazı hamleleri incelemeden atma |
| geriye dönük analiz | retrograde analysis | Oyun sonlarını sondan başa çözme |
| Monte Carlo ağaç araması | Monte Carlo tree search | Benzetimlerle durum değeri tahmini |
| benzetim / playout | simulation / playout | Oyunu sonuna kadar hızlıca oynama |
| sömürü / keşif | exploitation / exploration | Bilineni kullanma / yeniyi deneme |
| şans düğümü | chance node | Zar gibi rastgele olayları temsil eden düğüm |
| beklenti-minimaks | expectiminimax | Şans düğümlü minimax |
| metamuhakeme | metareasoning | Hangi hesaplamaya değer olduğu üzerine akıl yürütme |
