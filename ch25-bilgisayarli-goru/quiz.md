# Bölüm 25 — Quiz

Cevaplara bakmadan önce kendin yanıtla. Cevaplar dosyanın sonunda.

---

**S1.** İğne deliği kamerada bir nesnenin uzaklığı iki katına çıkarsa görüntüdeki boyu ne olur?

A) İki katına çıkar
B) Değişmez
C) Yarıya iner
D) Dörtte birine iner

**S2.** Kaybolma noktası nedir ve neden doğrunun geçtiği noktaya bağlı değildir?

**S3.** Lambert'in kosinüs yasasına göre hangisi doğrudur?

A) Yaygın yüzeyin parlaklığı bakış yönüne bağlıdır
B) Parlaklık ρ I₀ cos θ'dır; θ ışık yönü ile yüzey normali arasındaki açıdır
C) Aynalar Lambert yüzeyidir
D) Albedo 1'den büyük olabilir

**S4.** Üç renklilik ilkesi nedir? Bilgisayarlı görü için önemi ne?

**S5.** Kenar bulmadan önce görüntüyü neden Gauss ile düzeltiriz? Bunu tek bir evrişimle nasıl yaparız?

**S6.** Gradyan yönü histogramı için hangisi **yanlıştır**?

A) Işık şiddeti değişince değişmez
B) Dikey çizgilerde iki tepe verir
C) Desen 90° döndürülünce de aynı kalır
D) Doku betimlemek için kullanılabilir

**S7.** SSD ile optik akış ölçümünde beyaz bir duvar neden sorun çıkarır?

**S8.** ImageNet'te 2010'dan 2019'a gelişme için hangisi kitapta verilen değerlerdir?

A) En iyi 5 doğruluğu %70'ten %98'e; 2019'da tek tahmin %87
B) En iyi 5 doğruluğu %50'den %90'a
C) Tek tahmin doğruluğu %98'e ulaştı
D) İnsan başarısı hiç geçilmedi

**S9.** Nesne tespitinde maksimum olmayanı bastırma (NMS) nasıl çalışır?

**S10.** Stereo görmede derinlik ile eşitsizlik arasındaki ilişki nedir? İnsan 30 cm'de ne kadar küçük bir derinlik farkını ayırt edebilir?

**S11.** Hangisi optik akıştan ölçek belirsizliğine rağmen elde edilebilir?

A) Duvara olan mutlak uzaklık
B) Kameranın mutlak hızı
C) Çarpışma zamanı Z/Tz
D) Nesnenin metre cinsinden boyu

**S12.** Bir "yüzme" etkinlik sınıflandırıcısı test kümesinde çok başarılı. Kitaba göre neden yine de güvenmemek gerekebilir?

---

## Cevaplar

**S1.** **C.** Görüntü boyu f/Z ile ölçeklenir.

**S2.** Aynı yönlü (paralel) doğruların görüntüde buluştuğu nokta: P∞ = (fU/W, fV/W). λ → ∞ iken başlangıç noktasının katkısı (X₀/λ gibi) sıfıra gider; yalnızca yön kalır.

**S3.** **B.** Yaygın yüzeyin parlaklığı bakış yönüne bağlı değildir; albedo pratikte 0.05–0.95.

**S4.** Üç ana rengin (örneğin RGB) uygun karışımı insan için her spektral dağılımı eşleyebilir (Young, 1802). Bu yüzden piksel başına üç sayı yeterlidir ve Lambert yasası üç kanala ayrı uygulanır.

**S5.** Gürültü türevde sahte tepeler üretir; Gauss ağırlıklı komşu ortalamasıyla bastırılır. (f ∗ g)′ = f ∗ g′ olduğundan görüntü doğrudan Gauss'un türeviyle evrişilir.

**S6.** **C.** Döndürme histogramı kaydırır; dikey ile yatay çizgileri ayırabilmesi bu sayede olur.

**S7.** Dokusuz bölgede bütün aday kaydırmalar aynı SSD'yi verir; eşleme belirsizdir, algoritma kör tahmin yapar.

**S8.** **A.** 2019'da en iyi 5 tahminde insan başarısı geçildi.

**S9.** Eşiği aşan pencereleri puana göre sırala; en yüksek puanlıyı kabul et, onunla büyük ölçüde örtüşenleri listeden at; liste boşalana dek tekrarla.

**S10.** Paralel kameralarda yatay eşitsizlik H = b/Z (f = 1); sabitlenmiş gözlerde açısal eşitsizlik b δZ / Z². b = 6 cm, δθ = 5 açı saniyesiyle Z = 30 cm'de yaklaşık 0.036 mm.

**S11.** **C.** Uzaklık ve hız aynı ölçekle değişir; oranları değişmez.

**S12.** Sınıflandırıcı bağlama dayanıyor olabilir: aslında bir yüzme havuzu dedektörü olup nehirde yüzenleri tanımayabilir. Ayrıca öğrenilen sınıflandırıcılar yalnızca eğitim ve test aynı dağılımdan geldiğinde iyi davranmaya garantilidir.
