# Bölüm 25 — Bilgisayarlı görü

> **Kitapta:** AIMA 4. baskı, Bölüm 25 *"Computer Vision"*.
> Önce kitabı oku, sonra bu notlarla pekiştir. Metin özgündür; kitaptan alıntı yoktur.
> Kodlar yalnızca numpy kullanır; görüntüler küçük ve yapaydır.

## Bu bölümün haritası

| Kitap alt bölümü | Bu nottaki karşılığı | Kod |
|---|---|---|
| 25.1 Introduction | §1 Görme, özellikler, yeniden yapılandırma ve tanıma | — |
| 25.2 Image Formation | §2 İğne deliği, kaybolma noktası, mercek, ortografik izdüşüm, ışık, renk | `goruntu_olusumu.py` |
| 25.3 Simple Image Features | §3 Kenar, doku, optik akış, bölütleme | `ozellikler.py` |
| 25.4 Classifying Images | §4 CNN ile sınıflandırma, ImageNet, veri çoğaltma, bağlam | `tespit.py` |
| 25.5 Detecting Objects | §5 Kayan pencere, RPN, NMS, kutu regresyonu | `tespit.py` |
| 25.6 The 3D World | §6 Stereo, hareketli kamera, tek görüntüden ipuçları | `goruntu_olusumu.py` |
| 25.7 Using Computer Vision | §7 İnsan hareketleri, resim–sözcük, yeniden yapılandırma, görüntü üretme, hareket denetimi | — |

## Öğrenme hedefleri

1. Perspektif izdüşümü, kaybolma noktasını ve ölçekli ortografik yaklaşımı hesaplamak.
2. Lambert yasasıyla parlaklığı hesaplamak; parlaklık ve renk belirsizliklerini açıklamak.
3. Gauss düzeltmesi + türevle kenar bulmak; yön histogramıyla doku betimlemek.
4. SSD ile optik akış ve stereo eşleme yapmak; derinliği eşitsizlikten hesaplamak.
5. CNN'lerin neden iyi sınıflandırdığını ("desenlerin deseni") açıklamak.
6. Nesne tespitinin adımlarını (öneri, sınıflandırma, NMS, kutu regresyonu, değerlendirme) uygulamak.

---

## 1. Giriş

Görme bir uyaranı alıp dünyanın bir temsilini üreten algı kanalıdır. Çoğu canlı **edilgin algılama** kullanır (ışık yollamaz); yarasa, yunus ya da radarlı robotlar **etkin algılama** yapar.

- **Özellik:** Görüntüye basit hesaplar uygulanarak elde edilen sayı. Örnek: Uçan hayvanlar bir nesneye çarpma zamanını basit bir özellikle kestirip kaslarına doğrudan iletir.
- **Model tabanlı yaklaşım:** nesne modeli (CAD modeli kadar kesin ya da "düşük çözünürlükte bütün yüzler benzer" kadar gevşek) + görüntü oluşturma (rendering) modeli. Uyaran çoğu zaman belirsizdir: Loş ışıkta beyaz nesne güçlü ışıkta siyah nesne gibi görünebilir; küçük-yakın nesne büyük-uzak nesneyle aynı görüntüyü verir.
- Belirsizlikle başa çıkmanın iki yolu: Bazı yorumlar daha olasıdır (gerçek Godzilla yok); bazı belirsizlikler önemsizdir (uzaktaki manzara ağaç mı boyalı yüzey mi, çoğu iş için fark etmez).
- Görünün iki temel sorunu: **yeniden yapılandırma** (görüntüden dünyanın modelini kurmak) ve **tanıma** (nesneler arasında ayrım yapmak). İkisi de geniş yorumlanır.

---

## 2. Görüntü oluşumu (`goruntu_olusumu.py`)

### 2.1 İğne deliği kamera

İnsan gözünde yaklaşık 100 milyon çubuk ve 5 milyon koni hücresi vardır; sayısal kameralarda görüntü düzlemi birkaç milyon piksele bölünür. Odak uzaklığı f olan iğne deliği kamerada sahne noktası (X, Y, Z):

