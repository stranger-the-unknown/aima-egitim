# A1–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A1 — Perspektif izdüşüm

1. İnsan: 50 mm × 1.8 / 10 = **9 mm**. Oyuncak: 50 mm × 0.18 / 1 = **9 mm**. Aynı.
2. İzdüşüm yalnızca boy/uzaklık oranını korur; tek görüntü bu oranı ayırt edemez. Ek bilgiler: önsel bilgi (gerçek Godzilla yoktur, insanlar ~1.7 m boyundadır), ikinci bir görüntü (stereo eşitsizliği, hareket paralaksı), nesnenin yere değdiği yerin ufka göre konumu, alan derinliği (yakın nesnede arka plan bulanık), doku sıklığı.
3. Görüntü hem sağ–sol hem alt–üst **ters** döner (ışınlar delikten geçerken çaprazlanır). Kitap kaybolma noktasını yazarken işaretleri atar: görüntü düzlemini deliğin önüne koymakla eşdeğerdir.

## A2 — Kaybolma noktaları

| Yön | Kaybolma noktası |
|---|---|
| (0, 0, 1) | (0, 0) |
| (1, 0, 1) | (1, 0) |
| (−1, 0, 1) | (−1, 0) |
| (1, 0, 3) | (1/3, 0) |
| (0, 1, 1) | (0, 1) |

