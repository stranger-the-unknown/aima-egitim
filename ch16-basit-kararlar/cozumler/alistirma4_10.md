# A4–A10 çözümleri

Kodlu kısımlar: `python cozumler/alistirma_kod.py` (bölüm klasöründen).

---

## A4 — Paranın faydası ve hayatın fiyatı

1. | Piyango | EMV | Kesinlik eşdeğeri | Sigorta primi |
   |---|---|---|---|
   | 0 / 1000 $ | 500 $ | ~499 $ | **~1 $** |
   | 0 / 800 000 $ | 400 000 $ | ~227 500 $ | **~172 500 $** |

   Bay Beard'ın serveti (yaklaşık 150 000 $ borçtan başlayan aralıkta) 1000 $'a göre çok büyüktür; o ölçekte logaritma neredeyse doğrusaldır, bu yüzden küçük kumarlarda risk-nötr davranır. 800 000 $'lık kumarda eğrinin içbükeyliği belirginleşir: Kazanmanın faydası, kaybetmenin kaybından çok daha azdır.
2. Hayır. U = −263.31 + 22.09 log(n + 150 000) bütün aralıkta **içbükeydir** (ikinci türev −22.09 / (n + 150 000)² < 0). Bay Beard her yerde riskten kaçınandır. Kitaptaki risk arayan "çaresiz" bölge, büyük borç içindeki genel eğri üzerindedir, Beard'ın ölçülmüş aralığında değil.
3. Arabanın ömrü 92 000 mil, 230 milde 1 mikromort → **400 mikromort**. Riski yarıya indiren araba 200 mikromort kazandırır ve insanlar bunun için ~12 000 $ öder: 12 000 / 200 = **60 $ / mikromort**.

## A5 — Allais'i kurtarmak

1. EMV(A) = 0.8 × 4000 = 3200 $, EMV(B) = 3000 $. B'yi seçen kişi **200 $** EMV'den vazgeçer.
2. u = U(3000 $):
   - B ≻ A ⇔ u > 0.8 × 1 + 0.2 × (−r) = 0.8 − 0.2r
   - C ≻ D ⇔ 0.2 × 1 > 0.25u ⇔ u < 0.8

   İkisi birlikte: **0.8 − 0.2r < u < 0.8**. r = 0 iken aralık boştur (paradoks). Ama **sıfırdan büyük her r** aralığı açar: r = 0.05 → u ∈ (0.79, 0.80); r = 0.25 → u ∈ (0.75, 0.80). Küçük bir pişmanlık duygusu bile tercihleri tutarlı kılar. Kitabın dediği gibi: Bu kişiler akıl dışı olmayabilir; "aptal gibi hissetme" ihtimalinden kaçınmak için para ödüyorlar.

## A6 — İyileştiricinin laneti ve büzme

Kodun çıktısı (20 000 deneme):

| Seçici | Seçilenin tahmini | Seçilenin gerçek değeri | Gürültülü gruptan seçme |
|---|---|---|---|
| Saf (en büyük tahmin) | **4.89** | 0.55 | %96 |
| Bayesçi (büzülmüş tahmin) | **1.38** | **1.38** | %4 |

1. Saf seçici neredeyse hep gürültülü gruptan seçer: Gürültülü tahminler aşırı uçlara daha kolay ulaşır. Seçtiğinin tahmini 4.89, gerçeği yalnızca 0.55: **4.3 standart sapmalık** hayal kırıklığı.
2. Bayesçi seçici gürültülü tahminleri sıfıra doğru çok, az gürültülüleri az büzer. Hem **daha iyi seçenekler** seçer (gerçek değer 0.55 → 1.38) hem de tahmini **yansızdır** (tahmin = gerçek ortalaması).
3. Hayır. σe herkes için aynıysa büzme bütün tahminleri aynı katsayıyla çarpar; sıralama değişmez, aynı seçenek seçilir. Yalnızca **tahmin** düzelir (hayal kırıklığı kaybolur). Seçimi değiştiren şey, belirsizliklerin farklı olmasıdır.

## A7 — Havalimanı karar ağında bilgi ve duyarlılık

1. **VPI(HavaTrafiği) = 0.** Trafik yoğun da olsa normal de olsa en iyi yer S1'dir (karar_agi.py'nin son tablosu). Bilgi kararı değiştiremediği için değeri yoktur.
2. Eşik **w_ölüm ≈ 5.26**. Varsayılan ağırlık 5 olduğu için karar çok **kırılgandır**: Ağırlıkta %5'lik bir değişiklik kararı S3'e çevirir. Duyarlılık analizinin önerisi: Bu ağırlığı daha dikkatle ölç (ör. mikromort değerinden yararlanarak) ya da başka bilgi topla.
3. Her yer için en kötü durum "trafik her zaman yoğun"dur: EU = S1 −10.73, S2 −11.38, S3 −10.76. Sağlam karar **S1**. Bu problemde sağlam karar ile MEU kararı aynı çıktı.