```text
x = −f X / Z      y = −f Y / Z        (perspektif izdüşüm)
```

Z paydada: Uzaklaştıkça görüntü küçülür (kodumuzda Z = 2 → 4 → 8 için x = −0.5 → −0.25 → −0.125). Eksi işaretler: Görüntü hem sağ–sol hem alt–üst ters döner. Bu yüzden "oyuncak kule yakında" ile "gerçek kule uzakta" aynı görüntüyü verebilir.

Delik büyükse görüntü bulanıklaşır; nesne pencere süresinde çok hareket ederse **hareket bulanıklığı** olur.

**Kaybolma noktası:** (U, V, W) yönündeki bir doğrunun noktaları (X₀ + λU, Y₀ + λV, Z₀ + λW). λ → ±∞ iken izdüşüm P∞ = (fU/W, fV/W) olur (W ≠ 0); (X₀, Y₀, Z₀)'dan bağımsızdır. Aynı yönlü bütün doğrular aynı noktada buluşur: tren rayları. Kodumuzda 1.5 m aralıklı iki ray λ = 1000'de (±0.0007, −0.0015) noktasına, yani kaybolma noktası (0, 0)'a yaklaşır.

### 2.2 Mercekler ve ortografik yaklaşım

- Delik küçükse az ışık girer: görüntü karanlık ve gürültülü. **Mercek** geniş bir alandan gelen ışığı tek noktaya odaklar. Yalnızca belli bir derinlik aralığı (**alan derinliği**) keskin görünür; en keskin olduğu yer **odak düzlemi**. Açıklık büyüdükçe alan derinliği küçülür.
- **Ölçekli ortografik izdüşüm:** Nesnenin bütün noktaları Z₀ ± ΔZ içinde ve ΔZ ≪ Z₀ ise f/Z yerine sabit s = f/Z₀: x = sX, y = sY. Kodumuzda Z₀ = 100, ΔZ = 1 için en büyük hata %1, ΔZ = 10 için %11. Kısalma (foreshortening) bu modelde de vardır, çünkü eğimden kaynaklanır.

### 2.3 Işık ve gölgeleme

Bir pikselin parlaklığını üç etken belirler: ortam ışığının gücü, noktanın ışığa dönük olup olmadığı (ya da gölgede kalması), noktanın yansıttığı ışık miktarı.

- **Yaygın yansıma:** Işığı her yöne eşit saçar; parlaklık bakış yönüne bağlı değildir (kumaş, boya, kaba ahşap, bitki, taş).
- **Aynasal yansıma:** Işık, gelişine bağlı dar bir yön demetinde çıkar (ayna). Geniş demetli yüzeylerde küçük parlak lekeler (**aynasal parlamalar**) oluşur: metal, plastik, ıslak yüzeyler. Çoğu iş için "yaygın + aynasal parlamalar" modeli yeterlidir.
- **Uzak nokta ışık kaynağı** (güneş gibi; ışınlar paralel) en önemli aydınlatma modelidir. **Lambert'in kosinüs yasası:**

```text
I = ρ I₀ cos θ      (ρ: yaygın albedo, pratikte 0.05–0.95;  θ: ışık yönü ile yüzey normali arasındaki açı)
```

Işığa dönük yamalar parlak, teğet bakanlar karanlık: Gölgeleme şekil bilgisi taşır. Kodumuzda θ = 60° parlaklığı yarıya indirir. Belirsizlik örneği: ρ = 0.05 (siyah) yüzey 19 kat güçlü ışıkta, ρ = 0.95 (beyaz) yüzeyle aynı parlaklığı verir. Gölgeler nadiren tam siyahtır: gökyüzü ve diğer yüzeylerden yansıyan ışık (**karşılıklı yansıma**) çoğu zaman sabit bir **ortam aydınlatması** terimiyle modellenir.

### 2.4 Renk