1. V = 0 ise kaybolma noktası (fU/W, 0): Hepsi **y = 0** doğrusunda toplanır. Yere paralel bütün doğruların kaybolma noktaları **ufuk çizgisini** oluşturur. (Kodda (1, 0, 1) doğrusunun çok uzak bir noktası gerçekten (1, 0)'a gider.)
2. W = 0: Doğru görüntü düzlemine paraleldir; izdüşümü de paralel kalır, kaybolma noktası yoktur (sonsuzdadır). Kod bu durumda hata verir.

## A3 — Lambert yasası ve renk

1. I = 0.6 · 200 · cos θ: θ = 0° → **120**, 45° → 84.9, 60° → **60**, 80° → 20.8. Yarıya inme: cos θ = 0.5 → **θ = 60°**.
2. Beyaz ışıkta (80, 40, 10), kırmızımsı ışıkta (80, 24, 4). Kırmızımsı ışıkta yüzey daha "kırmızı" görünür. İnsanlar ışığın rengini büyük ölçüde düzeltip yüzeyin beyaz ışıktaki rengini kestirir: **renk sabitliği**. Basit bir kamera bunu kendiliğinden yapmaz (beyaz dengesi gerekir).

## A4 — Stereo ile derinlik

1. δθ = 5″ = 2.42 × 10⁻⁵ rad. δZ = δθ Z² / b: Z = 100 cm → 2.42 × 10⁻⁵ · 10⁴ / 6 ≈ 0.040 cm = **0.4 mm**; Z = 30 cm → **0.036 mm** (kitapla aynı).
2. Z = f b / d = 700 · 0.12 / 7 = **12 m**. d = 6 → 14 m, d = 8 → 10.5 m: 1 piksel hata ±2 m kadar hata verir.
3. d = 70 → **1.2 m**; d = 69 → 1.217 m, d = 71 → 1.183 m: yalnızca ±1.7 cm. Hata yaklaşık δZ ≈ Z² δd / (f b): uzaklığın **karesiyle** büyür. On kat uzakta yüz kat kötü.

## A5 — Düzeltme ölçeği

| | Tepeler |
|---|---|
| Basamak, düzeltmesiz | 16 tepe (5, 8, 11, …, 94) |
| Basamak, σ = 1 | 8, 46, 50, 68, 85 |
| Basamak, σ = 2 | **50** |
| Basamak, σ = 4 | **50** |
| 2 piksellik şerit, σ = 1 | 48, 51 |
| 2 piksellik şerit, σ = 2 | 47, 52 |
| 2 piksellik şerit, σ = 4 | 45, 53 |

Büyük σ gürültüden doğan sahte tepeleri bastırır (kitaptaki Şekil 25.7). Ama yakın kenarlarda konum doğruluğu bozulur: Gerçek kenarlar 48|49 ve 50|51 arasındayken σ = 4 tepeleri 45 ve 53'e iter; daha da büyük σ'da iki kenar birleşebilir. Kitabın ifadesiyle: Daha çok düzeltme daha çok gürültü bastırır ama ayrıntı kaybettirir. (Eşik: en büyük yanıtın 0.4 katı.)

## A6 — Doku histogramları

| Desen | 0° | 45° | 90° | 135° | 180° | 225° | 270° | 315° |
|---|---|---|---|---|---|---|---|---|
| dikey | 0.5 | 0 | 0 | 0 | 0.5 | 0 | 0 | 0 |
| 90° döndürülmüş | 0 | 0 | 0.5 | 0 | 0 | 0 | 0.5 | 0 |
| 45° eğik | 0.03 | 0.45 | 0.03 | 0 | 0.02 | 0.45 | 0.02 | 0 |
| benekler | 0.15 | 0.1 | 0.15 | 0.1 | 0.15 | 0.1 | 0.15 | 0.1 |
| dikey, 0.3 kat + 0.5 | 0.5 | 0 | 0 | 0 | 0.5 | 0 | 0 | 0 |

İki istek de karşılanıyor: Işık değişince (çarpan ve sabit eklemek) gradyan uzar/kısalır ama yönü değişmez; histogram aynı. Döndürme histogramı kaydırır: 90° döndürme iki kutu, eğik çizgiler bir kutu kayar. Böylece dikey ve yatay çizgiler ayrılır. Benekler her yönde kenar ürettiği için düzgün dağılım (8 kutuya yuvarlamadan doğan küçük dalgalanmayla). Kodumuzda her çizginin iki kenarı iki tepeyi verir (kitaptaki "sol ve sağ kenar").

## A7 — Optik akış

1. Bulunan akış **(2, 1)**: Dokulu görüntüde tek bir kaydırma SSD'yi sıfırlar.
2. Dikey kaydırma adaylarının hepsi, (0, −5) … (0, 5), SSD = 0 verir. Dikey çizgiler dikey yönde değişmez: Bu yöndeki hareket görülemez, yalnızca çizgilere dik bileşen ölçülebilir. Beyaz duvarda iki yön de belirsizdi; burada bir yön belirsiz. (Bu literatürde "açıklık sorunu" olarak bilinir; kitap bu adı kullanmaz, yalnızca dokunun gerekli olduğunu söyler.)
3. Çarpışma zamanı Z/Tz = 0.5 / 0.25 = **2 s**. Akış alanında genişleme odağına uzaklık x′ ve akış hızı v için v = x′ Tz / Z, yani Z/Tz = x′/v: Sinek bunu yalnızca görüntüden ölçebilir; ölçek belirsizliği oranın içinde yok olur.

## A8 — Normalleştirilmiş kesme

| Eğim | Ncut (5 tohum) | En iyi tek eşik |
|---|---|---|
| 0 | 0.99 ×5 | 1.00 ×5 |
| 0.4 | 0.99 ×5 | 0.99–1.00 |
| 0.8 | 0.99, 0.99, 0.99, **0.76**, 0.99 | 0.87–0.90 |

Düzgün aydınlatmada tek eşik yeterlidir (hatta biraz daha iyi). Aydınlatma eğimi büyüyünce zeminin aydınlık ucu dairenin karanlık ucundan parlak olur; hiçbir genel eşik ikisini ayıramaz. Ncut yalnızca **yakın** piksellerin (r = 3) benzerliğine baktığı için yavaş değişen aydınlatma ağırlıkları pek etkilemez. Başarısızlık nedenleri: Gerçek Ncut problemi NP-zordur; özvektörle yaptığımız çözüm bir **gevşetmedir** ve gürültü kötü düştüğünde ölçütün kendisi de başka bir bölmeyi (örneğin görüntüyü ikiye bölen bir çizgiyi) tercih edebilir. 12 × 12 gibi küçük görüntülerde sınırın uzunluğu bölgelere göre büyük olduğundan bu daha sık olur.

## A9 — Desenlerin deseni

1. Alıcı alan 1 + 2k: 1–5 katman için **3, 5, 7, 9, 11** piksel.
2. 3. katman (5 × 5 çekirdek, 1. katmanın çıktıları üzerinde): sol kol + sağ kol (yatay haritada merkezin solu ve sağı) + üst kol + alt kol (dikey haritada) − sapma. Artıda dört kol da dolu: toplam 40; köşede ve tek çubukta yalnızca iki kol: 24. Sapma 32 ile ReLU çıktısı: artı **8**, L köşesi **0**, çubuklar **0**. Bu, kitaptaki "yerel desenlerin uzaysal ilişkileri bilgi taşır" gözleminin küçük bir örneğidir (bir 6'da çizgi sonu halkanın üstündedir). Gerçek CNN'de bu ağırlıklar elle değil, veriden öğrenilir.

## A10 — Nesne tespiti

1. Kesişim (2, 2)–(4, 4): 4. Birleşim 16 + 16 − 4 = 28. IoU = 4/28 = **1/7 ≈ 0.14**.
2. Sıra: 0.95 (kutu 0), 0.9 (kutu 1), 0.85 (kutu 3), 0.8 (kutu 2), 0.4 (kutu 4). Kutu 0 kabul; kutu 1 ile IoU = 81/119 = 0.68 → atılır. Kutu 3 kabul; kutu 2 ile IoU 0.68 → atılır. Kutu 4 kabul. Sonuç: **[0, 3, 4]**.
3. Kutu 0 ve kutu 3 gerçek kutularla eşleşir (IoU 1 ve 0.68), kutu 4 yanlış: kesinlik **2/3**, duyarlılık **2/3** (üçüncü nesne bulunamadı). Puan eşiği 0.5: [0, 3] → kesinlik **1**, duyarlılık 2/3. Eşiği yükseltmek kesinliği artırır, duyarlılığı artıramaz; ikisi dengelenmelidir.
4. (200 · 201 / 2)² = 20 100² = **404 010 000** dikdörtgen. Çapa: (1280/16) · (720/16) · 9 = 80 · 45 · 9 = **32 400**.