## A8 — Petrol ve VPI'nin özellikleri

1. n = 4, her blok C/4 $.
   - 1/4 olasılıkla "blok 3'te petrol var": Blok 3 alınır, kâr C − C/4 = 3C/4.
   - 3/4 olasılıkla "yok": Petrol kalan 3 bloktan birinde; başka bir blok alınır, beklenen kâr C/3 − C/4 = C/12.
   - Bilgiyle beklenen kâr: 1/4 × 3C/4 + 3/4 × C/12 = 3C/16 + C/16 = **C/4**. Bilgisiz beklenen kâr 0. VPI = **C/4** (= C/n).
2. Bilgisiz durumda ajan **tek bir** eylem seçer; o eylem, bilginin her olası sonucunda da seçilebilir. Bilgiyle ajan her sonuç için en iyisini seçer, bu yüzden her sonuçta en az bilgisizdeki kadar iyi yapar. Ortalama alınca VPI ≥ 0. Tek bir gözlem "kötü haber" olabilir (beklenen fayda düşer), ama bu bilginin zararı değildir: Durum zaten kötüydü, ajan bunu öğrenmiş oldu ve ona göre davranacak. **Beklenen** değer asla negatif değildir.
3. İkinci test büyük ölçüde aynı şeyi söyler: İlk testten sonra hastanın durumu hakkındaki belirsizlik azalmıştır, ikinci testin kararı değiştirme olasılığı düşüktür. `bilgi_degeri.py`'de VPI(T1) = 5.60 iken VPI(T1, T1b) = 5.66, yani 11.20 değil. VPI **toplamsal değildir**.

## A9 — Hazine avı

1. [4, 3, 1, 2] sırası (P/C oranları 0.2, 0.15, 0.1, 0.06):
   - Yer 4: maliyet 2, başarısızlık 0.6
   - Yer 3: 0.6 × 1 = 0.6, başarısızlık 0.6 × 0.85 = 0.51
   - Yer 1: 0.51 × 3 = 1.53, başarısızlık 0.51 × 0.7 = 0.357
   - Yer 2: 0.357 × 10 = 3.57
   - Toplam: 2 + 0.6 + 1.53 + 3.57 = **7.70**
2. | Kural | Sıra | Beklenen maliyet |
   |---|---|---|
   | P/C büyükten küçüğe | 4, 3, 1, 2 | **7.70** |
   | En ucuz önce | 3, 4, 1, 2 | 7.80 |
   | En olası önce | 2, 4, 1, 3 | 11.69 |
   | Kaba kuvvet en iyisi | 4, 3, 1, 2 | **7.70** |

   "En olası önce" en kötüsü, çünkü en olası yer aynı zamanda en pahalısı. Kaba kuvvet kitabın sonucunu doğrular.
3. wxyz ile wyxz'nin farkı: w'nin maliyeti iki sırada aynıdır; x ile y'ye yalnızca w başarısız olursa (F(w) olasılıkla) gelinir. z'ye ise xy de yx de başarısız olursa gelinir ve F(xy) = F(yx) (iki yerde de hazine olmaması sıraya bağlı değil). Bu yüzden fark F(w) [C(x) P(y) − C(y) P(x)] olur: w ve z'ye bağlı değildir. Komşu çiftleri karşılaştırarak sıralama (kabarcık sıralaması gibi) en iyi sırayı verir.

## A10 — Hata yapan Harriet

1. Harriet doğru karar verirse Robbie E[max(u, 0)] = 18 alır; yanlış karar verirse (iyi eylemi durdurur, kötüsüne izin verir) E[min(u, 0)] alır. E[min(u, 0)] = E[u] − E[max(u, 0)] = 10 − 18 = −8.
   **bekle(ε) = (1 − ε) × 18 + ε × (−8) = 18 − 26ε.**
2. Hemen yapmanın değeri 10. 18 − 26ε > 10 ⇔ **ε < 8/26 ≈ 0.31**. Harriet üç kararından birinden fazlasında yanılıyorsa Robbie ona danışmayı bırakır.
3. Kapatma düğmesinin güvenlik garantisi, robotun insanı **akılcı** sanmasına dayanır. İnsanın hata yapabildiğini düşünen bir robot ona daha az saygı gösterir. Kitap da aynı sonuca varır: Robbie, akıl dışı bir Harriet'e daha az danışır. Ama ε eşiğin altında kaldıkça danışma teşviki sürer; tercih belirsizliği hâlâ işe yarar.