İnsan ve kameralar yaklaşık 380 nm (mor) ile 750 nm (kırmızı) arasına duyarlıdır. İnsanda üç tür renk alıcısı olduğu için **üç renklilik ilkesi** geçerlidir (Thomas Young, 1802): Her spektral enerji yoğunluğu, uygun miktarda üç ana renk karıştırılarak eşlenebilir; bu yüzden piksel başına üç sayı (RGB) yeter. Pratikte her yüzeye üç (RGB) albedo, her ışığa üç şiddet verilir ve Lambert yasası her kanala ayrı uygulanır. Aynı yüzey farklı renkli ışıkta farklı renkte görünür; insan bunu büyük ölçüde düzeltir (**renk sabitliği**).

---

## 3. Basit görüntü özellikleri (`ozellikler.py`)

Bir görüntü örneğin on iki milyon üç baytlık pikseldir; ayrıntıyı azaltıp önemli olanı öne çıkaran temsiller gerekir. Genel dört özellik: **kenar**, **doku**, **optik akış**, **bölütleme**. Kenar "erken" (yerel) bir işlemdir; diğerleri daha geniş alanlara bakar ("orta düzey").

### 3.1 Kenarlar

Kenarlar parlaklığın belirgin değiştiği eğrilerdir. Nedenleri (Şekil 25.6): derinlik süreksizliği, yüzey yönelimi süreksizliği, yansıtma süreksizliği, aydınlatma süreksizliği (gölge). Kenar bulucu nedeni ayırt edemez.

- Türevin büyük olduğu yerleri aramak gürültü yüzünden sahte tepeler verir. Önce **Gauss süzgeciyle** düzelt (ağırlıklı komşu ortalaması; pratikte ±3σ'da kesilir): σ = 1 piksel az gürültüyü, 2 piksel daha çoğunu bastırır ama ayrıntı kaybolur.
- **Evrişim:** h = f ∗ g, h(x) = Σᵤ f(u) g(x − u). Kuram: (f ∗ g)′ = f ∗ g′. Yani düzeltip türev almak yerine görüntü doğrudan Gauss'un türeviyle evrişilir (kodumuz ikisinin aynı olduğunu doğrular). Kodumuzda gürültülü basamakta düzeltmesiz türev 16 tepe, σ = 2 ile yalnızca x = 50 bulunur.
- **2B:** Gradyan ∇I = (∂I/∂x, ∂I/∂y). Büyüklüğü kenar gücü; yönü θ kenar yönelimi. Görüntü kararınca büyüklük küçülür ama **yön değişmez** (kodumuzda 0.3 kat kararan görüntüde yönler aynı). Kenar noktası: gradyan büyüklüğü **gradyan yönünde yerel en büyük** ve eşik üstünde. Sonra tutarlı yönlü komşu kenar pikselleri eğrilere bağlanır. Sonuç kusursuz değildir: boşluklar ve anlamsız kenarlar kalır.

### 3.2 Doku

Doku, yüzeyde görsel olarak algılanan, kabaca düzenli desendir (binadaki pencereler, leoparın benekleri, kumsaldaki çakıllar). Kaba model: yinelenen öğeler (**texel**). Doku tek pikselin değil bir yamanın özelliğidir. İyi bir betimleme ışık değişince değişmemeli, döndürmeyle anlamlı biçimde değişmelidir (dikey ile yatay çizgileri ayırmalı).

Temel yapı: Yamadaki her pikselin gradyan yönünü hesapla, **yön histogramı** çıkar. Dikey çizgilerde iki tepe (çizginin sol ve sağ kenarı), benekli desende daha düzgün dağılım. Kodumuzda dikey çizgiler 0° ve 180°'de 0.5'er, yataylar 90° ve 270°'de; benekler sekiz kutuya dağılmış; karartılmış çizgilerde histogram aynı. Yama boyutu bilinmediğinden ölçek aralığında yamalar ve yama içinde kutu kutu histogramlar kullanılır. Günümüzde bu betimlemeleri elle değil CNN'ler üretir; ama öğrenilen temsiller bu yapıya kabaca benzer.

### 3.3 Optik akış

Kamera ile sahne arasındaki göreli hareketin görüntüdeki görünür hareketi. Uzak nesneler yakınlardan yavaş akar: Akış hızı uzaklık bilgisi taşır.

Basit yöntem: p çevresindeki bloğu sonraki karede (Dx, Dy) kadar kaydırılmış bloklarla karşılaştır; **kare farkları toplamı**

```text
SSD(Dx, Dy) = Σ (I(x, y, t) − I(x + Dx, y + Dy, t + Dt))²
```

en küçük olan kaydırma seçilir; akış (Dx/Dt, Dy/Dt). Sahnede doku gerekir: Düz beyaz duvarda bütün adayların SSD'si aynıdır (kodumuzda 121 adayın hepsi 0), algoritma kör tahmin yapar.

### 3.4 Bölütleme

Görüntüyü benzer piksel gruplarına ayırmak. Yalnızca kenarlar yetmez: Çimdeki kaplanın her çizgisi ve her çim yaprağı kenar üretir.

- **Sınır bulma:** (x, y)'de θ yönlü bir sınır olasılığı P_b(x, y, θ), yarım disklerin özellikleri karşılaştırılarak, insanların işaretlediği sınırlarla eğitilmiş bir sınıflandırıcıyla hesaplanır. Sınırlar kapalı eğri oluşturmayabilir ve yalnızca yerel bağlam kullanılır.
- **Bölge bulma:** Pikselleri parlaklık, renk, doku benzerliğine göre kümelemek. Shi ve Malik (2000): Pikseller düğüm, benzerlik Wᵢⱼ kenar ağırlığı; **normalleştirilmiş kesme** ölçütü gruplar arası ağırlığı küçültüp grup içini büyütür. Kodumuz bunu ikinci en küçük özvektörle yaklaşık çözer: Soldan sağa aydınlatma eğimi olan görüntüde Ncut %99 doğrulukla bölerken en iyi tek parlaklık eşiği %90'da kalır. (Yaklaşık çözüm her zaman başarılı değildir; A8'de bir tohumda %76.)
- Yalnızca düşük düzeyli özelliklerle nesne sınırlarını kesin bulmak beklenemez; nesne bilgisi gerekir. Yaygın strateji: **aşırı bölütleme** → **süperpikseller** (milyonlarca piksel yerine yüzlerce bölge).

---

## 4. Görüntü sınıflandırma (`tespit.py`)

İki durum: tek nesneli katalog görüntüleri ("kaşmir kazak") ve birçok nesneli sahne görüntüleri ("çayır", "oturma odası"). Sınıflandırma görünüşe (renk, doku) dayanır. Aynı sınıfın örnekleri farklı görünür; aynı nesne de farklı görünebilir (Şekil 25.11): **aydınlatma**, **kısalma**, **görünüş (aspect)** (simit yandan basık oval, üstten halka), **örtme** (öz-örtme dahil), **biçim bozulması**. Çözüm: çok büyük veriyle CNN eğitmek.

- **ImageNet:** 14 milyondan fazla eğitim görüntüsü, 30 000'den fazla ince sınıf (189 köpek alt sınıfı). İlk yarışmada (2010) en iyi 5 tahmin doğruluğu %70'i geçemedi; CNN'ler (2012) ve iyileştirmeleriyle 2019'da en iyi 5'te %98 (insanı geçti), tek tahminde %87. Başarının asıl nedeni: özelliklerin elle değil veriden öğrenilmesi. Hızlı ilerlemeyi açık veri kümeleri, adil yarışmalar ve kodların paylaşılması sağladı.
- **Neden CNN?** MNIST (70 000 el yazısı rakam) gösterir: Rakam kaydırılabilir, döndürülebilir, büyütülebilir; tek tek pikseller pek bilgi taşımaz ama **yerel desenler** (halka, kesişim, çizgi sonu) ve bunların **uzaysal ilişkileri** taşır. Konvolüsyon + ReLU bir yerel desen dedektörüdür; üstteki katman "desenlerin desenine" bakar ve her katman daha geniş bir pencere görür. Kodumuzda 1. katman yatay ve dikey çubukları, 2. katman çizgilerin buluştuğu yerleri bulur; 3×3 çekirdeklerle k. katmanın alıcı alanı (2k + 1) × (2k + 1).
- **Veri çoğaltma:** Eğitim örneklerini hafifçe kaydır, döndür, ger, rengini değiştir; yeni örnekler asıllarıyla güçlü ilişkili olsa da yararlıdır. Test zamanında da kullanılabilir: kopyaların sınıflandırmaları oylanır.
- **Bağlam:** Nesnenin dışındaki pikseller de ayırt edici olabilir (kedi oyuncağı, zilli tasma). Bağlam veri kümesine göre yardım da eder zarar da.

---

## 5. Nesne tespiti (`tespit.py`)

Tespit edici birden çok nesneyi bulur, sınıfını ve **sınırlayıcı kutusunu** verir. Kayan pencerede her konumda CNN sınıflandırıcı çalıştırılabilir; ama karar verilecekler: pencere biçimi (eksene hizalı dikdörtgen), sınıflandırıcı, bakılacak pencereler, raporlanacak pencereler, kesin konum.

- n × n görüntüde O(n⁴) dikdörtgen vardır (kodumuzda 100 × 100 için 25 502 500). Bu yüzden önce nesne türünden bağımsız bir **"nesnelik"** puanı.
- **Bölge öneri ağı (RPN), Faster RCNN:** Merkezler 16 piksel adımla; her merkezde 9 **çapa kutusu** (küçük/orta/büyük × uzun/geniş/kare). Yeterli puanlı kutular **ilgi bölgesi (ROI)**; farklı boyutlu bölgeler **ROI havuzlama** ile sabit sayıda özelliğe indirilip sınıflandırıcıya verilir.
- **Maksimum olmayanı bastırma:** Eşiği aşan pencereleri puana göre sırala; en iyisini kabul et, onunla çok örtüşenleri at; liste bitene dek tekrarla. Kodumuzda örtüşmeyi IoU ile ölçüp 0.5 eşiğini kullanıyoruz (bizim seçimimiz).
- **Sınırlayıcı kutu regresyonu:** Sınıflandırıcının özelliklerinden kutuyu nesneye oturtacak düzeltmeyi tahmin etmek; seyrek konum/ölçek örneklemesi doğruluğu düşürmez.
- **Değerlendirme:** Gerçek kutular ve etiketlerle karşılaştır; birkaç piksellik kaymayı kabul et; **duyarlılık** (var olanları bulmak) ile **kesinlik** (olmayanı bulmamak) dengelenmeli. Kodumuzda NMS sonrası kesinlik ve duyarlılık 2/3; puan eşiği 0.5'e çıkınca kesinlik 1, duyarlılık 2/3.

---

## 6. 3B dünya (`goruntu_olusumu.py`)

### 6.1 Birden çok görüntü ve stereo

İki görüntüdeki noktaları eşleyebilirsek 3B model kurulabilir; iki görüntüde iki nokta dört (x, y) koordinatı verir, 3B nokta için üçü yeter, fazlası kameraları anlamaya yarar. Asıl sorun **eşleme**dir: doku özellikleri, geometrik kısıtlar, yüzey düzgünlüğü.

**İki gözle derinlik (stereopsis):** Avcıların gözleri öndedir. Sol ve sağ görüntü arasındaki kayma **eşitsizlik**tir. Paralel eksenli, **taban uzunluğu** b olan iki kamerada (f = 1) yatay eşitsizlik H = b/Z, dikey eşitsizlik 0: b bilinip H ölçülünce Z bulunur. Göz bir noktaya **sabitlendiğinde** açısal eşitsizlik:

```text
δθ ≈ b δZ / Z²
```

İnsanda b ≈ 6 cm; en küçük δθ ≈ 5 açı saniyesi: Z = 100 cm'de δZ ≈ 0.4 mm, Z = 30 cm'de 0.036 mm (kodumuz aynı sayıları verir). Eşitsizlik, derinliğin karesiyle küçüldüğünden uzak nesnelerde derinlik kestirimi hızla kötüleşir.

### 6.2 Hareketli kamera

Hareketli bir kamerada eşitsizliğin yerini optik akış alır. f = 1, öteleme hızı T için:

```text
vx = (−Tx + x Tz) / Z      vy = (−Ty + y Tz) / Z
```

- **Genişleme odağı** (Tx/Tz, Ty/Tz): akışın sıfır olduğu nokta.
- **Ölçek belirsizliği:** Kamera iki kat hızlı, sahne iki kat büyük ve uzak olsa akış aynı.
- **Çarpışma zamanı** Z/Tz: Ölçek birbirini götürür; duvara konan sinek bunu kullanır.
- **Hareket paralaksı:** İki noktadaki akış büyüklüklerinin oranının tersi derinlik oranını verir; trenden bakınca yavaş akan manzara daha uzaktır.

### 6.3 Tek görüntüden ipuçları

Örtme (örten daha yakındır); doku (uzak çakıllar küçük, puantiyeler kısalmayla elips); gölgeleme (normal ışığa dönükse parlak; algoritmalar hakkında şaşırtıcı derecede az şey bilinir); bilinen nesnenin **pozu** (robot kolu, robotik cerrahi); nesneler arası ilişkiler (yayaların boyları benzer ve yerde dururlar: ufuk çizgisi biliniyorsa yayalar uzaklığa göre sıralanır, "ayakları ufka yakın dev yaya" tespitleri elenebilir; tersine yayalardan ufuk kestirilebilir).

---

## 7. Bilgisayarlı görünün kullanımı

- **İnsanların ne yaptığını anlamak:** Eklem konumları ve 3B vücut biçimi tek görüntüden iyi kestirilir (zayıf perspektif, sabit uzuv boyları). Davranış sınıflandırma daha zordur: bağlama aşırı dayanma ("yüzme" sınıflandırıcısı aslında havuz dedektörü olabilir), benzer davranışların farklı, farklıların benzer görünmesi, zaman ölçeği (buzdolabını açmak → süt almak → atıştırmalık hazırlamak), ortak sözcük dağarcığının olmaması. Öğrenilen sınıflandırıcılar yalnızca eğitim ve test aynı dağılımdan geliyorsa iyi davranmaya garantilidir; nadir durumlar (tek tekerlekli bisiklete binen yaya) için güvenlik kanıtlamak zordur.
- **Resim ve sözcük:** Etiketleme sistemleri kimin ne yaptığını kaçırır; **altyazı** sistemleri CNN + RNN/transformer ile cümle üretir (COCO: 200 000'den fazla görüntü, her birine beş altyazı). Sistemler bilgisizliklerini gizleyebilir (cinsiyeti eğitim istatistiğinden tahmin etmek gibi). **Görsel soru yanıtlama (VQA)** ve **görsel diyalog** gerçek anlamayı sınamaya yarar; hâlâ çok hata yaparlar (pizzadaki delik sayısı).
- **Çok görüntüden yeniden yapılandırma:** Turist fotoğraflarından bütün bir şehrin modeli; film efektleri için kamera yolu; robot yolu; inşaat takibi (dronlarla haftalık çekim, planla karşılaştırma).
- **Tek görüntüden geometri:** **Derinlik haritası** tahmini (özellikle iç mekânlarda kolay); benzer kuşların birçok görüntüsünden tek fotoğraftaki serçenin 3B modeli ve görünmeyen dokusu.
- **Görüntü üretme:** Fotoğrafa bilgisayar grafiği nesnesi yerleştirme (derinlik, albedo, ışık tahmini); eşli görüntü dönüşümü (hava fotoğrafı → harita; GAN kaybı); eşsiz dönüşüm (at → zebra, **döngü kısıtı**); **stil aktarımı** (erken katmanlar stili, geç katmanlar içeriği temsil eder; |L(x) − L(p)| ve |E(x) − E(s)| birlikte küçültülür); **deepfake**ler ve onlara karşı önlemler; mahremiyeti koruyan yapay tıbbi veri (radyologlar gerçek–yapay ayrımında ortalama %61 başarı; 12 radyolog arasında hata oranı %0'a yakından %80'e).
- **Hareketi görmeyle denetlemek:** Sürücüsüz araç algısı: **yanal denetim** (şeritte kalma), **boylamasına denetim** (öndeki araca mesafe), engelden kaçınma, trafik işaretlerine uyma. Ticari araçlar kamera, lidar, radar ve mikrofon birlikte kullanır (radar sisi deler). Mobil robotlarda klasik ayrım: **SLAM** ile harita + **yol planlama** (Bölüm 26); ya da uçtan uca eğitilen bilişsel haritalama ve planlama.

---

## Sık yapılan hatalar

| Yanılgı | Doğrusu |
|---|---|
| "Görüntüdeki büyüklük gerçek büyüklüğü gösterir." | Büyüklük f/Z ile ölçeklenir; yakın-küçük ve uzak-büyük aynı görünür. |
| "Paralel doğrular görüntüde de paraleldir." | Görüntü düzlemine paralel değillerse kaybolma noktasında buluşurlar. |
| "Parlak piksel = beyaz yüzey." | Parlaklık albedo, ışık şiddeti ve açının çarpımıdır; belirsizdir. |
| "Her kenar bir nesne sınırıdır." | Gölge, doku, yansıtma değişimi de kenar üretir. |
| "Daha çok düzeltme hep daha iyidir." | Gürültü azalır ama kenarlar kayar ve yakın kenarlar karışır. |
| "Optik akış her yerde ölçülebilir." | Dokusuz bölgelerde eşleme belirsizdir. |
| "Yüksek doğruluklu sınıflandırıcı doğru nedenle karar verir." | Bağlama dayanıyor olabilir (havuz dedektörü). |
| "Tespit edicinin bütün yüksek puanlı pencereleri raporlanmalı." | Aynı nesne için birçok pencere olur; NMS gerekir. |

## Kendini yokla

1. İğne deliği kamerada görüntü neden ters döner? Uzaklık iki katına çıkınca boy ne olur?
2. Kaybolma noktası neden doğrunun başlangıç noktasına bağlı değildir?
3. Lambert yasasında θ = 90° ne anlama gelir?
4. Üç renklilik ilkesi neden piksel başına üç sayıyı yeterli kılar?
5. Görüntüyü düzeltip türev almak ile Gauss'un türeviyle evrişmek neden aynıdır?
6. Gradyan yönü neden doku betimlemesi için iyi bir özelliktir?
7. Beyaz duvarda optik akış neden ölçülemez?
8. ImageNet'te en iyi 5 doğruluğu 2010'dan 2019'a nasıl değişti? Neden?
9. Nesne tespitinde NMS ne işe yarar?
10. Stereo görmede derinlik çözünürlüğü uzaklıkla nasıl değişir?
11. Çarpışma zamanı neden ölçek belirsizliğinden etkilenmez?

## Kod rehberi

```bash
python ornekler/goruntu_olusumu.py  # perspektif, kaybolma noktası, ortografik hata, Lambert, stereo, optik akış
python ornekler/ozellikler.py       # 1B/2B kenar, yön histogramı, SSD akış, normalleştirilmiş kesme
python ornekler/tespit.py           # konvolüsyon + ReLU dedektörleri, pencere sayısı, IoU, NMS, kesinlik/duyarlılık
python cozumler/alistirma_kod.py    # A2, A5, A6, A7, A8, A9, A10
```

## Terimler

| Türkçe | İngilizce | Kısa açıklama |
|---|---|---|
| edilgin / etkin algılama | passive / active sensing | Işık yollamadan / sinyal yollayarak algılama |
| özellik | feature | Görüntüden basit hesapla elde edilen sayı |
| yeniden yapılandırma | reconstruction | Görüntüden dünya modeli kurma |
| tanıma | recognition | Nesneler arasında ayrım |
| iğne deliği kamera | pinhole camera | Merceksiz, delikli kutu |
| odak uzaklığı | focal length | Delikten görüntü düzlemine uzaklık f |
| perspektif izdüşüm | perspective projection | x = −fX/Z |
| kaybolma noktası | vanishing point | Paralel doğruların buluştuğu nokta |
| kısalma | foreshortening | Eğik bakışta boyun kısalması |
| alan derinliği | depth of field | Keskin görünen derinlik aralığı |
| ölçekli ortografik izdüşüm | scaled orthographic projection | x = sX, s = f/Z₀ |
| yaygın / aynasal yansıma | diffuse / specular reflection | Her yöne / dar demette yansıma |
| albedo | diffuse albedo | Yansıtılan ışık oranı ρ |
| Lambert kosinüs yasası | Lambert's cosine law | I = ρ I₀ cos θ |
| üç renklilik | trichromacy | Üç ana renkle her rengi eşleme |
| renk sabitliği | color constancy | Işık rengini düzeltme yeteneği |
| kenar | edge | Parlaklığın belirgin değiştiği eğri |
| evrişim | convolution | h = f ∗ g |
| Gauss süzgeci | Gaussian filter | Ağırlıklı komşu ortalaması |
| doku / texel | texture / texel | Yinelenen yüzey deseni / öğesi |
| optik akış | optical flow | Görüntüdeki görünür hareket |
| kare farkları toplamı | sum of squared differences (SSD) | Blok eşleme ölçüsü |
| bölütleme | segmentation | Görüntüyü bölgelere ayırma |
| normalleştirilmiş kesme | normalized cut | Shi–Malik çizge bölme ölçütü |
| süperpiksel | superpixel | Aşırı bölütlemenin bölgeleri |
| görünüş | aspect | Bakış yönüne göre biçim değişimi |
| örtme | occlusion | Nesnenin bir kısmının gizlenmesi |
| veri çoğaltma | data set augmentation | Örnekleri hafifçe değiştirip ekleme |
| bağlam | context | Nesne dışındaki ayırt edici pikseller |
| sınırlayıcı kutu | bounding box | Nesneyi çevreleyen dikdörtgen |
| kayan pencere | sliding window | Görüntü üzerinde gezdirilen dikdörtgen |
| bölge öneri ağı | regional proposal network (RPN) | Nesnelik puanı veren ağ |
| çapa kutusu | anchor box | Her merkezdeki aday kutular |
| ROI havuzlama | ROI pooling | Farklı boyutlu bölgeden sabit sayıda özellik |
| maksimum olmayanı bastırma | non-maximum suppression | Örtüşen pencereleri eleme |
| kutu regresyonu | bounding box regression | Kutuyu nesneye oturtma |
| kesinlik / duyarlılık | precision / recall | Bulunanların doğruluğu / gerçeklerin bulunma oranı |
| stereopsis / eşitsizlik | binocular stereopsis / disparity | İki gözle derinlik / görüntüler arası kayma |
| taban uzunluğu | baseline | İki kamera arasındaki uzaklık b |
| genişleme odağı | focus of expansion | Akışın sıfır olduğu nokta |
| hareket paralaksı | motion parallax | Akış oranından derinlik oranı |
| poz | pose | Nesnenin konumu ve yönelimi |
| derinlik haritası | depth map | Her pikselin derinliği |
| altyazı sistemi | captioning system | Görüntüyü cümleyle betimleme |
| görsel soru yanıtlama | visual question answering (VQA) | Görüntü hakkında soruya yanıt |
| stil aktarımı | style transfer | İçeriği başka bir stille çizme |
| derin sahte | deepfake | Üretilmiş gerçekçi kişi görüntüsü |
| yanal / boylamasına denetim | lateral / longitudinal control | Şeritte kalma / takip mesafesi |
